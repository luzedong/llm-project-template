"""数据加载器"""
import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from loguru import logger


class DataLoader:
    """数据加载工具类"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

    def load_jsonl(
        self,
        file_path: str,
        max_samples: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """加载JSONL文件

        Args:
            file_path: 文件路径
            max_samples: 最大样本数

        Returns:
            数据列表
        """
        file_path = self.data_dir / file_path
        data = []

        with open(file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if max_samples and i >= max_samples:
                    break
                data.append(json.loads(line))

        logger.info(f"从 {file_path} 加载了 {len(data)} 条数据")
        return data

    def save_jsonl(
        self,
        data: List[Dict[str, Any]],
        file_path: str
    ) -> None:
        """保存为JSONL文件

        Args:
            data: 数据列表
            file_path: 文件路径
        """
        file_path = self.data_dir / file_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        logger.info(f"保存了 {len(data)} 条数据到 {file_path}")

    def iter_jsonl(
        self,
        file_path: str,
        max_samples: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
        """迭代JSONL文件

        Args:
            file_path: 文件路径
            max_samples: 最大样本数

        Yields:
            数据项
        """
        file_path = self.data_dir / file_path

        with open(file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if max_samples and i >= max_samples:
                    break
                yield json.loads(line)
