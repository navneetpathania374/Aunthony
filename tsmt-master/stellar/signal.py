import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from .models import LoginHistory

log = logging.getLogger(__name__)
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    log.debug('login user: {user} via ip: {ip}'.format(user=user,ip=ip))

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    username = request.user.username
    now = timezone.now()
    log.debug('logout user: {user} via ip: {ip}'.format(user=user,ip=ip))
    LoginHistory.objects.filter(user_name=username).update(last_logout=now,action='user_logged_out',ip=ip)

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    log.warning('logout failed for: {credentials}'.format(credentials=credentials,))