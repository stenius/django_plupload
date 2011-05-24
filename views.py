from django.shortcuts import render_to_response, get_object_or_404,HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

import datetime

from models import Upload


#also need to make fileDetail

from forms import UploadFileForm
from forms import UploadedFileForm

from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.encoding import smart_str
import os
import tempfile
from shutil import move
import shutil
import logging

@login_required
def fileUpload(request):
    c = RequestContext(request, {})
    if request.method == 'POST':
        name = request.REQUEST.get('name','')
        uploaded_file = request.FILES['file']
        if not name:
            name = uploaded_file.name
        name,ext = os.path.splitext(name)
        #check to see if a user has uploaded a file before, and if they have
        #not, make them a upload directory
        upload_dir = os.path.join(settings.MEDIA_ROOT, request.user.username)
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)
            pass

        dest_path = '{upload_url}{ds}{file}{ext}'.format(upload_url=upload_dir,ds=os.sep,file=name,ext=ext)
        
        chunk = request.REQUEST.get('chunk','0')
        chunks = request.REQUEST.get('chunks','0')


        with open(dest_path,('wb' if chunk==0 else 'ab')) as f:
            for content in uploaded_file.chunks():
                f.write(content)
        if int(chunk) + 1 >= int(chunks):
            u,isNewFile = Upload.objects.get_or_create(file_path=dest_path, defaults={'user':request.user,'filename':(name+ext),'datetime':datetime.datetime.now()})
            u.save()
        if request.is_ajax():
                response = HttpResponse('{"jsonrpc" : "2.0", "result" : null, "id" : "id"}', mimetype='text/plain; charset=UTF-8')
                response['Expires'] = 'Mon, 1 Jan 2000 01:00:00 GMT'
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
                response['Pragma'] = 'no-cache'
                return response
        else:
            return HttpResponseRedirect(reverse('plupload_form'))
        #return HttpResponse('ok',mimetype='text/plain')
    else:
        form = UploadFileForm()
    #c['uploads'] = Upload.objects.all()
    c['uploads'] = Upload.objects.filter().exclude(file_path='')
    c['untitled_uploads'] = c['uploads'].filter(title='').filter(user=request.user)
    c['uploads'] = Upload.objects.filter().exclude(title='')
    c['form'] = form
    return render_to_response('plupload/files.html', c)

@login_required
def fileDownload(request,fileId):
    upload = get_object_or_404(Upload,id=fileId)
    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(upload.filename)
    response['X-Accel-Redirect'] = smart_str('/protected/' + upload.user.username + '/' + upload.filename)
    return response

@login_required
def fileEdit(request,fileId):
    upload = get_object_or_404(Upload,id=fileId)
    if request.method == 'POST':
        form = UploadedFileForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            upload.title = title
            upload.save()
            return HttpResponseRedirect(reverse('plupload_form'))
    c = RequestContext(request, {})
    c['upload'] = upload
    c['form'] = UploadedFileForm()
    return render_to_response('plupload/file_edit.html', c)

@login_required
def fileDelete(request,fileId):
    upload = get_object_or_404(Upload,id=fileId)
    if request.method == 'POST':
        if upload.user == request.user:
            upload.title = ''
            upload.delete()
            #upload.save()
            return HttpResponseRedirect(reverse('plupload_form'))
    c = RequestContext(request, {})
    c['upload'] = upload
    if request.user != upload.user:
        return render_to_response('plupload/file_delete_failed.html', c)
    else:
        return render_to_response('plupload/file_delete_confirm.html', c)
