from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.utils import timezone
from django.db.models import Sum,  Q, Count
from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from decimal import Decimal
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder



from .models import Transaction, SavingGoal, Profile
from .forms import TransactionForm, SavingGoalForm, ContactForm

@login_required
def add_savings_deposit(request, goal_pk):
    template_name = "add_savings_deposit.html"
    goal = get_object_or_404(SavingGoal, pk=goal_pk)

    if request.method == "POST":
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.saving_goal = goal
            deposit.save()

            return redirect("saving_goals")
    else:
        form = TransactionForm(request.user)

    return render(request, template_name, {"form": form, "goal": goal})




class HomePageView(generic.View):
    """
    Basic homepage view.

    """

    def get(self, request):
        """
        Basic Get view for the homepage.

        """
        return render(
            request,
            "home.html",
        )


class TrackerPageView(LoginRequiredMixin, generic.View):
    """
    Tracking page view.

    """
    template_name = "tracker.html"

    def get(self, request):
        user = request.user

        # Get all friends profiles
        friends_profiles = user.profile.friends.all()
        friends_users = User.objects.filter(profile__in=friends_profiles)
        total_friends = friends_users.count()

        # Get all goals associated with the logged-in user and friends
        all_goals = SavingGoal.objects.filter(
            models.Q(user=user) | models.Q(user__in=friends_users)
        )    

        # Calculate total amount saved by the user's
        total_amount_saved_user_goals = Transaction.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate total amount saved for the user's goal by all
        total_amount_friends_saved = Transaction.objects.filter(saving_goal__in=all_goals)
        total_goals_amount = total_amount_friends_saved.aggregate(Sum('amount'))['amount__sum'] or 0


        print(total_amount_friends_saved)

        # Calculate total amount saved in the last week for the user's goals
        last_week_start = timezone.now() - timezone.timedelta(days=7)
        amount_saved_last_week_user_goals = Transaction.objects.filter(
            user=user,
            date__gte=last_week_start,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate total amount saved from friends
        total_amount_saved_friends_goals = Transaction.objects.filter(
            user__in=friends_users,
        ).exclude(user=user).aggregate(Sum('amount'))['amount__sum'] or 0


        total_user_goals = all_goals.filter(user=user).count()
        total_friends_goals = all_goals.exclude(user=user).count()
        total_goals = total_user_goals + total_friends_goals

        context = {
            "user": user,
            "total_friends": total_friends,
            "total_goals": total_goals,
            "total_goals_amount": total_goals_amount,
            "total_amount_saved_user_goals": total_amount_saved_user_goals,
            "amount_saved_last_week_user_goals": amount_saved_last_week_user_goals,
            "total_amount_saved_friends_goals": total_amount_saved_friends_goals,
        }

        return render(request, self.template_name, context)


class AllSavingsGoalsListView(LoginRequiredMixin, generic.ListView):
    model = SavingGoal
    template_name = "view_all_savings_goals.html"
    context_object_name = "goals"

    def get_queryset(self):
        user_profile = self.request.user.profile

        # Get all friends' profiles
        friends_profiles = user_profile.friends.all()

        # Extract User instances from friends_profiles
        friends_users = User.objects.filter(profile__in=friends_profiles)

        # Get all goals associated with the logged-in user and friends
        all_goals = SavingGoal.objects.filter(
            models.Q(user=user_profile.user) | models.Q(user__in=friends_users)
        )

        return all_goals



class AboutPageView(generic.View):
    """
    Basic about view.

    """

    def get(self, request):
        """
        Basic Get view for the homepage.

        """

        return render(
            request,
            "about.html",
        )


class ContactPageView(generic.View):
    """
    Basic homepage view.

    """

    def get(self, request):
        """
        Basic Get view for the homepage.

        """

        return render(
            request,
            "contact.html",
        )



class SavingGoalDetailsView(LoginRequiredMixin, generic.View):
    template_name = "saving_goal_details.html"

    def get(self, request, goal_pk):
        goal = get_object_or_404(SavingGoal, pk=goal_pk)

        depositing_users = User.objects.filter(transaction__saving_goal=goal).distinct()

        user_deposits = []
        for user in depositing_users:
            total_amount_deposited = Transaction.objects.filter(user=user, saving_goal=goal).aggregate(Sum('amount'))['amount__sum'] or 0
            deposit_count = Transaction.objects.filter(user=user, saving_goal=goal).count()

            user_deposit = {
                "user": user.username,  # Display username instead of User instance
                "deposits": deposit_count,
                "total": float(total_amount_deposited),  # Convert Decimal to float
            }

            user_deposits.append(user_deposit)

        depositing_users_count = depositing_users.count()

        user_deposits_json = JsonResponse(user_deposits, encoder=DjangoJSONEncoder, safe=False)

        decoded_data = user_deposits_json.content.decode('utf-8')

        context = {
            "goal": goal,
            "depositing_users": depositing_users,
            "depositing_users_count": depositing_users_count,
            "user_deposits": decoded_data,  
        }

        return render(request, self.template_name, context)

class SavingGoalsListView(LoginRequiredMixin, generic.ListView):
    model = SavingGoal
    template_name = "saving_goals.html"
    context_object_name = "goals"

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)


