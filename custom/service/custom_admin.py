#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mona on 2017/10/18

from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from custom.utils.page import Paginator
from django.forms import ModelForm
from django.http import QueryDict
import copy
from types import FunctionType
import functools


class FilterConfig:
    def __init__(self, name_or_func,multi_choose=False,text_func_name=None,val_func_name=None):
        '''
        :param name_or_func: 字段名或函数
        :param multi_choose: 是否支持多选
        :param text_func_name: 在model中定义函数，显示文本名称，默认使用str(对象)
        :param val_func_name: 在model中定义函数， url 上传的值，默认使用对象.pk
        '''
        self.name_or_func = name_or_func
        self.multi_choose = multi_choose
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    @property
    def is_func(self):
        if isinstance(self.name_or_func,FunctionType):
            return True

    @property
    def name(self):
        if isinstance(self.name_or_func, FunctionType):
            return self.name_or_func.__name__
        else:
            return self.name_or_func

class RowItem:
    def __init__(self,data_list,change_list_obj,params,option,):
        self.data_list = data_list
        self.change_list_obj = change_list_obj
        self.params = params
        self.option = option
        self.multi_choose = option.multi_choose
        self.request_get = copy.deepcopy(self.params)
        self.request_get.mutable=True

    def __iter__(self):
        base_url = self.change_list_obj.model_config_obj.changelist_url

        #获取当前的用户选中的列表
        current_pk_list=self.request_get.getlist(self.option.name)

        if self.request_get.get(self.option.name):
            '''有当前列的值，则清空，保留其它项的值'''
            self.request_get.pop(self.option.name)
            url = '{0}?{1}'.format(base_url, self.request_get.urlencode())
            tpl = '<a href=?{0}>全部</a>'.format(url)
        else:
            url ='{0}?{1}'.format(base_url,self.request_get.urlencode())
            tpl = '<a href=?{0} class="active">全部</a>'.format(url)

        yield mark_safe('<div class="whole">%s</div>'%tpl)

        yield mark_safe('<div class="others">')
        for row in self.data_list:
            self.request_get = copy.deepcopy(self.params)

            pk = self.option.val_func_name(row) if self.option.val_func_name else row.pk
            pk = str(pk)

            text = self.option.text_func_name(row) if self.option.text_func_name else str(row)
            exist = False
            current_pk_list = self.request_get.getlist(self.option.name)
            if pk in  current_pk_list:
                exist = True
            if self.multi_choose:
                if exist:
                    current_pk_list.remove(pk)

                self.request_get.setlist(self.option.name,current_pk_list)
                url = '{0}?{1}'.format(base_url, self.request_get.urlencode())

                if pk in current_pk_list:
                    tpl = '<a class="active" href=?{0}>{1}</a>'.format(url, text)
                else:
                    tpl = '<a href=?{0}>{1}</a>'.format(url, text)
            else:
                self.request_get[self.option.name] = pk
                #单选的列中，第二次点击取消
                if current_pk_list:
                    if current_pk_list[0] == str(pk):
                        self.request_get.pop(self.option.name)

                url = '{0}?{1}'.format(base_url, self.request_get.urlencode())
                tpl = '<a href=?{0}>{1}</a>'.format(url,text)
                if current_pk_list:
                    if pk == current_pk_list[0]:
                        tpl = '<a class="active" href=?{0}>{1}</a>'.format(url,text)
            yield mark_safe(tpl)
        yield mark_safe('</div>')

