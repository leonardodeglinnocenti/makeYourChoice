from django.contrib import admin

from users.models import UserFollows
from .models import Survey, Question, Choice, Response, Answer, Category, UserCategorySubscription

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(Category)
admin.site.register(UserCategorySubscription)
admin.site.register(UserFollows)
