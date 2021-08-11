from django.urls import path, re_path, include
from .views import *
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/users', UserList)
router.register(r'api/profiles', ProfileList)
router.register(r'api/categories', CategoryList)
router.register(r'api/articles', ArticleList)
router.register(r'api/videos', VideoList)
router.register(r'api/documents', DocumentList)
router.register(r'api/factOrmyth', FactOrMythList)
router.register(r'api/take-part', TakePartList)
router.register(r'api/campaigns', CampaignList)
router.register(r'api/join-campaign', JoinCampaignList)
router.register(r'api/about', AboutList)
router.register(r'api/donation-courses', DonationCourseList)
router.register(r'api/champions', ChampionList)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('api/get/categories', views.get_categories, name='categories'),
    path('api/get/articles', views.get_articles, name='articles'),
    path('api/get/videos', views.get_videos, name='videos'),
    path('api/get/documents', views.get_documents, name='documents'),
    path('api/get/factOrmyth', views.get_factormyth, name='factOrmyth'),
    path('api/get/campaigns/list', views.get_campaigns, name='campaigns'),
    path('api/get/campaign', views.get_campaign, name='campaign'),
    path('api/get/donation-courses/list', views.get_courses, name='courses'),
    path('api/get/donation-course', views.get_course, name='course'),
    path('api/get/champions', views.get_champions, name='champions'),
]