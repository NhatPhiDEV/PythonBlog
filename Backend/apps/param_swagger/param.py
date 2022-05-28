from rest_framework import serializers

class ParamLogin(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

class ParamRegister(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False,max_length = 20)
    last_name = serializers.CharField(required=False,max_length = 20)
    password = serializers.CharField(required=False)

class ParamSendPasswordResetEmail(serializers.Serializer):
    email = serializers.EmailField(required=False)

class ParamChangePassword(serializers.Serializer):
    password = serializers.CharField(required=False)

class ParamResetPassword(serializers.Serializer):
    password = serializers.CharField(required=False)