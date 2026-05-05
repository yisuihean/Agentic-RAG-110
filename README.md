# Topic4 Agentic RAG Evaluation

本项目对应 110 实验室课题四，研究面向学习与知识服务任务的 Agentic RAG 技术增强与评测。

## 项目定位

本项目不是单纯做一个学习助手产品，而是通过 C0-C4 对比实验，评估 query rewrite、多轮检索、rerank、self-check 和工具调用等 Agentic RAG 模块的作用。

## 对比配置

- C0 Naive RAG：普通 RAG 基线
- C1 Query Rewrite RAG：加入查询诊断与查询改写
- C2 Advanced RAG：加入 BM25、混合检索和 rerank
- C3 Agentic Retrieval RAG：加入任务规划、多轮检索和 self-check
- C4 Tool-Augmented Agentic RAG：加入文件读取、代码执行、计算器、表格分析工具

## 项目目录

```text
data/       数据、知识库、测试集
src/        项目代码，包括导入的本地 RAG 基础实现
configs/    C0-C4 配置文件
prompts/    Prompt 模板
runs/       实验日志、结果表、图表
docs/       项目文档、分工、实验记录
```

## 已导入的基础 RAG 代码

`Agentic-RAG-110` 仓库中的本地 RAG 基础实现已经套入本项目框架，主要包括：

```text
src/agentic_rag/   文档解析、向量接口、LLM 调用和本地 RAG pipeline
main.py            DeepSeek 对话连通性测试
demo.py            交互式本地 RAG Demo
rag_demo.py        单次命令行 RAG Demo
upload_demo.py     Gradio 上传文档问答 Demo
ARCHITECTURE.md    原仓库架构说明，作为代码参考文档保留
```

运行示例：

```powershell
uv run python main.py
uv run python demo.py
uv run python rag_demo.py 文档路径 "你的问题"
uv run python upload_demo.py
```

这些代码目前作为 C0 普通 RAG 和后续 Demo 的基础资产，后续会逐步整理进 C0-C4 实验配置与批量评测流程。

## 当前阶段

阶段 0：启动准备。

当前目标：

- 建立项目目录
- 初始化 uv 环境
- 固定 Python 版本
- 建立基础配置文件
- 明确三人分工
