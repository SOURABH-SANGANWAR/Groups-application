from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Otpdetails
from usercustom.models import CustomUser
# Create your views here.

class Verify(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    """
    This class is a view to verify a user email.
    
    url route: /validation/verify/<str:email>/<str:slug>/
    
    methods: GET
    
    """

    def get(self,request, email, slug):
        """
        This function is a view to verify a user email.
        
        url route: /validation/verify/<str:email>/<str:slug>/
        
        Response: "Your email Verified Successfully."
        
        status code:
        200
        """
        try:
            user = CustomUser.objectsall.get(email=email)
            otp = Otpdetails.objects.get(user=user)
            if otp.validate_string(slug):
                user.is_activated = True
                user.save()
                return Response("Your email Verified Successfully.", status=status.HTTP_200_OK)
            else:
                return Response("Invalid url", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"No urls found for this user. Do generate user validation link.", status=status.HTTP_400_BAD_REQUEST)

class Invalidate(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    """
    This class is a view to invalidate a user email.

    url route: /invalidate/<str:email>/<str:slug>/

    methods: GET

    """

    def get(self,request, email, slug):
        """
        This function is a view to invalidate a user email.

        url route: /invalidate/<str:email>/<str:slug>/

        Response: "Your validation link is invalidated successfully."

        status code:
        200
        """
        try:
            user = CustomUser.objectsall.get(email=email)
            otp = Otpdetails.objects.get(user=user)
            if otp.link_string == slug:
                otp.is_active = False
                otp.save()
                return Response("Your validation link is invalidated successfully.", status=status.HTTP_200_OK)
            else:
                return Response("Invalid url", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("No urls found for this user. Do generate user validation link", status=status.HTTP_400_BAD_REQUEST)

# class get_validation_email(APIView):
