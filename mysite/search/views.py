
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import FinanceDataReader as fdr
from .models import Stockname_stocks
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
from . import models
import os
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import matplotlib
import platform
# Create your views here.

def index(request):
    return render(request, 'search/firstmain.html')


def login_page(request):
    return render(request, 'search/login.html')


@login_required(login_url='common:login')
def again_search_stock(request):
    return render(request, 'search/stock_search.html')


@login_required(login_url='common:login')
def data_search(request):
        global stock_data
        global stock_name
        global stock_code
        stock_name = request.POST.get('stock_name')
        start_date = request.POST.get('startdate')
        finish_date = request.POST.get('finishdate')
        if request.method == 'POST':
            if (stock_name == "" and start_date == "" and finish_date == ""):
                messages.info(request, "주식 이름, 날짜를 설정해주세요.")
            elif (stock_name == "" and start_date == ""):
                messages.info(request, "주식 이름, 시작 날짜를 설정해주세요.")
            elif (stock_name == "" and finish_date == ""):
                messages.info(request, "주식 이름, 종료 날짜를 설정해주세요.")
            elif (start_date == "" and finish_date == ""):
                messages.info(request, "시작 날짜, 종료 날짜를 설정해주세요..")
            elif (stock_name == ""):
                messages.info(request, "주식 이름을 입력해주세요. ")
            elif (start_date == ""):
                messages.info(request, "시작 날짜를 설정해주세요.")
            elif (finish_date == ""):
                messages.info(request, "종료 날짜를 설정해주세요.")
            else:
             try:
                    if platform.system() == 'Windows':    #그래프 한글 설정
                        matplotlib.rc('font', family='Malgun Gothic')
                    elif platform.system() == 'Darwin': # Mac
                         matplotlib.rc('font', family='AppleGothic')
                    else: #linux
                         matplotlib.rc('font', family='NanumGothic')
                    stock_code = Stockname_stocks.objects.get(stockname=stock_name)
                    stock_data = fdr.DataReader(stock_code.stockcode, start_date, finish_date)
                    stock_data = stock_data.drop(['Change'], axis=1)
                    stock_data.columns = ['시가', '최고가', '최저가', '종가', '거래량']
                    stock_data.to_excel('media/{}.xlsx'.format(stock_code.stockcode))
                    fig = plt.figure()
                    mk2 = fig.add_subplot(1, 1, 1)
                    plt.plot(stock_data['종가'])
                    mk2.set_title('{}'.format(stock_name))
                    mk2.set_xlabel('Date')
                    mk2.set_ylabel('종가')
                    plt.xticks(rotation=20)
                    fig.savefig('./static/graph.png')
                    document = models.Document(
                        title=stock_name,
                        uploadedFile='media/{}.xlsx'.format(stock_code.stockcode))
                    document.save()
                    file_path = os.path.abspath("media/")
                    file_name = os.path.basename("media/{}.xlsx".format(stock_code.stockcode))
                    fs = FileSystemStorage(file_path)
                    response = FileResponse(fs.open(file_name, 'rb'), content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=' + "{}.xlsx".format(stock_code.stockcode)
                    return response
             except:
                    messages.info(request, "검색정보가 일치하지 않습니다.")

             context = {}
             return render(request, 'search/stock_search.html', context)

        else:
            return render(request, 'search/stock_search.html')


@login_required(login_url='common:login')
def stock_data_graph(request):
    file_path = "./static/graph.png"
    if os.path.exists(file_path):
      # os.remove(file_path)
       return render(request, 'search/graph.html')
    else:
       messages.info(request, "그래프 정보가 존재하지 않습니다.")
       return render(request, 'search/stock_search.html')


@login_required(login_url='common:login')
def change_pw(request):
    user = request.user
    oringin_pw = request.POST.get('currentPassword')
    new_pw = request.POST.get('new_password12')
    confirm_pw = request.POST.get('new_password22')
    if request.method == 'POST':
                if (oringin_pw == "" and new_pw == "" and confirm_pw == ""):
                    messages.info(request, "기존 비밀번호, 새 비밀번호을 입력해주세요.")
                elif (oringin_pw == "" and new_pw == ""):
                    messages.info(request, "기존 비밀번호, 새 비밀번호를 입력해주세요.")
                elif (oringin_pw == "" and confirm_pw == ""):
                    messages.info(request, "기존 비밀번호, 새 비밀번호 확인을 입력해주세요.")
                elif (new_pw == "" and confirm_pw == ""):
                    messages.info(request, "새 비밀번호, 새 비밀번호 확인을 입력해주세요.")
                elif (oringin_pw == ""):
                    messages.info(request, "기존 비밀번호를 입력해주세요. ")
                elif (new_pw == ""):
                    messages.info(request, "새 비밀번호를 입력해주세요.")
                elif (confirm_pw == ""):
                    messages.info(request, "새 비밀번호 확인을 입력해주세요.")
                else:
                    if check_password(oringin_pw, user.password):
                            if new_pw == confirm_pw:
                                user.set_password(new_pw)
                                user.save()
                                auth.login(request, user)
                                return render(request, 'search/stock_search.html')
                            else:
                                messages.info(request, '비밀번호가 다릅니다')
                    else:
                        messages.error(request, '기존 비밀번호가 옳바르지 않습니다.')
                        return render(request, 'search/password_reset_confirm.html')
                    return render(request, 'search/password_reset_confirm.html')
    context = {}
    return render(request, 'search/password_reset_confirm.html', context)