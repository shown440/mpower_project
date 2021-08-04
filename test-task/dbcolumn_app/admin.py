from django.contrib import admin 
from .models import HOUSEHOLDModel 


class HouseHoldAdmin(admin.ModelAdmin):
    list_display = ['id', 'hh_head', 'hh_gender', 'hh_age', 'hh_dob']
    class Meta:
        model = HOUSEHOLDModel


# Register your models here.
admin.site.register(HOUSEHOLDModel, HouseHoldAdmin) 
