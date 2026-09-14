"""
顺序工作流
多个 Agent 按顺序执行，前一个的输出作为后一个的输入
这是最基础的多智能体协作模式
"""

import time
from typing import List, Dict, Any, Callable


class SequentialWorkflow:
    """顺序工作流"""

    def __init__(self, name: str = "顺序工作流"):
        self.name = name
        self.steps: List[Dict[str, Any]] = []

    def add_step(self, agent_name: str, action: str, func: Callable):
        """
        添加一个工作步骤
        :param agent_name: 执行该步骤的 Agent 名称
        :param action: 动作描述
        :param func: 执行函数，接收上一步的输出，返回当前步的输出
        """
        self.steps.append({
            "agent_name": agent_name,
            "action": action,
            "func": func
        })

    def run(self, initial_input: str) -> Dict[str, Any]:
        """
        执行工作流
        :param initial_input: 初始输入
        :return: 最终结果和执行日志
        """
        start_time = time.time()
        current_input = initial_input
        execution_log = []

        print(f"\n【工作流启动】{self.name}")
        print(f"初始输入：{initial_input[:100]}...")

        for i, step in enumerate(self.steps, 1):
            print(f"\n[{i}/{len(self.steps)}] {step['agent_name']} - {step['action']}")
            step_start = time.time()

            output = step["func"](current_input)
            step_duration = time.time() - step_start

            execution_log.append({
                "step": i,
                "agent": step["agent_name"],
                "action": step["action"],
                "input": current_input[:200],
                "output": output[:200],
                "duration": step_duration
            })

            print(f"  耗时：{step_duration:.2f}s")
            print(f"  输出：{output[:100]}...")

            current_input = output

        total_duration = time.time() - start_time
        print(f"\n【工作流完成】总耗时：{total_duration:.2f}s")

        return {
            "workflow_name": self.name,
            "final_output": current_input,
            "execution_log": execution_log,
            "total_steps": len(self.steps),
            "total_duration": total_duration
        }