class ChangeList:
    def __init__(self,data_list,model_config_obj):

        self.list_display = model_config_obj.get_list_display()
        self.model_config_obj = model_config_obj
        self.actions = model_config_obj.get_actions()
        self.list_filter = model_config_obj.get_list_filter()



        request_get = copy.deepcopy(model_config_obj.request.GET)
        request_get.mutable = True

        page = Paginator(
            current_page= model_config_obj.request.GET.get('page'),
            total_item_count=data_list.count(),
            base_url=model_config_obj.request.path_info,
            per_page_item_count=2,
            request_params = request_get
        )

        self.data_list = data_list[page.start:page.end]
        self.page_html = page.pager

    def add_html(self):
        '''添加按钮'''

        add_html = mark_safe('<a class="btn btn-primary" href="%s">添加</a>'%self.model_config_obj.add_url_params)
        return add_html

    def get_list_filter_data(self):

        model_class = self.model_config_obj.model_class

        for option in self.model_config_obj.list_filter:
            if option.is_func:
                data_list = option.name_or_func(self.model_config_obj,self,option)
            else:

                from django.db.models.fields.related import RelatedField
                field_obj = model_class._meta.get_field(option.name)

                if isinstance(field_obj,RelatedField):
                    field_related_class = field_obj.rel.to
                    data_list = field_related_class.objects.all()
                else:
                    data_list = model_class.objects.all()

            yield RowItem(data_list,self,self.model_config_obj.request.GET,option)

