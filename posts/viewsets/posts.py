from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAuthenticated

from posts.models import Post, Media , Comment
from posts.serializers.posts import PostModelSerializer , CommentModelSerializer

class PostViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = PostModelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all().order_by('-created')
    
    def get_permissions(self):
        if self.action in ['add_like', 'remove_like']:
            permissions = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permissions = [AllowAny]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        description = request.data.get('description', '')
        media_urls = request.data.get('media', [])
        type_media = request.data.get('type_media')
        post = Post.objects.create(
            user=request.user,
            description=description,
        )
        for media_url in media_urls:
            Media.objects.create(
                post=post,
                url=media_url,  
                url_string=media_url,  
                media_type=type_media
            )
        data = PostModelSerializer(post , context={'request':request}).data
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'] , url_path='add-like')
    def add_like(self, request, pk=None):
        post = self.get_object()
        post.likes.add(request.user)
        post.save()
        data = PostModelSerializer(post , context={'request':request}).data
        return Response(data)
    
    @action(detail=True, methods=['post'] , url_path='remove-like')
    def remove_like(self, request, pk=None):
        post = self.get_object()
        post.likes.remove(request.user)
        post.save()
        data = PostModelSerializer(post , context={'request':request}).data
        return Response(data)
    
     
    @action(detail=True, methods=['post'] , url_path='add-comment')
    def add_comment(self, request, pk=None):
        post = self.get_object()
        
        comment_text = request.data.get('comment')
        if not comment_text:
            return Response({'error': 'Comment text is required.'}, status=400)
        
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            comment=comment_text,
        )
        data = CommentModelSerializer(comment , context={'request':request}).data
        return Response(data)
            
    
    
    
