import os
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")


def _env(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        return default
    return v.strip()


# 火山方舟：多模态向量（POST .../embeddings/multimodal，纯文本项）
ARK_BASE_URL = _env("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
ARK_API_KEY = _env("ARK_API_KEY")
ARK_EMBEDDING_MODEL = _env(
    "ARK_EMBEDDING_MODEL", "doubao-embedding-vision-250615"
)
ARK_EMBEDDING_DIMENSIONS = int(_env("ARK_EMBEDDING_DIMENSIONS", "2048") or "2048")

# DeepSeek：OpenAI 兼容对话（RAG 生成）
DEEPSEEK_API_KEY = _env("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = _env("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_CHAT_MODEL = _env("DEEPSEEK_CHAT_MODEL", "deepseek-chat")
