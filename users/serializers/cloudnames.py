from rest_framework import serializers

# models
from users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'avatar',
            'bio',
            'link'
        )

