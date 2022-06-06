from rest_framework import serializers
from app.models.room import Room
from app.serializers.userSerializers import UserNameSerializer
from django.utils.text import slugify
from django.contrib.auth.models import User


class CreateRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    host_username = serializers.CharField(max_length=150)
    participants_username = serializers.ListField(
        child=serializers.CharField(max_length=150)
    )

    def create(self, validated_data):
        name = validated_data['name']
        slug = slugify(name)
        host = User.objects.get(username=validated_data['host_username'])
        room = Room.objects.create(
            name=name,
            slug=slug,
            host=host
        )

        room.participants.add(host)
        for username in validated_data['participants_username']:
            participant = User.objects.get(username=username)
            room.participants.add(participant)

        return room

    def update(self, instance, validated_data):
        pass


class ListRoomSerializer(serializers.ModelSerializer):
    host = UserNameSerializer(read_only=True)
    participants = UserNameSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['name', 'slug', 'host', 'participants', 'type']


class RetrieveRoomSerializer(serializers.ModelSerializer):
    host = UserNameSerializer(read_only=True)
    participants = UserNameSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['name', 'slug', 'host', 'participants', 'type', 'round', 'quiz', 'choices']
