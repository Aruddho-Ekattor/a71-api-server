from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin
)
from django.contrib.postgres.fields import ArrayField
from django.utils.html import format_html

class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, phone_number, full_name, password, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            full_name=full_name,
            is_active=True,
            **other_fields
        )

        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        superUser = self.model(phone_number=phone_number, **other_fields)
        superUser.set_password(password)
        superUser.save()
        return superUser


class User(AbstractBaseUser, PermissionsMixin):
    
    USER_TYPE = (
        ('Member', 'Member'),
        ('Executive', 'Executive'),
        ('Admin', 'Admin'),
    )

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, blank=True)
    skills = ArrayField(models.CharField(max_length=10), blank=True, null=True) 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)

    objects = UserManager()     

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        if self.is_staff == True:
            return f"{self.phone_number}"
        return f"{self.full_name.split()[0]} - {self.user_type}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True)
    about = models.TextField()
    
    def __str__(self):
        return f"{self.user.full_name}'s Profile"

    def profile_picture_preview_html(self):
        return format_html('<img src="{}" width="200"/>'.format(self.profile_picture.url)) # Replace 'image' with the name of your image field

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experience')
    title = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.title} - {self.company}"
    

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=30)
    major = models.CharField(max_length=30)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.institution} - {self.major}"


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=130)
    organization = models.CharField(max_length=30)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.title} - {self.organization}"
    

class SocialLinks(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_links')
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.full_name} - {self.linkedin}"