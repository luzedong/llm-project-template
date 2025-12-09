"""基本使用示例"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src import create_llm, setup_logger
from src.utils import retry_on_failure

# 设置日志
logger = setup_logger("basic_usage.log")


@retry_on_failure()
def process_with_llm(text: str, provider: str = "openai") -> str:
    """使用LLM处理文本（带自动重试）"""
    # 创建LLM客户端
    llm = create_llm(provider=provider)

    # 调用LLM
    messages = [
        {"role": "system", "content": "你是一个专业的AI助手。"},
        {"role": "user", "content": text}
    ]

    response = llm.chat(messages)
    return response


def main():
    logger.info("=" * 50)
    logger.info("基本使用示例")
    logger.info("=" * 50)

    # 示例1: 使用OpenAI
    logger.info("\n使用 OpenAI:")
    result = process_with_llm("用一句话介绍机器学习", provider="openai")
    logger.info(f"回复: {result}")

    # 示例2: 使用不同provider（需要先配置）
    # logger.info("\n使用 vLLM:")
    # result = process_with_llm("什么是深度学习?", provider="vllm")
    # logger.info(f"回复: {result}")


if __name__ == "__main__":
    main()
