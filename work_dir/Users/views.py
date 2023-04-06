from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from Users.forms import *
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView


# Create your views here.


def home(request):
    return render(request, 'base/home.html')


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('models')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('models')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = '/home'


def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    context = {'user': request.user}
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def my_calendar(request):
    return render(request, 'calendar.html')







