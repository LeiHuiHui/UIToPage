from django.db import models

# Create your models here.


class Sampler(models.Model):
    img = models.ImageField(upload_to='img') # upload_to指定图片上传的途径，如果不存在则自动创建