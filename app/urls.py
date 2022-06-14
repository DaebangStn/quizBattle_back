from django.urls import path, include
from app.views.userViews import RegisterUser, \
    user_list, user_detail
from app.views.roomViews import room_create, RoomStart, \
    room_list, room_detail, room_available
from app.views.authViews import CustomAuthToken


urlpatterns = [
    path('signin/', CustomAuthToken.as_view()),
    path('signup/', RegisterUser.as_view()),
    path('password/reset/', include('django_rest_passwordreset.urls'), name='password_reset'),
    path('user/detail/', user_detail),
    path('user/list/', user_list),
    path('room/create/', room_create),
    path('room/list/', room_list),
    path('room/available/', room_available),
    path('room/<str:slug>/', room_detail),
    path('room/<str:slug>/start/', RoomStart.as_view()),
]
