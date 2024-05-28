from django.urls import path
from .views import AddFriend, FriendList, IncreaseProfileView, JobApplicationDetailAPIView, JobApplicationListAPIView, JobApplicationListCreateAPIView, JobDetailAPIView, JobListAPIView, NotificationCreateAPIView, NotificationDeleteAPIView, NotificationListAPIView, ProfileViewsCount, TeamListAPIView, TeamListCreateAPIView, user_list, user_detail, options, login_user, register_user, remove_friend, all_users
from .views import MyProfileUpdateAPIView, PersonalInfoUpdateAPIView, UserProfileAPIView, UserProfileView, UserProfileUpdateAPIView, ProfileUpdateAPIView, PostCreateAPIView, PostListAPIView, UserPostListAPIView


urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('options/', options, name='options'),
    path('login', login_user, name='login'),
    path('register', register_user, name='register_user'),




    # path('users/<int:user_id>/friends/', user_friends, name='user-friends'),
    path('api/my-profile/', MyProfileUpdateAPIView.as_view(), name='my-profile-update'),
    path('api/personal-info/', PersonalInfoUpdateAPIView.as_view(), name='personal-info-update'),

    path('user/profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('user/profiles/<str:username>/', UserProfileView.as_view(), name='user-profile'),

    path('user/profile/update/<str:username>/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
    path('profile/update/<str:username>/', ProfileUpdateAPIView.as_view(), name='profile-update'),

    path('posts/user/<str:username>/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/all/', PostListAPIView.as_view(), name='post-list'),
    path('posts/user/<str:username>/', UserPostListAPIView.as_view(), name='user-post-list'),

    path('profile/view/increase/', IncreaseProfileView.as_view(), name='increase-profile-view'),
    path('profile/views/count/<str:username>/', ProfileViewsCount.as_view(), name='profile-views-count'),

    path('all_users/', all_users, name='all-users'),
    path('friend/add/', AddFriend.as_view(), name='add-friend'),
    path('friend/remove/<int:friend_id>/', remove_friend, name='remove-friend'),
    path('friend/list/<str:username>/', FriendList.as_view(), name='friend-list'),


    path('teams/', TeamListCreateAPIView.as_view(), name='team-list-create'),
    path('teams/list/', TeamListAPIView.as_view(), name='team-list'),

    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),

    path('jobs/', JobListAPIView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailAPIView.as_view(), name='job-detail'),

    path('applications/', JobApplicationListAPIView.as_view(), name='job-application-list'),
    path('applications/<int:pk>/', JobApplicationDetailAPIView.as_view(), name='job-application-detail'),
    path('job-applications/', JobApplicationListCreateAPIView.as_view(), name='job-applications'),


    path('create-notification/', NotificationCreateAPIView.as_view(), name='create-notification'),

    path('notifications/<int:id>/', NotificationDeleteAPIView.as_view(), name='notification-delete'),

]
