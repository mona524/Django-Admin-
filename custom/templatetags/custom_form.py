#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mona on 2017/10/23

from django.template.library import Library
from django.forms.models import ModelChoiceField
from django.urls import reverse
from custom.service.custom_admin import site
register = Library()


def create_form(model_form_boj):
    for item in model_form_boj:
        tpl = {'has_popup':False,'item':item,'popup_url':None}
        if isinstance(item.field,ModelChoiceField) and item.field.queryset.model in site._registry:
            tpl['has_popup'] = True
            field_class = item.field.queryset.model
            app_label = field_class._meta.app_label
            model_name = field_class._meta.model_name
            url = reverse( '{0}:{1}_{2}_add'.format(site.namespace,app_label,model_name) )
            url = '{0}?_popup={1}'.format(url,item.auto_id)
            tpl['popup_url'] = url

        yield tpl


@register.inclusion_tag('custom/custom_form_style.html')
def show_form(model_form_obj):
    return {'form':create_form(model_form_obj)}