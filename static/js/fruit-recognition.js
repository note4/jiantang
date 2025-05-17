// 标签管理类
class LabelManager {
    constructor() {
        this.labels = null;
        this.modelMapping = null;
        this.initialized = false;
        this.cache = new Map();
    }

    async initialize() {
        if (this.initialized) {
            return;
        }

        try {
            debug('开始加载标签数据');
            const response = await fetch('/api/labels/');
            if (!response.ok) {
                throw new Error('标签数据加载失败');
            }

            const data = await response.json();
            this.labels = data.labels;
            this.modelMapping = data.model_mapping;
            this.initialized = true;
            debug('标签数据加载成功');
        } catch (error) {
            debug(`标签加载错误: ${error.message}`);
            throw error;
        }
    }

    getChineseName(modelIndex) {
        if (!this.initialized) {
            throw new Error('标签管理器未初始化');
        }

        // 检查缓存
        if (this.cache.has(modelIndex)) {
            return this.cache.get(modelIndex);
        }

        const labelPath = this.modelMapping[modelIndex];
        if (!labelPath) {
            return null;
        }

        const [category, type, variety] = labelPath.split('/');
        const categoryData = this.labels.fruits[category] || this.labels.vegetables[category];
        
        let result = null;
        if (categoryData) {
            if (variety && categoryData.varieties[variety]) {
                result = categoryData.varieties[variety];
            } else {
                result = categoryData.cn;
            }
        }

        // 存入缓存
        this.cache.set(modelIndex, result);
        return result;
    }

    getAllLabels() {
        if (!this.initialized) {
            throw new Error('标签管理器未初始化');
        }
        return this.labels;
    }
}

// 性能监控类
class PerformanceMonitor {
    constructor() {
        this.stats = {
            loadTime: 0,
            recognitionTime: 0,
            successCount: 0,
            failureCount: 0,
            averageProcessingTime: 0
        };
    }

    startTimer() {
        return performance.now();
    }

    endTimer(startTime, success) {
        const duration = performance.now() - startTime;
        if (success) {
            this.stats.successCount++;
            this.stats.averageProcessingTime = 
                (this.stats.averageProcessingTime * (this.stats.successCount - 1) + duration) 
                / this.stats.successCount;
        } else {
            this.stats.failureCount++;
        }
        return duration;
    }

    getStats() {
        return this.stats;
    }
}

// 创建全局实例
const labelManager = new LabelManager();
const modelCache = new ModelCache();
const performanceMonitor = new PerformanceMonitor();
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const dropZone = document.getElementById('dropZone');

// 图像识别函数
async function recognizeImage(image) {
    const startTime = performanceMonitor.startTimer();
    try {
        await labelManager.initialize();
        const model = await modelCache.getModel();
        showLoading('正在识别图片...');

        const tensor = tf.tidy(() => {
            const imageTensor = tf.browser.fromPixels(image)
                .resizeNearestNeighbor([224, 224])
                .toFloat();

            const normalized = imageTensor.div(255.0).sub(0.5).mul(2);
            return normalized.expandDims();
        });

        debug('开始进行预测');
        const predictions = await model.predict(tensor).data();
        debug('预测完成');
        tensor.dispose();

        const top5 = Array.from(predictions)
            .map((probability, index) => ({
                className: labelManager.getChineseName(index),
                probability: probability
            }))
            .filter(item => item.className !== null)
            .map(item => ({
                className: item.className,
                probability: (item.probability * 100).toFixed(2)
            }))
            .sort((a, b) => parseFloat(b.probability) - parseFloat(a.probability))
            .slice(0, 5)
            .filter(item => parseFloat(item.probability) > 5);

        const resultDiv = document.getElementById('result');
        if (top5.length > 0) {
            resultDiv.innerHTML = `
                <h3>识别结果：</h3>
                <ul>
                    ${top5.map(item => `
                        <li>
                            <span>${item.className}: ${item.probability}%</span>
                            <button onclick="searchFruit('${item.className}')" class="button">
                                搜索此结果
                            </button>
                        </li>
                    `).join('')}
                </ul>
                <p class="tip">提示：如果结果不准确，请尝试：
                    <br>1. 调整拍摄角度
                    <br>2. 改善光线条件
                    <br>3. 确保图片清晰度
                </p>
            `;
            performanceMonitor.endTimer(startTime, true);
        } else {
            resultDiv.innerHTML = `
                <p>无法识别出蔬果，请尝试：</p>
                <ul>
                    <li>使用其他角度的照片</li>
                    <li>确保光线充足</li>
                    <li>保持图片清晰</li>
                    <li>尝试单个水果的特写照片</li>
                </ul>
            `;
            performanceMonitor.endTimer(startTime, false);
        }
        resultDiv.style.display = 'block';

    } catch (error) {
        performanceMonitor.endTimer(startTime, false);
        showError(`识别失败: ${error.message}`);
        debug(`识别错误详情: ${error.stack || error.message}`);
    } finally {
        hideLoading();
    }
}

// 文件处理函数
function handleFile(file) {
    debug(`处理文件: ${file.name}, 类型: ${file.type}`);
    
    if (!file.type.startsWith('image/')) {
        showError('请选择图片文件');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        debug('文件读取完成，开始显示预览');
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
        
        const img = new Image();
        img.onload = function() {
            debug('图片加载完成，开始识别');
            recognizeImage(img).catch(err => {
                showError(`识别出错: ${err.message}`);
            });
        };
        img.onerror = function() {
            showError('图片加载失败，请确保图片格式正确');
            debug('图片加载失败');
        };
        img.src = e.target.result;
    };
    reader.onerror = function(e) {
        debug(`文件读取错误: ${e.target.error}`);
        showError('文件读取失败');
    };
    reader.readAsDataURL(file);
}

// 搜索功能
function searchFruit(fruitName) {
    debug(`搜索水果: ${fruitName}`);
    window.location.href = `/search/?q=${encodeURIComponent(fruitName)}`;
}

// 自动重试函数
async function retryOperation(operation, maxRetries = 3, delay = 1000) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await operation();
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            debug(`操作失败，${maxRetries - i - 1}次重试机会`);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}

// 事件监听器
fileInput.addEventListener('change', function(e) {
    debug('文件选择事件触发');
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
});

dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', function(e) {
    debug('拖放事件触发');
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');
    
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

imagePreview.addEventListener('click', function() {
    fileInput.click();
});

// 全局错误处理
window.onerror = function(message, source, lineno, colno, error) {
    debug(`全局错误: ${message}`);
    if (error && error.stack) {
        debug(`错误堆栈: ${error.stack}`);
    }
    showError('程序遇到错误，请刷新页面重试');
    return false;
};

// 页面初始化
document.addEventListener('DOMContentLoaded', async function() {
    debug('页面加载完成');
    
    try {
        await labelManager.initialize();
        debug('标签数据初始化成功');
        
        if (typeof tf !== 'undefined') {
            debug('TensorFlow.js 已加载，开始加载模型');
            await tf.ready();
            await modelCache.getModel();
            debug('模型加载成功');
        } else {
            throw new Error('TensorFlow.js 加载失败');
        }
    } catch (error) {
        debug(`初始化失败: ${error.message}`);
        showError('初始化失败，请刷新页面重试');
    }
});

// 导出需要在全局使用的函数
window.searchFruit = searchFruit;