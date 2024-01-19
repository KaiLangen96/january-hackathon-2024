from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date', 'category']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        # Set the DateInput widget for the 'date' field
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')

    def clean_date(self):
        # Ensure the date is in the correct format for submission
        date = self.cleaned_data['date']
        return date.strftime('%Y-%m-%d')

    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction.user = self.user
        if commit:
            transaction.save()
        return transaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
