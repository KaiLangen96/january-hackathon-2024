from django import forms
from .models import Transaction, SavingGoal
from django.core.validators import EmailValidator


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ["description", "amount", "date"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        # Set the DateInput widget for the 'date' field
        self.fields["date"].widget = forms.DateInput(
            attrs={"type": "date"}, format="%Y-%m-%d"
        )

    def clean_date(self):
        # Ensure the date is in the correct format for submission
        date = self.cleaned_data["date"]
        return date.strftime("%Y-%m-%d")

    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction.user = self.user
        if commit:
            transaction.save()
        return transaction


class SavingGoalForm(forms.ModelForm):
    class Meta:
        model = SavingGoal
        fields = ["name", "target_amount"]

class ContactForm(forms.Form):
    name = forms.CharField(label="",max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Your Name','class': 'my-2 w-50'}))
    email = forms.EmailField(label="",validators=[EmailValidator(message="Invalid Email")],widget=forms.TextInput(attrs={'placeholder': 'Your Email','class': 'my-2 w-50'}))
    subject = forms.CharField(label="",max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Subject','class': 'my-2 w-50'}))
    message = forms.CharField(label="",widget= forms.Textarea(attrs={'placeholder': 'Message','class': 'my-2 w-50'}) )
