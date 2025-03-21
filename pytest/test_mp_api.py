import pytest
import requests  # 用於發送 API 測試請求
import sys
import os

# 確保 Python 能找到 main.py 所在的路徑
# 這樣 pytest 執行時，能夠正確匯入 testmp.py 內的函式
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.testmp import distance  # 匯入 testmp.py 中的距離計算函數

# 隱藏 TensorFlow 不必要的警告 (如果使用 MediaPipe，TensorFlow 可能會顯示額外的訊息)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# FastAPI API 端點 URL
API_URL = "http://127.0.0.1:8000/api/detect_hand"


def test_distance():
    """
    測試距離計算函數 `distance()`，確保計算結果正確。
    - 測試 (0,0) 到 (3,4) 的歐式距離是否為 5 (畢氏定理)
    """
    assert distance(0, 0, 3, 4) == 5, "❌ 距離計算錯誤"
    print("✅ `distance()` 測試通過！")


def test_mp_to_api():
    """
    測試 `testmp.py` 是否正確發送手勢數據到 FastAPI，並驗證回應。
    1. 準備模擬的手勢數據
    2. 發送 `POST` 請求到 FastAPI
    3. 檢查 API 是否回應 HTTP 200
    4. 驗證 API 回應的手勢狀態是否正確
    """
    test_hand_state = [1, 0, 1, 0, 1]  # 模擬 OpenCV 偵測的手勢數據 (0: 關閉, 1: 張開)

    # 發送手勢數據到 FastAPI，設定 10 秒逾時 (避免請求卡住)
    response = requests.post(API_URL, json={"hand_state": test_hand_state}, timeout=10)
    
    # 確保 API 回應 200 OK
    assert response.status_code == 200, "❌ API 回應錯誤"
    
    # 解析 API 回應數據
    response_data = response.json()
    expected_hand_state = "".join(map(str, test_hand_state))
    
    # 確保 API 回應的手勢數據與輸入數據一致
    assert response_data["hand_state"] == expected_hand_state, f"❌ 錯誤: API 回應 {response_data['hand_state']}，但 OpenCV 偵測為 {expected_hand_state}"
    
    print("✅ testmp.py + FastAPI 測試通過！")
