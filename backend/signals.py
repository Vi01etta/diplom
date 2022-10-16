from django.dispatch import receiver, Signal

from backend.models import ConfirmEmailToken, User
from .tasks import send_email

new_user_registered = Signal()

new_order = Signal()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    message = token.key
    email = token.user.email
    send_email(message, email)

    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Password Reset Token for {token.user.email}",
    #     # message:
    #     token.key,
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [token.user.email]
    # )
    # msg.send()


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    title = "Обновление статуса заказа"
    message = 'Заказ сформирован'
    email = user.email
    send_email.apply_async((title, message, email), countdown=5 * 60)
