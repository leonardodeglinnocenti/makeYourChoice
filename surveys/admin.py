from django.contrib import admin
from .models import Survey, Question, Choice, Answer, Response, AnswerResponse

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(AnswerResponse)
