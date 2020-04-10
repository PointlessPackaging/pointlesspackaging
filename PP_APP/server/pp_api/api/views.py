from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication

from pp_api.models import hello_rest
from pp_api.models import image_post
from pp_api.api.serializers import (
    hello_rest_serializer, 
    UploadSerializer,
    ImagePostSerializer,
)

from accounts.models import Account

# UPLOAD
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def upload_imgs(request):
    upload_model = image_post(user_id=request.user)

    if request.method == 'POST':
        serializer = UploadSerializer(upload_model, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'upload successful.'}, status=status.HTTP_200_OK)
        return Response({'status':'upload failed.'}) 

# PAGINATION FEATURE FOR THE HOMEPAGE FEED
@permission_classes(())
class display_feed_view(ListAPIView):
    queryset = image_post.objects.all()
    serializer_class = ImagePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

################### HELLO REST ###################

# READ
@api_view(['GET'])
@permission_classes(())
def get_hello_rest(request):
    try:
        hello_model = hello_rest.objects.all()
    except hello_rest.DoesNotExist:
        return Response({"response":"Data not found."})

    if request.method == "GET":
        serializer = hello_rest_serializer(hello_model, many=True)
        return Response(serializer.data)

# UPDATE
@api_view(['PUT'])
@permission_classes(())
def update_hello_rest(request):
    try:
        hello_model = hello_rest.objects.get(name=request.data.get('name'))
    except hello_rest.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        serializer = hello_rest_serializer(hello_model, data=request.data)
        data = {}
        if serializer.is_valid(): # very similar to a Django form
            serializer.save()
            data["status"] = "Update successful!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE
@api_view(['DELETE'])
@permission_classes(())
def delete_hello_rest(request):
    try:
        hello_model = hello_rest.objects.get(name=request.data.get('name'))
    except hello_rest.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'DELETE':
        operation = hello_model.delete()
        data = {}
        if operation:
            data["status"] = "Delete successful."
            return Response(data)
        data['status'] = "Operation not successful."
        return Response(data=data)

# CREATE
@api_view(['POST'])
@permission_classes(())
def create_hello_rest(request):
    # request.data.get('name')
    # print("NAME AND MSG:", request.data.get('name'), request.data.get('msg'))
    hello_model = hello_rest()
    if request.method == 'POST':
        serializer = hello_rest_serializer(hello_model, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status':'Unable to create hello_rest.'}) 
