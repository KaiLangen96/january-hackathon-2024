from django.contrib import admin
from django.contrib.auth.models import User
from .models import Transaction, SavingGoal, Profile

# Register your models here.

class ProfileInline(admin.StackedInline):
    """
    Inline representation of user profiles for the admin panel.

    """

    model = Profile


class TransactionInline(admin.TabularInline):
    """
    Inline representation of blog posts for the admin panel.

    """

    model = Transaction
    fields = ("amount", "date", "description")
    extra = 0

class UserAdmin(admin.ModelAdmin):
    """
    Admin model configuration for user accounts.

    This class defines the admin panel configuration for user accounts,
    allowing administrators to manage user information such as username,
    first name, last name, and email. It also includes an inline
    representation of user profiles using the `ProfileInline` class

    Example:
        To use this admin configuration for user accounts:

        admin.site.register(User, UserAdmin)

    """

    model = User
    fields = ("username", "first_name", "last_name", "email")
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


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
