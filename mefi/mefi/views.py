from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Userlist

class HomeView(TemplateView):
    template_name = "home.html"

class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/accounts/profile")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)

class ProfilePage(TemplateView):
    template_name = "registration/profile.html"

class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            usersn = request.POST.get('usersn')
            username = request.POST.get('username')
            userfn = request.POST.get('userfn')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User = Userlist(ul_surname=usersn, ul_name=username, ul_secondname=userfn, ul_email=email, ul_password=password)
                User.save()
                return redirect(reverse("login"))

        return render(request, self.template_name)