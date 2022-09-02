from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'search'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('data_search/', views.data_search, name='data_search'),
    path('change_pw/', views.change_pw, name='change_pw'),
    path('data_search/', views.again_search_stock, name='again_search_stock'),
    path('appear_graph/', views.stock_data_graph, name='stock_data_graph'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )