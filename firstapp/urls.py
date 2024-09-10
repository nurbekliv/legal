from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ChangePasswordView, UpdateUserView, LogoutView, LessonListView, LessonDetailView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update-user/', UpdateUserView.as_view(), name='auth_update_user'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<slug:slug>/', LessonDetailView.as_view(), name='lesson-detail'),
]