class ModelCustom:
    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name
        self.url_save = '_url_save'


    def checkbox(self,obj=None,is_header = False):
        if is_header:
            return '选择'
        else:
            html_checkbox = "<input type='checkbox' name='pk' value='%s'/>" %(obj.pk)
            return mark_safe(html_checkbox)

    def manipulate(self,obj=None,is_header=False):
        if is_header:
            return '操作'
        else:
            delete_url = self.delete_url(obj.pk)
            change_url = self.change_url(obj.pk)
            html_delete = '<a class="btn btn-warning" href="%s">删除</a> &nbsp;&nbsp<a class="btn btn-info" href="%s">编辑</a>'%(delete_url,change_url)
            return mark_safe(html_delete)

    def get_list_display(self):
        if self.list_display:
            if  ModelCustom.checkbox not in self.list_display:
                self.list_display.insert(0, ModelCustom.checkbox)
            if ModelCustom.manipulate not in self.list_display:
                self.list_display.append(ModelCustom.manipulate)
            return self.list_display

    list_display = []
    show_add_btn = True

    def get_show_add_btn(self):
        return self.show_add_btn

    '''
    定制action
    '''
    actions = []
    def multi_del(self):
        pk_list = self.request.POST.getlist('pk')
        self.model_class.objects.filter(pk__in = pk_list).delete()

    multi_del.short_desc = '批量删除'


    def get_actions(self):
        result = []
        result.extend(self.actions)
        result.append(ModelCustom.multi_del)
        return result

    '''反向生成URL'''
    def reverse_change_list_url(self):
        url = reverse('%s:%s_%s_changelist' % (self.site.namespace,self.app_label,self.model_name))
        return url

    ''' 定制model form'''
    model_form = None

    def get_model_form_class(self):
        result = self.model_form
        if not result:
            class DefaultModeForm(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = '__all__'
            result = DefaultModeForm
        return result

    ''' 定制组合筛选 '''
    list_filter = []

    def get_list_filter(self):
        return self.list_filter

    def changelist_view(self, request, *args, **kwargs):
        self.request = request
        if self.request.method == 'POST':
            action_name = self.request.POST.get('action')
            action_func = getattr(self,action_name,None)
            if action_func:
                action_func()


        data_list = self.model_class.objects.all()
        cl = ChangeList(data_list,self)
        context= {'cl':cl}
        return render(request,'custom/changelist.html',context)

    def add_view(self, request, *args, **kwargs):
        popup_id = request.GET.get('_popup')
        self.request = request
        if self.request.method == 'GET':
            form = self.get_model_form_class()()
            return render(request, "custom/add_popup.html" if popup_id else "custom/add_list.html", {'form': form})

        elif self.request.method == 'POST':
            form = self.get_model_form_class()(data=self.request.POST)
            if form.is_valid():
                obj= form.save()
                if popup_id:
                    context={'obj':obj,'field':request.GET.get('_popup'),'data':obj.__str__()}
                    return render(request, 'custom/popup_response.html',context)
                else:
                     return redirect(self.change_list_url_params)

            context = {'form': form}
            return render(self.request, 'custom/add_list.html', context)

    def delete_view(self, request, *args, **kwargs):
        id = args[0]
        if request.method == 'GET':

            obj = self.model_class.objects.filter(id=id).first()
            return render(request,'custom/delete_list.html',{'obj':obj.__str__()})

        elif request.method == 'POST':
            status = request.POST.get('btn')
            if status == 'true':
                obj = self.model_class.objects.filter(id=id).first().delete()

            return redirect(self.reverse_change_list_url())

    def change_view(self, request, pk,*args, **kwargs):
        self.request = request
        obj = self.model_class.objects.filter(pk=pk).first()

        if self.request.method =='GET':
            form = self.get_model_form_class()(instance=obj)
            context = {
                'form':form
            }
            return render(self.request,'custom/change.html',context)

        elif self.request.method == 'POST':
            form = self.get_model_form_class()(data=self.request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return redirect(self.reverse_change_list_url())
            context = {
                'form': form
            }
            return render(self.request, 'custom/change.html', context)

    def wraps(self,func):
        @functools.wraps(func)
        def inner(request,*args,**kwargs):
            self.request = request
            return func(request,*args,**kwargs)

        return inner

    def get_urls(self):
        from django.conf.urls import url
        app_model_name = self.model_class._meta.app_label,self.model_class._meta.model_name

        patterns = [
            url(r'^$', self.wraps(self.changelist_view),name='%s_%s_changelist'%app_model_name),
            url(r'^add/$', self.wraps(self.add_view),name='%s_%s_add'%app_model_name),
            url(r'^(.+)/delete/$', self.wraps(self.delete_view),name='%s_%s_delete'%app_model_name),
            url(r'^(.+)/change/$', self.wraps(self.change_view),name='%s_%s_change'%app_model_name),
        ]
        patterns += self.extra_url()
        return patterns

    def extra_url(self):
        '''
        扩展url预留的钩子
        :return:
        '''
        return []

    @property
    def changelist_url(self):
        base_url = reverse("{0}:{1}_{2}_changelist".format(self.site.namespace, self.app_label, self.model_name))
        return base_url

    @property
    def change_list_url_params(self):
        query = self.request.GET.get(self.url_save)
        return '{0}?{1}'.format(self.changelist_url,query)

    @property
    def add_url(self):
        base_url = reverse("{0}:{1}_{2}_add".format(self.site.namespace, self.app_label, self.model_name))
        return base_url

    @property
    def add_url_params(self):
        if self.request.GET:
            return self.add_url
        else:
            query = QueryDict(mutable=True)
            query[self.url_save] = self.request.GET.urlencode()
            return '{0}?{1}'.format(self.add_url,query)

    def delete_url(self,pk):
        base_url = reverse("{0}:{1}_{2}_delete".format(self.site.namespace, self.app_label, self.model_name),args=(pk,))
        return base_url

    def change_url(self,pk):
        base_url = reverse('{0}:{1}_{2}_change'.format(self.site.namespace, self.app_label, self.model_name),args=(pk,))
        return base_url



    @property
    def urls(self):
        return self.get_urls(), None, None

class CustomSite:
    def __init__(self):
        self.name  = 'custom'
        self.namespace = 'custom'
        self._registry = {}

    def register(self,model,modelcustom=None):
        if not modelcustom:
           modelcustom= ModelCustom

        self._registry[model] = modelcustom(model,self)

    def login(self,request):
        return HttpResponse('登录页面')

    def logout(self,request):
        return HttpResponse('注销页面')

    def get_urls(self):
        patterns = []
        from django.conf.urls import url,include
        patterns += [
            url(r'^login/',self.login),
            url(r'^logout/', self.logout),
        ]

        for model_class,model_custom_obj in self._registry.items():

            patterns += [
                url(r'^%s/%s/'%(model_class._meta.app_label,model_class._meta.model_name),model_custom_obj.urls)
            ]
        return patterns

    @property
    def urls(self):
        return self.get_urls(),self.name,self.namespace

site = CustomSite()



