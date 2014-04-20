# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect


def default(request):
    return render_to_response(
        'todo/default.html',
        {}, context_instance=template.RequestContext(request),)


def hello(request):
    return HttpResponseRedirect(reverse('todo_default') + "?q=q#f=f")
