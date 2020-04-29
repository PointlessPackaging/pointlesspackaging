from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
import random

from pp_api.models import (
    PPUsers,
    Packager,
    ImagePost, 
    PredictedImagePost,
    )

from pp_api.api.serializers import (
    PPUsersSerializer,
    PackagerSerializer,
    UploadSerializer,
    PredictedImagePostSerializer,
    DisplayFeedSerializer,
)

from accounts.models import Account
from pp_api.api.mrcnn_inference.saved_model_inference import do_prediction

# UPLOAD IMAGE POST
@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
@permission_classes(())
def upload_imgs(request):
    # upload_model = ImagePost(user_id=request.user)

    """ Check if the email address is valid """
    normalized_email=BaseUserManager.normalize_email(request.data.get('email'))
    try:
        validate_email(normalized_email)
    except:
        return Response({'response':'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

    """ 1. Check if user exists. If not create a new user.
        2. Retreive the user_id
    """
    try:
        user_id = PPUsers.objects.get(email=normalized_email)
    except PPUsers.DoesNotExist:
        email_serializer = PPUsersSerializer(data={'email':normalized_email})
        if email_serializer.is_valid():
            user_id=email_serializer.save()
        else:
            return Response({'response':'Error.'}, status=status.HTTP_400_BAD_REQUEST)

    """ normalize the packager name """

    try:
        packager_name=str(request.data.get('packager'))
        normalized_packager=packager_name.strip().replace(" ", "").lower()
    except:
        return Response({'response':'Error parsing packager'}, status=status.HTTP_400_BAD_REQUEST)

    """ 1. Check if packager exists. If not create a new packager.
        2. Retreive the packager_inst
    """
    try:
        packager_inst = Packager.objects.get(name=normalized_packager)
    except Packager.DoesNotExist:
        packager_serializer = PackagerSerializer(data={'name':normalized_packager, 'display_name':packager_name, 'count':0, 'score':round(random.uniform(9,10), 1)})
        if packager_serializer.is_valid():
            packager_inst=packager_serializer.save()
        else:
            return Response({'response':'Error saving packager.'}, status=status.HTTP_400_BAD_REQUEST)
 
    """ Upload and save the image on the server"""
    upload_model=ImagePost(user_id=user_id)
    upload_serializer = UploadSerializer(upload_model, 
                data={'top_img':request.data.get('top_img'),
                        'side_img':request.data.get('side_img'),
                        'infer_img':request.data.get('top_img')})
    if upload_serializer.is_valid():
        ret_img_inst = upload_serializer.save()

        """ Call and do inference on the image using the Mask R-CNN API"""
        try:
            prediction_area = do_prediction(upload_serializer.data.get('infer_img'))
        except:
            """ If inference fails, delete the uploaded image. """
            if ret_img_inst.delete():
                return Response({'response':'upload failed, uploads deleted. Packager uncounted.'}, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({'response':'upload failed, uploads NOT deleted. Packager still counted.'}, status=status.HTTP_400_BAD_REQUEST) 

        """ Update the `count` for the packager """
        packager_inst.count=packager_inst.count+1
        packager_inst.save()

        """ Save the reponse from the Mask R-CNN API """
        predict_model = PredictedImagePost(img_post_id=ret_img_inst, packager=packager_inst)
        predict_model.outer_size = prediction_area.get('outerbox')
        predict_model.inner_size = prediction_area.get('innerbox')
        predict_model.item_size = prediction_area.get('item')
        predict_model.save()

        """ Send response back to the client """
        serializer = PredictedImagePostSerializer(predict_model)
        data={  'post_id': serializer.data.get('img_post_id'),
                'packager_id': serializer.data.get('packager'),
                'packager_name': packager_inst.display_name,
                'infer_img': upload_serializer.data.get('infer_img'),
                'outer_size':serializer.data.get('outer_size'),
                'inner_size':serializer.data.get('inner_size'),
                'item_size':serializer.data.get('item_size'),
            }

        return Response({'response':data}, status=status.HTTP_200_OK)
    return Response({'response':'upload failed.'}, status=status.HTTP_400_BAD_REQUEST) 

# DELETE IMAGE POST
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_post(request):
    try:
        img_post_model = ImagePost.objects.get(pk=request.data.get('post_id'))
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
    queryset = PredictedImagePost.objects.all()
    serializer_class = DisplayFeedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
