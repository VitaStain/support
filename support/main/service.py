from django.core.mail import send_mail


def send(email):
    send_mail(
        'Ответ',
        'Вам ответили.',
        'some@mail.ru',
        [email]
    )
