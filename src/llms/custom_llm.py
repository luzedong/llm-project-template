"""自定义 LLM API（支持任意 OpenAI 兼容的 API）"""
import os
import requests
from typing import Dict, List, Optional, Any
from .base import BaseLLM


class CustomLLM(BaseLLM):
    """自定义 LLM API 封装（支持任意 OpenAI 兼容的 API）"""

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.01,
        max_tokens: int = 2048,
        timeout: int = 60,
        verify_ssl: bool = True,
    ):
        # 优先用传入参数，其次用环境变量
        self.api_key = api_key or os.getenv("CUSTOM_API_KEY", "sk-your-api-key")
        self.base_url = base_url or os.getenv(
            "CUSTOM_BASE_URL",
            "https://u425633-a4aa-fff9c4b9.gda1.seetacloud.com:6443/v1",
        )
        model = model or os.getenv("CUSTOM_MODEL_NAME", "qwen3-32b-w8a8")
        self.timeout = timeout

        # SSL 验证配置（对应 curl -k）
        verify_ssl_env = os.getenv("CUSTOM_VERIFY_SSL", "true").lower()
        self.verify_ssl = verify_ssl if verify_ssl is not None else (verify_ssl_env == "true")

        if not self.base_url:
            raise ValueError("CUSTOM_BASE_URL is not set in env or passed in.")
        if not model:
            raise ValueError("CUSTOM_MODEL_NAME is not set in env or passed in.")

        # 标准 chat/completions 接口（兼容 OpenAI 格式）
        self.chat_url = f"{self.base_url.rstrip('/')}/chat/completions"

        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        调用自定义 API 的 chat/completions 接口

        Args:
            messages: 消息列表，格式与 OpenAI 一致
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数

        Returns:
            生成的文本
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        elif self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens

        # 允许透传其他参数
        payload.update(kwargs)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = self._make_request(payload, headers)
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected response format: {data}") from e

    def _make_request(
        self,
        payload: Dict[str, Any],
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        """支持 SSL 验证配置的请求方法，禁用代理以避免连接问题"""
        # 保存原始环境变量
        original_proxies = {}
        proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']
        for var in proxy_vars:
            if var in os.environ:
                original_proxies[var] = os.environ[var]
                del os.environ[var]

        try:
            resp = requests.post(
                self.chat_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
                proxies={},
                verify=self.verify_ssl,  # 控制 SSL 验证（False = curl -k）
            )
            resp.raise_for_status()
            return resp.json()
        finally:
            # 恢复原始环境变量
            for var, value in original_proxies.items():
                os.environ[var] = value
