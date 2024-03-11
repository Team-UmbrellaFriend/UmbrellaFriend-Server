#weather/views.py
from urllib.parse import urlencode
from datetime import datetime, timedelta
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


def calculate_base_date_and_time():
    current_time = datetime.now()
    base_times = ["0200", "0500", "0800", "1100", "1400", "1700", "2000", "2300"]

    for base_time in base_times:
        if current_time.hour < int(base_time[:2]):
            base_date = (current_time - timedelta(days = (1 if base_time == "0200" else 0))).strftime("%Y%m%d")
            base_time = "2300" if base_time == "0200" else base_times[base_times.index(base_time) - 1]
            break
    else:
        base_time = "2300"
        base_date = current_time.strftime("%Y%m%d")

    return current_time, base_date, base_time


def get_rain_percent(request):
    current_time, base_date, base_time = calculate_base_date_and_time()

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    queryString = "?" + urlencode(
        {
        "serviceKey": load_api_key(),
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": 60,   # 청파동 위치 좌표 (nx, ny)
        "ny": 125,
        }
    )
    queryURL = url + queryString
    response = requests.get(queryURL)

    date = current_time.strftime("%Y") + "년 " + current_time.strftime("%m") + "월 " + current_time.strftime("%d") + "일"

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
        if isinstance(result, dict) and "fcstValue" in result:
            return {"date": date, "percent": result["fcstValue"]}
        else:
            return {'date': date, 'percent': "-1"}
    except json.JSONDecodeError:
        return {'date': date, 'percent': "-1"}