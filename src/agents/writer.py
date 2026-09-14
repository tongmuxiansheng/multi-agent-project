"""
写作员 Agent
负责把研究员的结果整理成最终报告
相当于团队中的文案编辑
"""

from .base_agent import BaseAgent


WRITER_SYSTEM_PROMPT = """你是一个专业的文案编辑，负责把研究结果整理成清晰、专业的最终报告。

## 你的职责
1. 阅读研究员的研究结果
2. 整理成结构清晰、语言流畅的最终报告
3. 突出核心观点和关键结论
4. 确保报告完整回应用户的原始任务

## 输出格式
请按照以下结构输出最终报告：

# 报告标题

## 一、概述
（简要说明报告主题和核心结论，100-200字）

## 二、核心内容
（分点详细阐述，每个要点有小标题和详细说明）

### 2.1 xxx
### 2.2 xxx
### 2.3 xxx

## 三、关键结论
（列出3-5条最重要的结论）

## 四、建议与展望
（给出下一步建议或未来展望）

## 要求
- 语言专业、流畅、易懂
- 结构清晰，层次分明
- 不要简单复制研究员的输出，要重新组织语言
- 确保报告完整回应用户的原始任务
- 总字数控制在500-1000字
"""


class WriterAgent(BaseAgent):
    """写作员 Agent"""

    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(
            name="写作员",
            role="内容整理与报告撰写",
            system_prompt=WRITER_SYSTEM_PROMPT,
            api_key=api_key,
            **kwargs
        )

    def write(self, research_results: str, original_task: str) -> str:
        """
        撰写最终报告
        :param research_results: 研究员的研究结果
        :param original_task: 用户的原始任务
        :return: 最终报告
        """
        input_text = (
            f"【用户原始任务】\n{original_task}\n\n"
            f"【研究员的研究结果】\n{research_results}\n\n"
            f"请根据以上信息，撰写一份完整的最终报告。"
        )
        return self.run(input_text)
