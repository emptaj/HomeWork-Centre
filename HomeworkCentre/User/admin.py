from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentsClass
from .forms import CustomUserCreationForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # add_form = CustomUserCreationForm
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'groups', 'is_active'),
        }),
    )
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentsClass)
