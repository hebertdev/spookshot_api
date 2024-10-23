from rest_framework import mixins, status, viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from users.permissions.users import IsAccountOwner
from users.serializers.users import (
    UserLoginSerializer, UserModelSerializer,  ChangePasswordSerializer, UserSignUpSerializer)
from users.serializers.profiles import ProfileModelSerializer
from posts.serializers.posts import PostModelSerializer
from users.models import User
from posts.models import Post



class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet,
                  mixins.ListModelMixin):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    def get_permissions(self):
        if self.action in ['signup', 'login']:
            permissions = [AllowAny]
        elif self.action in ['retrieve']:
            permissions = [AllowAny]
        elif self.action in ['whoami']:
            permissions = [IsAuthenticated]
        elif self.action in ['tokenNotification']:
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'profile']:
            permissions = [IsAuthenticated, IsAccountOwner]
        elif self.action in ['follow']:
            permissions = [IsAuthenticated, AllowAny]
        elif self.action in ['list']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_serializer_class(self):
        return UserModelSerializer

    @action(detail=True, methods=['put', 'patch'])
    def profile_edit(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user, context={'request': request}).data
        return Response(data)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

   
    @action(methods=['get'], detail=False, url_path='delete/token', url_name='delete_token')
    def delete_token(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='whoami/me', url_name='whoami')
    def whoami(self, request, *args, **kwargs):
        username = request.user
        user = User.objects.filter(username=username).first()
        data = UserModelSerializer(user, context={'request': request}).data
        return Response(data)
    
    @action(methods=['get'], detail=True)
    def posts(self, request, *args, **kwargs):
        username = self.get_object()
        posts = Post.objects.filter(user=username).order_by('-created')
        data = PostModelSerializer(posts, context={'request': request} , many=True).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        username = response.data.get('username')
        posts = Post.objects.filter(user__username=username).order_by('-created')       
        posts_serialized = PostModelSerializer(posts, many=True , context={'request': request}).data
        
        data = {
            'user': response.data,
            'posts': posts_serialized
        }
        
        response.data = data
        return response



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
