from django.db import models
from django.db.models import CharField, TextField
from django.contrib.auth.models import User
import uuid
# from django_mysql.models import JSONField, ListTextField
import datetime
import jwt
# from .otp import generate_random_otp
from ywca.settings import SECRET_KEY
# from base import *
from ckeditor.fields import RichTextField

key = SECRET_KEY

class Profile(models.Model):
    imei = models.CharField(max_length=255, unique=True)
    profile_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    profile_token = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def encode_auth_token(self, profile_id, request=None):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
                # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': profile_id,
                "token_type":"access",
            }
        return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )

    @staticmethod  
    def decode_auth_token(session_token, request=None):
        """
        Decodes the auth token
        :param auth_token:
        :return: string
        """
        try:
            payload = jwt.decode(session_token, key, algorithms=["HS256"])
            print(payload)
            # is_blacklisted_token = BlackList.objects.filter(token=session_token)
            if payload:
                return payload['sub']
                # response = 'Token blacklisted. Please log in again.'

                #  log blacklisted token
                # critical_logger.critical(f'[{request.remote_addr}] - {__name__}.decode_auth_token() - Decode blacklisted token failure - Payload token: {auth_token} - Response: {response}')

            #     return response
            # else:
                # if payload['token_type'] and payload['unique'] and not payload['jti']:
                #     response = 'Invalid token. Please log in again.'
                #     return response
                
        except jwt.ExpiredSignatureError:
            response = 'Signature expired. Please log in again.'

            #  log expired token 
            # critical_logger.critical(f'[{request.remote_addr}] - {__name__}.decode_auth_token() - Decode expired token failure - Payload token: {auth_token} - Response: {response}')

            return response
        except jwt.InvalidTokenError:
            response = 'Invalid token. Please log in again.'

            #  log invalid token
            # critical_logger.critical(f'[{request.remote_addr}] - {__name__}.decode_auth_token() - Decode invalid token failure - Payload token: {auth_token} - Response: {response}')
            
            return response

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    desc = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
       return f'{self.title}'


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True, null=True)
    # article_url = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to = 'articles/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Champion(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    avatar_url = models.ImageField(upload_to = 'champions/')
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Videos(models.Model):
    caption = models.CharField(max_length=255)
    video_url =models.FileField(upload_to='videos/')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Document(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class FactOrMyth(models.Model):
    STATUSES_CHOICES = (
        ('Myth', 'Myth'),
        ('Fact', 'Fact'),
    )
    statement = models.TextField()
    status = models.CharField(max_length=25, choices=STATUSES_CHOICES)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class DonationCourse(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    target_amount = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
class Donation(models.Model):
    msisdn =  models.BigIntegerField()
    business_number = models.CharField(max_length=30)
    receipt_number = models.CharField(max_length=60)
    account_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    customer_name = models.CharField(max_length=50)
    org_balance = models.DecimalField(max_digits=6, decimal_places=2)
    donation_course = models.ForeignKey(DonationCourse, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class CheckOutRequest(models.Model):
    CHOICES = (
        ('New', 'New'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
        ('Success', 'Success'),
    )
    msisdn =  models.BigIntegerField()
    customer_name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_id = models.CharField(max_length=50)
    overall_status = models.CharField(max_length=25, choices=CHOICES)
    status_history = models.TextField()
    merchant_requestid = models.CharField(max_length=100)
    checkout_requestid = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Question(models.Model):
    quiz = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,)
    comment = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class About(models.Model):
    desc = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    image_url = models.ImageField(upload_to = 'articles/')
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class TakePart(models.Model):
    desc = models.TextField()
    image_url = models.ImageField(upload_to = 'articles/')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    image_url = models.ImageField(upload_to = 'articles/')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class JoinCampaign(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE,)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
