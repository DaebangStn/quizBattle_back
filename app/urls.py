from django.urls import path, include
from rest_framework.authtoken import views as auth_token
from app.views.userViews import RegisterUser
from app.views.roomViews import room_create, RoomStart, room_list, room_detail


urlpatterns = [
    path('login/', auth_token.obtain_auth_token),
    path('signup/', RegisterUser.as_view()),
    path('room/create/', room_create),
    path('room/list/', room_list),
    path('room/<slug:slug>/', room_detail),
    path('room/<slug:slug>/start/', RoomStart.as_view()),
]
