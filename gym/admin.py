from django.contrib import admin
from .models import  Event , Gym ,News ,Contact ,Trainer ,Workout ,ApplicantDetail ,NutritionPlan ,Feedback,Member,QueryDoubt,ResourceWork ,GymNews , Message,GymFacilities

'''class Feedback_admin(admin.ModelAdmin):
    list_display=['name','email','rating','review']
    list_filter=('rating',)

class Contact_admin(admin.ModelAdmin):
    list_display=['name','email','question','date']

class Event_admin(admin.ModelAdmin):
    list_display=['event_name','event_venue','event_time','event_organizer','event_description']
    list_filter=('event_time','event_venue')

class Coach_admin(admin.ModelAdmin):
    list_display=['name','email','phone','city','address','experience']
    search_fields=('city','experience')
    list_filter=('experience',)'''



# Register your models here.
admin.site.register(Event)
admin.site.register(Gym)
admin.site.register(News)
admin.site.register(Contact)
admin.site.register(Trainer)
admin.site.register(Workout)
admin.site.register(ApplicantDetail)
admin.site.register(NutritionPlan)
admin.site.register(Feedback)
admin.site.register(Member)
admin.site.register(QueryDoubt)
admin.site.register(ResourceWork)
admin.site.register(GymNews)
admin.site.register(Message)
admin.site.register(GymFacilities)

# Admin site customizations
admin.site.site_header = "Fit-Fusion Admin Dashboard"
admin.site.site_title = "Gym Management"
admin.site.index_title = "Manage Gym's, All Facilities & Gym-Members Efficiently"


