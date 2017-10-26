#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mona on 2017/10/18


from . import models
from custom.service import custom_admin


class UserInfoAdmin(custom_admin.ModelCustom):
    list_display = ['id','name','nickname','email',]

    list_filter = [custom_admin.FilterConfig('name'),
                    # custom_admin.FilterConfig('name',text_func_name=lambda x:x.email),
                   # custom_admin.FilterConfig('group',True,lambda x:x.title,lambda x:x.title),
                   custom_admin.FilterConfig('group',True,lambda x:x.title,lambda x:x.pk),
                   custom_admin.FilterConfig('roles',True)]


class UserGroupAdmin(custom_admin.ModelCustom):
    list_display = ['id','title']
    list_filter = ['title', ]

custom_admin.site.register(models.UserInfo,UserInfoAdmin)
custom_admin.site.register(models.UserGroup,UserGroupAdmin)

custom_admin.site.register(models.Role)