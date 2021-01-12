from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .forms import RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.utils.crypto import get_random_string
import string
from shop import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import django
import gzip
from pathlib import Path
from shop import custom_messages as Custom_Msg
from products.views import get_categories
import json, re

#authentication and authorization views  ( login , register and activation views)
UserModel = get_user_model()
def accountView(request):
    form=RegisterForm()
    context={
        'form':form,
    }
    return render(request,'accounts.html',context=context)


def name_validate(request):
    if request.method == 'POST':
        name=request.POST['contact_name']
        data={}
        reg = re.compile(r'^[A-Za-z]+$')
        if not reg.match(name):
            data={
                'status': 200,
                'is_valid': False,
                'error_msg': "Name must be in aphabets only."

            }
        else:
            data={
                'status': 200,
                'is_valid': True
            }
        return JsonResponse(data)
    else:
        return redirect('contact')

#customely validate email on onchange event of input using ajax and validate_email
def validateEmail(request):
    if request.method == 'POST':
        email=request.POST['email_id']
        data={}
        try:
            validate_email(email)
            data={
                'status': 200,
                'is_valid': True
            }
        except ValidationError:
            data={
                'status': 200,
                'is_valid': False,
                'error_msg': Custom_Msg.INVALID_EMAIL_FRMT_ERR_MSG
            }
        return JsonResponse(data)
    else:
        return redirect('home')


#customely validate main entred password on onchange event of input using ajax
def validatePass(request):
    if request.method == 'POST':
        password=request.POST['password']
        data={}
        if len(password) > 8:
            data={
                'status': 200,
                'is_valid': True
            }
        else:
            data={
                'status': 200,
                'is_valid': False,
                'error_msg': Custom_Msg.TO_SHORT_PASS_ERR_MSG
            }
        return JsonResponse(data)
    else:
        return redirect('home')

#check password is entirely numeric or not
def numericPass(request):
    if request.method == 'POST':
        password=request.POST['password']
        data={}
        if not password.isdigit():
            data={
                'status': 200,
                'is_valid': True
            }
        else:
            data={
                'status': 200,
                'is_valid': False,
                'error_msg': Custom_Msg.ONLY_NUMERIC_PASS_ERR_MSG
            }
        return JsonResponse(data)
    else:
        return redirect('home')

#get comman password list
def commanPasswordListGet():
    DEFAULT_PASSWORD_LIST_PATH = Path(django.__file__).resolve().parent / 'contrib/auth/common-passwords.txt.gz' 
    password_list_path=DEFAULT_PASSWORD_LIST_PATH
    try:
        common_passwords_lines = gzip.open(password_list_path).read().decode('utf-8').splitlines()
    except IOError:
        with open(password_list_path) as f:
            common_passwords_lines = f.readlines()
    
    passwords_list={p.strip() for p in common_passwords_lines}
    return passwords_list

#compare comman password list with entered password
def commanPassCheck(request):
    if request.method == 'POST':
        comman_password_list=commanPasswordListGet()
        password=request.POST['password']
        data={}
        if password.lower().strip() in comman_password_list:
            data={
                'status': 200,
                'is_valid': False,
                'error_msg': Custom_Msg.TOO_COMMAN_PASS_ERR_MSG
            }
        else:
            data={
                'status': 200,
                'is_valid': True
            }
        return JsonResponse(data)
    else:
        return redirect('home')

#check main password and re pass word are same or not
def comparePass(request):
    if request.method == 'POST':
        password=request.POST['password1']
        re_pass=request.POST['password2']
        data={}
        if password == re_pass:
            data={
                'status': 200,
                'is_valid': True
            }
        else:
            data={
                'status': 200,
                'is_valid': False,
                'error_msg': Custom_Msg.BOTH_PASS_NO_MATCH_ERR_MSG
            }
        return JsonResponse(data)
    else:
        return redirect('home')


#account activation view
def activate(request, uidb64, token):
    form = RegisterForm()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,Custom_Msg.ACC_EMAIL_VERIFIED)
        return render(request,'accounts.html',{'form': form})
    else:
        return redirect('invalid-url')



