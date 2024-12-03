from django.db import models
# import 
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager 
from django.core.validators import RegexValidator
# Create your models here.


# create user manager class to create users 

class CustomUserManager(BaseUserManager):
    def create_user(self ,username, first_name,password, last_name, email ):
        if not email:
            raise ValueError("must Enter Proper Email") 
        if not username:
            raise ValueError("must Enter Proper username")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name , 
            last_name = last_name , 
            password = password,
        ) 
        user.save(using = self._db)

        return user
    
    def create_superuser(self ,username, first_name,password, last_name, email):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name , 
            last_name = last_name , 
            password = password,
        )
        user.is_admin= True
        user.is_active = True 
        user.is_superadmin= True 
        user.is_staff= True
        user.save(using= self._db)
        return user


         
class CustomUser(AbstractBaseUser):

    # choices 
    RESTURANT = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
    (RESTURANT , 'Resturant'),
    (CUSTOMER , 'Customer'),
        )
    # connect between cutome manager and custome user model 
    objects = CustomUserManager()
    # table fields 
    first_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=150, unique=True)
    mobile_number = models.CharField(max_length=12, validators=[
        RegexValidator(regex=r'^[0-9]{12}$', message="Phone number must be 12 digits.")
    ])
    national_id = models.CharField(max_length=12, validators=[
        RegexValidator(regex=r'^[0-9]{15}$', message="Nations ID must be 15 digits.")
    ])
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

 
    # required fields 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    date_joind = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiy_date = models.DateTimeField(auto_now_add=True)

    # permmisions

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email 
    def has_perm(self, perm , obj=None):
        return self.is_admin
    def has_module(self, app_label):
        return True 
    
