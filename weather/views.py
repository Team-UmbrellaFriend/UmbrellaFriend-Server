#weather/views.py
from urllib.parse import urlencode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests, json


def load_api_key(filename="../secrets.json"):
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


@api_view(['GET'])
def get_rain_percent(request):
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    queryString = "?" + urlencode(
        {
        "serviceKey": load_api_key(),
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "base_date": "20240207",
        "base_time": "0500",
        "nx": 60,   # 청파동 위치 좌표 (nx, ny)
        "ny": 125,
        }
    )
    queryURL = url + queryString
    response = requests.get(queryURL)
    r_dict = json.loads(response.text)
    r_item = r_dict.get("response").get("body").get("items").get("item")

    result = {}
    for item in r_item:
        if(item.get("category") == "POP"): # 강수 확률
            result = item
            break

    return Response({"percent": result.get("fcstValue")}, status = status.HTTP_200_OK)