#common/exception_handler.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        # HTTP 401 Unauthorized 에러에 대한 커스텀 응답 생성
        custom_response = {'status': status.HTTP_401_UNAUTHORIZED, 'message': '인증되지 않았습니다', 'data': None}
        return Response(custom_response, status=status.HTTP_401_UNAUTHORIZED)

    if response is not None:
        custom_data = {
            'status': response.status_code,
            'message': '로그인 실패',
            'data': response.data
        }
        response.data = custom_data
    return response
