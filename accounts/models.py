from django.db import models

# Create your models here.
from django.db import models

# import
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# this RegexValidator import for validate input before save to db
from django.core.validators import RegexValidator

# Create your models here.


# create user manager class to create users


class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, password, last_name, email):
        if not email:
            raise ValueError("must Enter Proper Email")
        if not username:
            raise ValueError("must Enter Proper username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        # added i forgot to set_password before save to db
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, password, last_name, email):
        # when create new user any type user or superuser you should give us
        #  email = self.normalize_email(email),
        # username = username,
        # first_name = first_name ,
        # last_name = last_name ,
        # password = password,
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    # choices
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (VENDOR, "Vendor"),
        (CUSTOMER, "Customer"),
    )
    # connect between cutome manager and custome user model
    objects = CustomUserManager()
    # table fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    mobile_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{11}$", message="Phone number must be 11 digits."
            )
        ],
    )
    national_id = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{14}$", message="Nations ID must be 14 digits."
            )
        ],
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    # required fields
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    date_joind = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiy_date = models.DateTimeField(auto_now_add=True)

    # permmisions

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    # the name of function was wrong has_module_perms
    def has_module_perms(self, app_label):
        return True


# create user profile data model


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="users/profiles_pics",
        blank=True,
        null=True,
    )
    cover_pic = models.ImageField(
        upload_to="users/covers_pics",
        blank=True,
        null=True,
    )
    addres_line1 = models.CharField(max_length=50, blank=True, null=True)
    addres_line2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    post_code = models.IntegerField(blank=True, null=True)
    longi = models.CharField(max_length=50, blank=True, null=True)
    lati = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


