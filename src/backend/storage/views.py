# api/views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from storage.hybrid_storage import HybridStorageService
import uuid


class MaterialUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': '未提供文件'}, status=400)

        # 生成唯一文件名
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        # 读取文件数据
        file_data = uploaded_file.read()

        # 调用混合存储服务上传
        storage_service = HybridStorageService()
        result = storage_service.upload_file(
            object_name=unique_filename,
            file_data=file_data,
            content_type=uploaded_file.content_type
        )

        # 返回结果（包含可用于访问的URL）
        if result['minio_success'] or result['oss_success']:
            # 默认优先使用MinIO的URL
            file_url = storage_service.get_file_url(unique_filename, storage_type='minio')
            result['access_url'] = file_url
            return JsonResponse(result, status=201)

            # # 2. 在数据库中创建素材记录
            # material = Material.objects.create(
            #     title=request.data.get('title', file_obj.name),
            #     description=request.data.get('description', ''),
            #     object_key=unique_name,  # 关键关联字段
            #     uploader=request.user,  # 假设用户已认证
            #     category_id=request.data.get('category_id')
            # )
            # # 将数据库记录ID也返回给前端
            # data['material_id'] = material.id
            # return Response(data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': '文件上传到所有存储均失败'}, status=500)