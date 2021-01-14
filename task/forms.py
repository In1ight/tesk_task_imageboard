from django import forms


class ImageUploadForm(forms.Form):
    url_image = forms.URLField(label='Ссылка', required=False)
    image = forms.ImageField(label='Файл', required=False)


class ImageEditForm(forms.Form):
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)
