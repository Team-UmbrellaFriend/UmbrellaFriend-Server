from django.core.management import call_command

def send_return_reminder_email():
    call_command('send_return_reminders')