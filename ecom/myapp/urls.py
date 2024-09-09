from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home),
    path('about', views.about),
    path('product/<id>', views.product),
    path('login/', views.loginview),
    path('signup/', views.signupview),
    path('logout/', views.logoutview),
    path('addtocart/<id>', views.addtocart),
    path('cart', views.cart),
    path('delete/<id>', views.delete),
    path('makepayment', views.makepayment),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
