from django.shortcuts import render
from django.shortcuts import redirect
#引入表单 模型
from . import models
from . import forms
import hashlib

# Create your views here.
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    #session未登录限制访问的代码
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')
"""
def login(request):
    #request.method中封装了数据请求的方法
    if request.method == 'POST':
        #request.POST封装了所有POST请求中的数据，这是一个字典类型，可以通过get方法获取具体的值
        #username’是HTML模板中表单的input元素里‘name’属性定义的值。
        # 所以在编写form表单的时候一定不能忘记添加name属性。
        #username = request.POST.get('username')
        #password = request.POST.get('password')
        login_form = forms.UserForm(request.POST)
        message ='请检查填写的内容!'
        # 确保用户名和密码都不为空
        #if username.strip() and password:
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                #post的username 传入模型取得对象
                user = models.User.objects.get(name=username)
                #如果未匹配到用户，则执行except中的语句；注意这里没有区分异常的类型
                #我们要对用户屏蔽这些信息，不可以暴露给用户，而是统一返回一个错误提示
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html',{'message': message})
            if user.password == password:
                print(username, password)
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request,'login/login.html',{'message':message})
        else:
            return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')
#增加了message变量，用于保存提示信息。当有错误信息的时候，将错误信息打包成一个字典，
#然后作为第三个参数提供给render方法。这个数据字典在渲染模板的时候会传递到模板里供你调用。
"""
def login(request):
    # 不允许重复登录
    if request.session.get('is_login', None):
        return redirect('/index/')
    #先实例化，不然出不了输入框
    login_form = forms.UserForm()
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                #往session字典内写入用户状态和数据：
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())
"""重点在于注册逻辑，首先两次输入的密码必须相同，其次不能存在相同用户名和邮箱，
最后如果条件都满足，利用ORM的API，创建一个用户实例，然后保存到数据库内"""

def logout(request):
    # 如果本来就未登录，也就没有登出一说
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')