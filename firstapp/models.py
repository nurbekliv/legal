from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Foydalanuvchilar uchun email manzili talab qilinadi')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Foydalanuvchilar email orqali ro'yxatdan o'tadi
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)  # Foydalanuvchi aktiv yoki yo'qligini belgilaydi
    is_staff = models.BooleanField(default=False)  # Admin panelga kirish huquqi borligini belgilaydi
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()  # CustomUserManager dan foydalanamiz

    USERNAME_FIELD = 'email'  # Foydalanuvchi login qilish uchun emailni ishlatadi
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Superuser yaratishda bu maydonlar talab qilinadi

    def __str__(self):
        return self.email
