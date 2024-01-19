"""URL Patterns"""

from django.urls import path
from . import views
from .views import transaction_list, TransactionUpdateView, TransactionDeleteView, CategoryListView, \
    saving_goals, add_saving_goal, update_saving_goal, add_savings_deposit

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("tracker", views.TrackerPageView.as_view(), name="tracker"),
    path("about", views.AboutPageView.as_view(), name="about"),
    path("contact", views.ContactPageView.as_view(), name="contact"),
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name='update_transaction'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='delete_transaction'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('saving-goals/', saving_goals, name='saving_goals'),
    path('saving-goals/add/', add_saving_goal, name='add_saving_goal'),
    path('saving-goals/<int:pk>/update/', update_saving_goal, name='update_saving_goal'),
    path('saving-goals/<int:goal_pk>/add-deposit/', add_savings_deposit, name='add_savings_deposit'),
]