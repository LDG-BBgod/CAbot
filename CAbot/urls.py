from django.contrib import admin
from django.urls import path

from home import views as homeViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeViews.HomeView),
]
