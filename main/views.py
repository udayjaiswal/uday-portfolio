from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Contact
from django.conf import settings

def index(request):
    return render(request, 'main/index.html')

def contact_form(request):
    if request.method == 'POST':
        # Form se data le
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Database mein save kar
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Tujhe email bhej (notification)
        send_mail(
            f'🔔 New Contact: {subject}',
            f'''
Name: {name}
Email: {email}
Subject: {subject}
Message: {message}

Submitted at: {contact.submitted_at}
            ''',
            settings.EMAIL_HOST_USER,  # From (tera email)
            [settings.EMAIL_HOST_USER],  # To (tujhe hi jayega)
            fail_silently=False,
        )
        
        # User ko auto-reply bhej
        send_mail(
            'Thank you for contacting Uday Jaiswal',
            f'''
Hi {name},

Thank you for reaching out! I've received your message and will get back to you soon.

Here's a copy of your message:
Subject: {subject}
Message: {message}

Best regards,
Uday Jaiswal
AI System Builder | Data Science Enthusiast
            ''',
            settings.EMAIL_HOST_USER,  # From (tera email)
            [email],  # To (user ka email)
            fail_silently=False,
        )
        
        # Success message dikha
        messages.success(request, 'Message sent successfully! Check your email for confirmation.')
        return redirect('index')
    
    return redirect('index')