"""配置工具"""
import sys
from pathlib import Path
from typing import Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import config as project_config

from src.llms import (
    BaseLLM,
    VolcEngineLLM,
    AzureLLM,
    CustomLLM,
    AliyunLLM,
)


def create_llm(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> BaseLLM:
    """创建LLM实例

    Args:
        provider: LLM提供商 (openai, anthropic, vllm, volcengine, azure, custom, aliyun)
        model: 模型名称
        temperature: 温度参数
        max_tokens: 最大token数

    Returns:
        LLM实例
    """
    provider = provider or project_config.DEFAULT_LLM_PROVIDER
    model = model or project_config.DEFAULT_MODEL
    temperature = temperature or project_config.DEFAULT_TEMPERATURE
    max_tokens = max_tokens or project_config.DEFAULT_MAX_TOKENS

    if provider == "volcengine":
        return VolcEngineLLM(
            api_key=project_config.HUOSHAN_API_KEY,
            base_url=project_config.HUOSHAN_BASE_URL,
            model=model or project_config.HUOSHAN_MODEL_NAME,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == "azure":
        return AzureLLM(
            api_key=project_config.AZURE_API_KEY,
            endpoint=project_config.AZURE_ENDPOINT,
            api_version=project_config.AZURE_API_VERSION,
            model=model or project_config.AZURE_DEPLOYED_MODELS,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == "custom":
        return CustomLLM(
            api_key=project_config.CUSTOM_API_KEY,
            base_url=project_config.CUSTOM_BASE_URL,
            model=model or project_config.CUSTOM_MODEL_NAME,
            temperature=temperature,
            max_tokens=max_tokens,
            verify_ssl=(project_config.CUSTOM_VERIFY_SSL.lower() == "true")
        )
    elif provider == "aliyun":
        return AliyunLLM(
            api_key=project_config.ALIYUN_API_KEY,
            base_url=project_config.ALIYUN_BASE_URL,
            model=model or project_config.ALIYUN_MODEL_NAME,
            temperature=temperature,
            max_tokens=max_tokens
        )
    else:
        raise ValueError(f"不支持的provider: {provider}")


def get_config_value(key: str):
    """获取配置值"""
    return getattr(project_config, key, None)
