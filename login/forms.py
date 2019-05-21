from django import forms
#验证码
from captcha.fields import CaptchaField
#顶部要先导入forms模块所有的表单类都要继承forms.Form类
class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                          'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                             'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')
#widget=forms.PasswordInput用于指定该字段在form表单里表现为<input type='password' />，也就是密码输入框