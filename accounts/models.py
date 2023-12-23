from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from recipes.models import Recipe

class UserManager(BaseUserManager):
    # Creates and saves a user with the given email and password.
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not full_name:
            raise ValueError('Users must have a full name')
        
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    # Creates and saves a staff user with the given email and password.
    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        return user
    
    # Creates and saves a staff user with the given email and password.
    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
        email = models.EmailField(max_length=255, unique=True)
        full_name = models.CharField(max_length=255)
        is_active = models.BooleanField(default=True)
        staff = models.BooleanField(default=False) 
        admin = models.BooleanField(default=False)
        timestamp = models.DateTimeField(auto_now_add=True)
        favorite_recipes = models.ManyToManyField(Recipe, related_name='user_favorite_recipes',  default=[], blank=True)
        user_created_recipes = models.ManyToManyField(Recipe, related_name='created_by',  default=[], blank=True)

        # USERNAME_FIELD and password are required by default
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['full_name']

        objects = UserManager()

        def __str__(self):
            if self.full_name:
                return self.full_name
            return self.email

        def get_full_name(self):
            return self.email

        def get_short_name(self):
            return self.email
        
        def has_perm(self, perm, obj=None):
            "Does the user have a specific permission?"
            # Simplest possible answer: Yes, always
            return True

        def has_module_perms(self, app_label):
            "Does the user have permissions to view the app `app_label`?"
            # Simplest possible answer: Yes, always
            return True

        @property
        def is_staff(self):
            "Is the user a member of staff?"
            return self.staff

        @property
        def is_admin(self):
            "Is the user a admin member?"
            return self.admin

