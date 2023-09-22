from rest_framework.authtoken.views import ObtainAuthToken
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework import status, generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer,UserListSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully', "status":"201"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.views import TokenObtainPairView
# import jwt
#
# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1MzY1NTA4LCJpYXQiOjE2OTUzNjE5MDgsImp0aSI6ImY1YWYzNWYyZjczODRlMDNhMTRiMWUxNzVlMzgwNTU0IiwidXNlcl9pZCI6MTF9.25Rq3AwGMijxtUURg3Oi6UXsw0XWBTg2GBNJyO_JEa8"
#
# try:
#     decoded_token = jwt.decode(token, verify=False)  # Set verify to False for decoding without verification
#     print(decoded_token)
# except jwt.exceptions.DecodeError as e:
#     print(f"JWT DecodeError: {e}")


class UserLoginView(TokenObtainPairView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        print("====>ser", serializer)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print("===>email", email)
            password = serializer.validated_data['password']
            print("===>pass", password)
            user = authenticate(request, email=email, password=password)
            print("===user", user)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    refresh = RefreshToken.for_user(user)
                    # return Response({
                    #     'access': str(refresh.access_token),
                    #     'refresh': str(refresh)
                    # })
                    # refresh = RefreshToken.for_user(user)
                    # access_token = str(refresh.access_token)
                    return Response(
                        {'message': 'User logged in successfully', 'status': "200", 'access': str(refresh.access_token),
                        'refresh': str(refresh)})
                else:
                    return Response({'message': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserListView(generics.ListAPIView):
#
#     permission_classes = [permission.IsAuthenticated]
#     # permission_classes = (AllowAny,)
#     def get(self, request):
#         list= CustomUser.objects.all()
#         print("===>list", list)
#         serializer= UserListSerializer(list, many=True)
#         return Response(serializer.data)

class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = CustomUser.objects.all()
    print("===>que", queryset)
    permission_classes = [permissions.IsAuthenticated]