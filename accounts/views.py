from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import CustomUserForm
from django.contrib import messages

from accounts.models import CustomUser, UserProfile
from vendor.forms import VendorForm

# Create your views here.


def register_user(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        print(form.is_valid())

        if form.is_valid():

            form.save()
            # form = CustomUserForm()
            messages.success(request, "تم التسجيل بنجاح ")
            return redirect("register_new_user")
        # print(request.POST
        else:
            print(form.errors)
    else:
        print(request.method)

        form = CustomUserForm()
    context = {"form": form}
    return render(request, "accounts/register_user.html", context)


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
            email = request.POST.get("email")
            password = request.POST.get("password")
            new_user = CustomUser.objects.create(
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
            return redirect("register_new_user")
        else:
            print(form.errors)
            print(Vendor_form.errors)
    else:
        form = CustomUserForm()
        Vendor_form = VendorForm()

    context = {"form": form, "vendor_form": Vendor_form}
    return render(request, "accounts/register_vendor.html", context)
