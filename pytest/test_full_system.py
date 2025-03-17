import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# FastAPI API 端點 URL
API_URL = "http://127.0.0.1:8000/api/detect_hand"

# Web UI 端點 URL
WEB_URL = "http://127.0.0.1:8000"

@pytest.mark.order(1)  # 設定測試順序，確保 API 測試先執行
def test_api():
    """ 測試 FastAPI 的手勢偵測 API """
    test_hand_state = [1, 0, 1, 0, 1]  # 測試輸入的手勢數據

    # 發送手勢數據到 FastAPI API
    response = requests.post(API_URL, json={"hand_state": test_hand_state})

    # 確保 API 回應 200 OK
    assert response.status_code == 200, f"錯誤: API 回應狀態碼 {response.status_code}"

    # 解析 API 回應數據
    response_data = response.json()
    expected_hand_state = "".join(map(str, test_hand_state))

    # 確保 API 回應的數據與輸入數據一致
    assert response_data["hand_state"] == expected_hand_state, f"錯誤: API 回應 {response_data['hand_state']}，但預期為 {expected_hand_state}"

@pytest.mark.order(2) # 設定測試順序，確保 Web UI 測試在 API 測試後執行
def test_web_ui():
    """ 測試 Web UI 是否正確顯示 API 回應的手勢數據 """
    options = Options()
    # options.add_argument("--headless=new")  # ✅ 無頭模式
    # options.add_argument("--no-sandbox")  
    # options.add_argument("--disable-dev-shm-usage")  
    # options.add_argument("--disable-gpu")  
    # options.add_argument("--remote-debugging-port=9222")

    # ✅ 使用 `webdriver-manager` 來下載並安裝 `chromedriver`
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(WEB_URL)  # ✅ 確保連線到正確的 URL

    print(driver.page_source)  # ✅ 輸出 HTML 方便 Debug

    # 等待指定元素出現，而不是固定 sleep 5 秒
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/button'))
    )

    # 取得網頁顯示的手勢狀態
    response_text = driver.find_element(By.ID, "handState").text
    
    # 驗證網頁顯示的手勢狀態是否與預期一致
    assert response_text == "10101", f"錯誤: Web UI 顯示 {response_text}，但預期應為 '10101'"
    
    print("✅ Web UI 測試成功！")
    driver.quit()  # 關閉瀏覽器