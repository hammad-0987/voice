from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    # Complaint CRUD
    path('', views.ComplaintListCreateView.as_view(), name='complaint_list'),
    path('<int:pk>/', views.ComplaintDetailView.as_view(), name='complaint_detail'),
    
    # Complaint tracking
    path('track/<str:complaint_number>/', views.track_complaint, name='track_complaint'),
    path('by-number/<str:complaint_number>/', views.complaint_by_number, name='complaint_by_number'),
    
    # Complaint forwarding
    path('<int:complaint_id>/forward/', views.ComplaintForwardView.as_view(), name='complaint_forward'),
    
    # Comments and replies
    path('<int:complaint_id>/comments/', views.ComplaintCommentListCreateView.as_view(), name='complaint_comments'),
    path('<int:complaint_id>/comments/<int:comment_id>/reply/', views.ComplaintCommentReplyView.as_view(), name='comment_reply'),
    
    # Statistics
    path('statistics/', views.complaint_statistics, name='complaint_statistics'),
]

