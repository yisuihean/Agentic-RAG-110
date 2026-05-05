# Agentic RAG（教学实验项目）

## 使用说明

### 环境

- Python 3.11+
- 依赖与锁文件由 [uv](https://github.com/astral-sh/uv) 管理

**首次克隆：**

```bash
git clone <本仓库地址>
cd Agentic-RAG
uv sync
```

复制 `.env.example` 为 `.env`，按其中注释填写 **火山方舟**（向量）与 **DeepSeek**（对话）的密钥与模型名。

### 模型与密钥（控制台）

实际使用的 **Model ID / Endpoint ID** 以各平台控制台为准，与 `.env` 中变量对应关系如下。

| 用途 | `.env` 中主要变量 | 说明与配置入口 |
|------|-------------------|----------------|
| 对话（RAG 生成） | `DEEPSEEK_API_KEY`、`DEEPSEEK_CHAT_MODEL` | 在 [DeepSeek 平台 · 用量与 API Key](https://platform.deepseek.com/usage) 创建密钥、查看调用与用量。 |
| 多模态向量（本项目仅用文本项） | `ARK_API_KEY`、`ARK_EMBEDDING_MODEL`、`ARK_EMBEDDING_DIMENSIONS` | 方舟 [多模态向量化](https://www.volcengine.com/docs/82379/1523520) 开通模型（如 `doubao-embedding-vision-250615`），`dimensions` 为 **1024 或 2048**。 |

**协作与安全：** 勿提交 `.env`；勿将密钥写入仓库或文档。更完整的模块边界、目录说明与协作约定见 **[ARCHITECTURE.md](ARCHITECTURE.md)**。

**若 API 报错：** 检查 `.env` 中 Key、模型 ID、方舟 `ARK_EMBEDDING_DIMENSIONS`（1024/2048）是否与控制台开通的模型一致。

### 运行方式

| 脚本 | 作用 |
|------|------|
| `uv run python main.py` | 仅测试 DeepSeek 对话（不建库、不检索） |
| `uv run python demo.py` | **先输入/传入文档路径建索引**，再在同一终端多次提问（文档不重复向量化） |
| `uv run python demo.py "D:\资料\x.pdf"` | 同上，路径作为参数 |
| `uv run python rag_demo.py 文档路径 "你的问题"` | 单次问答：每次整条链路（含重建索引） |
| `uv run python upload_demo.py` | 浏览器上传文档 + 提问（Gradio） |

### 在代码里复用 RAG 一条线

```python
from agentic_rag.pipelines import local_rag_answer

text = local_rag_answer("资料.pdf", "这一节结论是什么？", top_k=4)
print(text)
```

多轮问答且只建一次索引：

```python
from agentic_rag.pipelines import build_vector_index, answer_with_index

index = build_vector_index("资料.pdf")
print(answer_with_index(index, "第一个问题"))
print(answer_with_index(index, "第二个问题"))
```

需已配置 `.env` 且能访问对应 API。

---

## 架构与协作

每个入口脚本、`src/agentic_rag/` 下各子目录及内部文件的职责、依赖方向、Git 与评审约定见 **[ARCHITECTURE.md](ARCHITECTURE.md)**。
