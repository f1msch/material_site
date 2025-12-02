# storage/hybrid_storage.py
import logging
from minio import Minio
from minio.error import S3Error
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger(__name__)


class HybridStorageService:
    """混合存储服务类 (SDK模式)"""

    def __init__(self):
        # 初始化MinIO客户端（热存储）
        self.minio_client = Minio(
            settings.MINIO_CONFIG['endpoint'],
            access_key=settings.MINIO_CONFIG['access_key'],
            secret_key=settings.MINIO_CONFIG['secret_key'],
            secure=settings.MINIO_CONFIG.get('secure', False)
        )
        # 初始化OSS客户端（冷备份）
        self.oss_client = boto3.client(
            's3',
            endpoint_url=settings.OSS_CONFIG['endpoint'],
            aws_access_key_id=settings.OSS_CONFIG['access_key'],
            aws_secret_access_key=settings.OSS_CONFIG['secret_key'],
            region_name=settings.OSS_CONFIG.get('region', 'us-east-1'),
            config=boto3.session.Config(signature_version='s3v4')
        )
        self.minio_bucket = settings.MINIO_CONFIG['bucket']
        self.oss_bucket = settings.OSS_CONFIG['bucket']
        self._ensure_buckets()

    def _ensure_buckets(self):
        """确保存储桶存在"""
        try:
            if not self.minio_client.bucket_exists(self.minio_bucket):
                self.minio_client.make_bucket(self.minio_bucket)
        except S3Error as e:
            logger.error(f"确保MinIO桶存在失败: {e}")
        try:
            self.oss_client.head_bucket(Bucket=self.oss_bucket)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                try:
                    self.oss_client.create_bucket(Bucket=self.oss_bucket)
                except ClientError as create_e:
                    logger.error(f"创建OSS桶失败: {create_e}")

    def upload_file(self, object_name, file_data, content_type='application/octet-stream'):
        """双写上传文件到MinIO和OSS"""
        # 1. 上传到MinIO (热存储)
        minio_success = False
        try:
            self.minio_client.put_object(
                self.minio_bucket,
                object_name,
                file_data,
                length=len(file_data) if hasattr(file_data, '__len__') else -1,
                content_type=content_type
            )
            minio_success = True
            logger.info(f"文件 {object_name} 成功上传至MinIO")
        except S3Error as e:
            logger.error(f"上传至MinIO失败: {e}")

        # 2. 上传到OSS (冷备份)
        oss_success = False
        try:
            # 确保file_data是字节流
            if hasattr(file_data, 'read'):
                file_data.seek(0)
                upload_data = file_data.read()
            else:
                upload_data = file_data

            self.oss_client.put_object(
                Bucket=self.oss_bucket,
                Key=object_name,
                Body=upload_data,
                ContentType=content_type
            )
            oss_success = True
            logger.info(f"文件 {object_name} 成功上传至OSS")
        except ClientError as e:
            logger.error(f"上传至OSS失败: {e}")

        # 3. 返回上传结果状态
        return {
            'minio_success': minio_success,
            'oss_success': oss_success,
            'object_name': object_name
        }

    def get_file_url(self, object_name, storage_type='minio', expires=3600):
        """获取文件访问URL（默认从MinIO获取）"""
        if storage_type.lower() == 'minio':
            try:
                url = self.minio_client.presigned_get_object(
                    self.minio_bucket,
                    object_name,
                    expires=expires
                )
                return url
            except S3Error as e:
                logger.error(f"生成MinIO预签名URL失败: {e}")
                return None
        else:
            # 降级：从OSS获取URL
            try:
                url = self.oss_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.oss_bucket, 'Key': object_name},
                    ExpiresIn=expires
                )
                return url
            except ClientError as e:
                logger.error(f"生成OSS预签名URL失败: {e}")
                return None