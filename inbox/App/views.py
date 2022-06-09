from django.shortcuts import render
# My imports
# Login required to access private pages
from django.contrib.auth.decorators import login_required
# Destroy the section after logout
from django.views.decorators.cache import cache_control
from .models import Customer  # From models.py
from App.forms import Customerform, EmailForm  # From forms.py
from django.contrib import messages  # Return messages
from django.http import HttpResponseRedirect  # Redirect the pages
from django.core.paginator import Paginator  # Paginatin
from django.db.models import Q  # Import for Global Search
# Used (in this example) to get message & recieve it today
from datetime import datetime
from django.core.mail import EmailMessage  # Send emails
from django.contrib.auth import logout  # Use it to get auto logout

# =============== FRONTEND  SECTION ===============

# Function to render the home page (frontend)


def home(request):
    return render(request, 'home.html')

# Function to send a message


def send_message(request):
    if request.method == "POST":
        form = Customerform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully !")
            return HttpResponseRedirect('/')
    else:
        form = Customerform()
        return render(request, 'home.html', {'form': form})

# =============== BACKEND SECTION ===============

# Function to render the inbox (backend)
@cache_control(no_cache=True, must_revalidate=True,
               no_store=True)  # For Security
@login_required(login_url='login')
def inbox(request):
    # condition for search (Q)
    if 'q' in request.GET:
        q = request.GET['q']
        all_customer_list = Customer.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q) | Q(subject__icontains=q) | Q(status__icontains=q) | Q(message__icontains=q)).order_by('-created_at')
    else:
        all_customer_list = Customer.objects.all().order_by('-created_at')

    # for paginaton
    paginator = Paginator(all_customer_list, 8)
    page = request.GET.get('page')
    all_customer = paginator.get_page(page)

    # -------------- MESSAGES COUNTER --------------

    # 1) Total
    total = Customer.objects.all().count()
    # 2) Read
    read = Customer.objects.filter(status="Read")
    # 3) Unread
    unread = Customer.objects.filter(status="Pending")
    # 4) Today
    base = datetime.now().date()
    today = Customer.objects.filter(created_at__gt=base)

    return render(request, 'inbox.html', {'customers': all_customer,
                                          'total': total,
                                          'read': read,
                                          'pending': unread,
                                          'today': today})

# Function to delete message from backend
@cache_control(no_cache=True, must_revalidate=True,
               no_store=True)  # For Security
@login_required(login_url='login')
def delete_message(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    messages.success(request, "Message successfully deleted !")
    return HttpResponseRedirect('/inbox')

# Function to have the access to the message individually
@cache_control(no_cache=True, must_revalidate=True,
               no_store=True)  # For Security
@login_required(login_url='login')
def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if customer != None:
        return render(request, 'customer.html', {'customer': customer})


# Function to mark the message as read
@cache_control(no_cache=True, must_revalidate=True,
               no_store=True)  # For Security
@login_required(login_url='login')
def mark_message(request):
    if request.method == "POST":
        customer = Customer.objects.get(id=request.POST.get('id'))
        if customer != None:
            customer.status = request.POST.get('status')
            customer.save()
            messages.success(request, "Message marked as READ !")
            return HttpResponseRedirect('/inbox')

# Function to reply the messages


def email(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)

        company = "Reply ExxonOil"

        if form.is_valid():

            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email = form.cleaned_data["email"]
            cc = form.cleaned_data["cc"]
            files = request.FILES.getlist("attach")

            mail = EmailMessage(subject, message, company, [email], [cc])
            for f in files:
                mail.attach(f.name, f.read(), f.content_type)
            mail.send()

            messages.success(request, "Reply sent successdully !")
            return HttpResponseRedirect('/inbox')
    else:
        form = EmailForm()
        return render(request, {'form': form})


# Auto logout function
def AutoLogoutUser(request):
    logout(request)
    request.user = None
    # I put a dot here because the argument can't be empty
    messages.info(request, ".")
    return HttpResponseRedirect('/')

# =============== ERRORS ===============


def E_500(request):
    return render(request, '500.html')


def E_404(request, exception):
    return render(request, '404.html')
