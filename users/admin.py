# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin    
# Register your models here.
from . import models

User = get_user_model()

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email',)
    list_filter = ('email', 'user_type', 'is_active',)
    ordering = ('-full_name',)
    list_display = ('__str__', 'email', 'user_type', 'is_active', 'phone_number')
    fieldsets = (
        (None, {'fields': (
            'email', 
            'phone_number', 
            'user_type', 
            'password', 
            'skills',
            'full_name',
            )}),
        ('Permissions',
         {
             'fields': (
                 'is_active',
                 'is_staff',
                 'is_superuser',
                 'verified',
                 'groups',
                 'user_permissions'
             )
         }),
    )

    # fieldsets to add a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'phone_number', 
                'full_name', 
                'user_type',
                'skills',
                'password1', 
                'password2', 
                'is_active',
                'is_staff',
                'groups', 
                'user_permissions'
                )}
         ),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'address', 'profile_picture_preview',)
    
    def profile_picture_preview(self, obj):
        return obj.profile_picture_preview_html()
    
    profile_picture_preview.allow_tags = True
    profile_picture_preview.short_description = 'Profile Picture'

    
    

admin.site.register(User, UserAdminConfig)
admin.site.register(models.Achievement)
admin.site.register(models.SocialLinks)
admin.site.register(models.Education)
admin.site.register(models.Experience)
admin.site.register(models.Profile, ProfileAdmin)