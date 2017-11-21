from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')

def crm_demo(request):
    return render(request, 'home/crm_demo.html')

def pdf_booklet_demo(request):
    return render(request, 'home/pdf_booklet_demo.html')
