from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'is_superuser')
        extra_kwargs = {'password' : {'write_only': True, 'required': True}}

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # exclude = ('profile_token',)
        fields = ('id','profile_uuid', 'profile_token', 'imei', 'date_created', 'date_modified')
        extra_kwargs = {
            'profile_uuid' : {'read_only': True, 'required': True},
            'profile_token' : {'read_only': True},
            'date_created': {'read_only': True, 'required': True},
            'date_modified': {'read_only': True, 'required': True}
            }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class FactOrMythSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactOrMyth
        fields = '__all__'

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'

class TakePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakePart
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class JoinCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinCampaign
        fields = '__all__'
        extra_kwargs = {
            'profile' : {'read_only': True}
            }

class DonationCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCourse
        fields = '__all__'

class ChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champion
        fields = '__all__'

