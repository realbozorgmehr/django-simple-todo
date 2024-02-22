from django.contrib import admin
from .models import Todo


# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('slug', 'updated', 'user')
    list_filter = ('updated',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user',)


admin.site.register(Todo, TodoAdmin)
