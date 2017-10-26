#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mona on 2017/10/19

from django.template.library import Library
from types import FunctionType

register= Library()

@register.inclusion_tag('custom/change_list_table.html')
def show_result_list(cl):
    def header():
        if not cl.list_display:
            yield cl.model_config_obj.model_class._meta.model_name
        else:
            for v in cl.list_display:
                yield v(cl.model_config_obj,is_header=True) if isinstance(v,FunctionType) else cl.model_config_obj.model_class._meta.get_field(v).verbose_name

    def body():
        for row in cl.data_list:
            if not cl.list_display:
                yield [str(row),]
            else:
                yield [name(cl.model_config_obj,obj=row) if isinstance(name,FunctionType) else getattr(row,name) for name in cl.list_display]

    return {'headers':header(),
            'body':body(),}

@register.inclusion_tag('custom/change_list_action.html')
def show_actions(cl):
    def get_action(cl):
        for item in cl.actions:
            yield (item.__name__,item.short_desc)

    return {'actions':get_action(cl)}
