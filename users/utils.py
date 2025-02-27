from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser

def genetoken(user):
    user=CustomUser.objects.filter(username=user['username']).first()
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }
    return token