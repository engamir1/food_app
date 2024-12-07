from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import CustomUserForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser, UserProfile
from accounts.utils import anonymous_required, send_activation_email
from vendor.forms import VendorForm
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.


@anonymous_required
def register_user(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        # print(form.is_valid())

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            new_user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            new_user.role = CustomUser.CUSTOMER

            new_user.save()
            # send verifications
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_verification_email.html"
            send_activation_email(request, new_user, mail_subject, email_template)
            messages.success(request, "Your account has been registered sucessfully!")
            messages.success(request, "تم التسجيل بنجاح ")
            return redirect("accounts:register_new_user")
        # print(request.POST
        else:
            pass
            # print(form.errors)
    else:
        pass
        # print(request.method)

        form = CustomUserForm()
    context = {"form": form}
    return render(request, "accounts/register_user.html", context)


@anonymous_required
def register_vendor(request):
    # return HttpResponse ("new")

    if request.method == "POST":

        form = CustomUserForm(request.POST)
        Vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and Vendor_form.is_valid():
            form.save(commit=False)
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = request.POST.get("username")
            # another way to get request data
            # username = request.POST["username"]

            email = request.POST.get("email")
            password = request.POST.get("password")
            new_user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            new_user.role = CustomUser.VENDOR
            new_user.save()

            new_vendor = Vendor_form.save(commit=False)
            new_vendor.user = new_user
            new_vendor.user_profile = UserProfile.objects.get(user=new_user)
            new_vendor.save()
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_verification_email.html"
            send_activation_email(request, new_vendor, mail_subject, email_template)
            messages.success(request, "Your account has been registered sucessfully!")

            return redirect("accounts:login")
        else:
            pass
            # print(form.errors)
            # print(Vendor_form.errors)
    else:
        form = CustomUserForm()
        Vendor_form = VendorForm()

    context = {"form": form, "vendor_form": Vendor_form}
    return render(request, "accounts/register_vendor.html", context)

# you should be anonymous to get login page
@anonymous_required
def login(request):

    # if request.user.is_authenticated:
    #     return redirect("accounts:dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        # get user from db and get status of is_active form CustomUser model
        temp_user = CustomUser.objects.get(email=email)
        # check temp_user.is_active
        print("the user is  ", temp_user.is_active)
        if not temp_user.is_active:
            print(temp_user)
            return render(request, "accounts/waiting_activate.html")
        elif user is not None and temp_user.is_active:
            auth.login(request, user)
            return redirect("accounts:dashboard")
    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    return redirect("accounts:login")

# if your not logged in go to login page first
# if you create superuser without specify the role it will be wrong
@login_required(login_url="accounts:login")
def dashboard(request):
    redirectUrl = ""
    user_type = request.user.role
    # print(user_type, type(user_type))
    if user_type == 1:
        redirectUrl = "vendor_dashboard"
    if user_type == 2:
        redirectUrl = "customer_dashboard"
    elif user_type is None:
        # you should specify the role of User fisrt
        return HttpResponse("You didnt specify Role for User")
    return redirect(f"accounts:{redirectUrl}")


@login_required(login_url="accounts:login")
def customer_dashboard(request):
    # return render(request, "accounts/customer_dashboard.html")
    user_role = request.user.role
    if user_role == 2:
        return render(request, "accounts/customer_dashboard.html")
    else:
        return render(request, "accounts/not_found.html")


@login_required(login_url="accounts:login")
def vendor_dashboard(request):
    user_role = request.user.role
    if user_role == 1:
        return render(request, "accounts/vendor_dashboard.html")
    else:
        return render(request, "accounts/not_found.html")


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your account is activated.")
        return redirect("accounts:dashboard")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("accounts:dashboard")


# forget password
def forget_password(request):
    return render(request, "accounts/forget_password.html")


# password reset
def reset_password(request):
    pass


def reset_password_token(request):
    pass
