from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string

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


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if user exists"""
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        """Generate temporary password and send email"""
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate temporary password (8 characters)
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

        # Update user password
        user.set_password(temp_password)
        user.save()

        # Send email
        subject = 'Temporary Password - Backend API'
        message = f"""
                    Hello {user.first_name or user.email},

                    Your temporary password is: {temp_password}

                    Please use this password to login and change it immediately for security.

                    Best regards,
                    Backend API Team
                            """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return {'message': 'Temporary password sent to your email'}


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    temporary_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8, validators=[validate_password])

    def validate(self, attrs):
        """Validate temporary password and user"""
        try:
            user = User.objects.get(email=attrs['email'])
            if not user.check_password(attrs['temporary_password']):
                raise serializers.ValidationError("Invalid temporary password.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        attrs['user'] = user
        return attrs

    def save(self):
        """Set new permanent password"""
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        return {'message': 'Password updated successfully'}