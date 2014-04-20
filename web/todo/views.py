# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse


def default(request):
    return TemplateResponse(
        request,
        'todo/default.html',
        {'request': request, })


def hello(request):
    return HttpResponseRedirect(reverse('todo_default') + "?q=q#f=f")
