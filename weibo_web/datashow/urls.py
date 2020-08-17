"""weibo_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from datashow import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^comment/$', views.comment, name='comment'),
    url(r'^user_config/$', views.user_config, name='user_config'),
    url(r'^user_results/$', views.user_results, name='user_results'),
    url(r'^topic_results/$', views.topic_results, name='topic_results'),
    url(r'^comment_config/$', views.comment_config_form, name='comment_config'),
    url(r'^comment_results/$', views.comment_results, name='comment_results'),
    url(r'^follow_config/$', views.follow_config, name='follow_config'),
    url(r'^follow_results/$', views.follow_results, name='follow_results'),
    url(r'^hotsearch_results/$', views.hotsearch_result, name='hotsearch_results'),
    # url(r'^weibo_filter/$',views.weibo_filter,name='weibo_filter'),
    url(r'^weibo_filter/$', views.weibo_filter, name='weibo_filter'),
    url(r'^comment_filter/$',views.comment_filter,name='comment_filter'),
    url(r'^topic_filter/$', views.topic_filter, name='topic_filter'),
    url(r'^wordcloud/$',views.wordcloud,name='wordcloud')
]
