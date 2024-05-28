from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Job, JobApplication, Notification, Profile, Friendship, Post, Like, ProfileView, Repost, Comment, Team

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['professional_field', 'education', 'current_job', 'experience', 'location', 'personal_qualities', 'certificates', 'resume', 'profile_photo' , 'education_date' , 'name_institution', 'desired_position' , 'type_of_work', 'operating_mode' , 'name_organization', 'position', 'experience_name', 'citizenship', 'city' ]
    extra = 0

class FriendshipInline(admin.TabularInline):
    model = Friendship
    fk_name = 'user'

class PostsInline(admin.TabularInline):
    model = Post
    fk_name = 'author'

class ProfileViewInline(admin.TabularInline):
    model = ProfileView
    fk_name = 'viewed_profile'
    extra = 0

class TeamVieWInline(admin.TabularInline):
    model = Team
    fk_name = 'creator'

class NotificationInline(admin.TabularInline):
    model = Notification
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'chat_token', 'birthday', 'gender', 'user_type' , 'instagram', 'telegram', 'website')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone_number'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff' , 'profile_views_count' )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    inlines = [ProfileInline, FriendshipInline, PostsInline, ProfileViewInline,TeamVieWInline , NotificationInline]

    def profile_views_count(self, obj):
        return obj.profile_views.count()

class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = 'post'

class LikeInline(admin.TabularInline):
    model = Like
    fk_name = 'post'

class RepostInline(admin.TabularInline):
    model = Repost
    fk_name = 'post'


class PostAdmin(admin.ModelAdmin):
    list_filter = ('author', 'created_at')
    
    inlines = [CommentInline, LikeInline, RepostInline]

admin.site.register(Post,PostAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Team)
admin.site.register(Notification)
admin.site.register(Job)
admin.site.register(JobApplication)