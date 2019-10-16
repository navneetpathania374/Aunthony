from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

class Transactions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    from_addr = models.CharField(max_length=200)
    to_addr = models.CharField(max_length=200)
    asset = models.CharField(max_length=20, default='EUR')
    amount = models.CharField(max_length=200)

class Accounts(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    seed = models.CharField(max_length=800)
    qrcode_file = models.ImageField(upload_to='qrcode', blank=True, null=True)
    mobile_number  = models.CharField(max_length=128,null=True)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user_name

class Contact(models.Model):
    user_name = models.CharField(max_length=200)
    #created = models.DateTimeField(auto_now_add=True, blank=True)
    contact = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    memo = models.CharField(max_length=28, blank=True)
    def __str__(self):
        return self.contact

class Feedbacks(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Subject = models.CharField(max_length=200)
    Message = models.TextField()
    def __str__(self):
        return self.Email


class LoginHistory(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    user_name = models.CharField(max_length=200)
    last_logout = models.DateTimeField(auto_now_add=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True, blank=True)
    print(last_logout)
    def __unicode__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(self.action, self.user_name, self.ip, self.last_logout, self.login_time)
    def __str__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(self.action, self.user_name, self.ip, self.last_logout, self.login_time)
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    LoginHistory.objects.create(action='user_logged_in', ip=ip, user_name=user.username)
@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    LoginHistory.objects.create(action='user_logged_out', ip=ip, user_name=user.username)
@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    LoginHistory.objects.create(action='user_login_failed', user_name=credentials.get('username', None))
