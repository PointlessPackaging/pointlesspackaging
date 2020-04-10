from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.api.serializers import (
    RegistrationSerializer,
    ChangePasswordSerializer,
)

from accounts.models import Account

# CREATE
@api_view(['POST'])
@permission_classes(())
def registration_view(request):

    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'Account Registered.'
        data['email'] = account.email
        data['username'] = account.username
        token = Token.objects.get(user=account).key
        data['token'] = token
        return Response(data, status=status.HTTP_200_OK)
    data = serializer.errors
    return Response(data) 

### NEED TO BE COMPLETED!
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        old_password = serializer.data.get('old_password')
        account = serializer.save()
        data['response'] = 'Password_change successful.'
        return Response(data, status=status.HTTP_200_OK)
    data['response'] = 'Error occurred'
    return Response(data) 

@api_view(['POST'])
def logout_view(request):
    request.user.authtoken.delete()
    return Response({'response':'Logout successful!'})