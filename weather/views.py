#weather/views.py
from urllib.parse import urlencode
from django.core.cache import cache
from datetime import datetime, timedelta
import requests, json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_api_key(filename="secrets.json"):
    """
    API 키를 파일에서 로드하는 함수
    """
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
    """
    기준 날짜와 시간을 계산하는 함수
    """
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


def fetch_rain_data(base_date, base_time):
    """
    외부 API를 통해 강수 정보를 가져오는 함수
    """
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    queryString = "?" + urlencode(
        {
            "serviceKey": load_api_key(),
            "pageNo": 1,
            "numOfRows": 10,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": 60,  # 청파동 위치 좌표 (nx, ny)
            "ny": 125,
        }
    )
    queryURL = url + queryString
    response = requests.get(queryURL)

    return response


def parse_rain_data(response):
    """
    API 응답에서 강수 정보를 파싱하는 함수
    """
    try:
        r_dict = json.loads(response.text)
        r_response = r_dict.get("response", {})
        r_body = r_response.get("body", {})
        r_items = r_body.get("items", {})
        r_item = r_items.get("item", None)

        if r_item:
            for item in r_item:
                if item.get("category") == "POP":  # 강수 확률
                    return item.get("fcstValue")
    except json.JSONDecodeError:
        pass

    return "0"  # 기본값 반환


def calculate_next_base_time(current_time, base_time):
    """
    다음 기준 시간을 계산하는 함수
    """
    next_hour = (int(base_time) + 300) % 2400
    next_base_time = f"{next_hour:04d}"
    
    if next_base_time == "0200" and base_time == "2300":
        # 현재 시간이 2300이고, 다음 시간이 0200인 경우 다음 날의 시간을 계산
        next_day = current_time + timedelta(days=1)
        return datetime.combine(next_day, datetime.strptime(next_base_time, '%H%M').time())
    else:
        return datetime.combine(datetime.today(), datetime.strptime(next_base_time, '%H%M').time())


def get_rain_percent(request):
    """
    강수 확률을 반환하고 캐시에 저장하는 함수
    """
    current_time, base_date, base_time = calculate_base_date_and_time()

    # 캐시가 존재하면 캐시 값 리턴
    cache_key = f'rain_percent_{base_date}_{base_time}'
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info(f"Caching data: {cached_data}")
        return cached_data

    # 캐시가 존재하지 않을 때 외부 API 호출해서 강수 확률 가져오기
    response = fetch_rain_data(base_date, base_time)
    rain_percent = parse_rain_data(response)

    date = current_time.strftime("%Y") + "년 " + current_time.strftime("%m") + "월 " + current_time.strftime("%d") + "일"
    rain_data = {"date": date, "percent": rain_percent}

    # 캐시에 강수 확률 저장
    next_base_time = calculate_next_base_time(current_time, base_time)
    remaining_time = next_base_time - current_time
    
    cache_timeout = remaining_time.total_seconds()
    cache.set(cache_key, rain_data, timeout=cache_timeout)

    logger.info(f"Caching data for key: {cache_key}, data: {rain_data}, current_time: {current_time}, next_time: {next_base_time}, remaining_time: {remaining_time}")
    return rain_data