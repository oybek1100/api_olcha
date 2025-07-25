from django.urls import path, include
from rest_framework import routers
from .views import CategoryAPIView, SubCategoryAPIView, ProductAPIView, CommentAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = routers.DefaultRouter()
router.register('category', CategoryAPIView)
router.register('subcatergory', SubCategoryAPIView)
router.register('product', ProductAPIView ,basename='product')
router.register('comment', CommentAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
