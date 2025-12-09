"""阿里云通义千问 LLM"""
import os
import requests
from typing import Dict, List, Optional, Any
from .base import BaseLLM


class AliyunLLM(BaseLLM):
    """阿里云通义千问大模型服务封装（DashScope API）"""

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.01,
        max_tokens: int = 2048,
        timeout: int = 60,
    ):
        # 优先用传入参数，其次用环境变量
        self.api_key = api_key or os.getenv("ALIYUN_API_KEY")
        self.base_url = base_url or os.getenv(
            "ALIYUN_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        model = model or os.getenv("ALIYUN_MODEL_NAME", "qwen-plus")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("ALIYUN_API_KEY is not set in env or passed in.")

        # 标准 chat/completions 接口（兼容 OpenAI 格式）
        self.chat_url = f"{self.base_url.rstrip('/')}/chat/completions"

        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: float = 0.8,
        **kwargs
    ) -> str:
        """
        调用阿里云 DashScope 的 chat/completions 接口

        Args:
            messages: 消息列表，格式与 OpenAI 一致
            temperature: 温度参数，范围 [0, 2]
            max_tokens: 最大token数
            top_p: 核采样参数，范围 [0, 1]
            **kwargs: 其他参数（如 stop、presence_penalty 等）

        Returns:
            生成的文本
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "top_p": top_p,
            "enable_thinking": False,  # 非流式调用必须设为 False
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

    def get_available_models(self) -> List[Dict[str, Any]]:
        """获取阿里云可用的模型列表"""
        models_url = f"{self.base_url.rstrip('/')}/models"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 完全禁用代理
        original_proxies = {}
        proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']
        for var in proxy_vars:
            if var in os.environ:
                original_proxies[var] = os.environ[var]
                del os.environ[var]

        try:
            resp = requests.get(
                models_url,
                headers=headers,
                timeout=self.timeout,
                proxies={},
            )
            resp.raise_for_status()
            data = resp.json()

            try:
                return data.get("data", [])
            except (KeyError, TypeError) as e:
                raise RuntimeError(f"Unexpected response format: {data}") from e
        finally:
            # 恢复原始环境变量
            for var, value in original_proxies.items():
                os.environ[var] = value

    def _make_request(
        self,
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
                self.chat_url,
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
