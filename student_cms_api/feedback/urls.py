from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    # Feedback CRUD
    path('', views.ComplaintFeedbackListCreateView.as_view(), name='feedback_list'),
    path('<int:pk>/', views.ComplaintFeedbackDetailView.as_view(), name='feedback_detail'),
    
    # Feedback responses
    path('<int:feedback_id>/responses/', views.FeedbackResponseListCreateView.as_view(), name='feedback_responses'),
    
    # User-specific endpoints
    path('my-feedback/', views.my_feedback, name='my_feedback'),
    
    # Analytics and statistics
    path('statistics/', views.feedback_statistics, name='feedback_statistics'),
    path('analytics/', views.feedback_analytics, name='feedback_analytics'),
]

