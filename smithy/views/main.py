import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from smithy.views.ko_slogan import process, ko_api, differ, extraction
from smithy.views.en_slogan import enslogan
from smithy.views.ko_model import koslogan


def main_slogan(request):
    if request.method == "POST":
        return render(request, "smithy/index.html")
    else:
        return render(request, "smithy/index.html")

def loading_view(request):
    request.session["select"] = request.POST.get("select", None)
    request.session["info"] = request.POST.get("info", None)
    request.session["sim"] = request.POST.get("sim", None)

    # if request.method == 'POST':
    #     form = DataForm(request.POST)
    #     if form.is_valid():
    #         temp = form.save()
    #         return render(request, "smithy/loading.html")
    # else:
    #     form = DataForm()
    # context = {'form' : form}

    return render(request, "smithy/loading.html")


def result(request):
    select = request.session["select"]
    info = request.session["info"]
    sim = request.session["sim"]
    sim = int(sim)
    if select == "ko_slogan":
        text = process(info, sim)
        slogan_list = ko_api(text)
        kor_list = differ(slogan_list)
        total_slogan = extraction(kor_list, sim)
        context = {"slogans": total_slogan, "select": select, "info": info, "sim": sim}
    elif select == "en_slogan":
        slogans = enslogan(info)
        context = {"slogans": slogans, "select": select, "info": info, "sim": sim}
    else:
        slogans = koslogan(info)
        context = {"slogans": slogans, "select": select, "info": info, "sim": sim}

    return render(request, "smithy/result_slogan.html", context=context)

