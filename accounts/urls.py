from django.urls import path, include

from accounts import views

urlpatterns = [

    path('registerUser/', views.register_user, name='registerUser')

]
