from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from rest_framework import generics
from rest_framework import filters
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
    DisplayPackagerSerializer,
)

from accounts.models import Account
from pp_api.api.mrcnn_inference.saved_model_inference import do_prediction

# UPLOAD IMAGE POST
@api_view(['POST'])
@permission_classes(())
def upload_imgs(request):
    """ 
    /api/upload
    request: (email, top_img, side_img)
    """
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
                return Response({'response':'upload failed, uploads deleted'}, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({'response':'upload failed, uploads NOT deleted.'}, status=status.HTTP_400_BAD_REQUEST) 

        """ Save the reponse from the Mask R-CNN API """
        predict_model = PredictedImagePost(img_post=ret_img_inst)
        predict_model.outer_size = prediction_area.get('outerbox')
        predict_model.inner_size = prediction_area.get('innerbox')
        predict_model.item_size = prediction_area.get('item')
        predict_model.save()

        """ Send response back to the client """
        serializer = PredictedImagePostSerializer(predict_model)
        data={  'post_id': serializer.data.get('img_post'),
                'infer_img': upload_serializer.data.get('infer_img'),
                'outer_size':serializer.data.get('outer_size'),
                'inner_size':serializer.data.get('inner_size'),
                'item_size':serializer.data.get('item_size'),
            }

        return Response({'response':data}, status=status.HTTP_200_OK)
    return Response({'response':'upload failed.'}, status=status.HTTP_400_BAD_REQUEST) 

# UPDATE IMAGE POST
@api_view(['PUT'])
@permission_classes(())
def update_img_post(request):
    """ 
    /api/update
    request: (post_id, packager, materials, score)
    """
    """ Retreive the post by post_id """
    try:
        update_model = PredictedImagePost.objects.get(img_post=request.data.get('post_id'))
    except PredictedImagePost.DoesNotExist:
        return Response({'response':'Invalid post id.'},status=status.HTTP_400_BAD_REQUEST)

    """ Normalize the packager name. If failure, delete the post. """
    try:
        packager_name=str(request.data.get('packager'))
        normalized_packager=packager_name.strip().replace(" ", "").lower()
    except:
        del_str=' not deleted.'
        if update_model.img_post.delete():
            del_str=' deleted.'
        return Response({'response':'Error parsing packager. Post'+del_str}, status=status.HTTP_400_BAD_REQUEST)

    """ 1. Check if packager exists. If not create a new packager.
        2. Retreive the packager_inst
        3. If failure occurred, delete the post.
    """
    try:
        packager_inst = Packager.objects.get(name=normalized_packager)
    except Packager.DoesNotExist:
        packager_serializer = PackagerSerializer(data={'name':normalized_packager, 'brand_name':packager_name, 'count':0, 'score':7})
        if packager_serializer.is_valid():
            packager_inst=packager_serializer.save()
        else:
            del_str=' not deleted.'
            if update_model.img_post.delete():
                del_str=' deleted.'
            return Response({'response':'Error saving packager. Post'+del_str}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_score=float(request.data.get('score'))
        avg_score=packager_inst.score
        count=packager_inst.count

        update_model.packager=packager_inst
        update_model.materials=str(request.data.get('materials'))
        update_model.score=min(10, new_score)
        update_model.save()

        """ Update the `count` for the packager """
        packager_inst.count=count+1
        packager_inst.score=min(10, (count*avg_score+new_score)/(count+1))
        packager_inst.save()
        
        return Response({'response':'Successfully updated.'},status=status.HTTP_200_OK)
    except:
        del_str=' not deleted.'
        if update_model.img_post.delete():
            del_str=' deleted.'
        return Response({'response':'Unable to save data. Post'+del_str},status=status.HTTP_400_BAD_REQUEST)

# DELETE IMAGE POST
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_post(request):
    try:
        img_post_model = ImagePost.objects.get(pk=request.data.get('post_id'))
    except img_post_model.DoesNotExist:
        return Response({'response':'invalid post.'}, status=status.HTTP_400_BAD_REQUEST)

    operation = img_post_model.delete()
    data = {}
    if operation:
        data['response'] = "post was deleted successfully."
        return Response(data, status=status.HTTP_200_OK)
    data['response'] = "failed to delete post."
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes(())
def top_five_best_view(request):
    """ 
    /api/best_five
    Displays the top five best ranked companies.
    """
    try:
        packager = Packager.objects.order_by('-score')[:5]
    except Packager.DoesNotExist:
        return Response({"response":"Cannot retreive top 5 best packagers."})

    if request.method == "GET":
        serializer = DisplayPackagerSerializer(packager, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes(())
def top_five_worst_view(request):
    """ 
    /api/worst_five
    Displays the top five worst ranked companies.
    """
    try:
        packager = Packager.objects.order_by('score')[:5]
    except Packager.DoesNotExist:
        return Response({"response":"Cannot retreive top 5 worst packagers."})

    if request.method == "GET":
        serializer = DisplayPackagerSerializer(packager, many=True)
        return Response(serializer.data)

@permission_classes(())
class display_feed_view(ListAPIView):
    """  
    /api/display_feed?page=NUMBER
    Displays all posts, ordered by newest-oldest. Paginated.
    """
    queryset = PredictedImagePost.objects.all().order_by('-img_post__date_posted')
    serializer_class = DisplayFeedSerializer
    pagination_class = PageNumberPagination

@permission_classes(())
class display_all_packagers_view(ListAPIView):
    """  
    /api/display_all_packagers?page=NUMBER
    Displays all paackagers, ordered by `brand_name`. Paginated.
    """
    queryset = Packager.objects.all().order_by('brand_name')
    serializer_class = DisplayPackagerSerializer
    pagination_class = PageNumberPagination

@permission_classes(())
class search_packager_posts_view(ListAPIView):
    """ 
    /api/search_post?packager=CompanyName&page=1
    Note: CompanyName must be URL encoded
    Displays all posts by a `packager`, ordered by newest-oldest. Paginated. 
    """
    def get_queryset(self):
        packager = self.request.query_params.get('packager', None).strip().replace(" ", "").lower()
        queryset = PredictedImagePost.objects.filter(packager__name=packager).order_by('-img_post__date_posted')
        return queryset
    serializer_class = DisplayFeedSerializer
    pagination_class = PageNumberPagination

@permission_classes(())
class search_user_posts_view(ListAPIView):
    """ 
    /api/search_user?packager=UserEmail&page=NUMBER
    Note: UserEmail must be URL encoded
    Displays all posts by a user based on their `email`, ordered by newest-oldest. Paginated. 
    """
    def get_queryset(self):
        email = self.request.query_params.get('email', None).strip()
        # order by newest-oldest
        queryset = PredictedImagePost.objects.filter(img_post__user_id__email=email).order_by('-img_post__date_posted')
        return queryset
    serializer_class = DisplayFeedSerializer
    pagination_class = PageNumberPagination