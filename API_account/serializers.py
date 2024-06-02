from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=123, validators=[validate_password], write_only=True)
    password2 = serializers.CharField(max_length=123, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return str(token.key)

    class Meta:
        model = User
        fields = ('username', 'token', 'password1', 'password2')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 != password2:
            raise ValidationError({'password2': 'password did not match'})
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(password1)
        return user


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_name', 'first_name', 'password')