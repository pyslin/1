from django.contrib import admin

# Register your models here.
#注册模型
from .import models
admin.site.register(models.User)
admin.site.register(models.ConfirmString)