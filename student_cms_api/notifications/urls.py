from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Notification CRUD
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification_detail'),
    
    # Notification actions
    path('mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('delete-read/', views.delete_all_read_notifications, name='delete_all_read'),
    
    # Notification queries
    path('unread/', views.unread_notifications, name='unread_notifications'),
    path('recent/', views.recent_notifications, name='recent_notifications'),
    path('stats/', views.notification_stats, name='notification_stats'),
    
    # User preferences
    path('preferences/', views.NotificationPreferenceView.as_view(), name='notification_preferences'),
    
    # Testing (debug only)
    path('test/', views.test_notification, name='test_notification'),
]

