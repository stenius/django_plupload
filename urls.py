from django.conf.urls.defaults import *

from django.views.generic import ListView

from models import Upload

urlpatterns = patterns('plupload.views',
        url(r'^$', 'fileUpload', name='plupload_form'),
        url(r'^(?P<fileId>[\d]+)/$','fileDownload',name='plupload_file_download'),
        url(r'^(?P<fileId>[\d]+)/edit/$','fileEdit',name='plupload_file_edit'),
        url(r'^(?P<fileId>[\d]+)/delete/$','fileDelete',name='plupload_file_delete'),
    )
