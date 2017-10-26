#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Mona on 2017/10/24


#
# class Foo:
#     def __init__(self,value):
#         self.value = value
#
#     def __getitem__(self, item):
#         print(item)
#         return self.value
#
#
# f = Foo('mona')
# print(f[1])



'''

{#                    <div class="row">#}
{#                        <a href="">全部</a>#}
{#                         {% for obj in l.data_list %}#}
{#                             <a href="{{ l.url }}_search={id:{{ obj.pk }}}">{{ obj }}</a>#}
{#                         {% endfor %}#}
{#                    </div>#}

'''

def foo():
    print(13)


print(foo.__name__)