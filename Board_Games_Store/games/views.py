from django.http import Http404
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Game, Publisher
from .serializers import GameSerializer, PublisherSerializer
import logging

logger = logging.getLogger(__name__)


class PublisherList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        serializer = PublisherSerializer(Publisher.objects.all(), many=True)
        logger.info("Publisher list viewed")
        return Response(serializer.data)

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Publisher created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Failed to create publisher")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublisherDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Publisher.objects.get(pk=pk)
        except Publisher.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        return Response(PublisherSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = PublisherSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Publisher updated")
            return Response(serializer.data)
        logger.warning("Failed to update publisher")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        serializer = GameSerializer(Game.objects.all(), many=True)
        logger.info("Game list viewed")
        return Response(serializer.data)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Game created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Failed to create game")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        return Response(GameSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = GameSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Game updated")
            return Response(serializer.data)
        logger.warning("Failed to update game")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("User registered")
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        logger.warning("Registration failed")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Enter username and password"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.warning("Login failed: user not found")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            logger.warning("Login failed: wrong password")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        logger.info("User logged in")
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        RefreshToken(request.data.get("refresh")).blacklist()
        logger.info("User logged out")
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
