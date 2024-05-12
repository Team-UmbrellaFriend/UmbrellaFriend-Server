from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import WithdrawalRecord
from datetime import datetime


class Command(BaseCommand):
    help = '만료된 회원탈퇴 기록 지우기'

    def handle(self, *args, **options):
        print("[", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "]")
        try:
            expired_records = WithdrawalRecord.objects.filter(expiration_date__lte=timezone.now())
            num_deleted, _ = expired_records.delete()
            print(f'{num_deleted} 개의 만료된 회원탈퇴 기록이 삭제되었습니다.')
        except Exception as e:
            print(f'회원탈퇴 기록 삭제 중 에러 발생: {e}')