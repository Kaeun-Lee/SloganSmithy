from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from smithy.forms import AccountUpdateForm


class AccountCreateView(CreateView):
    model = User  # 장고에서 기본 제공해주는 모델
    form_class = UserCreationForm
    success_url = reverse_lazy("smithy:index")  # 성공시 돌아가는 url
    template_name = "smithy/create.html"  # 회원가입 할 때 보여질 html


class AccountDetailView(DetailView):
    model = User
    context_object_name = "target_user"
    template_name = "smithy/detail.html"  # 모델 안에 있는 정보를 시각화해줄 페이지



class AccountUpdateView(UpdateView):
    model = User  # 장고에서 기본 제공해주는 모델
    form_class = AccountUpdateForm
    success_url = reverse_lazy("smithy:index")  # 성공시 돌아가는 url
    template_name = "smithy/update.html"  # 회원가입 할 때 보여질 html