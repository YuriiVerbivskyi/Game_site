from django.urls import path
from games.views import GameDetail, GameList, PublisherList, PublisherDetail, RegisterView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("games/", GameList.as_view(), name="game-list"),
    path("games/<int:pk>/", GameDetail.as_view(), name="game-detail"),
    path("publishers/", PublisherList.as_view(), name="publisher-list"),
    path("publishers/<int:pk>/", PublisherDetail.as_view(), name="publisher-detail"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair")
]
