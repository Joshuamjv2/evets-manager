from django.contrib import admin
from .models import Event, MyClubUser, Venue, Subscriber
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
import csv
from django import forms
from ckeditor.widgets import  CKEditorWidget


class MyClubUserInline(admin.StackedInline):
    model = MyClubUser
    can_delete = False
    verbose_name = 'Address and Phone'
    verbose_name_plural = 'Additional Info'

class MyClubUserAdmin(UserAdmin):
    inlines = (MyClubUserInline,)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'member_level')
    list_filter = ('member_level',)

class EventInline(admin.TabularInline):
    model = Event
    fields = ('name', 'event_date')
    extra = 1

class AttendeeInline(admin.TabularInline):
    model = Event.attendees.through
    verbose_name = 'Attendee'
    verbose_name_plural = 'Attendees'
    extra = 2

class EventAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget)
    class Meta:
        model = Event
        fields = '__all__'

# class EventsAdmin(AdminSite):
#     site_header = "MyClub Events Administration"
#     site_title = "MyClub Events Admin"
#     index_title = "MyClub Events Admin Home"

# admin_site = EventsAdmin(name='eventsadmin')

# Register your models here.


def venue_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venue_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['name', 'event_date', 'venue', 'description'])
    for record in queryset:
        rec_list = []
        rec_list.append(record.name)
        rec_list.append(record.event_date.strftime('%m/%d/%y=Y, %H:%M'))
        rec_list.append(record.venue.name)
        rec_list.append(record.description)
        writer.writerow(rec_list)
    return response
venue_csv.short_description = 'Export Selected Venues to CSV'




# @admin.register(Venue, site=admin_site)
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    list_display_links = ('name', 'address')
    list_editable = ('phone',)
    save_as = True
    ordering = ('name',)
    search_fields = ('name', 'address')
    inlines = [
        EventInline,
    ]

# @admin.register(Event, site=admin_site)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    form = EventAdminForm
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)
    fieldsets = (('Required Information', {
        'description': 'These fields are required for each event.',
        'fields':(('name', 'venue'), 'event_date')
    }),
                ('Optional Information', {
                    'classes':('collapse',),
                    'fields':('description', 'manager')
                })
    )
    inlines = [
        AttendeeInline,
    ]
    actions = [venue_csv]

admin.site.unregister(User)
admin.site.register(User, MyClubUserAdmin)
# admin.site.register(Event)
# admin.site.register(Venue)
# admin_site.register(User)
# admin_site.register(Group)
# admin.site.register(MyClubUser)