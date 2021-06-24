from django.contrib import admin
from .models import questions, challenges, test_cases,user_profile
# Register your models here.
admin.site.register(questions)
admin.site.register(challenges)
admin.site.register(test_cases)
admin.site.register(user_profile)