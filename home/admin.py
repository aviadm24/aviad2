from django.contrib import admin
from .models import User_tokens, Feedback, Time

admin.site.register(User_tokens)
admin.site.register(Feedback)
admin.site.register(Time)
