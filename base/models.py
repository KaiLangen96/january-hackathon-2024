from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from decimal import Decimal



class Profile(models.Model):
    """
    Model to represent extend auth User Class to add addition
    profile information.

    """

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        """Return a string representation of the object (the post's title)."""
        return str(self.user)

def create_user_profile(instance, created, *args, **kwargs):
    """
    Signal handler function to create a user profile when a
    new user is created.

    This function is connected to the User model's post_save signal.
    kwargs are required for dispatch signals

    """
    if created:
        Profile.objects.create(user=instance)

# Connects profile to user instance with signals


models.signals.post_save.connect(create_user_profile, sender=User)


class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def add_deposit(self, amount):
        self.current_amount += amount
        self.save()

    def calculate_remaining_percentage(self):
        if self.target_amount > 0:
            percentage = (self.current_amount / self.target_amount) * 100
            return round(percentage, 2)
        else:
            return Decimal('0.00')



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    saving_goal = models.ForeignKey(
        SavingGoal, on_delete=models.CASCADE, related_name="saving_goal"
    )

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create a deposit if a saving goal is associated with the transaction
        if self.saving_goal:
            self.saving_goal.add_deposit(self.amount)
