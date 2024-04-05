from django.contrib.auth.models import User
from rest_framework import serializers

from friend.models import FriendRequest
from friend.utils import get_name_from_email


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']

    def create(self, validated_data):
        # So that we can use django User model with unique username constraints
        validated_data['username'] = validated_data['email']

        name = get_name_from_email(validated_data['email'])
        validated_data['first_name'] = name[0]
        validated_data['last_name'] = name[1]

        return super().create(validated_data)
