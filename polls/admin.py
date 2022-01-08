from django.contrib import admin

from .models import Choice, Question, Comment

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Comment)