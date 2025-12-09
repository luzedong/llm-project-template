"""批量数据处理示例（带重试）"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

from src import DataLoader, create_llm, setup_logger
from src.utils import retry_on_failure

import config

# 设置日志
logger = setup_logger("batch_processing.log")


@retry_on_failure(max_attempts=3)
def call_llm_with_retry(llm, messages):
    """带重试的 LLM 调用"""
    return llm.chat(messages)


def process_item(item: dict, llm) -> dict:
    """处理单条数据"""
    try:
        messages = [
            {"role": "system", "content": "你是一个数据处理助手。"},
            {"role": "user", "content": item["text"]}
        ]

        # 使用带重试的调用
        response = call_llm_with_retry(llm, messages)

        return {
            **item,
            "result": response,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"处理失败 (已重试 {config.MAX_RETRIES} 次): {e}")
        return {
            **item,
            "result": None,
            "status": "failed",
            "error": str(e)
        }


def main():
    logger.info("=" * 50)
    logger.info("批量数据处理示例")
    logger.info("=" * 50)

    # 1. 创建LLM客户端
    llm = create_llm()
    logger.info(f"使用Provider: {config.DEFAULT_LLM_PROVIDER}")

    # 2. 加载数据
    loader = DataLoader(config.DATA_INPUT_DIR)

    # 创建示例数据（实际使用时从文件加载）
    sample_data = [
        {"id": 1, "text": "什么是机器学习？"},
        {"id": 2, "text": "深度学习的优势是什么？"},
        {"id": 3, "text": "如何开始学习AI？"}
    ]

    # 保存示例数据
    loader.save_jsonl(sample_data, "sample_input.jsonl")
    logger.info("示例数据已保存到 data/input/sample_input.jsonl")

    # 从文件加载
    data = loader.load_jsonl("sample_input.jsonl")
    logger.info(f"加载了 {len(data)} 条数据")

    # 3. 批量处理（并发）
    logger.info(f"开始批量处理（并发数: {config.MAX_WORKERS}）...")

    with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        futures = [executor.submit(process_item, item, llm) for item in data]

        results = []
        for future in tqdm(futures, desc="处理中"):
            results.append(future.result())

    # 4. 保存结果
    output_loader = DataLoader(config.DATA_OUTPUT_DIR)
    output_loader.save_jsonl(results, "sample_output.jsonl")

    # 5. 统计
    success_count = sum(1 for r in results if r["status"] == "success")
    logger.info(f"处理完成: {success_count}/{len(results)} 成功")


if __name__ == "__main__":
    main()
