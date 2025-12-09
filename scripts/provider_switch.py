"""切换不同Provider的示例"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src import create_llm, setup_logger

logger = setup_logger("provider_switch.log")


def test_provider(provider: str, model: str = None):
    """测试指定的provider"""
    logger.info(f"\n{'=' * 50}")
    logger.info(f"测试 {provider.upper()}")
    logger.info("=" * 50)

    try:
        # 创建LLM
        llm = create_llm(provider=provider, model=model)
        logger.info(f"模型: {llm.model}")

        # 测试请求
        messages = [{"role": "user", "content": "你好，请用一句话介绍自己。"}]
        response = llm.chat(messages)

        logger.success(f"✓ 成功!")
        logger.info(f"回复: {response[:100]}...")
        return True

    except Exception as e:
        logger.error(f"✗ 失败: {e}")
        return False


def main():
    logger.info("切换Provider示例")

    # 测试不同的provider
    providers = [
        ("azure", "gpt-5-chat"),
        ("aliyun", "qwen3-32b"),
        ("volcengine", "deepseek-v3-250324"),
    ]

    results = {}
    for provider, model in providers:
        results[provider] = test_provider(provider, model)

    # 总结
    logger.info(f"\n{'=' * 50}")
    logger.info("测试总结")
    logger.info("=" * 50)
    for provider, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        logger.info(f"{provider}: {status}")


if __name__ == "__main__":
    main()
