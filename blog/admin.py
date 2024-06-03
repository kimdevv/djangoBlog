from django.contrib import admin
from .models import Blog # 같은 폴더(.) 내에 있는 models 모듈에서 Blog를 import

class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

# Register your models here.
admin.site.register(Blog, BlogAdmin)