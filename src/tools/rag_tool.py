"""
RAG 知识库工具
调用 rag-project 的 API，查询知识库中的相关资料
让研究员 Agent 能基于特定资料进行分析
"""

import os
import requests


class RAGTool:
    """RAG 知识库查询工具"""

    def __init__(self, api_url: str = None):
        """
        初始化 RAG 工具
        :param api_url: RAG 服务的 API 地址
        """
        self.api_url = api_url or os.environ.get("RAG_API_URL", "http://localhost:8000")

    def query(self, question: str, top_k: int = 3) -> dict:
        """
        查询 RAG 知识库
        :param question: 查询问题
        :param top_k: 返回最相关的前几条
        :return: 查询结果（答案、置信度、相关文档）
        """
        try:
            response = requests.post(
                f"{self.api_url}/query",
                json={"question": question, "top_k": top_k},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "answer": f"RAG 服务返回错误：{response.status_code}",
                    "confidence": 0,
                    "sources": []
                }
        except requests.exceptions.ConnectionError:
            return {
                "answer": "无法连接到 RAG 知识库服务，请确认 RAG 服务已启动（端口8000）",
                "confidence": 0,
                "sources": []
            }
        except Exception as e:
            return {
                "answer": f"RAG 查询出错：{str(e)}",
                "confidence": 0,
                "sources": []
            }

    def is_available(self) -> bool:
        """检查 RAG 服务是否可用"""
        try:
            response = requests.get(f"{self.api_url}/status", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def upload_document(self, file_path: str, use_ocr: bool = False) -> dict:
        """
        上传文档到 RAG 知识库
        :param file_path: 本地文件路径
        :param use_ocr: 是否启用 OCR 识别图片中的文字（仅对 PDF 有效）
        :return: 上传结果
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                params = {'use_ocr': use_ocr}
                response = requests.post(
                    f"{self.api_url}/upload",
                    files=files,
                    params=params,
                    timeout=600  # OCR 可能需要很长时间，设为10分钟
                )
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"上传失败：{response.status_code} {response.text}"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "无法连接到 RAG 知识库服务"}
        except Exception as e:
            return {"success": False, "error": f"上传出错：{str(e)}"}

    def format_context(self, query_result: dict) -> str:
        """
        把 RAG 查询结果格式化成上下文文本，供大模型使用
        :param query_result: RAG 查询结果
        :return: 格式化后的上下文文本
        """
        if not query_result.get("sources"):
            return "（知识库中未找到相关资料）"

        context = "【从知识库中查到的相关资料】\n\n"
        for i, source in enumerate(query_result.get("sources", []), 1):
            context += f"--- 资料 {i} ---\n"
            context += f"内容：{source.get('content', source.get('text', ''))}\n"
            if source.get("metadata"):
                context += f"来源：{source['metadata'].get('source', '未知')}\n"
            context += "\n"

        if query_result.get("answer"):
            context += f"【知识库给出的参考答案】\n{query_result['answer']}\n\n"

        context += "请基于以上资料进行分析，如果资料不足，请明确指出。"
        return context
