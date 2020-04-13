from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from django.http import QueryDict

from pp_api.models import (
    hello_rest, 
    image_post, 
    image_post_predicted,
    )

from pp_api.api.serializers import (
    hello_rest_serializer, 
    UploadSerializer,
    ImagePostSerializer,
    PredictedSaveSerializer,
)

from accounts.models import Account
from pp_api.api.mrcnn_inference.saved_model_inference import do_prediction

# UPLOAD IMAGE POST
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def upload_imgs(request):
    upload_model = image_post(user_id=request.user)
    serializer = UploadSerializer(upload_model, data=request.data)
    data = {}
    if serializer.is_valid():
        ret_img_inst = serializer.save()
        post_id = ret_img_inst.id
        try:
            prediction_img, prediction_area = do_prediction(serializer.data.get('top_img'))
        except:
            if ret_img_inst.delete():
                return Response({'status':'upload failed, uploads deleted.'}) 
            else:
                return Response({'status':'upload failed, uploads NOT deleted.'}) 

        predict_model = image_post_predicted(img_post_id=ret_img_inst)
        predict_model.packager = request.data.get('packager')
        predict_model.infer_img = prediction_img
        predict_model.outerbox = prediction_area.get('outerbox')
        predict_model.innerbox = prediction_area.get('innerbox')
        predict_model.item = prediction_area.get('item')
        predict_model.save()

        serializer2 = ImagePostSerializer(predict_model)
        return Response({'response':serializer2.data}, status=status.HTTP_200_OK)
    return Response({'status':'upload failed.'}) 

# DELETE IMAGE POST
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_post(request):
    try:
        img_post_model = image_post.objects.get(pk=request.data.get('post_id'))
    except hello_rest.DoesNotExist:
        return Response({'response':'invalid post.'}, status=status.HTTP_204_NO_CONTENT)

    if img_post_model.user_id != request.user:
        return Response({'response':'invalid user.'}, status=status.HTTP_204_NO_CONTENT)

    operation = img_post_model.delete()
    data = {}
    if operation:
        data['response'] = "post was deleted successfully."
        return Response(data)
    data['response'] = "failed to delete post."
    return Response(data=data)

# PAGINATION FEATURE FOR THE HOMEPAGE FEED
@permission_classes(())
class display_feed_view(ListAPIView):
    queryset = image_post_predicted.objects.all()
    serializer_class = PredictedSaveSerializer
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
