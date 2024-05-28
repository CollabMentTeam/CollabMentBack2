from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Phone Number')
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='related_friends')
    
    # Поле для хранения токена чата
    chat_token = models.CharField(max_length=200, blank=True, null=True)

    # Доп поля для настроек
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    user_type = models.CharField(max_length=20, blank=True, null=True, choices=[('Job Seeker', 'Job Seeker'), ('Employer', 'Employer')])
    instagram = models.CharField(max_length=100, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
    
def user_directory_path(instance, filename):
    return f'media/profile_files/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    professional_field = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    education_date = models.CharField(max_length=100, blank=True, null=True)
    name_institution = models.CharField(max_length=100, blank=True, null=True)

    desired_position = models.CharField(max_length=100, blank=True, null=True)
    type_of_work = models.CharField(max_length=100, blank=True, null=True)
    operating_mode = models.CharField(max_length=100, blank=True, null=True)
    name_organization = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)

    current_job = models.CharField(max_length=100, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    experience_name = models.CharField(max_length=100, blank=True, null=True)
    citizenship = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    passage_time = models.CharField(max_length=100, blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=True)
    personal_qualities = models.TextField(blank=True, null=True)
    certificates = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    resume = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class ProfileView(models.Model):
    viewer = models.ForeignKey(CustomUser, related_name='viewed_profiles', on_delete=models.CASCADE)
    viewed_profile = models.ForeignKey(CustomUser, related_name='profile_views', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.viewer.username} viewed profile of {self.viewed_profile.username} at {self.viewed_at}'
    
class Friendship(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_friendships')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend_friendships')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'friend']


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.author.username}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Repost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

def user_directory_pathForTeam(instance, filename):
    return f'media/profile_files/user_{instance.creator.id}/{filename}'

class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    members = models.ManyToManyField(CustomUser, related_name='teams')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    investment_amount_needed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    join_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to=user_directory_pathForTeam, blank=True, null=True)

    contactEmail = models.EmailField(blank=True, null=True)
    contactPhone = models.CharField(max_length=15, blank=True, null=True)
    contactAddress = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def join_team(cls, join_code, user):
        """
        Метод для вступления пользователя в команду по коду
        """
        try:
            team = cls.objects.get(join_code=join_code)
            team.members.add(user)
            return True
        except cls.DoesNotExist:
            return False


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.message}'


class Job(models.Model):
    POSITION_CHOICES = [
        ('Position 1', 'Position 1'),
        ('Position 2', 'Position 2'),
        # Добавьте другие варианты должностей здесь
    ]

    EXPERIENCE_CHOICES = [
        ('1 year', '1 year'),
        ('1-2 years', '1-2 years'),
        ('3-5 years', '3-5 years'),
        ('5+ years', '5+ years'),
        # Добавьте другие варианты опыта работы здесь
    ]

    position = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    publish_date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    description = models.TextField()
    salary = models.CharField(max_length=50)

    def __str__(self):
        return self.position
    
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_applications')
    cv = models.FileField(upload_to='job_applications_cv/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.job.position}'