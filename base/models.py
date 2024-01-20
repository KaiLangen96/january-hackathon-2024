from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def add_deposit(self, amount):
        self.current_amount += amount
        self.save()

class Deposit(models.Model):
    goal = models.ForeignKey(SavingGoal, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Deposit of {self.amount} to {self.goal} on {self.date}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    saving_goal = models.ForeignKey(SavingGoal, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Automatically create a deposit if a saving goal is associated with the transaction
        if self.saving_goal:
            self.saving_goal.add_deposit(self.amount)

class SavingsDeposit(models.Model):
    goal = models.ForeignKey(SavingGoal, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}€ deposited for {self.goal.name} on {self.date}"