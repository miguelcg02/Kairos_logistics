from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','rol')
    search_fields=('user',)

class CVSAdmin(admin.ModelAdmin):
    list_display=('name',)

class TurnAdmin(admin.ModelAdmin):
    list_display=('cvs','typeTire','quantity','rotation','duration','date','hour','bill','done')
    list_filter=('cvs','typeTire','date','hour','done')

class BlockAdmin(admin.ModelAdmin):
    list_display=('cvs','duration','startDate','startHour','endDate','endHour', 'comment', 'scheduledBy')
    list_filter=('cvs','startDate')

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CVS, CVSAdmin)
admin.site.register(Turn, TurnAdmin)
admin.site.register(Block, BlockAdmin)
