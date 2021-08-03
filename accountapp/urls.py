from django.urls import path

from accountapp.views import main_slogan

app_nanme = "accountapp"

urlpatterns = [
    # account/main_slogan
    path('main_slogan/', main_slogan, name="main_slogan"),  # url, 연결할 view 함수명, name 
]