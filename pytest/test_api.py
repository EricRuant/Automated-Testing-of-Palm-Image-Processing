import pytest
from httpx import AsyncClient  # 用於發送非同步 API 測試請求
import sys
import os

# 確保 Python 能找到 main.py 所在的路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app  # 匯入 FastAPI 應用程式

# 建立非同步測試客戶端
@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:8000/", transport=None) as client:
        yield client

@pytest.mark.asyncio
async def test_detect_hand(client):
    """ 測試 FastAPI 的手勢偵測 API """
    test_data = {"hand_state": [1, 0, 1, 0, 1]}  # 模擬手勢數據
    
    # 發送非同步請求到 API
    response = await client.post("/api/detect_hand", json=test_data)
    
    # 驗證 API 是否正確回應 HTTP 200
    assert response.status_code == 200, f"錯誤: API 回應狀態碼 {response.status_code}"

    response_data = response.json()
    
    # 驗證 API 回應數據是否正確
    expected_hand_state = "10101"
    assert response_data["hand_state"] == expected_hand_state, f"錯誤: API 回應 {response_data['hand_state']}"
    
    print("✅ FastAPI API 測試通過！")
