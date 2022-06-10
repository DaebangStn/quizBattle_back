from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from app.serializers.userSerializers import CreateUserSerializer, \
    UserBriefSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class RegisterUser(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if request.auth is not None:
            body = {"message": "logout first"}
            return Response(body, status=status.HTTP_403_FORBIDDEN)

        if len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            body = {"message": serializer.errors}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        body = {
            "username": user.username,
            "token": token.key
        }
        return Response(body, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserBriefSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            permissions_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permissions_classes = [IsAuthenticated]
        else:
            permissions_classes = [IsAdminUser]

        return [permission() for permission in permissions_classes]


user_list = UserViewSet.as_view({"get": "list"})
user_detail = UserViewSet.as_view({"get": "retrieve"})
