from django.urls import path
from smithy.views.main import main_slogan, result, loading_view
from django.contrib.auth.views import LoginView, LogoutView
from smithy.views.account import AccountCreateView, AccountDetailView, AccountUpdateView


app_name = "smithy"

urlpatterns = [
    path("update/<int:pk>", AccountUpdateView.as_view(), name="update"),
    path("detail/<int:pk>", AccountDetailView.as_view(), name="detail"),
    path("login/", LoginView.as_view(template_name="smithy/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", AccountCreateView.as_view(), name="create"),
    path("index/", main_slogan, name="index"),  # url, 연결할 view 함수명, name
    path("loading/", loading_view, name="loading"),
    path("result_slogan/", result, name="result_slogan"),
]
