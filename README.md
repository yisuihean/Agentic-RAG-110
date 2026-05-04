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
src/        项目代码
configs/    C0-C4 配置文件
prompts/    Prompt 模板
runs/       实验日志、结果表、图表
docs/       项目文档、分工、实验记录
```

## 当前阶段

阶段 0：启动准备。

当前目标：

- 建立项目目录
- 初始化 uv 环境
- 固定 Python 版本
- 建立基础配置文件
- 明确三人分工
