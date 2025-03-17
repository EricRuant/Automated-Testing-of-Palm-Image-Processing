import cv2
import mediapipe as mp
import requests
import time

# FastAPI API 端點 URL，將手勢數據發送到此端點
API_URL = "http://127.0.0.1:8000/api/detect_hand"

# 初始化攝影機，開啟第一個可用的攝影機設備
cap = cv2.VideoCapture(0)

# 初始化 MediaPipe 手部偵測模組
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)  # 設定最多偵測一隻手
mpDraw = mp.solutions.drawing_utils  # 用於繪製手部關鍵點

# 計算兩點之間的距離
# 這在手勢辨識時很重要，可以幫助判斷手指是否張開
def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

# 設定計時器，用於 10 秒後自動結束
start_time = time.time()

while True:
    # 讀取攝影機畫面
    ret, img = cap.read()
    if ret:
        # 轉換顏色格式，將 BGR 轉為 RGB，供 MediaPipe 處理
        imgBGR = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgBGR)  # 偵測手部
        
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                # 取得所有 21 個手部關鍵點的 (x, y) 座標
                x = [int(lm.x * img.shape[1]) for lm in handLms.landmark]
                y = [int(lm.y * img.shape[0]) for lm in handLms.landmark]
                
                # 計算每個手指關鍵點到手掌根部 (x[0], y[0]) 的距離
                dis = [distance(x[i], y[i], x[0], y[0]) for i in range(21)]
                
                # 判斷每根手指是否張開 (1) 或閉合 (0)
                hand_state = [
                    1 if dis[8] > dis[6] else 0,   # 食指
                    1 if dis[12] > dis[10] else 0,  # 中指
                    1 if dis[16] > dis[14] else 0,  # 無名指
                    1 if dis[20] > dis[18] else 0,  # 小指
                    1 if dis[4] > dis[3] else 0,    # 拇指
                ]

                # 轉換手勢數據為字串格式，方便輸出與比對
                hand_str = "".join(map(str, hand_state))
                print(f"Detected Hand: {hand_str}")
                
                # 發送手勢數據到 FastAPI 伺服器
                try:
                    response = requests.post(API_URL, json={"hand_state": hand_state})
                    print("API 回應:", response.json())
                except requests.exceptions.RequestException as e:
                    print("❌ API 請求失敗:", e)
        
        # 顯示攝影機畫面
        cv2.imshow('Hand Detection', img)

    # 按下 'q' 鍵結束程式，或 10 秒後自動結束
    if cv2.waitKey(1) == ord('q') or time.time() - start_time > 10:
        break

# 釋放攝影機資源，關閉所有 OpenCV 視窗
cap.release()
cv2.destroyAllWindows()
