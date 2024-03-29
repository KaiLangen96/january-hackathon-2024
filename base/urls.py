"""URL Patterns"""

from django.urls import path
from . import views
from .views import ( add_saving_goal, update_saving_goal, add_savings_deposit, delete_saving_goal, contact, toggle_friend
)

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("tracker/", views.TrackerPageView.as_view(), name="tracker"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
    path('saving_goal_details/<int:goal_pk>/', views.SavingGoalDetailsView.as_view(), name='saving_goal_details'),
    path('saving-goals/', views.SavingGoalsListView.as_view(), name='saving_goals'),
    path('all_saving_goals/', views.AllSavingsGoalsListView.as_view(), name='all_saving_goals'),
    path('saving-goals/add/', add_saving_goal, name='add_saving_goal'),
    path('saving-goals/<int:pk>/update/', update_saving_goal, name='update_saving_goal'),
    path('saving-goals/<int:goal_pk>/add-deposit/', add_savings_deposit, name='add_savings_deposit'),
    path('saving-goals/<int:pk>/delete/', delete_saving_goal, name='delete_saving_goal'),
    path('contact/', contact, name='contact'),
    path('users_list/', views.UsersListView.as_view(), name='users_list'),
    path('toggle_friend/', toggle_friend, name='toggle_friend'),
]