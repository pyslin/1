from django.shortcuts import render
from django.shortcuts import redirect
from . import models

# Create your views here.
def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    #request.method中封装了数据请求的方法
    if request.method == 'POST':
        #request.POST封装了所有POST请求中的数据，这是一个字典类型，可以通过get方法获取具体的值
        #username’是HTML模板中表单的input元素里‘name’属性定义的值。
        # 所以在编写form表单的时候一定不能忘记添加name属性。
        username = request.POST.get('username')
        password = request.POST.get('password')
        message ='请检查填写的内容!'
        # 确保用户名和密码都不为空
        if username.strip() and password:
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

def register(request):
    pass
    return render(request, 'login/register.html')

def logout(request):
    pass
    return redirect('/login/')