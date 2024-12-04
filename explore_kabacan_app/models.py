from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True, help_text='Whether the user can login to the system')
    is_staff = models.BooleanField(default=False, help_text='Whether the user can access the super admin')
    is_superuser = models.BooleanField(default=False, help_text='Whether the user has the admin permission to system')
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def has_perm(self, perm, obj=None):
        return True if self.is_superuser else super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return True if self.is_superuser else super().has_module_perms(app_label)

    class Meta:
        db_table = "users_tbl"
        verbose_name = "User"
        verbose_name_plural = "Users"

class SpotCategory(models.Model):
    category = models.CharField(max_length=255, blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.category
    
    class Meta:
        db_table = "spot_category_tbl"
        verbose_name = "Spot Category"
        verbose_name_plural = "Spot Categories"

class Spot(models.Model):
    spot = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(SpotCategory, blank=True, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.spot

    class Meta:
        db_table = "spot_tbl"
        verbose_name = "Tourist Spot"
        verbose_name_plural = "Tourist Spots"


class Tourist(models.Model):

    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    firstname = models.CharField(max_length=255, null=False, blank=False)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, null=False, blank=False)
    dob = models.DateField(auto_now_add=False)
    gender = models.CharField(max_length=255, null=False, blank=False, choices=GENDER)
    email = models.EmailField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    destination = models.ForeignKey(Spot, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateTimeField(auto_now_add=True, editable=True, null=False, blank=False)

    def get_full_name(self):
        return (
            f"{self.firstname} {self.lastname}" if self.middlename else self.firstname
        )

    def __str__(self) -> str:
        return self.get_full_name()

    class Meta:
        db_table = "tourist_tbl"
        verbose_name = "Tourists"
        verbose_name_plural = "Tourists"
