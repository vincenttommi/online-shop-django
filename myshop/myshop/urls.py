from django.contrib import admin
from django.urls import path, include
from django.conf import  settings
from django.conf.urls.static import  static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    #registering  shops url in   the main project url
    path('cart/', include('cart.urls', namespace='cart')),
    #registering carts urls in the main project url
]


if  settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    