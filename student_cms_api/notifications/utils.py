from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Notification, NotificationPreference


def create_notification(recipient, message, title=None, notification_type='system', 
                       link=None, related_complaint_id=None, related_withdrawal_id=None, 
                       related_feedback_id=None, send_email=True):
    """
    Create a notification for a user
    
    Args:
        recipient: User object who will receive the notification
        message: Notification message text
        title: Optional title (defaults to first 50 chars of message)
        notification_type: Type of notification
        link: Optional link to related page
        related_complaint_id: ID of related complaint
        related_withdrawal_id: ID of related withdrawal request
        related_feedback_id: ID of related feedback
        send_email: Whether to send email notification
    
    Returns:
        Notification object
    """
    
    # Generate title if not provided
    if not title:
        title = message[:50] + '...' if len(message) > 50 else message
    
    # Create notification
    notification = Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link,
        related_complaint_id=related_complaint_id,
        related_withdrawal_id=related_withdrawal_id,
        related_feedback_id=related_feedback_id,
    )
    
    # Send email notification if enabled
    if send_email:
        send_email_notification(notification)
    
    return notification


def send_email_notification(notification):
    """
    Send email notification to user based on their preferences
    """
    try:
        # Get user preferences
        preferences = NotificationPreference.get_or_create_for_user(notification.recipient)
        
        # Check if user wants email notifications for this type
        should_send_email = False
        
        if notification.notification_type in ['complaint_created', 'complaint_forwarded', 'complaint_status_changed', 'comment_added', 'reply_added']:
            should_send_email = preferences.email_complaint_updates
        elif notification.notification_type in ['withdrawal_submitted', 'withdrawal_reviewed']:
            should_send_email = preferences.email_withdrawal_updates
        elif notification.notification_type in ['feedback_submitted', 'feedback_response']:
            should_send_email = preferences.email_feedback_updates
        elif notification.notification_type == 'system':
            should_send_email = preferences.email_system_updates
        
        # Check frequency preference
        if preferences.email_digest_frequency == 'never':
            should_send_email = False
        elif preferences.email_digest_frequency != 'immediate':
            # For daily/weekly digests, we would handle this separately
            # For now, just send immediate notifications
            pass
        
        if should_send_email and notification.recipient.email:
            # Prepare email content
            subject = f"Student CMS - {notification.title}"
            
            # Create HTML email content
            html_message = render_to_string('notifications/email_notification.html', {
                'notification': notification,
                'user': notification.recipient,
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:3000'),
            })
            
            # Create plain text version
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@studentcms.com',
                recipient_list=[notification.recipient.email],
                html_message=html_message,
                fail_silently=True,  # Don't raise exceptions for email failures
            )
            
            # Mark as sent
            notification.is_sent = True
            notification.save(update_fields=['is_sent'])
    
    except Exception as e:
        # Log the error but don't raise it
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send email notification {notification.id}: {str(e)}")


def create_complaint_notification(complaint, action, user=None, additional_message=""):
    """
    Create notifications for complaint-related actions
    
    Args:
        complaint: Complaint object
        action: Action type ('created', 'forwarded', 'status_changed', 'comment_added', 'reply_added')
        user: User who performed the action
        additional_message: Additional message to append
    """
    
    notifications_to_create = []
    
    if action == 'created':
        # Notify staff, heads, VCs, and admins about new complaint
        from users.models import User
        recipients = User.objects.filter(role__in=['staff', 'head', 'vc', 'admin'])
        
        for recipient in recipients:
            message = f"New complaint {complaint.complaint_number} has been submitted by {complaint.created_by.full_name}"
            if additional_message:
                message += f". {additional_message}"
            
            notifications_to_create.append({
                'recipient': recipient,
                'message': message,
                'title': f"New Complaint: {complaint.complaint_number}",
                'notification_type': 'complaint_created',
                'link': f'/complaints/{complaint.id}/',
                'related_complaint_id': complaint.id,
            })
    
    elif action == 'forwarded':
        # Notify the person who received the forwarded complaint
        if hasattr(complaint, 'assigned_to') and complaint.assigned_to:
            message = f"Complaint {complaint.complaint_number} has been forwarded to you"
            if user:
                message += f" by {user.full_name}"
            if additional_message:
                message += f". {additional_message}"
            
            notifications_to_create.append({
                'recipient': complaint.assigned_to,
                'message': message,
                'title': f"Complaint Forwarded: {complaint.complaint_number}",
                'notification_type': 'complaint_forwarded',
                'link': f'/complaints/{complaint.id}/',
                'related_complaint_id': complaint.id,
            })
    
    elif action == 'status_changed':
        # Notify the complaint creator about status change
        message = f"Your complaint {complaint.complaint_number} status has been updated to {complaint.get_status_display()}"
        if user:
            message += f" by {user.full_name}"
        if additional_message:
            message += f". {additional_message}"
        
        notifications_to_create.append({
            'recipient': complaint.created_by,
            'message': message,
            'title': f"Complaint Status Updated: {complaint.complaint_number}",
            'notification_type': 'complaint_status_changed',
            'link': f'/complaints/{complaint.id}/',
            'related_complaint_id': complaint.id,
        })
    
    elif action == 'comment_added':
        # Notify the complaint creator about new comment
        message = f"A new comment has been added to your complaint {complaint.complaint_number}"
        if user:
            message += f" by {user.full_name}"
        if additional_message:
            message += f". {additional_message}"
        
        notifications_to_create.append({
            'recipient': complaint.created_by,
            'message': message,
            'title': f"New Comment: {complaint.complaint_number}",
            'notification_type': 'comment_added',
            'link': f'/complaints/{complaint.id}/',
            'related_complaint_id': complaint.id,
        })
    
    elif action == 'reply_added':
        # Notify staff about student reply
        if user and hasattr(complaint, 'assigned_to') and complaint.assigned_to:
            message = f"Student replied to your comment on complaint {complaint.complaint_number}"
            if additional_message:
                message += f". {additional_message}"
            
            notifications_to_create.append({
                'recipient': complaint.assigned_to,
                'message': message,
                'title': f"Student Reply: {complaint.complaint_number}",
                'notification_type': 'reply_added',
                'link': f'/complaints/{complaint.id}/',
                'related_complaint_id': complaint.id,
            })
    
    # Create all notifications
    for notification_data in notifications_to_create:
        create_notification(**notification_data)


