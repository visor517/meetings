from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BasedLoginView, PasswordResetView as BasedPasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView, PasswordChangeView as BasePasswordChangeView)
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import CreateView, FormView

from apps.users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from apps.users.models import User


class LoginView(BasedLoginView):
    """ Авторизация """
    form_class = UserLoginForm
    template_name = "users/login.html"


class RegistrationView(CreateView):
    """ Регистрация """
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")
    template_name = "users/registration.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts"))
        return super(RegistrationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"form": form}
        if form.is_valid():
            data = form.cleaned_data
            username = data.pop("username")
            user = User.objects.create(username=username)
            user.set_password(data.pop("password"))
            user.save()
            login(self.request, user)
            return HttpResponseRedirect(reverse("accounts"))

        context["messages"] = [item[0] for item in form.errors.values()]
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, FormView):
    """ Личный кабинет для партнера """
    redirect_field_name = 'next'

    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form_class = UserProfileForm(instance=user)
        context = {
            'form': form_class,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user

        form = UserProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            if form.has_changed():
                user = User.objects.get(username=user)
                user.save()
            message = {"status": True, "message": "Данные успешно изменены!"}
        else:
            message = {"status": False, "message": "Что-то пошло не так с валидацией!"}

        context = {
            "form": form,
            "message": message
        }
        return render(request, self.template_name, context)
