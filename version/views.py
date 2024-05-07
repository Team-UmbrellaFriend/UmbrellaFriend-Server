from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@api_view(['GET'])
def get_version_info(request):
    try:
        version_data = {
            "iosVersion": {
                "appVersion": "1.0.0",
                "forceUpdateVersion": "0.0.0"
            },
            "androidVersion": {
                "appVersion": "1.0.0",
                "forceUpdateVersion": "0.0.0"
            },
            "notificationTitle": "새로운 버전이 업데이트 되었어요!",
            "notificationContent": "안정적인 서비스 사용을 위해\n최신버전으로 업데이트 해주세요."
        }
        response_data = {
            "status": status.HTTP_200_OK,
            "message": "버전 정보 조회 성공",
            "data": version_data
        }
        return Response(response_data, status = status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"버전 정보 호출 에러: {e}")
        response_data = {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "내부 서버 에러",
            "data": ""
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)