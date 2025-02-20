from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("statistics/", views.statistics, name="statistics"),
    path("all/", views.AllQuestionView.as_view(), name="all"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
    path("create/", views.create_question, name="create"),
    path("login/", views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
