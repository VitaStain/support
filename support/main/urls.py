from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import TicketViewSet, chat

app_name = 'main'

router = routers.SimpleRouter()
router.register(r'ticket', TicketViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/chat/', chat, name='chat'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
