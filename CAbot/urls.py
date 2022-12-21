from django.contrib import admin
from django.urls import path

from home import views as homeViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeViews.HomeView),
    path('caHome/', homeViews.CAHomeView),
    path('caHome/<str:userIP>', homeViews.CAChatView),
    path('consulting/', homeViews.ConsultingView.as_view()),
    path('consulting/consultingdata/', homeViews.ConsultingDataView),

    #API
    path('sendmessage/', homeViews.SendMessageAPI),

    # 추가페이지
    path('company/', homeViews.CompanyView),
    path('agreement/', homeViews.AgreementView),
]
