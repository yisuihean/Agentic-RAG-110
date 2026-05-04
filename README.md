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
| 文本/多模态向量 | `ARK_API_KEY`、`ARK_EMBEDDING_MODEL`、`ARK_EMBEDDING_DIMENSIONS` | 在火山引擎 [方舟 · 豆包向量化相关模型](https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-embedding) 开通并查询模型能力、维度（如 1024/2048）及 Model ID。 |

**协作注意：** 不要提交 `.env`；各成员本地自建密钥。提交前可执行 `git status` 确认未误加密钥文件。

**若 API 报错：** 检查 `.env` 中 Key、模型 ID、方舟 `ARK_EMBEDDING_DIMENSIONS`（1024/2048）是否与控制台开通的模型一致。

### 运行方式

| 脚本 | 作用 |
|------|------|
| `uv run python main.py` | 仅测试 DeepSeek 对话（不建库、不检索） |
| `uv run python rag_demo.py 文档路径 "你的问题"` | 完整流程：读文档 → 分块 → 方舟向量 → 检索 → DeepSeek 回答 |

### 在代码里复用 RAG 一条线

```python
from agentic_rag.pipelines import local_rag_answer

text = local_rag_answer("资料.pdf", "这一节结论是什么？", top_k=4)
print(text)
```

需已配置 `.env` 且能访问对应 API。

---

## 目录结构（每个文件夹做什么）

项目根目录（与 `src` 平级）只放**入口脚本**和工程配置，可执行逻辑在 **`src/agentic_rag/`** 包内。

```
项目根/
├── main.py                 # 入口：仅 DeepSeek 聊天
├── rag_demo.py             # 入口：完整本地 RAG 命令行
├── pyproject.toml          # 项目名、依赖、打包方式
├── uv.lock                 # 锁定的依赖版本（团队开发可提交）
├── .env.example            # 环境变量模板（勿提交真实密钥）
├── README.md               # 本说明
└── src/
    └── agentic_rag/        # 主包：所有可 import 的模块
        ├── __init__.py
        ├── config.py       # 从 .env 读 ARK / DeepSeek 等配置
        ├── documents/      # 文档解析：本地文件 → 纯文本
        ├── ark/            # 火山方舟：多模态向量等 HTTP 调用
        ├── llm/            # 大模型客户端：当前为 DeepSeek（OpenAI 兼容）
        ├── rag/            # 检索层：分块、内存向量索引、相似度
        └── pipelines/      # 业务编排：把上面模块串成「一条 RAG 流程」
```

| 目录/文件 | 职责 |
|-----------|------|
| **`config.py`** | 集中读取环境变量，避免各模块直接 `os.getenv` 散乱。 |
| **`documents/`** | 按扩展名解析 `.txt` / `.md` / `.pdf` / `.docx`，统一出口 `parse_path` → `ParsedDocument`。 |
| **`ark/`** | 与火山方舟 REST 对接；当前提供 `embed_texts_multimodal`（`POST .../embeddings/multimodal`）。 |
| **`llm/`** | 对话侧 HTTP 客户端工厂，如 `create_deepseek_client()`，供 pipeline 与 `main.py` 复用。 |
| **`rag/`** | 与「模型厂商」无关的纯逻辑：文本分块、余弦相似度、内存 `SimpleVectorIndex`。 |
| **`pipelines/`** | 组合「解析 → 向量 → 检索 → 生成」；`local_rag_answer` 是完整一条线，供脚本或其它项目调用。 |

**依赖方向（便于维护）**：`pipelines` → 可依赖 `documents` / `ark` / `llm` / `rag`；底层模块**不**依赖 `pipelines`，避免循环引用。

---

## 提交规范（建议）

采用 [Conventional Commits](https://www.conventionalcommits.org/)，便于阅读历史：

- `feat:` 新功能  
- `fix:` 修复  
- `docs:` 仅文档 / README  
- `refactor:` 重构（不改对外行为）  
- `chore:` 构建、依赖、杂项  

示例：`feat(rag): add chunk overlap option`


