"""
本地文件 RAG：解析 → 分块 → 方舟向量 → 余弦检索 → DeepSeek 生成。
"""

from __future__ import annotations

from pathlib import Path

from agentic_rag import config
from agentic_rag.ark.embeddings import embed_texts
from agentic_rag.documents import parse_path
from agentic_rag.llm.deepseek import create_deepseek_client
from agentic_rag.rag.simple import SimpleVectorIndex, chunk_text


def build_vector_index(doc_path: str | Path) -> SimpleVectorIndex:
    """解析文档、切块并向量化，返回内存索引（可多次用于问答）。"""
    doc = parse_path(doc_path)
    chunks = chunk_text(doc.text)
    if not chunks:
        raise ValueError("文档解析后无文本，无法建索引")
    vectors = embed_texts(chunks, is_query=False)
    return SimpleVectorIndex(chunks=chunks, vectors=vectors)


def answer_with_index(
    index: SimpleVectorIndex,
    question: str,
    *,
    top_k: int = 4,
    system_prompt: str | None = None,
) -> str:
    """在已有索引上检索并调用 DeepSeek 生成回答。"""
    qv = embed_texts([question], is_query=True)[0]
    hits = index.top_k(qv, k=top_k)
    context = "\n\n---\n\n".join(h for h, _ in hits)

    sys_msg = system_prompt or (
        "你是课程助手。请只根据「参考片段」作答；不够就说不知道，不要编造。"
    )

    client = create_deepseek_client()
    resp = client.chat.completions.create(
        model=config.DEEPSEEK_CHAT_MODEL or "deepseek-chat",
        messages=[
            {"role": "system", "content": sys_msg},
            {
                "role": "user",
                "content": f"参考片段：\n{context}\n\n问题：{question}",
            },
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def local_rag_answer(
    doc_path: str | Path,
    question: str,
    *,
    top_k: int = 4,
    system_prompt: str | None = None,
) -> str:
    """
    对单个本地文档做检索增强问答（每次调用都会重新建索引）。
    需要环境变量：ARK_*（向量）、DEEPSEEK_*（生成）。
    """
    index = build_vector_index(doc_path)
    return answer_with_index(
        index, question, top_k=top_k, system_prompt=system_prompt
    )
