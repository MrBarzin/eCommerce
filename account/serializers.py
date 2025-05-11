from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EmailVerification

class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SignupSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "token", "password", "password_confirmation") 
        
    def validate_password_confirmation(self, data):
        if data != self.initial_data["password"]:
            raise serializers.ValidationError("password and password_confirmation mismatch.")
        
    def validate_token(self, data):
        email_verifications = EmailVerification.objects.filter(token=data, email=self.initial_data["email"])
        if not email_verifications.exists():
            raise serializers.ValidationError("Please verify your email first.")
        
        for email_verification in email_verifications:
            if not email_verification.is_expired():
                return 
            
        raise serializers.ValidationError("Your email verification is expired.")
        
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # class Meta:
    #     model = get_user_model()
    #     fields = ("username", "password")
    
    
class UpdateProfileView(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    profile_picture = serializers.ImageField(required=False, allow_null=True)