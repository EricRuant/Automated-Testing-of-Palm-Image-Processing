# 專案名稱: HandSimTest - 手勢模擬測試
## 1️⃣ 專案簡介 (Introduction)
這是一個基於 **FastAPI** 和 **MediaPipe** 的手勢偵測應用，透過 **OpenCV** 讀取攝影機畫面，辨識手勢並將數據傳送至 **FastAPI** 後端，最後在 **Web UI** 上顯示最新的手勢狀態。

### 🔹 **應用場景**
- **遊戲控制**：可以透過手勢來模擬按鍵操作
- **人機交互**：可應用於手勢驅動的應用程式
- **機器人控制**：利用手勢來發送控制指令

### 🔹 **為什麼使用 API？**
本專案的 API 設計讓系統更具靈活性，提供跨裝置、跨平台的支援：
- **行動裝置支援**：API 可以讓手機 App 透過網路存取手勢數據，而不受限於特定設備。
- **跨平台兼容性**：不管是 Windows、Linux、Mac，甚至 IoT 設備，都可以透過 API 進行手勢控制。
- **擴展性與整合性**：未來可以整合 **機器人控制、遊戲、智能家居** 等應用，讓 API 成為核心介面。

## 2️⃣ 功能列表 (Features)
✅ **即時手勢偵測** - 使用 **MediaPipe** 進行手勢追蹤  
✅ **FastAPI API** - 提供 API 端點以接收手勢數據  
✅ **Web UI** - 顯示最新的手勢狀態  
✅ **自動測試** - 使用 **Pytest + Selenium** 進行 API 及 UI 測試  
✅ **GitHub Actions CI/CD** - 自動執行測試  

## 3️⃣ 環境需求 (Requirements)
請確保你的系統符合以下需求：
- Python `3.10+`
- FastAPI
- OpenCV
- MediaPipe
- Selenium（測試用）
- Requests（測試用）
- Pytest （測試用）
- Google Chrome & ChromeDriver（測試用）

## 4️⃣ 安裝與執行 (Installation & Usage)
```bash
# 下載專案
git clone https://github.com/你的帳號/你的專案.git
cd 你的專案

# 建立虛擬環境 (可選)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```
啟動 FastAPI 伺服器
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
伺服器啟動後，開啟瀏覽器並前往：
- Web UI: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## 5️⃣ API 端點 (API Endpoints)

|方法	    |端點	            |說明                                  |
|-----------|-------------------|--------------------------------------|
|GET	    |/	                |渲染 Web UI                           |
|POST	    |/api/detect_hand	|接收手勢數據，更新 latest_hand_state   |
|GET	    |/get_hand_state	|獲取最新的手勢狀態                     |

範例 API 請求
```bash
curl -X 'POST' 'http://127.0.0.1:8000/api/detect_hand' \
     -H 'Content-Type: application/json' \
     -d '{"hand_state": [1, 0, 1, 0, 1]}'
```

## 6️⃣ 測試方式 (Testing)
使用 Pytest 進行測試：
```bash
pytest
```
或手動測試：
```bash
python pytest/test_full_system.py
```

GitHub Actions 自動測試
本專案已設定 GitHub Actions，在 Push/PR 時會自動執行測試。CI 設定檔為：
- .github/workflows/pytest.yml

## 7️⃣ 專案架構 (Project Structure)
```bash
├── app/                            # FastAPI 應用
│   ├── main.py                     # 主要後端 API
├── pytest/                         # 測試相關
│   ├── test_api.py                 # API 測試
│   ├── test_mp_api.py              # MediaPipe API 測試
│   ├── test_full_system.py         # 端對端 (E2E) 測試
├── scripts/                        # 手勢辨識相關腳本
│   ├── testmp.py                   # OpenCV 手勢辨識
├── static/                         # 前端靜態文件 (CSS, JS)
│   ├── style.css                   # 網頁樣式
├── templates/                      # HTML 模板
│   ├── index.html                  # Web UI
├── .github/workflows/pytest.yml    # GitHub Actions CI 設定
├── requirements.txt                # 依賴套件
├── README.md                       # 專案說明
```

## 8️⃣ TODO / 未來改進 (Future Improvements)
### 效能優化
- **提升 API 效能**
     - 目前 API 回應時間約 `100ms`，希望能最佳化 FastAPI + Uvicorn 來降低延遲至 `<50ms`。
     - 嘗試使用 **Gunicorn + Uvicorn Workers** 提升並行能力，支援高併發請求。
     - 研究 **FastAPI 的 Background Tasks** 來減少請求時的同步計算，讓 API 更快回應。

- **改善 CI/CD 效能**
     - 目前 GitHub Actions 需要 **2 分鐘** 完成測試，希望最佳化流程，以 **降低 CI/CD 執行時間至 1 分鐘內**。
     - 探索 **pytest 並行測試** (`pytest-xdist`) 來加速測試運行。
     - 減少 `sleep 5` 等靜態等待時間，改為 **事件驅動**（例如 `wait_for_service`）。
     - 使用 **依賴快取 (`cache dependencies`)**，減少每次執行時重複安裝 Python 套件的時間。

### 開發與環境改進
- **新增 Docker 支援**
     - 提供 `Dockerfile` 讓開發者可以 **一鍵啟動 FastAPI 伺服器**。
     - 新增 `docker-compose.yml`，將 FastAPI、測試環境、資料庫（如果有）整合為容器化應用。

- **整合 Postman**
     - 提供 **Postman Collection**，讓開發者可以快速測試 API。
     - Postman 測試案例將包含：
          - `POST /api/detect_hand` 測試手勢數據傳輸
          - `GET /get_hand_state` 測試最新手勢狀態
     - 考慮使用 **Postman CLI** 或 **Newman** 來在 CI/CD 中自動執行 API 測試。

## 9️⃣ 參考資源 (References)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?fbclid=IwAR3hT07UJOu5xgsdQE1-3vW2n-TOaj86aLjJo4kGokPF94KQTI7i5TXY9KA#get_started)
- [OpenCV](https://opencv.org/?fbclid=IwAR21DYrTYs0TF5WrNZ2FD9woqVS2iUaf3XWLQsDK0gZxlOErBSwAUjj5D7w)
- [Selenium](https://selenium-python.readthedocs.io/)
- [Pytest](https://docs.pytest.org/en/stable/contents.html)