def custom_mail(request,email_send_type,mail_subject,message,to_email,content_subtype=''):
    if email_send_type == "Account Activation" or email_send_type == "forget password":
        email = EmailMessage(
            mail_subject, message,to=[to_email],
        )
        email.content_subtype=content_subtype
        email.send()
    elif email_send_type == "Login Code" or email_send_type == "Contact Email":
        emailMsg = EmailMessage(
            mail_subject, message,to=[to_email],
        )
        emailMsg.send()


#register view
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            #raw_password = form.cleaned_data.get('password1')
            current_site = get_current_site(request)
            mail_subject = 'Activate your zoddok account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            custom_mail(request,"Account Activation",mail_subject,message,to_email,'html')
            messages.success(request,Custom_Msg.ACC_CONFIRMATION_EMAIL_SENT)
            return render(request,'accounts.html',{'form': form})
    else:
        form = RegisterForm()
    return render(request, 'accounts.html', {'form': form})

#login view
def loginUser(request):
    form = RegisterForm()
    if request.method == 'POST' and 'otplogin' in request.POST or 'resendcode' in request.POST:
        if request.POST.get('email'):
            email=request.POST.get('email')
            try:
                validate_email(email)
                UserModel.objects.get(email=email)
                mail_subject = 'Zoddok Account Login Code'
                login_otp_generated = get_random_string(8, allowed_chars=string.ascii_uppercase + string.ascii_lowercase + string.digits)
                message = "Use the login code "+login_otp_generated+' to login into your zoddok account. Login code can be valid till 15 mins.'
                to_email = email
                custom_mail(request,"Login Code",mail_subject,message,to_email,'')
                request.session['otp']=login_otp_generated
                request.session['otpEmail']=to_email
                request.session.modified = True
                request.session.set_expiry(900)
                if 'resendcode' in request.POST:
                    resendcode_sent=Custom_Msg.NEW_OTP_SUCC_SEND
                    return render(request,'accounts.html',{'form':form,'otp_send_mail':to_email,'resend_code_sent':resendcode_sent})
                else:
                    return render(request,'accounts.html',{'form':form,'otp_send_mail':to_email})
            except ValidationError:
                email_error=Custom_Msg.INVALID_EMAIL_FRMT_ERR_MSG
                return render(request,'accounts.html',{'email_error':email_error,'form':form})
            except UserModel.DoesNotExist:
                user_not_exsist=Custom_Msg.USER_NOT_REGISTERED_ERR_MSG
                return render(request,'accounts.html',{'user_not_exsist':user_not_exsist,'form':form})
        else:
            email_error=Custom_Msg.FIELD_REQUIRE_ERR_MSG
            return render(request,'accounts.html',{'email_error':email_error,'form':form})
    if request.method == 'POST' and 'login' in request.POST:     
        if request.POST.get('email') and ( request.POST.get('otp') or request.POST.get('password') ):
            try:
                email=request.POST.get('email')
                validate_email(email)
                password=request.POST.get('password')
                otp=request.POST.get('otp')
                UserModel.objects.get(email=email)
                if otp is not None: 
                    if request.session.get('otpEmail') == email:
                        if request.session.get('otp') == otp:
                            user=UserModel.objects.get(email=email)
                            if not request.POST.get('remember_me'):
                                request.session.set_expiry(0)  # if remember me is 
                                request.session.modified = True
                            login(request,user,backend=settings.AUTHENTICATION_BACKENDS[0])
                            return redirect('home')
                        else:
                            password_or_otp_error=Custom_Msg.INVALID_OTP_ERR_MSG
                            return render(request,'accounts.html',{'form':form,'password_or_otp_error':password_or_otp_error,'otp_send_mail':email})
                    else:
                        password_or_otp_error=Custom_Msg.NO_OTP_SENT_ERR_MSG
                        return render(request,'accounts.html',{'form':form,'password_or_otp_error':password_or_otp_error})
                if request.POST.get('password') is not None:
                    user=authenticate(email=email,password=password)
                    if user is not None:
                        login(request,user)
                        if not request.POST.get('remember_me'):
                                request.session.set_expiry(0)  # if remember me is 
                                request.session.modified = True
                        if 'next' in request.GET:
                            return redirect(request.GET['next'])
                        else:
                            return redirect('home')
                    else:
                        password_or_otp_error=Custom_Msg.INVALID_CREDS_ERR_MSG
                        return render(request,'accounts.html',{'password_or_otp_error':password_or_otp_error,'form':form})
            except ValidationError:
                email_error=Custom_Msg.INVALID_EMAIL_FRMT_ERR_MSG
                return render(request,'accounts.html',{'email_error':email_error,'form':form})
            except UserModel.DoesNotExist:
                user_not_exsist=Custom_Msg.USER_NOT_REGISTERED_ERR_MSG
                return render(request,'accounts.html',{'user_not_exsist':user_not_exsist,'form':form})
        else:
            email=request.POST.get('email')
            email_error=''
            password_or_otp_error=''
            otp_send_mail=''
            
            if email == '':
                email_error=Custom_Msg.FIELD_REQUIRE_ERR_MSG
            else:
                try:
                    validate_email(email)
                    if request.session.get('otpEmail') is not None and email == '':
                        otp_send_mail=None
                    elif request.session.get('otpEmail') is None and email is not None:
                        otp_send_mail=None
                    else:
                        otp_send_mail=request.session.get('otpEmail')
                except ValidationError:
                    email_error=Custom_Msg.INVALID_EMAIL_FRMT_ERR_MSG
        
            if request.POST.get('otp') is None or request.POST.get('password') is None:
                password_or_otp_error=Custom_Msg.FIELD_REQUIRE_ERR_MSG
           
            return render(request,'accounts.html',{'form':form,'password_or_otp_error':password_or_otp_error,'email_error':email_error,'otp_send_mail':otp_send_mail})
    else:
        return render(request,'accounts.html',{'form':form})

