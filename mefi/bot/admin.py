from django.contrib import admin

# Register your models here.
from .models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist, Placelist


@admin.register(Eventlist)
class EventlistAdmin(admin.ModelAdmin):
    list_display = ('el_id', 'el_title', 'el_date')


@admin.register(Userlist)
class UserlistAdmin(admin.ModelAdmin):
    list_display = ('ul_id', 'ul_login')


@admin.register(Eventtaglist)
class EventtaglistAdmin(admin.ModelAdmin):
    list_display = ('etl_id', 'etl_id_event', 'etl_id_tag')


@admin.register(Taglist)
class TaglistAdmin(admin.ModelAdmin):
    list_display = ('tl_id', 'tl_title')


@admin.register(Usertaglist)
class UsertaglistAdmin(admin.ModelAdmin):
    list_display = ('utl_id', 'utl_id_user', 'utl_id_tag')


@admin.register(Placelist)
class PlacelistAdmin(admin.ModelAdmin):
    list_display = ('pl_id', 'pl_place_name', 'pl_city', 'pl_str_name', 'pl_house_num', 'pl_letter')


# admin.site.register(Eventlist)
# admin.site.register(Eventtaglist)
# admin.site.register(Usertaglist)
# admin.site.register(Userlist)
# admin.site.register(Taglist)
# admin.site.register(Placelist)