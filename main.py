import requests
from bs4 import BeautifulSoup
import time
import random
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9",
    "Referer": "https://tixcraft.com/",
    "Cookie": "eps_sid=0bde2f1534bbf6f4.1779168376.46G0Q6c+a/qlTBPfDHo4UCZ/isQPeVD+/JeYMvFczto=; tmpt=1:CAESGJYAhzBV93uuuuZ3aqoJ9TSp-t-Nq1Kudxj56K_QBiIvk-1Ptzk9x_d1iD2YGzyQBItA04ywB3H0qFvU15KyJdvNogFIicLDQAB6TRq8row; TIXUISID=rto510t3og9kc96o14g2anm89h; _csrf=1d0a7644beb6883220fec7999e78607420a71ca44c098d8e2b784f6b644e55afa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ynp_iPJNL_gaGPhdfSkJdJ2r0bkBBP9F%22%3B%7D; BID=3YLJF1xPTNefOXAR0hC0RSrnIt3lzLGGELwxrme-BAyZkW92HW4-AVhraRESi84yzsPTH4IbG3fGRTMi; _fbp=fb.1.1779168379021.428883649654155426; OptanonAlertBoxClosed=2026-05-19T05:26:21.227Z; _ga=GA1.2.370534075.1779168379; _gid=GA1.2.1570397975.1779168381; _dc_gtm_UA-51347908-1=1; _ga_C3KRPGTSF6=GS2.1.s1779168378$o1$g1$t1779168381$j60$l0$h0; ab.storage.deviceId.e715aa3d-e50f-4f5a-a073-a3d081f5fa19=%7B%22g%22%3A%22022ccf3b-358d-1d0f-847a-aca1ccb72ef4%22%2C%22c%22%3A1779168381446%2C%22l%22%3A1779168381446%7D; ab.storage.sessionId.e715aa3d-e50f-4f5a-a073-a3d081f5fa19=%7B%22g%22%3A%22387a84b3-f49e-e270-a56a-9e2f452fc368%22%2C%22e%22%3A1779170181451%2C%22c%22%3A1779168381445%2C%22l%22%3A1779168381451%7D; OptanonConsent=isGpcEnabled=0&datestamp=Tue+May+19+2026+13%3A26%3A21+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202601.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=ae8906ab-79db-4702-9383-040d0176d15f&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&intType=1&crTime=1779168381851"
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

TARGET_URL = "https://tixcraft.com/ticket/area/26_aespa/22415"
# TARGET_URL = "https://tixcraft.com/ticket/area/26_youngji/22448"

def notify_mac(title, message):
    # 跳出系統通知 + 播放音效
    os.system(f"""osascript -e 'display notification "{message}" with title "{title}" sound name "Glass"'""")


# resp = SESSION.get(TARGET_URL, timeout=10)
# soup = BeautifulSoup(resp.text, "html.parser")

# # 存成檔案方便你用瀏覽器開來看
# with open("debug.html", "w", encoding="utf-8") as f:
#     f.write(resp.text)

# print("狀態碼:", resp.status_code)
# print("已存成 debug.html")

# # 印出所有含「票」「sold」「buy」的文字節點
# for tag in soup.find_all(True):
#     text = tag.get_text(strip=True)
#     cls = tag.get("class", [])
#     if any(k in text.lower() for k in ["售完", "sold", "已售"]) or \
#        any(k in str(cls).lower() for k in ["buy", "sold", "ticket", "btn"]):
#         print(f"<{tag.name} class={cls}>: {text[:80]}")

def check_tickets():
    try:
        resp = SESSION.get(TARGET_URL, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # 找所有區域 li
        area_items = soup.select("ul.area-list li")
        
        available = []
        sold_out = []

        for li in area_items:
            text = li.get_text(strip=True)
            if "熱賣中" in text or "剩餘" in text:
                available.append(text)
        
        if available:
            print(f"[{time.strftime('%H:%M:%S')}] 🎫 有票: {available}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] 目前全數售完，繼續監控...")

        return available

    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def main():
    print("開始監控拓元票務...", f"目標網址: {TARGET_URL}")
    notified = set()  # 避免重複通知同一區域

    while True:
        available = check_tickets()

        for zone in available:
            if zone not in notified:
                notify_mac("🎫 拓元有票！", f"{zone}\n快去搶！")
                msg = f"🎫 有票！{zone}\n立即購票：{TARGET_URL}"
                print(msg)
                notified.add(zone)

        # 售完後又出現新票要重新通知，清除記錄
        if not available:
            notified.clear()

        time.sleep(random.uniform(30, 60))

if __name__ == "__main__":
    main()