from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer, ListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from otpdetails.models import Otpdetails
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class UserRegister(generics.CreateAPIView):
    """
    This class is a view to register a new user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination


class getUser(APIView):
    """
    This class is a view to get a user.

    url route: 
    /user/getuser/<int:id>

    methods:
    GET
    """
    queryset = CustomUser.objects.all()
    serializer_class = ListSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request,id, *args, **kwargs):
        """
        This function is a view to get a user.
        
        url route:
        /user/getuser<int:id> : GET
        
        Response:
        {
            "id": <id:int>,
            "username": <username:string>,
            "email": <email:string>,
            "first_name": <first_name:string>,
            "last_name": <last_name:string>,
            "Profile_picture": <Profile_picture:link>,
            "is_activated: <is_activated:boolean>
        }

        status code:
        200
        """
        user = CustomUser.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class Login(APIView):
    """
    This class is a view to login.
    This generates access and refresh token if valid credentials else returns error message.

    url route:
    /user/login : POST

    methods:
    POST
    """

    def post(self,request):
        """
        This function handles login
        url route:
        /user/login : POST

        Request:
        {
            "email": <email:string>,
            "password": <password:string>
        }

        Response:
        {
            data:(None if invalid credentials else user data){
                "refresh": <refresh:token>,
                "access": <access:token>,
                "login": <login:boolean>,
                user:{
                    "id": <id:int>,
                    "username": <username:string>,
                    "email": <email:string>,
                    "first_name": <first_name:string>,
                    "last_name": <last_name:string>,
                    "Profile_picture": <Profile_picture:link>,
                    "is_activated: <is_activated:boolean>
                }
            }
            errors:(None if valid credentials else error message)<errors:string>
        }

        status code:
        200 if valid credentials
        400 if invalid credentials
        401 if invalid password
        """
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return Response({'data':None,'errors': 'No email found. Please register to login  or verify your email if already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if user.check_password(password):
            serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            data = {}
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['login'] = True
            data['user'] = serializer.data
            return Response({'data':data,'errors':None}, status=status.HTTP_200_OK)
        print("Invalid password", user.check_password(password), password)
        return Response({'data':None,'errors': 'Invalid credentials. Please check your email and password.'}, status=status.HTTP_401_UNAUTHORIZED)

class LoginOtp(APIView):
    """
    This class is a view to login using otp.
    This generates otp if verified user else generates a verification link.

    url route:
    /user/login_otp 

    methods:
    POST
    PUT
    """

    def post(self, request):
        """
        This function handles login using otp
        url route:
        /user/login_otp : POST

        Request:
        {
            "email": <email:string>
        }

        Response:
        {
            data:(None if invalid credentials else user data)"OTP sent successfully."
            errors:(None if valid credentials else error message)<errors:string>
        }

        status code:
        200 if valid credentials
        400 if invalid credentials
        401 if not verified
        """
        email = request.data.get('email')
        print(email)
        user = CustomUser.objectsall.filter(email=email).first()
        print(user)
        if user is None:
            return Response({'data':None,'errors': 'No email found. Please register to login'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_activated:
            # get all previous otps and delete them
            Otpdetails.objects.filter(user=user).delete()
            opt_obj = Otpdetails.objects.create(user=user)
            opt_obj.setup()
            return Response({'data':"OTP sent successfully.",'errors':None}, status=status.HTTP_200_OK)
        return Response({'data':None,'errors': 'Please verify your email before Logging in.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        """
        This handles verification of otp and login.
        url route:
        /user/login_otp : PUT
        
        Request:
        {
            "email": <email:string>,
            "otp": <otp:string>
        }

        Response:
        {
            data:(None if invalid credentials else user data){
                "refresh": <refresh:token>,
                "access": <access:token>,
                "login": <login:boolean>,
                user:{
                    "id": <id:int>,
                    "username": <username:string>,
                    "email": <email:string>,
                    "first_name": <first_name:string>,
                    "last_name": <last_name:string>,
                    "Profile_picture": <Profile_picture:link>,
                    "is_activated: <is_activated:boolean>
                }
            }
            errors:(None if valid credentials else error message)<errors:string>
        }

        status code:
        200 if valid credentials
        400 if invalid credentials
        401 if not verified
        """

        email = request.data.get('email')
        otp = request.data.get('otp')
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return Response({'data':None,'errors': 'No email found. Please register to login or verify your email'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_activated:
            opt_obj = Otpdetails.objects.filter(user=user).first()
            if opt_obj is None:
                return Response({'data':None,'errors': 'Please generate otp first.'}, status=status.HTTP_400_BAD_REQUEST)
            if opt_obj.is_valid_otp(otp):
                serializer = UserSerializer(user)
                refresh = RefreshToken.for_user(user)
                data = {}
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                data['login'] = True
                data['user'] = serializer.data
                return Response({'data':data,'errors':None}, status=status.HTTP_200_OK)
            return Response({'data':None,'errors': 'Invalid OTP. Please check your email and otp.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'data':None,'errors': 'Please verify your email before Logging in.'}, status=status.HTTP_401_UNAUTHORIZED)


class Profile(APIView):
    """
    This class is to get profile details.
    
    url route:
    /user/profile
    
    methods: GET, PUT.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        This function handles get request for profile details.
        url route:
        /user/profile : GET
        
        Response:
        {
            data:(None if invalid credentials else user data){
                "id": <id:int>,
                "username": <username:string>,
                "email": <email:string>,
                "first_name": <first_name:string>,
                "last_name": <last_name:string>,
                "Profile_picture": <Profile_picture:link>,
                "is_activated: <is_activated:boolean>
                }
            errors:(None if valid credentials else error message)<errors:string>
        }
        """
        try:
            userSer = UserSerializer(request.user)
            return Response({'data':userSer.data,'errors':None}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            userSer = UserSerializer(request.user, data=request.data, partial=True)
            if userSer.is_valid():
                userSer.save()
                return Response({'data':userSer.data,'errors':None}, status=status.HTTP_200_OK)
            return Response({'data':None,'errors':userSer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
