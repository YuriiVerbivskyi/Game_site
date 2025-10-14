from django.urls import path
from games.views import GameDetail, GameList, PublisherList, PublisherDetail

urlpatterns = [
    path("", GameList.as_view(), name="game-list"),
    path("games/<int:pk>/", GameDetail.as_view(), name="game-detail"),
    path("publishers/", PublisherList.as_view(), name="publisher-list"),
    path("publishers/<int:pk>/", PublisherDetail.as_view(), name="publisher-detail"),
]