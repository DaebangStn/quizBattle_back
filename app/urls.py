from django.urls import path, include
from app.views.userViews import RegisterUser, \
    user_list, user_detail
from app.views.roomViews import room_create, RoomStart, \
    room_list, room_detail
from app.views.authViews import CustomAuthToken


urlpatterns = [
    path('signin/', CustomAuthToken.as_view()),
    path('signup/', RegisterUser.as_view()),
    path('user/detail/', user_detail),
    path('user/list/', user_list),
    path('room/create/', room_create),
    path('room/list/', room_list),
    path('room/<slug:slug>/', room_detail),
    path('room/<slug:slug>/start/', RoomStart.as_view()),
]
