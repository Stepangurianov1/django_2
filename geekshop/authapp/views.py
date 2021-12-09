from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm
from authapp.models import User
from baskets.models import Basket
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#         # else:
#         #     print(form.errors)
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Geekshop | Авторизация',
#         'form': form
#     }
#     return render(request, 'authapp/login.html', context)

class LoginListView(LoginView,BaseClassContextMixin):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class RegisterListView(FormView,BaseClassContextMixin):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    title = 'GeekShop - Регистрация'
    success_url = reverse_lazy('auth:login')


    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

#
#
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Вы успешно зарегистрировались')
#             return HttpResponseRedirect(reverse('authapp:login'))
#         else:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': 'Geekshop | Регистрация',
#         'form': form}
#     return render(request, 'authapp/register.html', context)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#        form = UserProfilerForm(instance=request.user,data=request.POST,files=request.FILES)
#        if form.is_valid():
#            messages.set_level(request, messages.SUCCESS)
#            messages.success(request, 'Вы успешно сохранили профайл')
#            form.save()
#        else:
#            messages.set_level(request, messages.ERROR)
#            messages.error(request,form.errors)
#     context = {
#         'title': 'Geekshop | Профайл',
#         'form' : UserProfilerForm(instance=request.user),
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'authapp/profile.html', context)
#

class ProfileFormView(FormView,BaseClassContextMixin,UserDispatchMixin):
    template_name = 'authapp/profile.html'
    form_class = UserProfilerForm
    success_url = reverse_lazy('auth:profile')
    title = 'GeekShop - Профиль'

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context



class Logout(LogoutView):
    template_name = "mainapp/index.html"

# def logout(request):
#     auth.logout(request)
#     return render(request, 'mainapp/index.html')