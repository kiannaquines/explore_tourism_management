from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from explore_kabacan_app.models import *

class MyUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class SpotAdmin(admin.ModelAdmin):
    list_display = ("spot","category","date_added")
    search_fields = ("spot",)

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

class SpotCategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "date_added")
    search_fields = ("category",)

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

class TouristAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "phone_number")
    list_filter = ("lastname", "visit_date", "destination")
    search_fields = ("firstname", "lastname")

    def has_view_permission(self, request, obj=None):
        return True
    
    def has_module_permission(self, request):
        return True
    
admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Spot, SpotAdmin)
admin.site.register(Tourist, TouristAdmin)
admin.site.register(SpotCategory, SpotCategoryAdmin)