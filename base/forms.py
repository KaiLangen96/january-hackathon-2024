from django import forms
from .models import Transaction, Category, SavingGoal, SavingsDeposit

class TransactionForm(forms.ModelForm):
    saving_goal = forms.ModelChoiceField(
        queryset=None,  # You'll set this dynamically in the view
        required=False,
        empty_label="Select a Saving Goal"
    )

    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date', 'category']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        # Set the DateInput widget for the 'date' field
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        self.fields['saving_goal'].queryset = SavingGoal.objects.filter(user=user)

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

class SavingGoalForm(forms.ModelForm):
    class Meta:
        model = SavingGoal
        fields = ['name', 'target_amount']

class SavingsDepositForm(forms.ModelForm):
    class Meta:
        model = SavingsDeposit
        fields = ['amount']
