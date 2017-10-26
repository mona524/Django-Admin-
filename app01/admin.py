from django.contrib import admin
from app01.models import *
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

class Ugg(admin.SimpleListFilter):
    title = _('decade born')
    parameter_name = 'xxxxxx'

    def lookups(self, request, model_admin):
        """
        显示筛选选项
        :param request:
        :param model_admin:
        :return:
        """
        return UserGroup.objects.values_list('id', 'title')

    def queryset(self, request, queryset):
        """
        点击查询时，进行筛选
        :param request:
        :param queryset:
        :return:
        """
        v = self.value()
        return queryset

#方式一：装饰器
@admin.register(UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','nickname','email']
    list_display_links = ('nickname',)
    # list_filter = ('group__title','roles')

    list_select_related = ['group']
    ordering = ['-id', ]
    # prepopulated_fields = {'name':('nickname','email')}

    list_filter = ('group',Ugg)
    list_editable = ('name',)
    search_fields = ('namer', 'email')
    date_hierarchy = 'ctime'


    # exclude = ['name','email']

    # readonly_fields = ['name',]

    fieldsets = (
        ('基本数据', {
            'fields': ('name', )
        }),
        ('其他', {
            'classes': ('collapse', 'wide', 'extrapretty'),  # 'collapse','wide', 'extrapretty'
            'fields': ('email','group','roles'),
        }),
    )
    change_list_template = ['list.py']

    filter_vertical = ("roles",)  # 或filter_horizontal = ("m2m字段",)

    def func(self, request, queryset):
            print(self, request, queryset)
            print(request.POST.getlist('_selected_action'))

    func.short_description = "中文显示自定义Actions"
    actions = [func, ]

    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False

    # 是否显示选择个数
    actions_selection_counter = True



#方式二：参数传入
# admin.site.register(UserInfo,UserAdmin)

admin.site.register(Role)

class UserInfoInline(admin.StackedInline): # TabularInline
    extra = 0
    model = UserInfo

class UserGropuAdmin(admin.ModelAdmin):
    inlines = [UserInfoInline]

admin.site.register(UserGroup,UserGropuAdmin)