def create_withdrawal_notification(withdrawal_request, action, user=None, additional_message=""):
    """
    Create notifications for withdrawal request actions
    """
    
    if action == 'submitted':
        # Notify heads, VCs, and admins about new withdrawal request
        from users.models import User
        recipients = User.objects.filter(role__in=['head', 'vc', 'admin'])
        
        for recipient in recipients:
            message = f"New withdrawal request {withdrawal_request.request_number} has been submitted by {withdrawal_request.submitted_by.full_name}"
            if additional_message:
                message += f". {additional_message}"
            
            create_notification(
                recipient=recipient,
                message=message,
                title=f"New Withdrawal Request: {withdrawal_request.request_number}",
                notification_type='withdrawal_submitted',
                link=f'/withdrawals/{withdrawal_request.id}/',
                related_withdrawal_id=withdrawal_request.id,
            )
    
    elif action == 'reviewed':
        # Notify the student about review decision
        message = f"Your withdrawal request {withdrawal_request.request_number} has been {withdrawal_request.status}"
        if user:
            message += f" by {user.full_name}"
        if additional_message:
            message += f". {additional_message}"
        
        create_notification(
            recipient=withdrawal_request.submitted_by,
            message=message,
            title=f"Withdrawal Request {withdrawal_request.status.title()}: {withdrawal_request.request_number}",
            notification_type='withdrawal_reviewed',
            link=f'/withdrawals/{withdrawal_request.id}/',
            related_withdrawal_id=withdrawal_request.id,
        )


def create_feedback_notification(feedback, action, user=None, additional_message=""):
    """
    Create notifications for feedback actions
    """
    
    if action == 'submitted':
        # Notify heads, VCs, and admins about new feedback
        from users.models import User
        recipients = User.objects.filter(role__in=['head', 'vc', 'admin'])
        
        for recipient in recipients:
            message = f"New feedback has been submitted for complaint {feedback.complaint.complaint_number} - {feedback.rating} stars"
            if additional_message:
                message += f". {additional_message}"
            
            create_notification(
                recipient=recipient,
                message=message,
                title=f"New Feedback: {feedback.complaint.complaint_number}",
                notification_type='feedback_submitted',
                link=f'/feedback/{feedback.id}/',
                related_feedback_id=feedback.id,
            )
    
    elif action == 'response_added':
        # Notify the student about feedback response
        message = f"Management has responded to your feedback for complaint {feedback.complaint.complaint_number}"
        if user:
            message += f" by {user.full_name}"
        if additional_message:
            message += f". {additional_message}"
        
        create_notification(
            recipient=feedback.submitted_by,
            message=message,
            title=f"Feedback Response: {feedback.complaint.complaint_number}",
            notification_type='feedback_response',
            link=f'/feedback/{feedback.id}/',
            related_feedback_id=feedback.id,
        )


def mark_all_as_read(user):
    """Mark all notifications as read for a user"""
    from django.utils import timezone
    
    unread_notifications = Notification.objects.filter(
        recipient=user,
        is_read=False
    )
    
    unread_notifications.update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return unread_notifications.count()


def get_unread_count(user):
    """Get count of unread notifications for a user"""
    return Notification.objects.filter(
        recipient=user,
        is_read=False
    ).count()


def cleanup_old_notifications(days=90):
    """
    Clean up old notifications (older than specified days)
    This should be run as a periodic task
    """
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    old_notifications = Notification.objects.filter(
        created_at__lt=cutoff_date,
        is_read=True  # Only delete read notifications
    )
    
    count = old_notifications.count()
    old_notifications.delete()
    
    return count

