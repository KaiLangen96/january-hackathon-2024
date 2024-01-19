from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm

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
    def get(self, request):
        """
        Basic Get view for the homepage.

        """
        return render(
            request,
            "tracker.html",
        )


@method_decorator(login_required, name='dispatch')
class TransactionListView(UserPassesTestMixin, View):
    template_name = 'transaction_list.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        transactions = Transaction.objects.filter(user=request.user)

        # Calculate the total amount for each category
        category_totals = {category.name: 0 for category in categories}

        for transaction in transactions:
            if transaction.category:
                category_totals[transaction.category.name] += transaction.amount

        # Calculate the total income, expenses, and savings
        total_income = category_totals.get('Income', 0)
        total_expenses = category_totals.get('Expense', 0)
        total_savings = category_totals.get('Savings', 0)

        # Calculate the leftover money
        leftover_money = total_income - (total_expenses + total_savings)

        form = TransactionForm()
        return render(request, self.template_name, {'transactions': transactions, 'categories': categories, 'form': form, 'category_totals': category_totals, 'leftover_money': leftover_money})
    
    def post(self, request, *args, **kwargs):
        categories = Category.objects.all()
        transactions = Transaction.objects.filter(user=request.user)
        category_totals = {category.name: 0 for category in categories}
        
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.save()

        # Recalculate the total amount for each category
        for transaction in transactions:
            if transaction.category:
                category_totals[transaction.category.name] += transaction.amount

        # Recalculate the total income, expenses, and savings
        total_income = category_totals.get('Income', 0)
        total_expenses = category_totals.get('Expense', 0)
        total_savings = category_totals.get('Savings', 0)

        # Recalculate the leftover money
        leftover_money = total_income - (total_expenses + total_savings)

        return render(request, self.template_name, {'transactions': transactions, 'categories': categories, 'form': form, 'category_totals': category_totals, 'leftover_money': leftover_money})


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
    
    
