from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Tasks
# Register your models here.

@admin.register(Tasks)
class AdminTasksView(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'status')
    list_editable = ('status',)
    list_filter = ('start_time', 'end_time')


