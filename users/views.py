from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from surveys.models import Answer, Choice, Response
from users.models import UserFollows


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect("index")
        else:
            messages.error(request, "Error logging in")
            return redirect("login_user")
    else:
        return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("index")


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form, })


# Manage users followed by the current user

def search_user(request):
    # create a method to search for users using the search bar
    if request.method == "POST":
        search_text = request.POST['search_text']
        # make it not case sensitive
        users = User.objects.filter(username__icontains=search_text)
        # get the users that the current user is following with the UserFollows model, selecting only the followed_user
        followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
        return render(request, 'searchUser.html', {'users': users, 'followed_users': followed_users})
    else:
        return render(request, 'searchUser.html')


class ManageFollowedUsers(ListView):
    model = UserFollows
    template_name = 'manageFollowedUsers.html'
    context_object_name = 'followed_users'

    def get_context_data(self, *, object_list=None, **kwargs):
        # get all users that follow the current user using the UserFollows model
        context = super(ManageFollowedUsers, self).get_context_data(**kwargs)
        context['followers'] = UserFollows.objects.filter(followed_user=self.request.user)
        context['following'] = UserFollows.objects.filter(user=self.request.user).values_list('followed_user', flat=True)
        return context

    def get_queryset(self):
        return UserFollows.objects.filter(user=self.request.user)


def follow_user(request, pk):
    if UserFollows.objects.filter(user=request.user, followed_user=User.objects.get(pk=pk)).exists():
        messages.error(request, "You are already following this user")
        return HttpResponseRedirect(reverse_lazy('manage_followed_users'))
    else:
        user = request.user
        followed_user = User.objects.get(pk=pk)
        UserFollows.objects.create(user=user, followed_user=followed_user)
        messages.success(request, "You have successfully followed " + followed_user.username)
        return HttpResponseRedirect(reverse_lazy('manage_followed_users'))


def unfollow_user(request, pk):
    if UserFollows.objects.filter(user=request.user, followed_user=User.objects.get(pk=pk)).exists():
        followed_user = User.objects.get(pk=pk)
        user = request.user
        UserFollows.objects.filter(user=user, followed_user=followed_user).delete()
        messages.success(request, "You have successfully unfollowed " + followed_user.username)
        return HttpResponseRedirect(reverse_lazy('manage_followed_users'))
    else:
        messages.error(request, "You are not following this user")
        return HttpResponseRedirect(reverse_lazy('manage_followed_users'))


def is_following(user, followed_user):
    return UserFollows.objects.filter(user=user, followed_user=followed_user).exists()


class DeleteUser(View):
    model = User
    template_name = 'deleteUser.html'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    if user.id == request.user.id or request.user.is_superuser:
        # delete all the responses of the user that is being deleted, so that they don't appear in the statistics
        # get responses ids of the current user and store them in responses
        responses = Response.objects.filter(user_id=pk).all()
        for response in responses:
            # delete all the answers of the current response and update the number of votes for each choice
            answers = Answer.objects.filter(response_id=response.id).all()
            for answer in answers:
                choice = Choice.objects.get(pk=answer.choice_id)
                choice.number_of_votes -= 1
                choice.save()
                answer.delete()
            response.delete()
        if user.delete():
            messages.success(request, "You have successfully deleted " + user.username)
            return redirect('login_user')
        else:
            messages.error(request, "Something went wrong, you have not deleted the user")
            return render(request, "deleteUser.html")
    else:
        messages.error(request, "You are not allowed to delete this user")
        return render(request, "index.html")

