# Multi-Agent 多智能体协作系统

> 基于 LangGraph / AutoGen 的多 Agent 协作系统，支持角色分工、工作流编排、MCP 协议集成。

## 项目简介

本项目实现了一个完整的多 Agent 协作系统，覆盖从角色定义到工作流编排的全流程，是 AI Agent 工程师岗位的进阶项目（加分项）。

## 技术栈

- **框架**: LangGraph / AutoGen / CrewAI
- **Agent 架构**: Multi-Agent / Supervisor / Workflow
- **协议**: MCP (Model Context Protocol) / A2A (Agent-to-Agent)
- **大模型**: OpenAI / 通义千问 / 智谱 GLM
- **工作流**: 状态图 / DAG 编排
- **后端**: FastAPI
- **部署**: Docker

## 功能特性

- [ ] 多 Agent 角色定义（研究员 / 写手 / 审核员 / 程序员）
- [ ] Supervisor 主管模式（统一调度）
- [ ] 工作流编排（LangGraph 状态图）
- [ ] Agent 间通信与消息传递
- [ ] MCP 协议集成（外部工具接入）
- [ ] 任务分配与结果汇总
- [ ] RESTful API 接口
- [ ] Docker 一键部署

## 目录结构

```
multi-agent-project/
├── src/
│   ├── agents/            # Agent 角色定义
│   ├── workflows/         # 工作流编排
│   ├── tools/             # 共享工具
│   ├── memory/            # 共享记忆
│   └── api/               # FastAPI 接口
├── config/                # 配置文件
├── tests/                 # 单元测试
├── docs/                  # 文档
├── requirements.txt
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp config/.env.example config/.env

# 3. 运行服务
python -m src.api.main
```

## 学习路径

1. **Week 1**: 单 Agent 复习 + LangGraph 基础
2. **Week 2**: 多 Agent 角色定义 + 通信
3. **Week 3**: Supervisor 模式 + 工作流编排
4. **Week 4**: MCP 协议集成 + 工具共享
5. **Week 5**: 复杂场景实战 + API 封装

## 简历亮点（完成后可写）

- 独立开发 Multi-Agent 多智能体协作系统，实现 4+ 角色分工（研究员/写手/审核/程序员）
- 基于 LangGraph 实现状态机工作流编排，支持复杂任务自动拆解与分配
- 实现 Supervisor 主管模式，统一调度多个 Agent 协作完成任务
- 集成 MCP 协议，支持外部工具动态接入
- 支持 Agent 间消息传递与共享记忆，协作效率提升 XX%
- FastAPI 封装服务接口，Docker 部署
