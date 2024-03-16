from django.urls import path
from seller_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('seller_registration',views.seller_register),
    path('seller_login',views.seller_login),
    path('seller_home',views.seller_home),
    path('add_product',views.addproduct),
    path('viewtable',views.viewpdct),
    path('update/<str:product_id>',views.edit),
    path('remove/<str:product_id>',views.remove),
    path('image/<str:product_id>',views.image,name='image'),
    path('specification/<str:product_id>',views.speci ,name='speci'),
    path('logouts', views.logouts, name='logouts'),
    path('producthome',views.producthome),
    path('addproducthome',views.addproducthome),
    path('offerhome',views.offerhome),
    path('add_offer/<str:product_id>',views.addoffer),
    path('update_offer/<str:offer_id>',views.edit_offer),
    path('view_offer',views.viewoffer),
    path('seller_order',views.seller_order),
    path('remove_offer/<str:offer_id>',views.remove_offer)

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)