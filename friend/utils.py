
from datetime import datetime, timedelta

from friend.models import FriendRequest


def get_friend_request_count(user):
    """
    Count the num of requests the user has send in the last minute
    :param user: The user for whom to check the pending friend requests
    :return: Count of friend request sent
    """

    # Calculate the timestamp for 1 minute ago
    last_1_min = datetime.today() - timedelta(minutes=1)

    # Count the number of pending friend requests from the user within the
    # last minute
    request_count = FriendRequest.objects.filter(
        from_user=user, status='pending', created_on__gte=last_1_min
    ).count()

    return request_count


def get_name_from_email(email):
    # Split email address at '@' symbol
    parts = email.split('@')
    if len(parts) != 2:
        return None  # Return None if email format is invalid

    # Get the part before '@'
    name_part = parts[0]

    # Split the name part at '.'
    name_parts = name_part.split('.')
    first_name = ''
    last_name = ''

    if len(name_parts) > 0:
        first_name = name_parts[0].capitalize()

    if len(name_parts) > 1:
        last_name = name_parts[1].capitalize()

    return first_name, last_name


