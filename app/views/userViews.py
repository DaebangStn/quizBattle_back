from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from app.serializers.userSerializers import CreateUserSerializer


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
