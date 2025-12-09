"""Azure OpenAI LLM"""
import os
import requests
from typing import Dict, List, Optional, Any
from .base import BaseLLM


class AzureLLM(BaseLLM):
    """Azure OpenAI 大模型服务封装"""

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        api_version: Optional[str] = None,
        temperature: float = 0.01,
        max_tokens: int = 2048,
        timeout: int = 60,
    ):
        # 优先用传入参数，其次用环境变量
        self.api_key = api_key or os.getenv("AZURE_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_ENDPOINT")
        self.api_version = api_version or os.getenv("AZURE_API_VERSION", "2025-01-01-preview")
        model = model or os.getenv("AZURE_DEPLOYED_MODELS")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("AZURE_API_KEY is not set in env or passed in.")
        if not self.endpoint:
            raise ValueError("AZURE_ENDPOINT is not set in env or passed in.")
        if not model:
            raise ValueError("AZURE_DEPLOYED_MODELS is not set in env or passed in.")

        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        调用 Azure OpenAI 的 chat/completions 接口

        Args:
            messages: 消息列表，格式与 OpenAI 一致
            temperature: 温度参数，范围 [0, 2]
            max_tokens: 最大token数
            **kwargs: 其他参数（如 top_p、stop、presence_penalty 等）

        Returns:
            生成的文本
        """
        deployment_name = self.model

        # Azure OpenAI URL 格式特殊
        chat_url = (
            f"{self.endpoint.rstrip('/')}/openai/deployments/{deployment_name}/"
            f"chat/completions?api-version={self.api_version}"
        )

        payload: Dict[str, Any] = {
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        elif self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens

        # 允许透传其他参数
        payload.update(kwargs)

        # Azure 使用 api-key header 而不是 Bearer token
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        data = self._make_request(chat_url, payload, headers)
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected response format: {data}") from e

    def _make_request(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        """通用请求方法，禁用代理以避免连接问题"""
        # 保存原始环境变量
        original_proxies = {}
        proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']
        for var in proxy_vars:
            if var in os.environ:
                original_proxies[var] = os.environ[var]
                del os.environ[var]

        try:
            # 设置 proxies 参数为空字典，确保不使用任何代理
            resp = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
                proxies={},  # 空字典表示不使用代理
            )
            resp.raise_for_status()
            return resp.json()
        finally:
            # 恢复原始环境变量
            for var, value in original_proxies.items():
                os.environ[var] = value
