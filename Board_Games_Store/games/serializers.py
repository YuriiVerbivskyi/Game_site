from django.contrib.auth.models import User
from .models import Game, Publisher
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_check')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({"password_check": "Паролі не збігаються."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Ця електронна пошта вже використовується."})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Це ім'я користувача вже зайняте."})

        return data

    def create(self, validated_data):
        validated_data.pop('password_check')
        user = User.objects.create_user(**validated_data)
        return user

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'founded']

class GameSerializer(serializers.ModelSerializer):
    publisher = serializers.CharField(source='publisher.name', read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'price', 'publisher', 'genre', 'players', 'duration']