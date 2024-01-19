from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

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

    if request.method == 'POST':
        form = TransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TransactionForm(user=request.user)

    # Filter transactions for the authenticated user
    transactions = Transaction.objects.filter(user=request.user)
    
    category_totals = {category.name: 0 for category in categories}

    for transaction in transactions:
        if transaction.category:
            category_totals[transaction.category.name] += transaction.amount

    total_income = category_totals.get('Income', 0)
    total_expenses = category_totals.get('Expense', 0)
    total_savings = category_totals.get('Savings', 0)

    leftover_money = total_income - (total_expenses + total_savings)

    return render(request, template_name, {'transactions': transactions, 'categories': categories, 'form': form, 'category_totals': category_totals, 'leftover_money': leftover_money})


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
