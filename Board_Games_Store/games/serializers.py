from rest_framework import serializers
from .models import Game, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'founded']


class GameSerializer(serializers.ModelSerializer):
    publisher = serializers.CharField(source='publisher.name', read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'price', 'publisher', 'genre', 'players', 'duration']
