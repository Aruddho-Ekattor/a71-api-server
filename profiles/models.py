from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=30, blank=True)
    skills = ArrayField(models.CharField(max_length=10), blank=True, null=True) 
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True)
    about = models.TextField()
    
    def __str__(self):
        return f"{self.user.full_name}'s Profile"

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Profile.objects.get(pk=self.pk)
            if old_instance.profile_picture and self.profile_picture != old_instance.profile_picture:
                old_instance.profile_picture.delete(save=False)
            if old_instance.cover_photo and self.cover_photo != old_instance.cover_photo:
                old_instance.cover_photo.delete(save=False)
        super(Profile, self).save(*args, **kwargs)

    def profile_picture_preview_html(self):
        return format_html('<img src="{}" height="100"/>'.format(self.profile_picture.url)) 
    
    def cover_photo_preview_html(self):
        return format_html('<img src="{}" height="100"/>'.format(self.cover_photo.url))

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