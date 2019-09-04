from django import forms
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.conf import settings

from .models import Profile, MaritalStatus, Gender
# from entryApp.forms import UserCreationForm

class UserAdmin(BaseUserAdmin):
    # add_form = UserCreationForm
    list_display = (
    	'username',
    	'first_name',
    	'last_name', 
    	'date_of_birth', 
    	'gender',
    	'marital_status',
    	'number_of_children'
	)
    list_filter = (
    	'username',
    	'first_name',
    	'last_name',
	)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            	'username', 
            	'first_name',
            	'last_name',
            	'gender',
            	'number_of_children',
            	'marital_status',
            	'date_of_birth', 
            	'password1', 
            	'password2'
        	)}
        ),
    )
    search_fields = (
    	'username',
    	'first_name',
    	'last_name',
	)
    ordering = ('username',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Profile, UserAdmin)
admin.site.register(MaritalStatus)
admin.site.register(Gender)
admin.site.unregister(Group)

