// 调试函数
function debug(message) {
    const debugDiv = document.getElementById('debug');
    debugDiv.style.display = 'block';
    debugDiv.innerHTML += `<div>${new Date().toISOString()}: ${message}</div>`;
    console.log(message);
}

function showError(message) {
    debug(`错误: ${message}`);
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function showLoading(message) {
    debug(`加载中: ${message}`);
    const loadingText = document.getElementById('loadingText');
    const loadingElement = document.getElementById('loading');
    loadingText.textContent = message;
    loadingElement.style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function searchFruit(fruitName) {
    window.location.href = `/search/?q=${encodeURIComponent(fruitName)}`;
}