from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import OTPRequest
from .serializers import RequestOTPSerializer, RequestOTPResponseSerializer, VerifyOTPRequestSerializer, \
    ObtainTokenSerializer
from rest_framework import status
# Create your views here.
class OTPView(APIView):
    def get(self, request):
        serializer = RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPRequest.objects.generate(data)
                return Response(data=RequestOTPResponseSerializer(otp).data)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = VerifyOTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['reciver'] , data['request_id'] , data['password']):
                return Response(self._handel_login(data))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _handel_login(self , otp):
        User = get_user_model()
        query = User.objects.filter(username=otp['reciver'])
        if query.exists():
            created = False
            user = query.first()
        else:
            user = User.objects.create(username=otp['reciver'])
            created = True
        refresh = RefreshToken.for_user(user)
        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'created':created,

        }).data