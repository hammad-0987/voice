from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Analytics snapshots
    path('snapshots/', views.AnalyticsSnapshotListView.as_view(), name='analytics_snapshots'),
    path('departments/', views.DepartmentAnalyticsListView.as_view(), name='department_analytics'),
    
    # Dashboard and overview
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    
    # Detailed analytics
    path('complaints/', views.complaint_analytics, name='complaint_analytics'),
    path('feedback/', views.feedback_analytics, name='feedback_analytics'),
    path('users/', views.user_analytics, name='user_analytics'),
    
    # Snapshot generation
    path('generate-snapshot/', views.generate_snapshot, name='generate_snapshot'),
]

