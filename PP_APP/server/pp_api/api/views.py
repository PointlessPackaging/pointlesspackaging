from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication

from pp_api.models import (
    image_post, 
    image_post_predicted,
    )

from pp_api.api.serializers import (
    UploadSerializer,
    ImagePostSerializer,
    PredictedSaveSerializer,
)

from accounts.models import Account
from pp_api.api.mrcnn_inference.saved_model_inference import do_prediction

# UPLOAD IMAGE POST
@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
@permission_classes(())
def upload_imgs(request):
    # upload_model = image_post(user_id=request.user)
    upload_model = image_post(user_id=Account.objects.get(pk=2))
    serializer = UploadSerializer(upload_model, data=request.data)
    data = {}
    if serializer.is_valid():
        ret_img_inst = serializer.save()
        post_id = ret_img_inst.id
        try:
            prediction_img, prediction_area = do_prediction(serializer.data.get('top_img'))
        except:
            if ret_img_inst.delete():
                return Response({'response':'upload failed, uploads deleted.'}, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({'response':'upload failed, uploads NOT deleted.'}, status=status.HTTP_400_BAD_REQUEST) 

        predict_model = image_post_predicted(img_post_id=ret_img_inst)
        predict_model.packager = request.data.get('packager')
        predict_model.infer_img = prediction_img
        predict_model.outerbox = prediction_area.get('outerbox')
        predict_model.innerbox = prediction_area.get('innerbox')
        predict_model.item = prediction_area.get('item')
        predict_model.save()

        serializer2 = ImagePostSerializer(predict_model)
        return Response({'response':serializer2.data}, status=status.HTTP_200_OK)
    return Response({'response':'upload failed.'}, status=status.HTTP_400_BAD_REQUEST) 

# DELETE IMAGE POST
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_post(request):
    try:
        img_post_model = image_post.objects.get(pk=request.data.get('post_id'))
    except img_post_model.DoesNotExist:
        return Response({'response':'invalid post.'}, status=status.HTTP_400_BAD_REQUEST)

    # if img_post_model.user_id != request.user:
    #     return Response({'response':'invalid user.'}, status=status.HTTP_204_NO_CONTENT)

    operation = img_post_model.delete()
    data = {}
    if operation:
        data['response'] = "post was deleted successfully."
        return Response(data, status=status.HTTP_200_OK)
    data['response'] = "failed to delete post."
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

# PAGINATION FEATURE FOR THE HOMEPAGE FEED
@permission_classes(())
class display_feed_view(ListAPIView):
    queryset = image_post_predicted.objects.all()
    serializer_class = PredictedSaveSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
