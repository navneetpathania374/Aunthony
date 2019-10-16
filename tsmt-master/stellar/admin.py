from django.contrib import admin

from .models import Accounts,LoginHistory
admin.site.register(Accounts)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user_name','action', 'ip','last_logout']
    list_filter = ['action',]