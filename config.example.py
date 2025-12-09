# 配置文件示例
# 复制此文件为 config.py 并填入您的实际配置

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key_here"
OPENAI_BASE_URL = None

# Anthropic API Key
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"

# vLLM配置
VLLM_BASE_URL = "http://localhost:8000/v1"
VLLM_API_KEY = ""

# 火山引擎配置
HUOSHAN_API_KEY = "your_huoshan_api_key_here"
HUOSHAN_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
HUOSHAN_MODEL_NAME = "your_model_endpoint_id"

# Azure OpenAI 配置
AZURE_API_KEY = "your_azure_api_key_here"
AZURE_ENDPOINT = "https://your-resource-name.openai.azure.com"
AZURE_API_VERSION = "2025-01-01-preview"
AZURE_DEPLOYED_MODELS = "your_deployment_name"

# 自定义LLM配置（支持任意 OpenAI 兼容的 API）
CUSTOM_API_KEY = "sk-your-api-key"
CUSTOM_BASE_URL = "https://your-api-endpoint/v1"
CUSTOM_MODEL_NAME = "your-model-name"
CUSTOM_VERIFY_SSL = "true"  # 设置为 "false" 可禁用 SSL 验证（对应 curl -k）

# 阿里云通义千问配置
ALIYUN_API_KEY = "your_aliyun_api_key_here"
ALIYUN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
ALIYUN_MODEL_NAME = "qwen-plus"  # 可选: qwen-turbo, qwen-plus, qwen-max

# 默认配置
DEFAULT_LLM_PROVIDER = "openai"  # 可选: openai, anthropic, vllm, volcengine, azure, custom, aliyun
DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048

# 重试配置
MAX_RETRIES = 3
RETRY_DELAY = 1.0
MAX_RETRY_DELAY = 60.0

# 并发配置
MAX_WORKERS = 5

# 数据路径
DATA_INPUT_DIR = "data/input"
DATA_OUTPUT_DIR = "data/output"
DATA_CACHE_DIR = "data/cache"

# 日志配置
LOG_LEVEL = "INFO"
LOG_DIR = "logs"
