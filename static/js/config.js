// 修改模型配置
const MODEL_CONFIG = {
    // url: 'https://tfhub.dev/google/tfjs-model/imagenet/mobilenet_v2_140_224/classification/2/default/1',
    url: 'https://tfhub.dev/google/tfjs-model/imagenet/mobilenet_v3_large_075_224/classification/5/default/1',
    // url: 'https://tfhub.dev/google/tfjs-model/imagenet/mobilenet_v3_small_075_224/classification/5/default/1',
    version: '0.0.2',
    cacheKey: 'fruit-model-cache-v3'
};

// 直接使用完整的标签映射
const IMAGENET_CLASSES = IMAGENET_LABELS;
const FOOD_CLASSES = CHINESE_LABELS;