from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Homework
from HomeworkCentre.settings import EMAIL_HOST_USER


# @receiver(m2m_changed, sender=Homework.students.through)
# def homework_has_been_created(sender, instance, action, model, pk_set, **kwargs):
#     if action == 'post_add':
#         print('NOWE ZADANIE')
#         hom = Homework.objects.get(id=instance.id)
#         student_class_before = hom.students.all()
#         rec_list = set()
        
#         for id in pk_set:
#             student_class = model.objects.get(id=id).members.all()
#             for student in student_class:
#                 rec_list.add(student.email)

#         message = f'''
#         <center>
#         <h1>{instance.teacher} DODAŁ NOWE ZADANIE!</h1>
#         <div style='border:5px solid green;'>
#         <p>tytuł: {instance.title}</p>
#         <p>opis: <q>{instance.description}</q></p>
#         <p>termin oddania: {instance.deadline}<p>
#         <div>
#         <p>Aby oddać odpowiedź do zadania, zaloguj się do serwisu HomeCentre</p>
#         </center>
#         '''
#         send_mail('[HomeworkCentre] - nowe zadanie ', message=message, html_message=message,
#                    from_email=f'HomeworkCentre <{EMAIL_HOST_USER}>', recipient_list=list(rec_list))
