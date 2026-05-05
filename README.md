# Agentic RAG 110

本项目对应 110 实验室课题四，研究面向学习与知识服务任务的 Agentic RAG 技术增强与评测。

项目当前由两部分合并而来：

1. 远程仓库已有的本地 RAG 代码、DeepSeek/火山方舟调用示例、文档解析与 Demo。
2. 本课题新增的 C0-C4 对比实验规划、协作规范、目录规范、日志与评测文档。

## 项目定位

本项目不是单纯做一个学习助手产品，而是通过 C0-C4 对比实验，评估 query rewrite、多轮检索、rerank、self-check 和工具调用等 Agentic RAG 模块的作用。

## 对比配置

- C0 Naive RAG：普通 RAG 基线
- C1 Query Rewrite RAG：加入查询诊断与查询改写
- C2 Advanced RAG：加入 BM25、混合检索和 rerank
- C3 Agentic Retrieval RAG：加入任务规划、多轮检索和 self-check
- C4 Tool-Augmented Agentic RAG：加入文件读取、代码执行、计算器、表格分析工具
- C5 Open-source Reference：Dify 或 RAGFlow 横向参考

## 环境

- Python 3.12
- 依赖与锁文件由 uv 管理

首次克隆后运行：

```powershell
uv sync
uv run python --version
```

复制 `.env.example` 为 `.env`，按需填写 DeepSeek、OpenAI-compatible API 或火山方舟相关密钥。

注意：

- 不要提交 `.env`。
- 不要提交 `.venv/`。
- 新增依赖统一使用 `uv add`。

## 项目目录

```text
data/       数据、知识库、测试集
src/        项目代码
configs/    C0-C4 和消融配置文件
prompts/    Prompt 模板
runs/       实验日志、结果表、图表
docs/       项目文档、分工、实验记录
```

远程仓库已有代码结构和入口说明可继续参考：

- `ARCHITECTURE.md`
- `main.py`
- `demo.py`
- `rag_demo.py`
- `upload_demo.py`
- `src/agentic_rag/`

## 常用运行方式

```powershell
uv run python main.py
uv run python demo.py
uv run python rag_demo.py 文档路径 "你的问题"
uv run python upload_demo.py
```

后续 C0-C4 批量实验入口会逐步补充到 `src/` 和 `configs/` 中。

## 当前阶段

阶段 0：启动准备。

当前目标：

- 建立项目目录
- 初始化 uv 环境
- 固定 Python 版本
- 建立基础配置文件
- 明确三人分工
- 合并远程已有 RAG 代码与本课题规范文档
