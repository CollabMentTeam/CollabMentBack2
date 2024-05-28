from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Friendship, Job, JobApplication, Notification , Profile, ProfileView, Team
from rest_framework import generics
from .serializers import FriendshipSerializer, JobApplicationSerializer, JobSerializer, NotificationCreateSerializer, NotificationSerializer, ProfileSerializer, TeamSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404




from stream_chat import StreamChat


from .models import CustomUser
from .serializers import CustomUserSerializer


@csrf_exempt
def options(request, *args, **kwargs):
    response = JsonResponse({'message': 'OPTIONS request received'})
    response['Access-Control-Allow-Origin'] = '*' 
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    response['Access-Control-Max-Age'] = '86400'
    return response


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()  # Fetch all users from the database
        user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse(user_list, safe=False)

    elif request.method == 'POST':
        return JsonResponse({'message': 'POST request received'})

    response = JsonResponse({'message': 'Method not allowed'})
    response.status_code = 405 
    return response

@csrf_exempt
def user_detail(request, pk):
    if request.method == 'GET':
        return JsonResponse({'message': 'GET request received'})
    elif request.method == 'PUT':
        return JsonResponse({'message': 'PUT request received'})
    elif request.method == 'DELETE':
        return JsonResponse({'message': 'DELETE request received'})
    
    response = JsonResponse({'message': 'Method not allowed'})
    response.status_code = 405 
    return response

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  

        # Получаем токен пользователя из модели
        token = user.chat_token

        return Response({
            'message': 'Authentication successful',
            'token': token,
            'user_id': user.id,
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



User = get_user_model()

api_key = '5E8C08782F3DBC157E2A2E9802D629F20A16F2793D69311F8F64F4767072F5AE19BD6E0B614E9857FBF8B56744571859'
subject = 'Test Email'
body = 'This is a test email.'
to = ''

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Инициализация клиента Stream Chat
        chat_client = StreamChat(api_key="233vmgucsgte", api_secret="3qx3x8zp5enjcz9es34pdq2mxv8xuqnvv837745f4jag6c54wtmnsa84c62zfw4n")
        cleaned_username = "".join(user.username.split())
        # Добавление пользователя
        chat_client.update_user({"id": cleaned_username, "name": user.username})

        # Создание токена для пользователя
        token = chat_client.create_token(user.username)

        # Сохраняем токен в модели пользователя
        user.chat_token = token
        user.save()

        profile = Profile.objects.create(user=user)

        response_data = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'token': token,  # Возвращаем токен в ответе на успешную регистрацию
        }

        # if send_email(api_key, subject, body, user.email):
        #     print('Email was sent successfully.')
        # else:
        #     print('Email sending failed.')
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def send_email(api_key, subject, body, to):
    response = requests.post(
        'https://api.elasticemail.com/v2/email/send',
        data={
            'apikey': api_key,
            'subject': subject,
            'from': 'Test1',
            'fromName': 'Test2',
            'to': to,
            'bodyHtml': body,
        }
    )

    if response.status_code == 200:
        return True
    else:
        return False
    

class AddFriend(APIView):
    def post(self, request, *args, **kwargs):
        user_username = request.data.get('username')
        friend_username = request.data.get('friend_username')
        
        user = get_object_or_404(User, username=user_username)
        friend = get_object_or_404(User, username=friend_username)

        if user == friend:
            return Response({'error': 'Cannot add yourself as a friend'}, status=status.HTTP_400_BAD_REQUEST)

        if Friendship.objects.filter(user=user, friend=friend).exists():
            return Response({'error': 'Friendship already exists'}, status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.create(user=user, friend=friend)
        Friendship.objects.create(user=friend, friend=user)

        return Response({'message': 'Friend added successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def remove_friend(request, friend_id):
    try:
        friend = User.objects.get(pk=friend_id)
    except User.DoesNotExist:
        return Response({'error': 'Friend does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user

    if user == friend:
        return Response({'error': 'Cannot remove yourself from friends'}, status=status.HTTP_400_BAD_REQUEST)

    Friendship.objects.filter(user=user, friend=friend).delete()
    Friendship.objects.filter(user=friend, friend=user).delete()

    return Response({'message': 'Friend removed successfully'}, status=status.HTTP_204_NO_CONTENT)

class FriendList(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        friendships = Friendship.objects.filter(user=user)
        friend_ids = [friend.friend.id for friend in friendships]
        friends = User.objects.filter(id__in=friend_ids)
        serializer = CustomUserSerializer(friends, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

class MyProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class PersonalInfoUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserProfileAPIView(APIView):
    def get(self, request):
        username = request.query_params.get('username')

        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

class IncreaseProfileView(APIView):
    def post(self, request, *args, **kwargs):
        viewed_profile_username = request.data.get('viewed_profile_username')
        viewer_username = request.data.get('viewer_username')

        # Получаем пользователя, чей профиль просматривают
        viewed_profile = get_object_or_404(User, username=viewed_profile_username)

        # Получаем пользователя, который просматривает профиль
        viewer = get_object_or_404(User, username=viewer_username)

        # Создаем запись в модели ProfileView
        profile_view = ProfileView.objects.create(viewer=viewer, viewed_profile=viewed_profile)

        # Возвращаем успешный ответ
        return Response(status=status.HTTP_201_CREATED)
    

class ProfileViewsCount(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user = User.objects.get(username=username)
        profile_views_count = ProfileView.objects.filter(viewed_profile=user).count()
        return Response({'profile_views_count': profile_views_count})
    



class UserProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        return self.queryset.get(username=username)
    
# class UserProfileView(generics.RetrieveAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = ProfileSerializer

#     def get_object(self):
#         username = self.kwargs.get('username')
#         return self.queryset.get(username=username)
    
from django.http import Http404
from rest_framework.generics import RetrieveUpdateAPIView
from django.http import QueryDict


class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            return user
        except CustomUser.DoesNotExist:
            raise Http404("User not found.")

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Установка partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        print(username)
        try:
            profile = Profile.objects.get(user__username=username)
            print(profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404("Profile not found.")

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from .models import Post
from .serializers import PostSerializer

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        username = self.kwargs.get('username')
        author = User.objects.get(username=username)
        # Получаем профиль пользователя
        profile = author.profile
        serializer.save(author=author, profile=profile)

    

from rest_framework import generics, pagination

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
        
class UserPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Post.objects.filter(author__username=username)


class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def post(self, request, *args, **kwargs):
        # Получение имени пользователя из запроса
        username = request.data.get('creator')
        if username:
            try:
                # Поиск пользователя по имени пользователя
                creator = CustomUser.objects.get(username=username)
                # Замена имени пользователя на его ID в запросе
                request.data['creator'] = creator.id
            except CustomUser.DoesNotExist:
                # Обработка случая, когда пользователь с указанным именем не найден
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Создание экземпляра сериализатора с данными из запроса
        serializer = self.serializer_class(data=request.data)
        # Проверка валидности данных
        if serializer.is_valid():
            # Сохранение данных
            serializer.save()
            # Возвращение успешного ответа с данными созданного объекта и статусом 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Возвращение ответа с информацией об ошибках в данных и статусом 400 Bad Request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from django.db.models import F, ExpressionWrapper, DateField, Subquery, OuterRef

class TeamListAPIView(generics.ListAPIView):
    serializer_class = TeamSerializer

    def get_queryset(self):
        # Аннотируем запрос для получения списка имен пользователей
        queryset = Team.objects.annotate(
            creator_last_login_date=ExpressionWrapper(
                F('creator__last_login'),
                output_field=DateField()
            ),
            # Возвращает список имен пользователей для каждой команды
            usernames=Subquery(
                CustomUser.objects.filter(teams=OuterRef('pk')).values('username')
            )
        ).all()
        return queryset

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            # Находим пользователя по его имени пользователя (username)
            user = User.objects.get(username=username)
            # Фильтруем уведомления по пользователю
            return Notification.objects.filter(user=user)
        else:
            # Если параметр username не указан, возвращаем пустой queryset
            return Notification.objects.none()
        

class NotificationCreateAPIView(generics.CreateAPIView):
    serializer_class = NotificationCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NotificationDeleteAPIView(generics.DestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.db.models import Count

class JobListAPIView(generics.ListCreateAPIView):
    queryset = Job.objects.annotate(applications_count=Count('applications'))
    serializer_class = JobSerializer


class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobApplicationListAPIView(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class JobApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)

class JobApplicationListCreateAPIView(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            job_application = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error('Некорректные данные при создании отклика на вакансию: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
