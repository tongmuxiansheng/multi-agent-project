"""
协调者（Orchestrator）
负责管理多个 Agent 之间的协作流程
相当于团队的总监，安排各个 Agent 按顺序工作
"""

import time
from typing import List, Dict, Any
from .planner import PlannerAgent
from .researcher import ResearcherAgent
from .writer import WriterAgent


class Orchestrator:
    """多智能体协调者"""

    def __init__(self, api_key: str = None):
        """
        初始化协调者，创建所有 Agent
        """
        self.planner = PlannerAgent(api_key=api_key)
        self.researcher = ResearcherAgent(api_key=api_key)
        self.writer = WriterAgent(api_key=api_key)
        self.agents = [self.planner, self.researcher, self.writer]

    def run(self, task: str) -> Dict[str, Any]:
        """
        运行多智能体协作流程
        :param task: 用户的原始任务
        :return: 包含最终报告和协作过程的字典
        """
        start_time = time.time()
        collaboration_log = []

        print("\n" + "=" * 60)
        print(f"【多智能体协作开始】任务：{task}")
        print("=" * 60)

        # ========== 第一步：规划员拆解任务 ==========
        print("\n【1/3】规划员正在制定计划...")
        plan = self.planner.plan(task)
        collaboration_log.append({
            "agent": "规划员",
            "action": "制定计划",
            "output": plan,
            "timestamp": time.strftime("%H:%M:%S")
        })
        print(f"规划员输出：\n{plan[:200]}...")

        # ========== 第二步：研究员执行研究 ==========
        print("\n【2/3】研究员正在分析...")
        research_result = self.researcher.research(
            task=f"根据以下计划执行研究任务：\n{plan}",
            context=f"用户原始任务：{task}"
        )

        # 获取 RAG 查询状态
        rag_status = self.researcher.get_rag_status()
        rag_info = ""
        if rag_status.get("enabled"):
            if self.researcher.last_rag_result and self.researcher.last_rag_result.get("sources"):
                rag_info = f"（已从RAG知识库获取{len(self.researcher.last_rag_result['sources'])}条资料）"
            else:
                rag_info = "（RAG知识库未找到相关资料）"

        collaboration_log.append({
            "agent": "研究员",
            "action": f"执行研究 {rag_info}",
            "output": research_result,
            "timestamp": time.strftime("%H:%M:%S")
        })
        print(f"研究员输出：\n{research_result[:200]}...")

        # ========== 第三步：写作员整理报告 ==========
        print("\n【3/3】写作员正在撰写报告...")
        final_report = self.writer.write(research_result, task)
        collaboration_log.append({
            "agent": "写作员",
            "action": "撰写报告",
            "output": final_report,
            "timestamp": time.strftime("%H:%M:%S")
        })
        print(f"写作员输出：\n{final_report[:200]}...")

        total_duration = time.time() - start_time

        print("\n" + "=" * 60)
        print(f"【协作完成】总耗时：{total_duration:.2f}s")
        print("=" * 60)

        return {
            "task": task,
            "final_report": final_report,
            "collaboration_log": collaboration_log,
            "agents_used": len(self.agents),
            "duration": total_duration,
            "rag_enabled": self.researcher.use_rag,
            "rag_available": rag_status.get("available", False)
        }
