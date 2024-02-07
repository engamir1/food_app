from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.forms import UserForm
from accounts.models import User


# Create your views here.
def register_user(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            cd = form.cleaned_data
            user.set_password(cd["password"])
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'your account has been created!')
            return redirect('registerUser')

    else:
        form = UserForm()
    return render(request, 'accounts/register_user.html', {'form': form})
