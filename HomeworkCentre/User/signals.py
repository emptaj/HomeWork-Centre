from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import CustomUser
from HomeworkCentre.settings import EMAIL_HOST_USER


# @receiver(pre_save, sender=CustomUser)
# def user_has_been_activated(sender, instance, **kwargs):
#     try:
#         old_status = CustomUser.objects.get(id=instance.id).is_active
#         if old_status is False and instance.is_active:
#             message = f'''
#             <center>
#             <h2>AKTYWACJA KONTA W SERWISIE HOMEWORK-CENTRE!</h2>
#             <p>użytkownik: {instance.first_name} {instance.last_name}, Twoje konto zostało aktywowane</p>
#             <p>Możesz w pełni korzystać z serwisu.</p>
#             <p>Zaloguj się: <a href="127.0.0.1:8000/user">ZALOGUJ</p>
#             </center>
#             '''
#             send_mail('[HomeworkCentre] - aktywacja nowego użytkownika ', message=message, html_message=message,
#                       from_email=f'HomeworkCentre <{EMAIL_HOST_USER}>', recipient_list=[instance.email])

#     except CustomUser.DoesNotExist:
#         return

