from rest_framework import generics, permissions, response, status
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import UserSerializer


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response.Response({
                "user": UserSerializer(user).data,
                "message": "User Created Successfully."
            }, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return response.Response({
                "user": UserSerializer(user).data,
                "message": "User Logged In Successfully."
            }, status=status.HTTP_200_OK)
        return response.Response({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
