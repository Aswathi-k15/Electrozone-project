
from django.urls import path
from user_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('user_register',views.user_regi),
    path('user_login',views.user_login),
    path('welcome',views.wel),
    path('view_product/cart/<str:product_id>',views.cart,name='cart'),
    path('cart',views.cart),
    path('logout', views.logout, name='logout'),
    path('', views.home),
    path('moreproduct',views.more),
    path('about',views.about),
    path('view_product/<str:product_id>', views.view_product, name='view_product'),
    path('profile',views.profile),
    path('address',views.address),
    path('category/<str:maincategory_id>',views.category),
    path('viewaddress',views.viewaddress),
    path('update/<str:address_id>',views.editaddress),
    path('remove/<str:address_id>',views.remove),
    path('add_review/<str:product_id>',views.addreview),
    path('removes/<str:cart_id>',views.removes),
    path('wishlist',views.wishlist),
    path('search',views.search),
    # path('view_product/order/<str:product_id>',views.order ,name='order'),
    path('view_order',views.view_order),
    path('cancel/<str:order_id>',views.cancel),
    path('discount',views.discount)


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)