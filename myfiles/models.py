from django.db import models

# Create your models here.

class Catalog(models.Model):
    id = models.CharField(max_length=20, default=None, primary_key=True, verbose_name='目录ID')
    parent_id = models.CharField(max_length=20, default=None, verbose_name='目录父ID')
    name = models.CharField(max_length=50, default=None, verbose_name='目录名')
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, verbose_name='更新时间')
    objects = models.Manager()

    class Meta:
        db_table = 'catalog'
        indexes = [models.Index(fields=['parent_id'])]


class Files(models.Model):
    id = models.CharField(max_length=20, default=None, primary_key=True, verbose_name='文件ID')
    name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    origin_name = models.CharField(max_length=50, default=None, verbose_name='原始文件名')
    format = models.CharField(max_length=8, default=None, verbose_name='文件格式')
    parent = models.ForeignKey(Catalog, on_delete=models.PROTECT, verbose_name='目录ID')
    path = models.CharField(max_length=30, default=None, verbose_name='文件路径')
    size = models.IntegerField(default=None, verbose_name='文件大小')
    md5 = models.CharField(max_length=50, default=None, verbose_name='文件的MD5值')
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, verbose_name='更新时间')
    objects = models.Manager()

    class Meta:
        db_table = 'files'
        indexes = [models.Index(fields=['md5']), models.Index(fields=['create_time']), models.Index(fields=['update_time'])]


class History(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    # id = models.IntegerField(primary_key=True, verbose_name='主键')
    file_id = models.CharField(max_length=20, default=None, verbose_name='文件Id')
    file_name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    operate = models.CharField(max_length=10, default=None, verbose_name='操作类型')
    operate_time = models.DateTimeField(null=True, verbose_name='操作时间')
    ip = models.CharField(max_length=18, default=None, verbose_name='操作IP')
    objects = models.Manager()

    class Meta:
        db_table = 'history'


class Delete(models.Model):
    id = models.CharField(max_length=20, default=None, primary_key=True, verbose_name='文件ID')
    name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    origin_name = models.CharField(max_length=50, default=None, verbose_name='原始文件名')
    format = models.CharField(max_length=8, default=None, verbose_name='文件格式')
    parent_id = models.CharField(max_length=20, default=None, verbose_name='目录ID')
    path = models.CharField(max_length=30, default=None, verbose_name='文件路径')
    size = models.IntegerField(default=None, verbose_name='文件大小')
    md5 = models.CharField(max_length=50, default=None, verbose_name='文件的MD5值')
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, verbose_name='更新时间')
    delete_time = models.DateTimeField(null=True, verbose_name='删除时间')
    objects = models.Manager()

    class Meta:
        db_table = 'delete'


class Shares(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='主键')
    file_id = models.CharField(max_length=20, default=None, verbose_name='文件ID')
    name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    path = models.CharField(max_length=30, default=None, verbose_name='文件路径')
    format = models.CharField(max_length=8, default=None, verbose_name='文件格式')
    times = models.IntegerField(default=None, verbose_name='链接已打开次数')
    total_times = models.IntegerField(default=None, verbose_name='分享链接打开最大次数')
    create_time = models.DateTimeField(null=True, verbose_name='创建时间')
    objects = models.Manager()

    class Meta:
        db_table = 'shares'
