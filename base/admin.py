from django.contrib import admin
from .models import Transaction, SavingGoal


# Register your models here.

class TransactionInline(admin.TabularInline):
    """
    Inline representation of blog posts for the admin panel.

    """

    model = Transaction
    fields = ("amount", "date", "description")
    extra = 0



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin model configuration for post categories.

    """

@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    """
    Admin model configuration for post categories.

    """
    inlines = [TransactionInline]
