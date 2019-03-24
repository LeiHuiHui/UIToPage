from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from .models import Sampler
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def index(request):
    template = loader.get_template('UItoPage/index.html')
    context = {
        'result': "<html></html>"
    }
    if request.method == "POST":
        img = request.FILES.get('inputImage')
        save_path = settings.STATICFILES[0] + '/upload/img/' + img.name
        path = default_storage.save(save_path, ContentFile(img.read()))
        context = {
            'result':path
        }
    return render(request, 'UItoPage/index.html', context)

