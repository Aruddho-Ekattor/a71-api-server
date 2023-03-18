from django.contrib import admin
from . import models

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'skills', 'address', 'profile_picture_preview', 'cover_photo_preview',)
    search_fields = ('user__full_name', 'address',)  

    def profile_picture_preview(self, obj):
        return obj.profile_picture_preview_html()
    
    def cover_photo_preview(self, obj):
        return obj.cover_photo_preview_html()
    
    profile_picture_preview.allow_tags = True
    profile_picture_preview.short_description = 'Profile Picture'

admin.site.register(models.Achievement)
admin.site.register(models.SocialLinks)
admin.site.register(models.Education)
admin.site.register(models.Experience)
admin.site.register(models.Profile, ProfileAdmin)

    