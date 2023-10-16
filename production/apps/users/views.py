from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BasedLoginView
from django.urls import reverse, reverse_lazy
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

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class ProfileView(LoginRequiredMixin, FormView):
    """ Личный кабинет для партнера """
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
