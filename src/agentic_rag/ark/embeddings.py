"""火山方舟多模态向量 API（文本项）：POST .../embeddings/multimodal"""

from __future__ import annotations

import httpx

from agentic_rag import config

_BATCH = 16


def _parse_embedding_payload(payload: object) -> list[list[float]]:
    """兼容 data 为 list（OpenAI 风格）或文档描述的单个 object。"""
    if payload is None:
        raise ValueError("响应缺少 data 字段")
    if isinstance(payload, list):
        ordered = sorted(
            payload,
            key=lambda x: x.get("index", 0) if isinstance(x, dict) else 0,
        )
        out: list[list[float]] = []
        for item in ordered:
            if isinstance(item, dict) and "embedding" in item:
                emb = item["embedding"]
                if isinstance(emb, list):
                    out.append([float(x) for x in emb])
        if out:
            return out
    if isinstance(payload, dict) and "embedding" in payload:
        emb = payload["embedding"]
        if isinstance(emb, list):
            return [[float(x) for x in emb]]
    raise ValueError(f"无法解析 embedding 结构: {type(payload)}")


def embed_texts_multimodal(
    texts: list[str],
    *,
    model: str | None = None,
    dimensions: int | None = None,
    encoding_format: str = "float",
) -> list[list[float]]:
    """
    纯文本向量化：每项 input 为 {\"type\":\"text\",\"text\":...}。
    参考：https://ark.cn-beijing.volces.com/api/v3/embeddings/multimodal
    """
    if not texts:
        return []

    key = config.ARK_API_KEY
    if not key:
        raise ValueError("请配置环境变量 ARK_API_KEY")

    m = model or config.ARK_EMBEDDING_MODEL
    if not m:
        raise ValueError("请配置 ARK_EMBEDDING_MODEL（控制台 Model ID 或 Endpoint ID）")

    dim = dimensions if dimensions is not None else config.ARK_EMBEDDING_DIMENSIONS
    base = (config.ARK_BASE_URL or "").rstrip("/")
    url = f"{base}/embeddings/multimodal"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    all_vecs: list[list[float]] = []
    with httpx.Client(timeout=120.0) as http:
        for i in range(0, len(texts), _BATCH):
            batch = texts[i : i + _BATCH]
            body: dict = {
                "model": m,
                "input": [{"type": "text", "text": t} for t in batch],
                "encoding_format": encoding_format,
                "dimensions": dim,
            }
            r = http.post(url, headers=headers, json=body)
            r.raise_for_status()
            data = r.json()
            err = data.get("error")
            if err:
                raise RuntimeError(err)
            vecs = _parse_embedding_payload(data.get("data"))
            if len(vecs) != len(batch):
                raise RuntimeError(
                    f"本批请求 {len(batch)} 条文本，但返回 {len(vecs)} 条向量，请检查模型或响应格式"
                )
            all_vecs.extend(vecs)

    return all_vecs
