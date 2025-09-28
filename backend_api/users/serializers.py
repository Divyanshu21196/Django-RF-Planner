from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name',
                  'is_super_user','is_retailer','is_salesrep')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm',None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name',
                  'is_super_user','is_retailer','is_salesrep')
        read_only_fields = ('id','is_super_user','is_retailer','is_salesrep','created_at','updated_at')

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_super_user','is_retailer','is_salesrep','created_at','updated_at')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_super_user','is_retailer','is_salesrep','created_at','updated_at')
        read_only_fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_super_user','is_retailer','is_salesrep','created_at','updated_at')
