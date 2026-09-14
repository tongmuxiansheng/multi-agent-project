"""
研究员 Agent
负责查资料、分析问题、给出研究结果
相当于团队中的研究员
支持调用 RAG 知识库查询相关资料
"""

from .base_agent import BaseAgent
from tools.rag_tool import RAGTool


RESEARCHER_SYSTEM_PROMPT = """你是一个专业的研究员，负责深入分析问题并给出详细的研究结果。

## 你的职责
1. 先阅读提供的知识库资料（如果有）
2. 深入分析分配给你的研究任务
3. 从多个角度思考问题
4. 给出结构化、有深度的分析结果
5. 如果信息不足，明确指出需要补充什么

## 输出格式
请按照以下结构输出：

【研究主题】xxx

【核心发现】
- 发现1：详细说明
- 发现2：详细说明
- 发现3：详细说明

【详细分析】
（对每个发现进行深入分析，200-500字）

【结论与建议】
（总结研究结论，给出下一步建议）

## 要求
- 优先基于提供的知识库资料进行分析
- 如果知识库资料不足，可以结合你的知识补充，但要明确标注"基于通用知识"
- 分析要有深度，不要泛泛而谈
- 结构清晰，便于后续写作员整理
- 客观中立，基于事实分析
"""


class ResearcherAgent(BaseAgent):
    """研究员 Agent"""

    def __init__(self, api_key: str = None, use_rag: bool = True, **kwargs):
        """
        初始化研究员
        :param api_key: API Key
        :param use_rag: 是否使用 RAG 知识库
        """
        super().__init__(
            name="研究员",
            role="资料查询与深度分析",
            system_prompt=RESEARCHER_SYSTEM_PROMPT,
            api_key=api_key,
            **kwargs
        )
        self.use_rag = use_rag
        self.rag_tool = RAGTool() if use_rag else None
        self.last_rag_result = None

    def research(self, task: str, context: str = "") -> str:
        """
        执行研究任务
        :param task: 研究任务
        :param context: 上下文信息（规划员的计划等）
        :return: 研究结果
        """
        research_context = context

        # 如果启用了 RAG，先查询知识库
        if self.use_rag and self.rag_tool:
            print(f"  [研究员] 正在查询 RAG 知识库...")
            rag_result = self.rag_tool.query(task)
            self.last_rag_result = rag_result

            if rag_result.get("sources"):
                rag_context = self.rag_tool.format_context(rag_result)
                research_context = f"{context}\n\n{rag_context}" if context else rag_context
                print(f"  [研究员] 从知识库找到 {len(rag_result['sources'])} 条相关资料")
            else:
                print(f"  [研究员] 知识库中未找到相关资料，将基于通用知识分析")
                research_context = f"{context}\n\n（注：知识库中未找到相关资料，以下分析基于通用知识）" if context else "（注：知识库中未找到相关资料，以下分析基于通用知识）"

        return self.run(task, research_context)

    def get_rag_status(self) -> dict:
        """获取 RAG 工具状态"""
        if not self.use_rag:
            return {"enabled": False, "available": False}
        return {
            "enabled": True,
            "available": self.rag_tool.is_available() if self.rag_tool else False
        }
