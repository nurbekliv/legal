from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .permissions import LessonPermission
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .custom_user import Lesson
from .serializers import LessonSerializer, LessonDetailSerializer

from .serializers import RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer, LoginSerializer

User = get_user_model()


# Ro'yxatdan o'tish
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            password = serializer.validated_data['password']

            if User.objects.filter(email=email).exists():
                return Response({'detail': 'Bunday email bilan foydalanuvchi mavjud.'},
                                status=status.HTTP_400_BAD_REQUEST)

            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            user.save()
            return Response({'detail': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tkazildi.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Foydalanuvchi yoki parol noto\'g\'ri'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Parol muvaffaqiyatli yangilandi.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = UpdateUserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = request.user
            user.first_name = serializer.validated_data.get('first_name', user.first_name)
            user.last_name = serializer.validated_data.get('last_name', user.last_name)
            user.email = serializer.validated_data.get('email', user.email)
            user.save()
            return Response({'detail': 'Foydalanuvchi muvaffaqiyatli yangilandi.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': 'Xatolik yuz berdi.'}, status=status.HTTP_400_BAD_REQUEST)

# Barcha darslarni qaytaruvchi API
class LessonListView(APIView):
    permission_classes = [AllowAny]  # Hamma foydalanuvchilar kirishi mumkin

    # Cache bilan ishlatamiz, bu yerda 15 daqiqa (900 soniya) cache qilamiz
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Slug bo'yicha bitta darsni qaytaruvchi API
class LessonDetailView(APIView):
    permission_classes = [LessonPermission]

    def get(self, request, slug, *args, **kwargs):
        # Agar slug bo'yicha dars topilmasa 404 qaytaradi
        lesson = get_object_or_404(Lesson, slug=slug)
        serializer = LessonDetailSerializer(lesson)
        return Response(serializer.data, status=status.HTTP_200_OK)
