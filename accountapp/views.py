from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from accountapp.models import main_slogan
from django.utils import timezone
from django.views.generic import CreateView


def main_slogan(request):
   
    
    if request.method == "POST":
        
        temp = request.POST.get('main_slogan_input')
        
        new_main_slogan = main_slogan()
        new_main_slogan.content = temp
        # new_main_slogan.create_date = timezone.now()
        new_main_slogan.save()
        
        # main_slogan_list = main_slogan.objects.all()
        
        return render(request, 'accountapp/main_slogan.html', context={'main_slogan_output' : new_main_slogan})
    else:
        # main_slogan_list = main_slogan.objects.all()
        return render(request, 'accountapp/main_slogan.html', context={'main_slogan_output' :'hihi'})
    

# class AccountCreateView(CreateView):
#     model = User # 장고에서 기본 제공해주는 모델
#     form_class = 