#logout view
def logoutUser(request):
    logout(request)
    return redirect('home')


def forget_pass_view(request):
    category=get_categories()
    forget_pass_form = PasswordResetForm(request.POST)
    if request.method == "POST":
        if forget_pass_form.is_valid():
            email=forget_pass_form.cleaned_data['email']
            try:
                validate_email(email)
                check_user=UserModel.objects.get(email=email)
                if check_user is not None:
                    current_site = get_current_site(request)
                    mail_subject = 'Forget password your zoddok account'
                    message = render_to_string('forget_password_email.html', {
                        'user': check_user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(check_user.pk)),
                        'token': default_token_generator.make_token(check_user),
                    })
                    to_email = email
                    custom_mail(request,"forget password",mail_subject,message,to_email,'html')
                    messages.success(request,Custom_Msg.PASS_RESET_EMAIL_SENT)
                    return redirect('accounts')
            except ValidationError:
                email_error=Custom_Msg.INVALID_EMAIL_FRMT_ERR_MSG
                return render(request,'forget_password.html',{'email_error':email_error,'form':forget_pass_form})
            except UserModel.DoesNotExist:
                user_not_exsist=Custom_Msg.USER_NOT_REGISTERED_ERR_MSG
                return render(request,'forget_password.html',{'user_not_exsist':user_not_exsist,'form':forget_pass_form})

    return render(request,'forget_password.html',{'form':forget_pass_form})


def forget_pass_comfirm_view(request, uidb64, token):
    category=get_categories()
    if request.method == "GET":
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            UserModel.objects.get(pk=uid)
            user = UserModel._default_manager.get(pk=uid)
            pass_confirm=SetPasswordForm(user=user)
        except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
            return redirect('invalid-url')
    if request.method == "POST":
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            UserModel.objects.get(pk=uid)
            user = UserModel._default_manager.get(pk=uid)
            pass_confirm=SetPasswordForm(user=user,data=request.POST)
            if pass_confirm.is_valid():
                pass_confirm.save()
                messages.success(request,Custom_Msg.PASS_RESET_SUCC)
                return redirect('accounts')
        except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
            return redirect('invalid-url')
    return render(request,'forget_password_confirm.html',{'form':pass_confirm})


@login_required
def change_password(request):
    category=get_categories()
    form=PasswordChangeForm(request.user)
    if request.method == "POST":
        form=PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            form.save()
            login(request,request.user)
            return redirect('home')
    return render(request,'change_password.html',{'form':form})