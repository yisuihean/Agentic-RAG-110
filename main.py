"""仅 DeepSeek 对话示例（不经过 RAG）。"""

import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from agentic_rag import config
from agentic_rag.llm import create_deepseek_client

if not config.DEEPSEEK_API_KEY:
    sys.exit("请在 .env 中填写 DEEPSEEK_API_KEY")

client = create_deepseek_client()
text = input("输入一句话: ")
r = client.chat.completions.create(
    model=config.DEEPSEEK_CHAT_MODEL or "deepseek-chat",
    messages=[{"role": "user", "content": text}],
)
print(r.choices[0].message.content or "")
