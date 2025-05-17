class ModelCache {
    constructor() {
        this.model = null;
    }

    async getModel() {
        if (this.model) {
            debug('使用内存中的模型');
            return this.model;
        }

        try {
            debug('从网络加载模型');
            // 使用更高精度的模型配置
            this.model = await tf.loadGraphModel(MODEL_CONFIG.url, {
                fromTFHub: true,
                modelUrl: MODEL_CONFIG.url
            });
            debug('模型加载成功');
            
            try {
                await this.model.save('indexeddb://' + MODEL_CONFIG.cacheKey);
                debug('模型已缓存到 IndexedDB');
            } catch (cacheError) {
                debug('模型缓存失败，但不影响使用: ' + cacheError.message);
            }

            return this.model;
        } catch (error) {
            debug(`尝试从 IndexedDB 加载模型`);
            try {
                this.model = await tf.loadGraphModel('indexeddb://' + MODEL_CONFIG.cacheKey);
                debug('成功从 IndexedDB 加载模型');
                return this.model;
            } catch (localError) {
                debug(`本地加载失败: ${localError.message}`);
                throw error;
            }
        }
    }
}