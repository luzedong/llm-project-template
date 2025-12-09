"""LLM基类"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseLLM(ABC):
    """LLM基类"""

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """聊天接口

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            生成的文本
        """
        pass

    def __call__(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """支持直接调用"""
        return self.chat(messages, **kwargs)
