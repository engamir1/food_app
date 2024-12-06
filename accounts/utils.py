from functools import wraps

from django.shortcuts import redirect


# helper function
def anonymous_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                "accounts:dashboard"
            )  # Replace 'home' with your desired redirect URL name
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def dectect_role(user):
    if user.role == 1:
        redirectUrl = "vendor_dashboard"
        return redirectUrl
    if user.role == 2:
        redirectUrl = "customer_dashboard"
        return redirectUrl
    elif user.role == None and user.is_superuser:
        redirectUrl = "/admin"
        return redirectUrl
