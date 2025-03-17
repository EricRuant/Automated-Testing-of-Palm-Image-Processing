from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# 創建 FastAPI 應用程式
app = FastAPI()

BASE1_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE1_DIR / "templates"

# 確保 `templates` 目錄存在
if not TEMPLATES_DIR.exists():
    print(f"❌ ERROR: 找不到 templates 目錄 ({TEMPLATES_DIR})")

# 設定模板目錄，讓 FastAPI 可以渲染 HTML 頁面
templates = Jinja2Templates(directory=TEMPLATES_DIR)

BASE2_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE2_DIR / "static"

# 掛載靜態文件（CSS, JS, 圖片等），讓網頁能夠讀取 CSS 樣式
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 變數來儲存最新的手勢狀態，初始值為 "00000"（所有手指皆關閉）
latest_hand_state = "00000"

# 定義 API 端點的請求格式
class HandInput(BaseModel):
    hand_state: List[int]  # 手勢數據，包含五根手指的開關狀態（0: 關閉, 1: 打開）

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """ 渲染 Web UI，並顯示當前的手勢狀態 """
    return templates.TemplateResponse("index.html", {"request": request, "hand_state": latest_hand_state})

@app.post("/api/detect_hand")
def detect_hand(hand: HandInput):
    """ 接收來自 OpenCV 偵測的手勢數據，並更新最新的手勢狀態 """
    global latest_hand_state
    latest_hand_state = "".join(map(str, hand.hand_state))  # 轉換數據為字串格式
    print(f"Received Hand State: {latest_hand_state}")  # 印出接收到的手勢數據
    return {"hand_state": latest_hand_state, "message": "Hand detected successfully."}  # 返回 JSON 回應

# 伺服器啟動入口
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)  # 啟動 FastAPI 伺服器，允許熱重載

# 使用終端執行: uvicorn main:app --host 127.0.0.1 --port 8000 --reload 來啟動伺服器

# 測試網址: http://127.0.0.1:8000