"""
规划员 Agent
负责接收用户任务，拆解成子任务，并分配给合适的 Agent
相当于团队中的项目经理
"""

from .base_agent import BaseAgent


PLANNER_SYSTEM_PROMPT = """你是一个专业的项目规划员，负责把用户的复杂任务拆解成清晰的子任务。

## 你的职责
1. 分析用户的任务需求
2. 把任务拆解成2-4个清晰的子任务
3. 每个子任务要具体、可执行
4. 按执行顺序排列

## 输出格式
请严格按照以下格式输出：

【任务拆解】
1. [子任务1名称]：具体描述
2. [子任务2名称]：具体描述
3. [子任务3名称]：具体描述

【分配建议】
- 子任务1 → 研究员（负责查资料、分析）
- 子任务2 → 研究员（负责查资料、分析）
- 子任务3 → 写作员（负责整理成报告）

## 要求
- 子任务要具体，不要太笼统
- 研究类任务分配给研究员
- 整理、写作类任务分配给写作员
- 最多拆解4个子任务
"""


class PlannerAgent(BaseAgent):
    """规划员 Agent"""

    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(
            name="规划员",
            role="项目规划，任务拆解",
            system_prompt=PLANNER_SYSTEM_PROMPT,
            api_key=api_key,
            **kwargs
        )

    def plan(self, task: str) -> str:
        """
        制定计划
        :param task: 用户的原始任务
        :return: 拆解后的任务计划
        """
        return self.run(f"请为以下任务制定执行计划：\n{task}")
