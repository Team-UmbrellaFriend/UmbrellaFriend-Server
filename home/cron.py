from django.core.management import call_command

def send_return_reminders():
    call_command('send_return_reminders')

def delete_withdrawal_records():
    call_command('delete_expired_withdrawal_records')