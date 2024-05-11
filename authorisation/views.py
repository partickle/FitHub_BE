<<<<<<< Updated upstream
from django.shortcuts import render

# Create your views here.
=======
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework import generics, permissions, response, status
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from FitHub_BE import settings
from .models import ActivationCode, generate_activation_code
from .serializers import MyUserSerializer, User


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = MyUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response.Response({
                "user": MyUserSerializer(user).data,
                "message": "User Created Successfully."
            }, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = MyUserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return response.Response({
                "user": MyUserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User Logged In Successfully."
            }, status=status.HTTP_200_OK)
        return response.Response({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class SendActivationCodeView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        code_obj, created = ActivationCode.objects.update_or_create(
            user=user,
            defaults={'code': generate_activation_code()}
        )

        context = {'code': code_obj.code, 'user': user}
        html_content = render_to_string('activation_email.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            'Your Activation Code',
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"message": "Activation code sent to email"}, status=status.HTTP_200_OK)


class VerifyActivationCodeView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        code = request.data.get('code')

        if not user_id or not code:
            return Response({"error": "Both user_id and code must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        if ActivationCode.verify_code(user_id, code):
            return Response({"message": "Activation code is valid."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired activation code."}, status=status.HTTP_400_BAD_REQUEST)

# class RefreshTokenView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         user = request.user
#         refresh = RefreshToken.for_user(user)
#
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_200_OK)


# class ResetPasswordRequest(APIView):
#    def post(self, request, *args, **kwargs):
#        email = request.data.get('email')  # Используйте request.data для DRF
#
#        user = User.objects.filter(email=email).first()
#        if user:
#            # Подготавливаем и отправляем письмо
#            subject = "Password Reset Request"
#            message = "Hi, you have requested a password reset. Please contact our support if you didn't make this request."
#            from_email = 'fithub.csv@gmail.com'  # Это ваш отправительский email
#            recipient_list = [email]  # Список получателей, в данном случае один получатель
#
#            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#
#            return JsonResponse({'message': 'Email sent successfully'}, status=200)
#        else:
#            # Если пользователь с таким email не найден, возвращаем ошибку
#            return JsonResponse({'error': 'User not found'}, status=404)
>>>>>>> Stashed changes
