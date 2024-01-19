from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy

from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm
from django.views.generic.edit import UpdateView, DeleteView

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


@method_decorator(login_required, name='dispatch')
class TransactionListView(UserPassesTestMixin, View):
    template_name = 'transaction_list.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        transactions = Transaction.objects.filter(user=request.user)
        category_totals = {category.name: 0 for category in categories}

        for transaction in transactions:
            if transaction.category:
                category_totals[transaction.category.name] += transaction.amount

        total_income = category_totals.get('Income', 0)
        total_expenses = category_totals.get('Expense', 0)
        total_savings = category_totals.get('Savings', 0)

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

        for transaction in transactions:
            if transaction.category:
                category_totals[transaction.category.name] += transaction.amount

        total_income = category_totals.get('Income', 0)
        total_expenses = category_totals.get('Expense', 0)
        total_savings = category_totals.get('Savings', 0)

        leftover_money = total_income - (total_expenses + total_savings)

        return render(request, self.template_name, {'transactions': transactions, 'categories': categories, 'form': form, 'category_totals': category_totals, 'leftover_money': leftover_money})

    # Add the following methods for updating and deleting transactions
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_form'] = TransactionForm()
        return context

    def get_context_object_name(self, obj):
        return 'transaction'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(Transaction, id=self.kwargs['pk'], user=self.request.user)

    def get_template_names(self):
        return 'transaction_list.html'

    def get_success_url(self):
        return reverse('transaction_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_update.html'
    success_url = reverse_lazy('transaction_list')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')
