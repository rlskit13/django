from django.contrib import admin
from .models import Tutorial, TutorialSeries, TutorialCategory, Poll
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
    ("Title/date", {"fields": ["tutorial_title" , "tutorial_published"]}),
    ("URL", {"fields": ["tutorial_slug"]}),
    ("Series", {"fields": ["tutorial_series"]}),
    ("Content", {"fields": ["tutorial_content"]})
    ]

    formfield_overrides = {
    	models.TextField: {'widget': TinyMCE()}

    }


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
    ("Poll question", {"fields": ["question"]}),
    ("Option 1", {"fields": ["option_one"]}),
    ("Option 2", {"fields": ["option_two"]}),
    ("Option 3", {"fields": ["option_three"]})
    ]


admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Poll, PollAdmin)

