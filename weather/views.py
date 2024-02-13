#weather/views.py
from urllib.parse import urlencode
from datetime import datetime
import requests, json


def load_api_key(filename="secrets.json"):
    try:
        with open(filename, "r") as file:
            secrets = json.load(file)
            return secrets.get("WEATHER_KEY")
    except FileNotFoundError:
        print(f"{filename} 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"{filename} 파일을 파싱할 수 없습니다.")
        return None


def get_rain_percent(request):
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    queryString = "?" + urlencode(
        {
        "serviceKey": load_api_key(),
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "base_date": datetime.today().strftime("%Y%m%d"),
        "base_time": "0500",
        "nx": 60,   # 청파동 위치 좌표 (nx, ny)
        "ny": 125,
        }
    )
    queryURL = url + queryString
    response = requests.get(queryURL)

    date = datetime.today().strftime("%Y") + "년" + datetime.today().strftime("%m") + "월" + datetime.today().strftime("%d") + "일"
    try:
        r_dict = json.loads(response.text)
        r_response = r_dict.get("response", {})
        r_body = r_response.get("body", {})
        r_items = r_body.get("items", {})
        r_item = r_items.get("item", None)

        result = {}
        if r_item:
            for item in r_item:
                if(item.get("category") == "POP"): # 강수 확률
                    result = item
                    break
            return {"date": date, "percent": result.get("fcstValue")}
        else:
            return {'date': date, 'percent': -1}
    except (json.JSONDecodeError, ValueError):
        return {'date': date, 'percent': -1}