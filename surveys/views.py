from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView
from .models import Survey, Question, Choice, Answer, Response, AnswerResponse, Category
from .forms import AnswerForm

# Create your views here.


class ViewSurveys(ListView):
    model = Survey
    template_name = 'index.html'
    context_object_name = 'surveys'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.all()
        return context

    def get_queryset(self):
        return Survey.objects.all()


class CreateSurvey(CreateView):
    model = Survey
    fields = ['name', 'description', 'category']
    template_name = 'createSurvey.html'
    success_url = reverse_lazy('index')

    # This method is called when the form is submitted and adds current user to the survey
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.request.user.username)
        return context


class DeleteSurvey(DeleteView):
    model = Survey
    template_name = 'deleteSurvey.html'
    success_url = reverse_lazy('index')

    # Checks whether the user is the owner of the survey or is a staff member
    def form_valid(self, form):
        if self.request.user == self.object.user or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            messages.success(self.request, "You are not the owner of this survey")
            return HttpResponseRedirect(reverse_lazy('index'))


class ViewSurvey(ListView):
    model = Question
    template_name = 'viewSurvey.html'
    context_object_name = 'questions'

    # Allows us to pass the survey object to the template
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = Survey.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Question.objects.filter(survey_id=self.kwargs['pk'])


class AddQuestion(CreateView):
    model = Question
    fields = ['text', 'is_open']
    template_name = 'addQuestion.html'

    def get_success_url(self):
        return reverse_lazy('viewSurvey', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = Survey.objects.get(pk=self.kwargs['pk'])
        return context

    # Checks whether the user is the owner of the survey or is a staff member
    def form_valid(self, form):
        form.instance.survey_id = self.kwargs['pk']
        # Check whether the user is the owner of the survey which the question is being added to
        if self.request.user == Survey.objects.get(pk=self.kwargs['pk']).user or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            messages.success(self.request, "You are not the owner of this survey, so you cannot add questions")
            return HttpResponseRedirect(reverse_lazy('index'))


class DeleteQuestion(DeleteView):
    model = Question
    template_name = 'deleteQuestion.html'

    def get_success_url(self):
        return reverse_lazy('viewSurvey', kwargs={'pk': self.object.survey_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = Survey.objects.get(pk=self.object.survey_id)
        return context

    # Checks whether the user is the owner of the survey or is a staff member
    def form_valid(self, form):
        if self.request.user == Survey.objects.get(pk=self.object.survey_id).user or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            messages.success(self.request, "You are not the owner of this survey, so you cannot delete questions")
            return HttpResponseRedirect(reverse_lazy('index'))


class AddChoice(CreateView):
    model = Choice
    fields = ['text']
    template_name = 'addChoice.html'

    def get_success_url(self):
        return reverse_lazy('viewSurvey', kwargs={'pk': self.object.question.survey_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # gets the question object from the url
        context['survey'] = Question.objects.get(pk=self.kwargs['pk']).survey
        return context

    # Checks whether the user is the owner of the survey or is a staff member
    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        if self.request.user == Question.objects.get(pk=self.kwargs['pk']).survey.user or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            messages.success(self.request, "You are not the owner of this survey, so you cannot add choices")
            return HttpResponseRedirect(reverse_lazy('index'))


class DeleteChoice(DeleteView):
    model = Choice
    template_name = 'deleteChoice.html'

    def get_success_url(self):
        return reverse_lazy('viewSurvey', kwargs={'pk': self.object.question.survey_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = Survey.objects.get(pk=self.object.question.survey_id)
        return context

    # Checks whether the user is the owner of the survey or is a staff member
    def form_valid(self, form):
        if self.request.user == Question.objects.get(pk=self.object.question_id).survey.user or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            messages.success(self.request, "You are not the owner of this survey, so you cannot delete choices")
            return HttpResponseRedirect(reverse_lazy('index'))


class TakeSurvey(ListView):
    model = Question
    template_name = 'takeSurvey.html'
    context_object_name = 'questions'

    # Allows us to pass the survey object to the template
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = Survey.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Question.objects.filter(survey_id=self.kwargs['pk'])

    # Override post method: get answers from form, save them to Answer objects (which have question id and choice id)
    # and link them to the Response object. The AnswerResponse object links the Answer and Response objects through
    # their ids.
    def post(self, request, *args, **kwargs):
        # Check to see if the user has already taken the survey
        user = request.user
        survey = Survey.objects.get(pk=self.kwargs['pk'])
        if not Response.objects.filter(survey_id=survey, user_id=user).exists():
            form = AnswerForm(request.POST, choices=Choice.objects.filter(question__survey_id=self.kwargs['pk']))
            if form.is_valid():
                response = Response.objects.create(survey_id=self.kwargs['pk'], user_id=user.id)
                for question in Question.objects.filter(survey_id=self.kwargs['pk']):
                    answer = Answer.objects.create(question_id=question.id, choice_id=form.cleaned_data[question.text].id)
                    AnswerResponse.objects.create(answer_id=answer.id, response_id=response.id)
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return render(request, self.template_name, {'form': form, 'survey': Survey.objects.get(pk=self.kwargs['pk'])})
        else:
            messages.error(request, 'You have already taken this survey.')
            return HttpResponseRedirect(reverse_lazy('index'))

    def get(self, request, *args, **kwargs):
        form = AnswerForm(choices=Choice.objects.filter(question__survey_id=self.kwargs['pk']))
        return render(request, self.template_name, {'form': form, 'survey': Survey.objects.get(pk=self.kwargs['pk'])})

    def get_success_url(self):
        return reverse_lazy('index')


class ViewResponses(ListView):
    model = AnswerResponse
    template_name = 'viewResponses.html'
    context_object_name = 'answers_responses'

    def get_context_data(self, *, object_list=User, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer'] = Answer.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return AnswerResponse.objects.filter(response__survey_id=self.kwargs['pk'])

    # Make this object not accessible to users who are not the owner of the survey or are not staff members


class CreateCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'createCategory.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteCategory(DeleteView):
    model = Category
    template_name = 'deleteCategory.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    # Checks whether the user is the owner of the category or is a staff member
    def form_valid(self, form):
        if self.request.user == Category.objects.get(pk=self.kwargs['pk']).user or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            messages.success(self.request, "You are not the owner of this category, so you cannot delete it")
            return HttpResponseRedirect(reverse_lazy('index'))


class ManageCategories(ListView):
    model = Category
    template_name = 'manageCategories.html'
    context_object_name = 'categories'


