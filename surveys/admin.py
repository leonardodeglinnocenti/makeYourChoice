from django.contrib import admin
from .models import Survey, Question, Choice, Answer, Response, AnswerResponse, Category, UserCategorySubscription

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(AnswerResponse)
admin.site.register(Category)
admin.site.register(UserCategorySubscription)
