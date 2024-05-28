from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Friendship, Job, JobApplication, Notification, Profile, Post, Team, CustomUser

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class ProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user', 'professional_field', 'education', 'current_job', 'experience',
            'location', 'personal_qualities', 'certificates', 'resume',
            'profile_photo', 'education_date', 'name_institution', 
            'desired_position', 'type_of_work', 'operating_mode', 
            'name_organization', 'position', 'experience_name', 'citizenship', 
            'city', 'passage_time'
        ]

class ProfileSerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'professional_field', 'education', 'current_job', 'experience', 
            'location', 'personal_qualities', 'certificates', 'resume', 
            'profile_photo', 'education_date', 'name_institution', 
            'desired_position', 'type_of_work', 'operating_mode', 
            'name_organization', 'position', 'experience_name', 'citizenship', 
            'city', 'passage_time'
        ]

class CustomUserSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    profile = ProfileSerializerForUser(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'email', 'phone_number', 'friends', 
            'birthday', 'gender', 'user_type', 'first_name', 'last_name', 
            'instagram', 'telegram', 'website', 'profile'
        ]
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = get_user_model().objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def get_friends(self, obj):
        friends = Friendship.objects.filter(user=obj)
        friend_ids = [friend.friend.id for friend in friends]
        friend_users = CustomUser.objects.filter(id__in=friend_ids)
        return SimpleUserSerializer(friend_users, many=True).data

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1  # Ограничиваем глубину сериализации до 1 уровня

    def get_author(self, obj):
        # Получаем данные автора поста
        author = obj.author
        return {
            'id': author.id,
            'username': author.username,
            'email': author.email,
            'phone_number': author.phone_number,
            'first_name': author.first_name,
            'last_name': author.last_name,
            'user_type': author.user_type
        }

    def get_profile(self, obj):
        # Получаем данные профиля автора поста
        profile = obj.author.profile
        serializer = ProfileSerializer(profile)
        return serializer.data
    

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'
        
class LastLoginDateField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.date()
        return None

class TeamSerializer(serializers.ModelSerializer):
    creator_last_login_date = LastLoginDateField(source='creator.last_login', read_only=True)
    members = serializers.SerializerMethodField()

    def get_members(self, obj):
        # Получаем список имен пользователей из списка members
        return [member.username for member in obj.members.all()]

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'creator', 'creator_last_login_date', 'investment_amount_needed', 'members', 'image' , 'join_code' , 'contactEmail', 'contactPhone']

    def create(self, validated_data):
        creator_username = validated_data.pop('creator')
        creator = CustomUser.objects.get(username=creator_username)
        team = Team.objects.create(creator=creator, **validated_data)
        return team

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'link', 'timestamp']

class NotificationCreateSerializer(serializers.Serializer):
    usernames = serializers.ListField(child=serializers.CharField())
    message = serializers.CharField()
    link = serializers.CharField(required=False)

    def create(self, validated_data):
        usernames = validated_data.get('usernames')
        message = validated_data.get('message')
        link = validated_data.get('link')

        # Получаем пользователей по именам
        users = CustomUser.objects.filter(username__in=usernames)

        # Создаем и сохраняем уведомление для каждого пользователя
        for user in users:
            Notification.objects.create(
                user=user,
                message=message,
                link=link
            )
        return validated_data

        
class JobSerializer(serializers.ModelSerializer):
    applications_count = serializers.IntegerField()  # добавляем это поле

    class Meta:
        model = Job
        fields = ['id', 'position', 'company_name', 'experience', 'publish_date', 'location', 'job_type', 'description', 'salary', 'applications_count']


class JobApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'username', 'cv']

    def validate_username(self, value):
        try:
            CustomUser.objects.get(username=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с указанным именем не найден.")
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        user = CustomUser.objects.get(username=username)
        job_application = JobApplication.objects.create(user=user, **validated_data)
        return job_application
