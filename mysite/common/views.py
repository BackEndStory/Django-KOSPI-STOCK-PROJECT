
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import random
from django.contrib import messages
import os



# Create your views here.


def register(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return render(request, 'search/secondmain.html')
    else:
        form = UserForm()
    return render(request, 'search/new_account.html', {'form': form})


def forgot_id(request):
    return render(request, 'search/forgot_id.html')


def next_stock_search(request):
    file_path = "./static/graph.png"
    if os.path.exists(file_path):
       os.remove(file_path)
    return render(request, 'search/stock_search.html')


def ForgotIDview(request):
    context = {}
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    if request.method == 'POST':
        try:
            user = User.objects.get(email=email, first_name=first_name)
            subject = "KOSPI SEARCH SITE"
            content1 = "회원님의 아이디는 "
            content2 = " 입니다."
            from_email = "opop0421@naver.com"
            if user is not None:
                EmailMessage(subject=subject, body=(content1 + str(user.username) + content2), to=[email],
                             from_email=from_email).send()
                return render(request, 'search/secondmain.html')
        except:
            if (email == "" and first_name == ""):
                messages.info(request, "이름, 이메일을 입력해주세요.")
            elif (email == ""):
                messages.info(request, "이메일을 입력해주세요. ")
            elif (first_name == ""):
                messages.info(request, "이름을 입력해주세요.")
            else :
                messages.info(request, "이름 또는 이메일이 옳바르지 않습니다.")
    context = {}
    return render(request, 'search/forgot_id.html', context)


def ForgotPWview(request):
    random_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
                       '5', '6', '7', '8', '9']
    answer_string = [random.choice(random_alphabet) for i in range(10)]
    result = ''.join(s for s in answer_string)
    context = {}
    username = request.POST.get('username')
    email = request.POST.get('email')
    if request.method == 'POST':
        try:
            user = User.objects.get(email=email, username=username)
            user.set_password(result)
            user.save()
            subject = "KOSPI SEARCH SITE"
            content1 = "회원님의 임시비밀번호는 "
            content2 = " 입니다."
            from_email = "opop0421@naver.com"
            if user is not None:
                EmailMessage(subject=subject, body=(content1 + str(result) + content2), to=[email],
                  from_email=from_email).send()
                return render(request, 'search/secondmain.html', context)
        except:
            if (email == "" and username == ""):
                messages.info(request, "아이디, 이메일을 입력해주세요.")
            elif (email == ""):
                messages.info(request, "이메일을 입력해주세요. ")
            elif (username == ""):
                messages.info(request, "아이디를 입력해주세요.")
            else:
                messages.info(request, "아이디 또는 이메일이 옳바르지 않습니다.")
    context = {}
    return render(request, 'search/password_reset.html', context)


