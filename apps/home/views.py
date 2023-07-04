# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import smtplib
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from email.message import EmailMessage
from .sendemail import send_email

def index(request):
    context = {'segment': 'index'}
    context['gallery_images'] = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # Add the gallery images here

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@csrf_exempt
def send_email_view(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")

        if full_name and email and message:
            sender_email = email  # Use the client's email as the sender
            receiver_email = "mmellodesignsite@gmail.com"  # Replace with the recipient email address
            subject = f"New Contact Form Submission from {full_name}"
            body = f"Full Name: {full_name}\nEmail: {email}\nMessage: {message}"

            if send_email(sender_email, receiver_email, subject, body):
                return HttpResponse("Message sent successfully!")
            else:
                return HttpResponse("Failed to send the message.", status=500)
        else:
            return HttpResponse("Invalid form data.", status=400)
    else:
        return HttpResponse("Invalid request.", status=400)