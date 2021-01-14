import uuid
from urllib import request as requests
from django.core.files.base import ContentFile

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import never_cache

from .models import ImageUpload
from .forms import ImageUploadForm, ImageEditForm


@never_cache
def post_list(request):
    posts = ImageUpload.objects.all()
    return render(request, 'task/post/list.html', {'posts': posts})


@never_cache
def post_add(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        url = ''
        if form.is_valid():
            new_image = ImageUpload()
            if form.cleaned_data.get('image') and not form.cleaned_data.get('url_image'):
                new_image.image = form.cleaned_data.get('image')
                new_image.prev_image = form.cleaned_data.get('image')
                new_image.save()
                url = reverse('task:post_edit', args=(new_image.pk,))
            elif form.cleaned_data.get('url_image') and not form.cleaned_data.get('image'):
                result = requests.urlopen(form.cleaned_data.get('url_image'))
                new_image.image.save(f'{uuid.uuid4()}.jpg', ContentFile(result.read()), save=False)
                new_image.prev_image.save(f'{uuid.uuid4()}.jpg', ContentFile(result.read()), save=False)
                new_image.save()
                url = reverse('task:post_edit', args=(new_image.pk,))
            else:
                return render(request, 'task/post/error.html')

        a = 3
        return HttpResponseRedirect(url)
    else:
        form = ImageUploadForm
        return render(request, 'task/post/add.html', {'form': form})


@never_cache
def post_edit(request, idd):
    image = ImageUpload.objects.get(pk=idd)
    if request.method == 'POST':
        form = ImageEditForm(request.POST)
        if form.is_valid():
            width = form.data['width'] if form.data['width'] else image.image.width
            height = form.data['height'] if form.data['height'] else image.image.height
            # img = Image.open(image.image)
            # new_img = img.convert('RGB')
            # resized_img = new_img.resize((width, height), Image.ANTIALIAS)
            # filestream = BytesIO()
            # file_ = resized_img.save(filestream, 'JPEG', quality=90)
            image.save(int(width), int(height))
        return HttpResponseRedirect(reverse('task:post_list'))
    else:
        form = ImageEditForm()
        return render(request, 'task/post/edit.html', {'image': image, 'form': form})

