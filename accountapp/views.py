from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def main_slogan(request):
    return HttpResponse('Welcom Slgan smithy!')