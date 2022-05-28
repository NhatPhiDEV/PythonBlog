from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.serializers import ParamChangePassword, ParamLogin, ParamRegister, ParamResetPassword, ParamSendPasswordResetEmail, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UserSendPasswordResetEmailSerializer 
from django.contrib.auth import authenticate  
from apps.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'display_name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Registration
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    @swagger_auto_schema(request_body=ParamRegister)
    def post(self, request, format = None):
        serializer_class = UserRegistrationSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.save()
        token = get_tokens_for_user(user)
        return Response({'Token':token,'msg':'Registration Success'},
        status=status.HTTP_201_CREATED)      
# Login
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    @swagger_auto_schema(request_body=ParamLogin)
    def post(self,request,format= None):
        serializer_class = UserLoginSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        email = serializer_class.data.get('email')
        password = serializer_class.data.get('password')
        user = authenticate(email=email,password=password)
        if user is None:
            return Response({'errors':{'non_field_errors':['Email or password is not Valid']}},
            status=status.HTTP_404_NOT_FOUND)
        token = get_tokens_for_user(user)
        return Response({'Token':token,'msg':'Login Success'},
        status=status.HTTP_200_OK)
# Profile
class UserProfileView(APIView):         
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer_class = UserProfileSerializer(request.user)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
# Change Password
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ParamChangePassword)
    def patch(self, request, format=None):
        serializer_class = UserChangePasswordSerializer(data = request.data
        ,context={'user':request.user})
        serializer_class.is_valid(raise_exception=True)
        return Response({'msg':'Password change Successfully'},
        status=status.HTTP_200_OK)
# Send Password Reset Email
class UserSendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    @swagger_auto_schema(request_body=ParamSendPasswordResetEmail)
    def post(self,request,format=None):
        serializer_class = UserSendPasswordResetEmailSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        return Response({'msg':'Password reset link send. Please check your Email'},
        status=status.HTTP_200_OK)
# Reset Password
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    @swagger_auto_schema(request_body=ParamResetPassword)
    def patch(self,request,uid,token,format=None):
        serializer_class = UserPasswordResetSerializer(data = request.data,
        context={'uid':uid,'token':token})
        serializer_class.is_valid(raise_exception=True)
        return Response({'msg':'Password reset Successfully!'},
            status=status.HTTP_200_OK)