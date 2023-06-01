from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from users.models import UserFollows
from .models import Survey, Question, Choice, Answer, Response, AnswerResponse, Category, UserCategorySubscription
from .forms import AnswerForm

from django import template
register = template.Library()


# Create your views here.


class ViewSurveys(ListView):
    model = Survey
    template_name = 'index.html'
    context_object_name = 'surveys'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.all()
        # get all the surveys related to the categories the user is subscribed to
        # check whether a user is authenticated
        if self.request.user.is_authenticated:
            context['subscribed_surveys'] = Survey.objects.filter(category__in=UserCategorySubscription.objects.filter(user=self.request.user).values_list('category', flat=True))
            # get all the surveys made by the users the current user is following
            context['followed_users_surveys'] = Survey.objects.filter(user__in=User.objects.filter(pk__in=UserFollows.objects.filter(user=self.request.user).values_list('followed_user', flat=True)))
        return context

    def get_queryset(self):
        return Survey.objects.all()


class CreateSurvey(CreateView):
    model = Survey
    fields = ['name', 'description', 'category', 'deadline']
    template_name = 'createSurvey.html'
    success_url = reverse_lazy('manageSurveys')

    # This method is called when the form is submitted and adds current user to the survey
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.request.user.username)
        context['categories'] = Category.objects.all()
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
            messages.error(self.request, "You are not the owner of this survey")
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


class EditSurvey(UpdateView):
    model = Survey
    fields = ['name', 'description', 'category', 'deadline']
    template_name = 'editSurvey.html'

    # This method is called when the form is submitted and adds current user to the survey
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Survey edited successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('viewSurvey', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the survey object
        context['survey'] = Survey.objects.get(pk=self.kwargs['pk'])
        # get the user object
        context['user'] = User.objects.get(username=self.request.user.username)
        # get all the categories
        context['categories'] = Category.objects.all()
        return context


class AddQuestion(CreateView):
    model = Question
    fields = ['text']
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
            messages.success(self.request, "Question added successfully")
            return super().form_valid(form)
        else:
            messages.error(self.request, "You are not the owner of this survey, so you cannot add questions")
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
            messages.success(self.request, "Question deleted successfully")
            return super().form_valid(form)
        else:
            messages.error(self.request, "You are not the owner of this survey, so you cannot delete questions")
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
            messages.success(self.request, "Choice added successfully")
            return super().form_valid(form)
        else:
            messages.error(self.request, "You are not the owner of this survey, so you cannot add choices")
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
            messages.success(self.request, "Choice deleted successfully")
            return super().form_valid(form)
        else:
            messages.error(self.request, "You are not the owner of this survey, so you cannot delete choices")
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
                    # Update the number of responses for each choice
                    choice = Choice.objects.get(pk=form.cleaned_data[question.text].id)
                    choice.number_of_votes = choice.number_of_votes + 1
                    choice.save()
                messages.success(request, 'Survey completed successfully')
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


class DeleteResponse(DeleteView):
    model = Response
    template_name = 'deleteResponse.html'
    context_object_name = 'response'

    # delete the response made to the survey by the current user
    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.get(pk=self.object.id)
        return context

    def form_valid(self, form):
        if self.request.user == Response.objects.get(pk=self.object.id).user or self.request.user.is_staff:
            messages.success(self.request, "Response deleted successfully")
            user = self.request.user
            response = Response.objects.get(pk=self.kwargs['pk'])
            for question in AnswerResponse.objects.filter(response_id=response.id):
                # Update the number of responses for each choice
                choice = Choice.objects.get(pk=question.answer.choice_id)
                choice.number_of_votes = choice.number_of_votes - 1
                choice.save()
            collector = AnswerResponse.objects.filter(response_id=response.id).all()
            for answer in collector:
                answer.delete()
            AnswerResponse.objects.filter(response_id=response.id).all().delete()
            response.delete()
            return super().form_valid(form)
        else:
            messages.error(self.request, "You are not the owner of this response, so you cannot delete it")
            return HttpResponseRedirect(reverse_lazy('index'))


class ViewResponses(ListView):
    model = AnswerResponse
    template_name = 'viewResponses.html'
    context_object_name = 'answers_responses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = Survey.objects.get(pk=self.kwargs['pk'])
        context['questions'] = Question.objects.filter(survey_id=self.kwargs['pk'])
        context['answers'] = Answer.objects.filter(question__survey_id=self.kwargs['pk'])
        context['choices'] = Choice.objects.all()
        return context

    def get_queryset(self):
        return AnswerResponse.objects.filter(response__survey_id=self.kwargs['pk'])


class CreateCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'createCategory.html'

    def get_success_url(self):
        return reverse_lazy('manageCategories')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteCategory(DeleteView):
    model = Category
    template_name = 'deleteCategory.html'

    def get_success_url(self):
        return reverse_lazy('manageCategories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    # Checks whether the user is the owner of the category or is a staff member
    def form_valid(self, form):
        if self.request.user == Category.objects.get(pk=self.kwargs['pk']).user or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            messages.error(self.request, "You are not the owner of this category, so you cannot delete it")
            return HttpResponseRedirect(reverse_lazy('manageCategories'))


class ManageCategories(ListView):
    model = Category
    template_name = 'manageCategories.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # get all categories that the user is subscribed to
        context['subscribed_categories'] = UserCategorySubscription.objects.filter(user=self.request.user).values_list('category', flat=True)
        return context


def subscribe_to_category(request, pk):
    # this function is called when a user clicks the subscribe button on a category
    # it adds the user to the category's subscribers through UserCategorySubscription
    # and redirects the user to the index page
    # check if the user is already subscribed to the category
    if not UserCategorySubscription.objects.filter(user=request.user, category=Category.objects.get(pk=pk)).exists():
        category = Category.objects.get(pk=pk)
        user = request.user
        UserCategorySubscription.objects.create(user=user, category=category)
        messages.success(request, "You have successfully subscribed to this category!")
        return HttpResponseRedirect(reverse_lazy('manageCategories'))
    else:
        messages.error(request, "You are already subscribed to this category!")
        return HttpResponseRedirect(reverse_lazy('manageCategories'))


def unsubscribe_from_category(request, pk):
    # this function is called when a user clicks the unsubscribe button on a category
    # it removes the user from the category's subscribers through UserCategorySubscription
    # and redirects the user to the index page
    # check if the user is already subscribed to the category
    if UserCategorySubscription.objects.filter(user=request.user, category=Category.objects.get(pk=pk)).exists():
        category = Category.objects.get(pk=pk)
        user = request.user
        UserCategorySubscription.objects.filter(user=user, category=category).delete()
        messages.success(request, "You have successfully unsubscribed from this category!")
        return HttpResponseRedirect(reverse_lazy('manageCategories'))
    else:
        messages.error(request, "You are not subscribed to this category!")
        return HttpResponseRedirect(reverse_lazy('manageCategories'))


# create a class that allows the user to edit their surveys
class ManageSurveys(ListView):
    model = Survey
    template_name = 'manageSurveys.html'
    context_object_name = 'surveys'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # get all surveys that the user owns
        context['owned_surveys'] = Survey.objects.filter(user=self.request.user)
        return context

