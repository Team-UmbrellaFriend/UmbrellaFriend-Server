from django.core.mail import EmailMessage

def send_return_reminder_email(user_name, user_email, days_remaining):
    subject = '[우산친구] 🚨 우산 대여 기간 만료 예정 알림 🚨'
    message = f'{user_name}님, 우산 대여 기간이 곧 만료될 예정입니다. \n'\
            f'우산 반납까지 {days_remaining}일 남았습니다. \n' \
            f'연체한 일 수 만큼 우산 대여가 불가하오니 기한 만료 전 반납 부탁드립니다.'

    recipient_list = [user_email]
    EmailMessage(subject = subject, body = message, to = recipient_list).send()
