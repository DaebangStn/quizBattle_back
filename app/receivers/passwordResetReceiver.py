from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    reset_url = "http://localhost:3000/password/reset/confirm/?token={}".format(
            reset_password_token.key)

    email_content = "사용자 {}의 비밀번호 초기화 링크 {}".format(
        reset_password_token.user.username, reset_url)

    send_mail(
        '퀴즈게임 비밀번호 초기화',
        email_content,
        'from@example.com',
        [reset_password_token.user.email],
        fail_silently=False,
    )
