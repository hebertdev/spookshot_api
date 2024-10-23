    #compressssss
    # @action(detail=True, methods=['post'] , url_path='effects/compress')
    # def compress(self, request, pk=None):
    #     file = self.get_object()
    #     image_compress = cloudinary.utils.cloudinary_url(
    #         source=file.public_id,
    #         quality=90,
    #         format='webp',
    #         sign_url=True,
    #     )[0]
        
    #     print(image_compress)
       
        
    #     public_id_compress = image_compress.split('/')[-1].split('.')[0]
    #     compressed_image_details = cloudinary.api.resource(public_id_compress)
    #     file.json_field = compressed_image_details
    #     file.save()
        
    #     serializer = FileModelSerializer(file)
    #     return Response(serializer.data)

#    image_compress = cloudinary.utils.cloudinary_url(
#             source=file.public_id,
#             quality=80,
#             format="webp",
#             width=300,
#             height=300,
#             crop="fill",
#             gravity="center",
#             sign_url=True,
#             effect="sharpen",
#             #radius="10",
#             #border="5px_solid_black",
#             secure=True
#         )[0]
        
#         print(image_compress)
       
        
#         public_id_compress = image_compress.split('/')[-1].split('.')[0]
#         compressed_image_details = cloudinary.api.resource(public_id_compress)
#         file.json_field = compressed_image_details
#         file.save()

from cloudinary import CloudinaryImage


       auto_crop_url = CloudinaryImage(file.public_id).build_url(transformation=[
            request.data,
            {'quality': "auto"},
            {'fetch_format': "webp"},
            {'format': "webp"}
        ])
        
        
              # auto_crop_url = CloudinaryImage(file.public_id).build_url(transformation=[
        #     request.data,
        #     {'quality': "auto"},
        #     {'fetch_format': "webp"},
        #     {'format': "webp"}
        # ])