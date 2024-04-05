from django.contrib.auth.models import User

from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FriendRequest
from .serializers import UserSerializer
from .utils import get_friend_request_count


class ListFriendsAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        page = self.request.query_params.get('page', '0')
        page = int(page) if page.isdigit() else 0

        # Get the current user's accepted friend requests
        accepted_requests = FriendRequest.objects.filter(
            from_user=self.request.user, status='accepted'
        )[page*10:10+(page*10)]

        # Extract the to_user from the accepted friend requests
        friends = [friend_request.to_user for friend_request in accepted_requests]
        return friends


class ListPendingFriendsAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        page = self.request.query_params.get('page', '0')
        page = int(page) if page.isdigit() else 0

        # Get the current user's pending friend requests
        accepted_requests = FriendRequest.objects.filter(
            from_user=self.request.user, status='pending'
        )[page*10:10+(page*10)]

        # Extract the to_user from the accepted friend requests
        friends = [friend_request.to_user for friend_request in accepted_requests]
        return friends


class RequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    MAX_FRIEND_REQUEST_IN_MIN = 3

    def post(self, request, response_text):
        """
        Handles sending, accepting, and rejecting friend requests.
        :param request: HTTP request object
        :param response_text: Text indicating the action to perform ('sent', 'accepted', or 'rejected')
        :return: HTTP response indicating the status of the request
        """
        # Validate parameters
        email = request.data.get('email', '')
        if not email or response_text not in ['sent', 'accepted', 'rejected']:
            return Response(
                {"error": 'Please pass the valid parameter or url'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email__iexact=email, is_active=True)
        except User.DoesNotExist:
            return Response(
                {"error": f"{email} is not an active user in the platform"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure user exists and is active
        if not user:
            return Response(
                {"error": "Please pass the active user email"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request_count = get_friend_request_count(self.request.user)
        if request_count > self.MAX_FRIEND_REQUEST_IN_MIN:
            return Response(
                {"error": "Friend Requests limit reached for a min"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create or get the friend request based on the response_text
            param = {
                'from_user': request.user,
                'to_user': user,
                'status': 'pending'
            }
            action = (
                FriendRequest.objects.create
                if response_text == 'sent' else FriendRequest.objects.get
            )
            friend_request = action(**param)

        except Exception as e:
            return Response(
                {"error": "Friend request does not exist or has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update status if response_text indicates 'accepted' or 'rejected'
        if response_text in ['accepted', 'rejected']:
            friend_request.status = response_text
            friend_request.save()

        return Response(
            {"message": 'request processed successfully'},
            status=status.HTTP_200_OK
        )
