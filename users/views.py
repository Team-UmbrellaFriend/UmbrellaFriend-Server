#users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SignUpSerializer, LoginSerializer, UserUpdateSerializer
from .models import CustomUser

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response({'status': status.HTTP_201_CREATED, 'message': '회원가입이 완료되었습니다', 'data': {'token': user_data['token']}}, status = status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            error_messages = {
                "profile_studentID": "이미 존재하는 학번입니다.",
                "email": "이미 등록된 이메일 주소입니다."
            }
            profile_error = None
            email_error = None
            password_error = None

            for field, error in errors.items():
                if field == 'profile':
                    if not profile_error:
                        for sub_field, sub_error in error.items():
                            if sub_field == 'studentID':
                                profile_error = error_messages.get("profile_studentID")
                elif field == 'email':
                    if not email_error:
                        email_error = error_messages.get("email")
                elif field == 'password':
                    if not password_error:
                        password_errors = []
                        for error_detail in error:
                            if error_detail.code == 'blank':
                                password_errors.append("비밀번호를 입력하세요.")
                            elif error_detail.code == 'password_too_short':
                                password_errors.append("비밀번호는 최소 8자 이상이어야 합니다.")
                            elif error_detail.code == 'invalid':
                                password_errors.append("비밀번호가 일치하지 않습니다.")
                        password_error = password_errors
            if profile_error:
                return Response({'status': 400, 'message': profile_error, 'data': ''}, status = status.HTTP_400_BAD_REQUEST)
            if email_error:
                return Response({'status': 400, 'message': email_error, 'data': ''}, status = status.HTTP_400_BAD_REQUEST)
            if password_error:
                return Response({'status': 400, 'message': password_error[0], 'data': ''}, status = status.HTTP_400_BAD_REQUEST)
            return Response({'status': 400, 'message': '복잡한 비밀번호로 설정해주세요.', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        token = serializer.validated_data # validate()의 리턴값인 token 받아오기
        return Response({'status': status.HTTP_200_OK, 'message': '로그인되었습니다', 'data': {'token': token.key}}, status = status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def get(self, request, format = None):
        request.user.auth_token.delete()

        logout_data = {
            'status': status.HTTP_200_OK,
            'message': '로그아웃되었습니다',
            'data': ''
        }
        return Response(logout_data, status = logout_data['status'])

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user)
        return Response({'status': status.HTTP_200_OK, 'message': '응답 성공', 'data': serializer.data}, status = status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'message': '프로필이 수정되었습니다', 'data': serializer.data}, status = status.HTTP_200_OK)
        else:
            errors = serializer.errors
            invalid_error = None
            password_error = None

            for field, error in errors.items():
                if field == 'password':
                    if not password_error:
                        password_errors = []
                        for error_detail in error:
                            if error_detail.code == 'password_too_short':
                                password_errors.append("비밀번호는 최소 8자 이상이어야 합니다.")
                            elif error_detail.code == 'password_too_common':
                                password_errors.append("비밀번호는 최소 8자 이상이어야 합니다.")
                            elif error_detail.code == 'invalid':
                                password_errors.append("비밀번호가 일치하지 않습니다.")
                        password_error = password_errors
                elif field == 'non_field_errors':
                    if not invalid_error:
                        invalid_error = error

            if invalid_error:
                return Response({'status': 400, 'message': invalid_error[0], 'data': ''}, status = status.HTTP_400_BAD_REQUEST)
            if password_error:
                return Response({'status': 400, 'message': password_error[0], 'data': ''}, status = status.HTTP_400_BAD_REQUEST)
            return Response({'status': 400, 'message': '유효하지 않은 데이터입니다.', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)