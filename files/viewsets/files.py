from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from files.models import File , Version
from files.serializers.files import FileModelSerializer, FileCreateSerializer , VersionModelSerializer
import cloudinary
import cloudinary.api
import cloudinary.uploader
import random


class FileViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet , mixins.RetrieveModelMixin):
    serializer_class = FileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(user=user).order_by('-created')

    def create(self, request, *args, **kwargs):
        serializer = FileCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            file_instance = serializer.save()
            data = FileModelSerializer(file_instance).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='effects-transformation')
    def trasnformation(self, request, pk=None):
        file = self.get_object()
        auto_crop_url = cloudinary.utils.cloudinary_url(
            source=file.public_id,
            transformation=[
                request.data,
                {'quality': "auto"},
                {'fetch_format': "webp"},
                {'format': "webp"}
            ],
            sign_url=True
        )[0]
        public_id_compress = auto_crop_url.split('/')[-1].split('.')[0]
        compressed_image_details = cloudinary.api.resource(public_id_compress)
        file.json_field = compressed_image_details
        file.save()
        serializer = FileModelSerializer(file)
        data = {
            'url': auto_crop_url,
            'file': serializer.data  
        }
        return Response(data)
    
    @action(detail=True, methods=['post'], url_path='effects-halloween')
    def trasnformation_halloween(self, request, pk=None):
        file = self.get_object()
        rest_of_data = [item for item in request.data if 'effect' not in item]
        filtered_data = [{k: v for k, v in rest_of_data[0].items() if k in ['crop', 'aspect_ratio']}]
        first_transform = cloudinary.utils.cloudinary_url(
            source=file.public_id,
            transformation=[
                filtered_data,
                {'quality': "auto"},
                {'fetch_format': "webp"},
                {'format': "webp"}
            ],
            sign_url=True
        )[0]   
        second_transformation = cloudinary.utils.cloudinary_url(
            source=file.public_id,
            transformation=[
                rest_of_data,
                {'quality': "auto"},
                {'fetch_format': "webp"},
                {'format': "webp"}
            ],
            sign_url=True
        )[0]   
        halloween_transform = cloudinary.utils.cloudinary_url(
            source=file.public_id,
            transformation=[
                request.data,
                {'quality': "auto"},
                {'fetch_format': "webp"},
                {'format': "webp"}
            ],
            sign_url=True
        )[0]   
        data = {
            'url_normal': first_transform,
            'url_gen_ai': second_transformation,
            'url_halloween': halloween_transform,
        }
        return Response(data)
    
    @action(detail=True, methods=['post'], url_path='effects-video-screamer')
    def apply_video_transformations(self, request, pk=None):
        video_file = self.get_object()
        aspect_ratio = request.data[0].get('aspect_ratio')
        
        height = 0
        width = 0
        
        if aspect_ratio == '9:16':
            height = 1920
            width = 1080
        elif aspect_ratio == '1:1':
            width = 1080 
            height = 1080 
        else:
            height = 1350
            width = 1080
        
        # Lista de efectos disponibles
        available_effects = [
            {'effect': 'sepia'},
            {'effect': 'grayscale'},
            {'effect': 'oil_paint'},
            {'effect': 'cartoonify:5:30'},
            {'effect': 'pixelate:10'}
        ]
        
        # Selecciona 4 efectos aleatorios
        random_effects = random.sample(available_effects, 4)
        
        # Crea las URLs transformadas
        transformed_urls = []
        for effect in random_effects:
            transformed_video_url = cloudinary.utils.cloudinary_url(
                source=video_file.public_id,
                transformation=[
                    {'crop': 'fill', 'width': width, 'height': height, 'gravity': "auto"},
                    effect,
                    {'quality': "auto"},
                    {'fetch_format': "webp"},
                    {'format': "webp"}
                ],
                sign_url=True
            )[0] + '.webp'
            transformed_urls.append(transformed_video_url)
            
        upload_response = cloudinary.uploader.multi(
            urls=transformed_urls,
            delay=1500,
            signature=True,
            format='webm'
        )
        
        uploaded_video_response = cloudinary.uploader.upload(upload_response.get('url'), resource_type="video")
        cloudinary.uploader.destroy(upload_response.get('public_id'), type="multi")
        
        
        final_video_public_id = uploaded_video_response.get('public_id')
        audio_public_id = 'grito_hombre_swxk8c'
        image_public_id = '1_cb8fzd'
        
        # Generar URL con texto, audio e imagen
        final_url = cloudinary.utils.cloudinary_url(final_video_public_id, 
        resource_type="video", 
            transformation=[
                {
                    'overlay': f'image:{image_public_id}',
                    'gravity': 'center',
                    'start_offset': "3.0", 
                    'end_offset': "3.5"
                },
                {
                    'overlay': f'audio:{audio_public_id}',
                    'start_offset': "3.0",  # El audio también comienza en 3 segundos
                }
            ]
        )[0] + '.webm'
        
        final_video_upload = cloudinary.uploader.upload(final_url, resource_type="video")
        response_data = {
            'url_video': final_video_upload.get('secure_url'),
        }
        return Response(response_data)

    
    @action(detail=True, methods=['post'] , url_path='save-transformation')
    def save_version(self, request, pk=None):
        file = self.get_object()
        version = Version.objects.create(
            file=file,
            url=request.data['url'],
            description=request.data['description'],
            public_id=request.data['public_id'],
        )
        serializer = VersionModelSerializer(version)
        data = {
            'url': request.data['url'],
            'file': serializer.data  
        }
        return Response(data)

   