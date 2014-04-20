from django.conf.urls import patterns, url
from views import default, hello

urlpatterns = patterns(
    '',
    url(r'hello', hello, name="todo_hello"),
    url(r'', default, name="todo_default"),
)
