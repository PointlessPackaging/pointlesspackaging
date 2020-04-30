from django.contrib import admin

# Register your models here.
from pp_api.models import (
    #hello_rest,
    Packager,
    PPUsers,
    ImagePost,
    PredictedImagePost,
)

class PPUsersAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    readonly_fields = ()
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PackagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_name', 'count', 'score')
    search_fields = ('name', 'brand_name', 'count', 'score')
    readonly_fields = ()
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ImagePostAdmin(admin.ModelAdmin):
    def get_username(self, obj):
        return obj.user_id.email
    get_username.admin_order_field  = 'user_id'  #Allows column order sorting
    get_username.short_description = 'User'  #Renames column head

    list_display = ('user_id', 'get_username', 'date_posted', 'infer_img', 'top_img', 'side_img')
    search_fields = ('user_id__email', 'date_posted')
    readonly_fields = ()
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PredictedImagePostAdmin(admin.ModelAdmin):
    def get_name(self, obj):
        return obj.packager.brand_name
    get_name.admin_order_field  = 'packager'  #Allows column order sorting
    get_name.short_description = 'Packager Name'  #Renames column head

    def get_username(self, obj):
        return obj.img_post.user_id.email
    get_username.admin_order_field  = 'img_post'  #Allows column order sorting
    get_username.short_description = 'User'  #Renames column head

    list_display = ('img_post', 'get_username', 'get_name','materials','score','outer_size','inner_size','item_size')
    search_fields = ('img_post__user_id__email', 'packager__brand_name','materials','score','outer_size','inner_size','item_size')
    readonly_fields = ()
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

#These register the models with the admin classes.
admin.site.register(Packager, PackagerAdmin)
admin.site.register(PPUsers, PPUsersAdmin)
admin.site.register(ImagePost, ImagePostAdmin)
admin.site.register(PredictedImagePost, PredictedImagePostAdmin)
