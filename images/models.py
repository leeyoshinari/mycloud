from django.db import models

# Create your models here.

class Catalog(models.Model):
    id = models.CharField(max_length=20, default=None, primary_key=True, verbose_name='目录ID')
    parent_id = models.CharField(max_length=20, default=None, verbose_name='目录父ID')
    name = models.CharField(max_length=50, default=None, verbose_name='目录名')
    # level = models.IntegerField(default=None, verbose_name='目录级别')
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, verbose_name='更新时间')
    objects = models.Manager()

    class Meta:
        db_table = 'catalog'
        # indexes = [models.Index(fields=['parent_id']), models.Index(fields=['level'])]
        indexes = [models.Index(fields=['parent_id'])]


class Files(models.Model):
    id = models.CharField(max_length=20, default=None, primary_key=True, verbose_name='文件ID')
    name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    origin_name = models.CharField(max_length=50, default=None, verbose_name='原始文件名')
    format = models.CharField(max_length=8, default=None, verbose_name='文件格式')
    # parent_id = models.CharField(max_length=20, default=None, verbose_name='目录ID')
    parent = models.ForeignKey(Catalog, on_delete=models.PROTECT, verbose_name='目录ID')
    path = models.CharField(max_length=50, default=None, verbose_name='文件FDFS路径')
    size = models.IntegerField(default=None, verbose_name='文件大小')
    md5 = models.CharField(max_length=50, default=None, verbose_name='文件的MD5值')
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, verbose_name='更新时间')
    objects = models.Manager()

    class Meta:
        db_table = 'files'


class History(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='主键')
    file_id = models.CharField(max_length=20, default=None, verbose_name='文件Id')
    file_name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    operate = models.CharField(max_length=10, default=None, verbose_name='操作类型')
    operate_time = models.DateTimeField(null=True, verbose_name='操作时间')
    objects = models.Manager()

    class Meta:
        db_table = 'history'
        indexes = [models.Index(fields=['file_id'])]
