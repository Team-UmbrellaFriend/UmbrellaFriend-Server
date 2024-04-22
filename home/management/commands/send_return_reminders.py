from django.core.management.base import BaseCommand
from umbrella.models import Rent
from django.core.mail import EmailMessage
from datetime import datetime
from firebase_admin import messaging


# 푸시 알림
def send_push_notification(token):
    message = messaging.Message(
        notification=messaging.Notification(
            title='🚨우산 대여 만료 예정🚨',
            body='우산 반납일까지 1일 남았습니다!',
        ),
        token=token,
    )
    response = messaging.send(message)
    print("푸쉬 알림 성공")


# 이메일
def send_return_reminder_email(user_name, user_email, days_remaining):
    subject = '[우산친구] 🚨 우산 대여 기간 만료 예정 알림 🚨'
    message = f'{user_name}님, 우산 대여 기간이 곧 만료될 예정입니다. \n'\
            f'우산 반납까지 {days_remaining}일 남았습니다. \n' \
            f'연체한 일 수 만큼 우산 대여가 불가하오니 기한 만료 전 반납 부탁드립니다.'

    recipient_list = [user_email]
    EmailMessage(subject = subject, body = message, to = recipient_list).send()
    print('이메일 전송 성공')


class Command(BaseCommand):
    help = '반납일 하루 남은 유저에게 반납 리마인드 메세지 전송하기'

    def handle(self, *args, **options):
        users_to_remind = Rent.objects.filter(return_date = None)
        for user in users_to_remind:
            try:
                days_remaining = max(0, (user.return_due_date - datetime.now()).days)
                if days_remaining == 1:
                    user_email = user.user.email  # Rent 모델의 ForeignKey 관계인 user 필드를 통해 사용자 정보에 접근
                    fcm_token = user.user.profile.fcm_token # 푸시 알림을 보낼 사용자의 FCM 토큰
                    print("사용자 토큰 : ", fcm_token)

                    send_return_reminder_email(user.user.username, user_email, days_remaining)
                    send_push_notification(fcm_token)
            except Exception as e:
                print(f'알림 에러 발생: {e}')