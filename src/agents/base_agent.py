"""
基础 Agent 类
所有智能体的基类，定义通用的接口和行为
"""

import os
from openai import OpenAI


class BaseAgent:
    """智能体基类"""

    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        api_key: str = None,
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-chat"
    ):
        """
        初始化 Agent
        :param name: Agent 名称
        :param role: Agent 角色描述
        :param system_prompt: 系统提示词，定义 Agent 的行为
        :param api_key: API Key
        :param base_url: API 地址
        :param model: 模型名称
        """
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        self.model = model

    def run(self, input_text: str, context: str = "") -> str:
        """
        运行 Agent，处理输入并返回结果
        :param input_text: 输入内容（任务、问题等）
        :param context: 上下文信息（其他 Agent 的输出等）
        :return: Agent 的输出
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        # 如果有上下文，加入上下文
        if context:
            messages.append({
                "role": "user",
                "content": f"【上下文信息】\n{context}\n\n【你的任务】\n{input_text}"
            })
        else:
            messages.append({"role": "user", "content": input_text})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    def __repr__(self):
        return f"<Agent name={self.name} role={self.role}>"
