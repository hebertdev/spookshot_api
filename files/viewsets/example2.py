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
        print(request.data)
        # Lista de efectos disponibles
        available_effects = [
            {'effect': 'sepia'},
            {'effect': 'grayscale'},
            {'effect': 'oil_paint'},
            {'effect': 'cartoonify:5:30'},
            {'effect': 'blackwhite'},
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
            format='mp4'
        )
        
        uploaded_video_response = cloudinary.uploader.upload(upload_response.get('url'), resource_type="video")
        cloudinary.uploader.destroy(upload_response.get('public_id'), type="multi")
        
        
        final_video_public_id = uploaded_video_response.get('public_id')
        audio_public_id = 'grito_hombre_swxk8c'
        image_public_id = '5ad16009d2bf997bbe1fbe6940066893_w200_ch7p0r'
        
        # Generar URL con texto, audio e imagen
        final_url = cloudinary.utils.cloudinary_url(final_video_public_id, resource_type="video", transformation=[
            {
                'overlay': f'text:Arial_90:GET%20READY',
                'flags': 'layer_apply',
                'color': 'red',
                'gravity': 'center',  # Posición del texto
                'y': 20,  # Desplazamiento vertical
                'start_offset': "3.0"  # Comienza el texto al principio del video
            },
            {
                'overlay': f'audio:{audio_public_id}',
                'start_offset': "3.0"  # Comienza el audio después de 3 segundos
            },
            {
                'overlay': f'image:{image_public_id}',  # Overlay de la imagen
                'gravity': 'center',  # Ajusta según donde quieras que aparezca
                'start_offset': "2.9"
            }
        ])

        print(final_url)
        response_data = {
            'transformed_video_urls': transformed_urls,
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

   