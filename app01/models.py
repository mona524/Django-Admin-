from django.db import models

# Create your models here.


class UserGroup(models.Model):
    title = models.CharField(max_length=32,verbose_name='组名')
    test = models.CharField(max_length=32,verbose_name='测试',null=True,blank=True,)

    def __str__(self):
        return self.title

class Role(models.Model):
    name= models.CharField(max_length=32,verbose_name='角色名')


    def __str__(self):
        return self.name

class UserInfo(models.Model):

    group = models.ForeignKey(UserGroup,null=True,blank=True,verbose_name='组名')
    name = models.CharField(max_length=32,verbose_name='姓名')
    nickname =  models.CharField(max_length=32,null=True,blank=True,verbose_name='昵称')
    email = models.EmailField(max_length=32,verbose_name='邮箱')

    ctime = models.DateTimeField(null=True,blank=True,verbose_name='创建时间')

    roles = models.ManyToManyField(to=Role,verbose_name='角色')

    def __str__(self):
        return self.name