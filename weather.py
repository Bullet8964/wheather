import os
import requests


# =========================
# 設定地點
# =========================

LOCATION_NAME = "台北市"

LATITUDE = 25.0330
LONGITUDE = 121.5654


# =========================
# 降雨機率門檻
# =========================

RAIN_THRESHOLD = 30


# =========================
# 從 GitHub Secrets 取得
# Telegram Bot Token / Chat ID
# =========================

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


# 檢查 Secret 是否存在

if not TELEGRAM_TOKEN:
    raise RuntimeError("找不到 TELEGRAM_BOT_TOKEN")

if not TELEGRAM_CHAT_ID:
    raise RuntimeError("找不到 TELEGRAM_CHAT_ID")


# =========================
# Open-Meteo API
# =========================

api_url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "daily": "precipitation_probability_max",
    "forecast_days": 1,
    "timezone": "Asia/Taipei"
}


# =========================
# 取得天氣資料
# =========================

response = requests.get(
    api_url,
    params=params,
    timeout=10
)

response.raise_for_status()

data = response.json()


# =========================
# 取得今天日期
# =========================

date = data["daily"]["time"][0]

rain_probability = data["daily"][
    "precipitation_probability_max"
][0]


print("================================")
print("今日降雨機率檢查")
print("================================")

print(f"地點：{LOCATION_NAME}")
print(f"日期：{date}")
print(f"最高降雨機率：{rain_probability}%")
print(f"通知門檻：{RAIN_THRESHOLD}%")

print("================================")


# =========================
# 判斷是否需要通知
# =========================

if rain_probability > RAIN_THRESHOLD:

    message = (
        f"☔ 降雨提醒\n\n"
        f"地點：{LOCATION_NAME}\n"
        f"日期：{date}\n"
        f"今日最高降雨機率：{rain_probability}%\n\n"
        f"降雨機率已超過 {RAIN_THRESHOLD}%！\n"
        f"記得帶傘喔！"
    )

    telegram_url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_TOKEN}/sendMessage"
    )

    telegram_response = requests.post(
        telegram_url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        },
        timeout=10
    )

    telegram_response.raise_for_status()

    print("Telegram 通知已發送！")

else:

    print(
        f"降雨機率沒有超過 {RAIN_THRESHOLD}%，"
        "不需要通知。"
    )
