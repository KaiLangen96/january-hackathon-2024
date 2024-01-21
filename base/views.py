from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


from .models import Transaction, SavingGoal, SavingsDeposit
from .forms import TransactionForm, SavingGoalForm, SavingsDepositForm, ContactForm



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


class TrackerPageView(generic.View):
    """

    Basic tracker view.

    """

    template_name = "tracker.html"

    def get(self, request):
        """
        Basic Get view for the homepage.

        """

        all_users = User.objects.all()
        user = request.user

        context = {
            "all_users": all_users,
            "user": user,
        }

        return render(request, self.template_name, context)


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



@login_required
def saving_goal_details(request, goal_pk):
    template_name = "saving_goal_details.html"
    goal = get_object_or_404(SavingGoal, pk=goal_pk)

    return render(request, template_name, {"goal": goal})

@login_required
def saving_goals(request):
    template_name = "saving_goals.html"
    goals = SavingGoal.objects.filter(user=request.user)

    return render(request, template_name, {"goals": goals})


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
