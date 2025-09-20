from django.urls import path
from . import views

app_name = 'withdrawals'

urlpatterns = [
    # Withdrawal request CRUD
    path('', views.WithdrawalRequestListCreateView.as_view(), name='withdrawal_list'),
    path('<int:pk>/', views.WithdrawalRequestDetailView.as_view(), name='withdrawal_detail'),
    
    # Review withdrawal requests
    path('<int:pk>/review/', views.WithdrawalRequestReviewView.as_view(), name='withdrawal_review'),
    
    # Statistics and user-specific endpoints
    path('statistics/', views.withdrawal_statistics, name='withdrawal_statistics'),
    path('my-requests/', views.my_withdrawal_requests, name='my_withdrawal_requests'),
]

