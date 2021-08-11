from django.shortcuts import render
import datetime
from django.core import serializers
from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# from .otp import generate_random_otp, get_otp_phone_number, is_otp_expired
# from .code_location import code_location, get_distance, get_duration, get_client_ip
# import requests as req

# Create your views here.
class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileList(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request):
        print(request.data)

        serializer = ProfileSerializer(data=request.data)
        
        
        if serializer.is_valid():
            # print(serializer.validated_data)
            profile =serializer.save()
            # print(profile.id)
            token = Profile.encode_auth_token(Profile, profile.id, request.data)
            # print(token)
            # print(type(profile))
            profile.profile_token = token
            # serializer.data[]
            profile.save()

            # print(serializer.data)
            # return Response(serializer.data['profile_token'], status=status.HTTP_201_CREATED)
            return JsonResponse({'status':True, 'message':'user sucessfully created', 'session_token': serializer.data['profile_token']})
    
        # print(serializer.data['imei'])
        try:
            profile = Profile.objects.get(imei=serializer.data['imei'])
        # print(profile)
            if profile:
                return JsonResponse({'status':True, 'message':'user already exists', 'session_token': profile.profile_token})
        except Exception as e:  
            return JsonResponse({'status':False, 'message':'Invalid data'})


class CategoryList(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# receives a session_token
@api_view(['POST'])
def get_categories(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = Category.objects.all()
            serializer = CategorySerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'categories': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object) 

class ArticleList(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# receives a session_token $ category_id
@api_view(['POST'])
def get_articles(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)
    category_id = request.data['category_id']

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token and category_id:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            # rider_id = resp
            # result = Request.objects.filter(rider=rider_id).exclude(status='Completed')
            result = Article.objects.filter(category=category_id)
            serializer = ArticleSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'articles': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token or a valid category_id.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object) 

class VideoList(viewsets.ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class = VideoSerializer

# receives a session_token
@api_view(['POST'])
def get_videos(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = Videos.objects.all()
            serializer = VideoSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'videos': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object) 

class DocumentList(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# receives a session_token
@api_view(['POST'])
def get_documents(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = Document.objects.all()
            serializer = DocumentSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'documents': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object)

class FactOrMythList(viewsets.ModelViewSet):
    queryset = FactOrMyth.objects.all()
    serializer_class = FactOrMythSerializer

    # receives a session_token
@api_view(['POST'])
def get_factormyth(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = FactOrMyth.objects.all()
            serializer = FactOrMythSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'results': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object)

class AboutList(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class TakePartList(viewsets.ModelViewSet):
    queryset = TakePart.objects.all()
    serializer_class = TakePartSerializer

class CampaignList(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    # receives a session_token
@api_view(['POST'])
def get_campaigns(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = Campaign.objects.all()
            serializer = CampaignSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'campaigns': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object)

    # receives a session_token & campaign_id
@api_view(['POST'])
def get_campaign(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)
    campaign_id = request.data['campaign_id']

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = Campaign.objects.filter(id=campaign_id)
            serializer = CampaignSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'campaign': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object)

class JoinCampaignList(viewsets.ModelViewSet):
    queryset = JoinCampaign.objects.all()
    serializer_class = JoinCampaignSerializer

    def create(self, request):
        print(request.data)

        serializer = JoinCampaignSerializer(data=request.data)
        token = request.headers.get('Authorization')
        # ip = get_client_ip(request)

        if token:
            session_token = token.split(" ")[1]
        else:
            session_token = ''

        if session_token:
            print(session_token)
            resp = Profile.decode_auth_token(session_token, request)

            if isinstance(resp, int):
                profile_id = resp

                if serializer.is_valid():
                    # print(serializer.validated_data)
                    join_data =serializer.save()
                    join_data.profile = profile_id
                    join_data.save()
                    
                    return JsonResponse({'status':True, 'message':'user sucessfully created'})
                return JsonResponse({'status':False, 'message':'Invalid data'})

            response_object = {'status':False, 'message':resp}
            # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
            return JsonResponse(response_object)

        response_object = {'status':False, 'message':'Provide a valid session token.'}
        # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

class DonationCourseList(viewsets.ModelViewSet):
    queryset = DonationCourse.objects.all()
    serializer_class = DonationCourseSerializer

      # receives a session_token
@api_view(['POST'])
def get_courses(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = DonationCourse.objects.all()
            serializer = DonationCourseSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'courses': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object)

    # receives a session_token & course_id
@api_view(['POST'])
def get_course(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)
    course_id = request.data['course_id']

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = DonationCourse.objects.filter(id=course_id)
            serializer = DonationCourseSerializer(result, many=True)
            data = serializer.data

            donations = Donation.objects.filter(donation_course=course_id)
            total_amount=0

            for donation in donations:
                amount = donation['amount']
                total_amount += amount


            return JsonResponse({'status':True, 'message':'OK', 'course': data, 'total_amount':total_amount})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object)

class ChampionList(viewsets.ModelViewSet):
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer

    
    # receives a session_token & category_id
@api_view(['POST'])
def get_champions(request):
    token = request.headers.get('Authorization')
    # ip = get_client_ip(request)
    category_id = request.data['category_id']

    if token:
        session_token = token.split(" ")[1]
    else:
        session_token = ''

    if session_token:
        print(session_token)
        resp = Profile.decode_auth_token(session_token, request)

        if isinstance(resp, int):
            result = Champion.objects.filter(category=category_id)
            serializer = ChampionSerializer(result, many=True)
            data = serializer.data
            return JsonResponse({'status':True, 'message':'OK', 'champions': data})

        response_object = {'status':False, 'message':resp}
        # logger.critical(f'[{ip}] - {resp} - Payload-token: {session_token} -Response: {response_object}')
        return JsonResponse(response_object)

    response_object = {'status':False, 'message':'Provide a valid session token.'}
    # logger.critical(f'[{ip}] - Wrong token - Payload-token: {session_token} -Response: {response_object}')
    return JsonResponse(response_object)
