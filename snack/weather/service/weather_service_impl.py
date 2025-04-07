import requests
from datetime import datetime, timedelta
from urllib.parse import quote
import os

class WeatherServiceImpl:

    def __init__(self):
        self.service_key = os.getenv("KMA_API_KEY")
        self.base_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
        self.nx = 60  # 서울시청 기준 격자 좌표
        self.ny = 127

    def get_base_time(self, now: datetime) -> str:
        """
        현재 시간 기준으로 가장 가까운 정시 (10분 이전까지 보정)
        예: 14:03 → 1300, 14:15 → 1400
        """
        adjusted = now - timedelta(minutes=10)
        return adjusted.strftime("%H") + "00"

    def get_seoul_weather(self) -> dict:
        now = datetime.now()
        base_date = now.strftime("%Y%m%d")
        base_time = self.get_base_time(now)

        params = {
            "serviceKey": self.service_key,
            "numOfRows": 10,
            "pageNo": 1,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": self.nx,
            "ny": self.ny
        }

        try:
            response = requests.get(self.base_url, params=params)
            print("📡 요청 URL:", response.url)
            print("📄 응답 상태코드:", response.status_code)
            print("📩 응답 미리보기:", response.text[:300])

            data = response.json()

            if "response" not in data or data["response"]["header"]["resultCode"] != "00":
                return {
                    "message": "기상 정보를 불러오는 데 실패했습니다.",
                    "error": data.get("response", {}).get("header", {}).get("resultMsg", "알 수 없음")
                }

            items = data["response"]["body"]["items"]["item"]
            result = {}

            for item in items:
                category = item["category"]
                value = item["obsrValue"]
                if category == "T1H":
                    result["기온"] = f"{value}°C"
                elif category == "REH":
                    result["습도"] = f"{value}%"
                elif category == "RN1":
                    result["강수량"] = f"{value}mm"
                elif category == "WSD":
                    result["풍속"] = f"{value}m/s"

            return result or {"message": "해당 시간대에 기상 정보가 없습니다."}

        except requests.RequestException as req_err:
            return {"message": "기상청 API 요청 실패", "error": str(req_err)}
        except ValueError as val_err:
            return {"message": "응답 JSON 파싱 실패", "error": str(val_err)}
        except Exception as e:
            return {"message": "알 수 없는 에러 발생", "error": str(e)}