@login_required
def add_saving_goal(request):
    template_name = "add_saving_goal.html"

    if request.method == "POST":
        form = SavingGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect("saving_goals")
    else:
        form = SavingGoalForm()

    return render(request, template_name, {"form": form})


@login_required
def update_saving_goal(request, pk):
    template_name = "update_saving_goal.html"
    goal = get_object_or_404(SavingGoal, pk=pk)

    if request.method == "POST":
        form = SavingGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("saving_goals")
    else:
        form = SavingGoalForm(instance=goal)

    return render(request, template_name, {"form": form, "goal": goal})


class SavingGoalDeleteView(DeleteView):
    model = SavingGoal
    success_url = reverse_lazy('/')  # Redirect to the transaction list after deletion
    template_name = 'saving_goal_confirm_delete.html'  # Create this template if it doesn't exist


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Processes the form data
            pass
            messages.success(request, 'Your contact form has been submitted!')
            return HttpResponseRedirect(reverse('contact'))
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def handler404(request, exception):
    """
    Custom 404 page
    """
    return render(request, "error_html/404.html", status=404)


def handler500(request):
    """
    Custom 500 page
    """
    return render(request, "error_html/500.html", status=500)


def handler403(request, exception):
    """
    Custom 403 page
    """
    return render(request, "error_html/403.html", status=403)


def handler405(request, exception):
    """
    Custom 405 page
    """
    return render(request, "error_html/405.html", status=405)


class UsersListView(generic.View):
    """
    Basic homepage view.
    """

    template_name = "users_list.html"

    def get(self, request):
        """
        Basic Get view for the homepage.
        """

        # Get all users
        all_users = User.objects.all()

        # Calculate the total saved amount for each user in transactions
        user_totals = []
        for user in all_users:
            total_saved = Transaction.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
            user_totals.append({"user": user, "total_saved": total_saved})

        context = {
            "all_users": all_users,
            "user_totals": user_totals,
        }

        return render(request, self.template_name, context)

@login_required
@require_POST
def toggle_friend(request):
    friend_id = request.POST.get('friend_id')
    friend_profile = get_object_or_404(Profile, id=friend_id)
    
    user_profile = request.user.profile

    if user_profile.friends.filter(id=friend_id).exists():
        # If friend is already in the friends list, remove them
        user_profile.friends.remove(friend_profile)
        message = 'Friend removed successfully'
    else:
        # If friend is not in the friends list, add them
        user_profile.friends.add(friend_profile)
        message = 'Friend added successfully'

    return redirect('users_list')