
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friend.serializers import UserSerializer


@api_view(['POST'])
def signup(request):
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    # Validate if email and password are provided
    if not email or not password:
        return Response(
            {"error": "Please provide both email and password."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Check if the user with the provided email already exists
        email = serializer.validated_data['email']
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email', '')
    password = request.data.get('password', '')

    # Validate if email and password are provided
    if not email or not password:
        return Response(
            {"error": "Please provide both email and password."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate user with case-insensitive email
    user = authenticate(request, username=email.lower(), password=password)

    # Check if authentication is successful
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        page = self.request.query_params.get('page', '0')
        page = int(page) if page.isdigit() else 0

        filter_query = []
        if query:
            # Perform exact search by email or partial search by name
            filter_query = [
                Q(email=query) | Q(first_name__icontains=query)
                | Q(first_name__icontains=query)
            ]
        return User.objects.filter(*filter_query)[page*10:10+(page*10)]
