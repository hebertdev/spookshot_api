from rest_framework import serializers
import cloudinary
import cloudinary.uploader

# models
from files.models import File, Version

class VersionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"

class FileModelSerializer(serializers.ModelSerializer):
    versions = serializers.SerializerMethodField('get_versions')

    def get_versions(self, file):
        versions = Version.objects.filter(file=file)
        return VersionModelSerializer(
            versions, many=True, context=self.context).data

    class Meta:
        model = File
        fields = "__all__"


class FileCreateSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        file_obj = validated_data['file']
        user = self.context['request'].user 
        # Subir el archivo a Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(file_obj)
        except cloudinary.exceptions.Error as e:
            raise serializers.ValidationError({'error': str(e)})

        # Crear el objeto File en la base de datos
        file_instance = File.objects.create(
            user=user,
            name=file_obj.name,
            public_id=upload_result['public_id'],
            url=upload_result['secure_url'],
            type_file=file_obj.content_type,
            folder=None,
            json_field=upload_result,
            created=upload_result['created_at'],
            modified=upload_result['created_at'],
        )

        return file_instance
