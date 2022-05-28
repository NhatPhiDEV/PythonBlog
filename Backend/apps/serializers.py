import email
from email.policy import default
from xml.dom import ValidationErr
from pkg_resources import require
from rest_framework import serializers
from apps.models import User
# Reset Password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from apps.utils import Util

class ParamLogin(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

class ParamRegister(serializers.Serializer):
    email = serializers.EmailField(required=False)
    image = serializers.ImageField(default='/uploads/default.jpg')
    first_name = serializers.CharField(required=False,max_length = 20)
    last_name = serializers.CharField(required=False,max_length = 20)
    password = serializers.CharField(required=False)

class ParamSendPasswordResetEmail(serializers.Serializer):
    email = serializers.EmailField(required=False)

class ParamChangePassword(serializers.Serializer):
    password = serializers.CharField(required=False)

class ParamResetPassword(serializers.Serializer):
    password = serializers.CharField(required=False)

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','avatar', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
# Login
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
# Profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
#Change Password
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, 
    style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password']

    def validate(self, attrs):
        password = attrs.get('password')
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return attrs
#Reset Password
class UserSendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token',token)
            link = f'http://localhost:3000/api/user/reset-password/{uid}/{token}/'
            print('Password reset link', link)
            #Send Email
            body = str(f'Click following link to reset your password {link}')
            data = {
                'subject':'Reset your password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr('You are not a Registered User')
#Reset Password
class UserPasswordResetSerializer(serializers.ModelSerializer):
        password = serializers.CharField(max_length=255, 
        style={'input_type':'password'},write_only=True)
        class Meta:
            model = User
            fields = ['password']

        def validate(self, attrs):
            try:
                password = attrs.get('password')
                uid = self.context.get('uid')
                token = self.context.get('token')
                id = smart_str(urlsafe_base64_decode(uid))
                user = User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user,token):
                    raise ValidationErr('Token is not Valid or Expired')
                user.set_password(password)
                user.save()
                return attrs
            except DjangoUnicodeDecodeError as identifier:
                PasswordResetTokenGenerator().check_token(user, token)
                raise ValidationErr('Token is not Valid or Expired') from identifier