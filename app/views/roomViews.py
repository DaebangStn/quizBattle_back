from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from app.serializers.roomSerializers import CreateRoomSerializer, \
    ListRoomSerializer, RetrieveRoomSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, api_view, permission_classes
from app.models.room import Room
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class IsHost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.host.id == request.user.id
        else:
            return False


class IsParticipants(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.participants.filter(id=request.user.id).exists()
        else:
            return False


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def room_create(request):
    name = request.data.get('name', None)
    if name is None:
        body = {
            "message": "[name] of quiz room is empty, please submit"
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

    participants_username = request.data.get('participants_username', None)
    if participants_username is None:
        body = {
            "message": "[participants_username] of quiz room is empty, please submit"
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

    data = {
        "name": name,
        "host_username": request.user.username,
        "participants_username": participants_username.split(",")
    }

    serializer = CreateRoomSerializer(data=data)
    if not serializer.is_valid():
        body = {"message": serializer.errors}
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

    room = serializer.save()
    body = {
        "slug": room.slug,
    }

    return Response(body, status=status.HTTP_201_CREATED)


class RoomStart(generics.GenericAPIView):
    queryset = Room.objects.all()
    permission_classes = [IsHost]

    def get(self, request, slug=None):
        room = self.get_object(slug)

        if room.round > 0:
            body = {"message": "quiz room is already started"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        else:
            if room.submit_answer(room.answer):
                body = {"message": "quiz room is now started, going next round"}
                return Response(body, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, slug=None):
        queryset = self.get_queryset()
        room = get_object_or_404(queryset, slug=slug)
        self.check_object_permissions(self.request, room)
        return room


class RoomViewSet(viewsets.ViewSet):
    def get_object(self, slug=None):
        queryset = Room.objects.all()
        room = get_object_or_404(queryset, slug=slug)
        self.check_object_permissions(self.request, room)
        return room

    def list(self, request):
        queryset = Room.objects.all()
        serializer = ListRoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        room = self.get_object(slug)
        serializer = RetrieveRoomSerializer(room)
        return Response(serializer.data)

    def update(self, request, slug=None):
        room = self.get_object(slug)
        answer = request.data.get('answer', None)
        if answer is None:
            body = {"message": "answer is empty, please submit"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        if room.submit_answer(int(answer)):
            body = {"message": "answer is correct, going next round"}
            return Response(body, status=status.HTTP_202_ACCEPTED)
        else:
            body = {"message": "answer is incorrect"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug=None):
        room = self.get_object(slug)
        name = room.name
        room.delete()
        body = {"message": "room [{}] is deleted".format(name)}
        return Response(body, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def modify(self, request, slug=None):
        room = self.get_object(slug)
        _type = request.data.get('type', None)
        _participants_username = request.data.get('participants_username', None)

        if (_type is None) and (_participants_username is None):
            body = {"message": "[type] and [participants_username] of quiz room is empty, please submit"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        if _type is not None:
            room.type = _type
            room.round = 0

        if _participants_username is not None:
            room.participants.clear()
            room.participants.add(request.user)
            for username in _participants_username.split(","):
                participant = User.objects.get(username=username)
                room.participants.add(participant)

        room.save()
        serializer = RetrieveRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def list_available(self, request):
        user = request.user
        serializer = ListRoomSerializer(user.room_participants.all(), many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            permissions_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permissions_classes = [IsParticipants]
        elif self.action == 'update':
            permissions_classes = [IsParticipants]
        elif self.action == 'modify':
            permissions_classes = [IsHost]
        elif self.action == 'list_available':
            permissions_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permissions_classes = [IsHost]
        else:
            permissions_classes = [IsAdminUser]

        return [permission() for permission in permissions_classes]


room_list = RoomViewSet.as_view({'get': 'list'})
room_detail = RoomViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'put': 'modify',
    'delete': 'destroy'
})
room_available = RoomViewSet.as_view({'get': 'list_available'})