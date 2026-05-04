"""
RAG 命令行入口。业务逻辑在 agentic_rag.pipelines.local_rag。
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

import argparse
import sys

from agentic_rag import config
from agentic_rag.pipelines import local_rag_answer


def main() -> None:
    p = argparse.ArgumentParser(description="本地 RAG：方舟向量 + DeepSeek 回答")
    p.add_argument("file", help="本地文档路径")
    p.add_argument("question", help="问题")
    p.add_argument("-k", type=int, default=4, help="检索条数，默认 4")
    args = p.parse_args()

    if not config.ARK_API_KEY or not config.ARK_EMBEDDING_MODEL:
        sys.exit("请配置 .env 中的 ARK_API_KEY 与 ARK_EMBEDDING_MODEL。")
    if not config.DEEPSEEK_API_KEY:
        sys.exit("请配置 .env 中的 DEEPSEEK_API_KEY。")

    try:
        out = local_rag_answer(args.file, args.question, top_k=args.k)
    except Exception as e:
        sys.exit(str(e))
    print(out)


if __name__ == "__main__":
    main()
