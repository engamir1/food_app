from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import CustomUserForm

# Create your views here.


def register_user(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        print(form.is_valid())

        if form.is_valid():

            form.save()
            # form = CustomUserForm()
            return redirect("register_new_user")
        # print(request.POST
        else:
            print(form.errors)
    else:
        print(request.method)

        form = CustomUserForm()
    context = {"form": form}
    return render(request, "accounts/register_user.html", context)
