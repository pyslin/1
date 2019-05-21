from django.db import models

# Create your models here.
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        #定义用户按创建时间的反序排列，也就是最近的最先显示
        ordering = ['-c_time']
        #模型的名字，便于引用使用
        verbose_name = '用户'
        verbose_name_plural = '用户'


