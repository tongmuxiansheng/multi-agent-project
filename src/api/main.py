"""
多智能体系统 API 接口
基于 FastAPI，提供多智能体协作服务
"""

import os
import sys
import tempfile
from typing import Optional, List
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 把 src 目录加到路径
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 从 .env 加载环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from agents import Orchestrator
from tools.rag_tool import RAGTool

# 初始化 FastAPI
app = FastAPI(
    title="多智能体协作系统 API",
    description="基于多智能体协作的任务处理系统，包含规划员、研究员、写作员三个角色",
    version="1.0.0"
)

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")


# 请求/响应模型
class TaskRequest(BaseModel):
    task: str


class AgentLog(BaseModel):
    agent: str
    action: str
    output: str
    timestamp: str


class TaskResponse(BaseModel):
    task: str
    final_report: str
    collaboration_log: List[AgentLog]
    agents_used: int
    duration: float
    rag_enabled: bool = False
    rag_available: bool = False


class StatusResponse(BaseModel):
    status: str
    agents: List[str]
    workflow: str


@app.get("/status", response_model=StatusResponse)
async def status():
    """系统状态"""
    return {
        "status": "running",
        "agents": ["规划员 (Planner)", "研究员 (Researcher)", "写作员 (Writer)"],
        "workflow": "顺序协作（规划→研究→写作）"
    }


@app.post("/task", response_model=TaskResponse)
async def process_task(request: TaskRequest):
    """
    提交任务，多智能体协作完成
    """
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="任务不能为空")

    if not API_KEY:
        raise HTTPException(status_code=500, detail="未配置 DEEPSEEK_API_KEY，请在 .env 文件中设置")

    try:
        orchestrator = Orchestrator(api_key=API_KEY)
        result = orchestrator.run(request.task)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"多智能体协作失败: {str(e)}")


@app.post("/upload")
async def upload_document(file: UploadFile = File(...), use_ocr: bool = False):
    """
    上传文档到 RAG 知识库
    支持 .txt / .pdf / .docx / .xlsx / .xls
    :param use_ocr: 是否启用 OCR 识别 PDF 图片中的文字（默认关闭）
    """
    # 检查文件格式
    allowed_extensions = {'.txt', '.pdf', '.docx', '.xlsx', '.xls'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式: {ext}，支持 {allowed_extensions}")

    try:
        # 保存上传的文件到临时目录
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        # 调用 RAG 工具上传（传递 use_ocr 参数）
        rag_tool = RAGTool()
        result = rag_tool.upload_document(tmp_path, use_ocr=use_ocr)

        # 删除临时文件
        os.unlink(tmp_path)

        if result.get("success") is False:
            raise HTTPException(status_code=500, detail=result.get("error", "上传失败"))

        ocr_note = "（已启用OCR）" if use_ocr else ""
        return {
            "success": True,
            "filename": file.filename,
            "chunks": result.get("chunks", 0),
            "message": f"文档 '{file.filename}' 上传成功{ocr_note}，已处理成 {result.get('chunks', 0)} 个片段"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


# 挂载前端静态文件
static_dir = os.path.join(src_path, "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
