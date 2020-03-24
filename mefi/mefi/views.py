from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse

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
                full_name_user = usersn + ' ' + username + ' ' + userfn
                User = get_user_model()
                User.objects.create_user(full_name_user, email, password)
                return redirect(reverse("login"))

        return render(request, self.template_name)