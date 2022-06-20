from api.views import UserViewSet, ListViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
app_name = 'api'

router = DefaultRouter()
router.register('articles', ListViewSet, basename='articles')
router.register('users', UserViewSet, basename='user')

urlpatterns = (
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
)
