# 需要下載的套件

📌 必要的 Python 套件
```bash
pip install fastapi uvicorn requests pytest pytest-asyncio pytest-order pytest-timeout selenium httpx opencv-python mediapipe jinja2
```

📜 套件說明

|套件	                |用途   |
|-----------------------|-------------------|
|fastapi	            |用於建立 FastAPI 伺服器    |
|uvicorn	            |FastAPI 伺服器的 ASGI 服務器   |
|requests	            |讓 test_mp.py 和 test_mp_api.py 可以發送 HTTP 請求 |
|pytest	                |執行測試   |
|pytest-asyncio	        |讓 pytest 支援 async 測試  |
|pytest-order	        |允許設定測試執行順序   |
|pytest-timeout	        |避免測試無限卡住   |
|selenium	            |用於 test_full_system.py 測試 Web UI   |
|httpx	                |FastAPI 測試 API 用的非同步 HTTP 客戶端    |
|opencv-python	        |讓 testmp.py 進行影像處理  |
|mediapipe	            |MediaPipe 手部偵測模型 |
|jinja2	                |FastAPI 的 HTML 模板渲染引擎   |

🚀 安裝
📌 安裝全部套件
```bash
pip install fastapi uvicorn requests pytest pytest-asyncio pytest-order pytest-timeout selenium httpx opencv-python mediapipe jinja2 webdriver-manager
```

# 執行流程

# 測試 api
1. 在 main.py 中執行 `uvicorn main:app --host 127.0.0.1 --port 8000 --reload` 來啟動 FastAPI 伺服器
2. 執行 pytest test_api.py -s (測試 api)
3. 執行 pytest pytest/test_full_system.py -s (測試 selenium)

# 測試 testmp.py
1. 在 main.py 中執行 `uvicorn main:app --host 127.0.0.1 --port 8000 --reload` 來啟動 FastAPI 伺服器
2. 執行 testmp.py

# 測試 test_mp_api.py 
## 不能執行 testmp.py 因為 Windows 在 同一時間只允許一個應用程式存取相機，當 test_mp.py 佔用了相機，test_mp_api.py 可能會失敗。
1. 在 main.py 中執行 `uvicorn main:app --host 127.0.0.1 --port 8000 --reload` 來啟動 FastAPI 伺服器
2. 執行 pytest test_mp_api.py -s  (測試 requests)