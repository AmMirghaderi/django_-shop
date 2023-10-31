from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
import random
from .models import OtpCode, User
from utils import Send_Otp_Code
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = random.randint(1000, 9999)
            Send_Otp_Code(cd['phone_number'], code)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=code)
            request.session['user_registration_info'] = {
                'email': cd['email'],
                'phone_number': cd['phone_number'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }
            messages.success(request, 'we send code for you', 'success')
            return redirect('accounts:verify_code')
        return render(request,'accounts/register.html',{'form':form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if code_instance.code == cd['code']:
                User.objects.create_user(user_session['email'], user_session['phone_number'], user_session['full_name'],user_session['password'])

                code_instance.delete()
                messages.success(request, 'you register success', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


