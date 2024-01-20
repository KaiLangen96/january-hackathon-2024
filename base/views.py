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


from .models import Transaction, Category, SavingGoal, SavingsDeposit
from .forms import TransactionForm, CategoryForm, SavingGoalForm, SavingsDepositForm, ContactForm


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

    Basic homepage view.

    """
    template_name = "tracker.html"

    def get(self, request):
        """
        Basic Get view for the homepage.

        """

        all_users = User.objects.all()
        user = request.user

        context = {
            'all_users': all_users,
            'user': user,
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
def transaction_list(request):
    template_name = 'transaction_list.html'
    categories = Category.objects.all()
    transactions = Transaction.objects.filter(user=request.user)
    saving_goals = SavingGoal.objects.filter(user=request.user)

    category_totals = {category.name: 0 for category in categories}

    for transaction in transactions:
        if transaction.category:
            category_totals[transaction.category.name] += transaction.amount

            # Update the SavingGoal if a saving_goal is associated with the transaction
            if transaction.saving_goal:
                transaction.saving_goal.current_amount += transaction.amount
                transaction.saving_goal.save()

    total_income = category_totals.get('Income', 0)
    total_expenses = category_totals.get('Expense', 0)
    total_savings = category_totals.get('Savings', 0)

    leftover_money = total_income - (total_expenses + total_savings)

    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            # Update the SavingGoal if the transaction is associated with one
            if transaction.saving_goal:
                transaction.saving_goal.current_amount += transaction.amount
                transaction.saving_goal.save()

            return redirect('transaction_list')
    else:
        form = TransactionForm(request.user)

    return render(request, template_name, {
        'transactions': transactions,
        'categories': categories,
        'form': form,
        'category_totals': category_totals,
        'leftover_money': leftover_money,
        'saving_goals': saving_goals,
    })


@method_decorator(login_required, name='dispatch')
class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_update.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        # Ensure only the transactions of the authenticated user are considered
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        # Ensure only the transactions of the authenticated user are considered
        return Transaction.objects.filter(user=self.request.user)



@method_decorator(login_required, name='dispatch')
class CategoryListView(UserPassesTestMixin, View):  # Update the class definition
    template_name = 'category_list.html'

    # Add the following test function
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, self.template_name, {'categories': categories, 'form': form})

    def post(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('category_list')

        return render(request, self.template_name, {'categories': categories, 'form': form})

@login_required
def saving_goals(request):
    template_name = 'saving_goals.html'
    goals = SavingGoal.objects.filter(user=request.user)

    return render(request, template_name, {'goals': goals})

@login_required
def add_saving_goal(request):
    template_name = 'add_saving_goal.html'

    if request.method == 'POST':
        form = SavingGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('saving_goals')
    else:
        form = SavingGoalForm()

    return render(request, template_name, {'form': form})

@login_required
def update_saving_goal(request, pk):
    template_name = 'update_saving_goal.html'
    goal = get_object_or_404(SavingGoal, pk=pk)

    if request.method == 'POST':
        form = SavingGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('saving_goals')
    else:
        form = SavingGoalForm(instance=goal)

    return render(request, template_name, {'form': form, 'goal': goal})

@login_required
def add_savings_deposit(request, goal_pk):
    template_name = 'add_savings_deposit.html'
    goal = get_object_or_404(SavingGoal, pk=goal_pk)

    if request.method == 'POST':
        form = SavingsDepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.goal = goal
            deposit.save()

            # Update the current amount of the saving goal
            goal.current_amount += deposit.amount
            goal.save()

            return redirect('saving_goals')
    else:
        form = SavingsDepositForm()

    return render(request, template_name, {'form': form, 'goal': goal})

class SavingGoalDeleteView(DeleteView):
    model = SavingGoal
    success_url = reverse_lazy('transaction_list')  # Redirect to the transaction list after deletion
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