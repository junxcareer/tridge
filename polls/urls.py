from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/comment/', views.add_comment, name='comment'),
    path('<int:choice_id>/approve_choice/', views.approve_choice, name='approve_choice'),
    path('<int:question_id>/choice/', views.ChoiceView.as_view(), name='choice'),
    path('<int:comment_id>/reply/', views.add_reply, name='reply'),
]
