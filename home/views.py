from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home/home.html')

@csrf_exempt
def send_mail(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        email = EmailMessage('sent from '+name, message + ' ' + str(phone), to=[email])
        email.send()
    return HttpResponse("")


def pdf_booklet_demo(request):
    return render(request, 'home/pdf_booklet_demo.html')
