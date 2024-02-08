from .models import CustomerUser
from datetime import timedelta
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_active_users():
    # Set the threshold for considering a session as active (e.g., 15 minutes)
    threshold = timezone.now() - timedelta(seconds=15)

    # Query active sessions
    active_sessions = Session.objects.filter(expire_date__gt=threshold)
    print(active_sessions)
    # Extract user IDs from active sessions
    user_ids = [int(session.get_decoded().get('_auth_user_id')) for session in active_sessions]
    print(user_ids)
    # Query User model to get user objects
    active_users = CustomerUser.objects.filter(id__in=user_ids)

    return active_users

def remove_user_session(user):
    # Get the session associated with the user
    sessions = Session.objects.filter(session_key__in=user.session_key)
    
    # Delete the sessions
    sessions.delete()