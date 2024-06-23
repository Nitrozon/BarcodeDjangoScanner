from urllib.request import urlopen

from django.shortcuts import render, redirect
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from PIL import Image
from generator.models import GeneratedBarcode
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile


def scan_barcode(request):
    if request.method == 'POST':
        try:
            barcode_image = request.FILES['barcode_image']
            image = Image.open(barcode_image)
            decoded_objects = decode(image)

            if decoded_objects:
                barcode_data = decoded_objects[0].data.decode('utf-8')
                barcode_data = barcode_data[:-1]  # Removing the extra checksum
                barcode_obj = GeneratedBarcode.objects.get(code=barcode_data)
                return HttpResponse(
                    f'Scanned Barcode: {barcode_obj.code}, Image: <a href="{barcode_obj.image.url}">IMAGE LINK</a>.')
            else:
                return HttpResponse('No barcode found.')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)
    else:
        return render(request, 'barcode_scanner/scan.html')


def image_upload(request):
    context = dict()
    if request.method == 'POST':
        username = "username"
        image_path = request.POST["src"]  # src is the name of input attribute in your html file, this src value is set in javascript code
        image = NamedTemporaryFile()
        #image.write(urlopen(path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.jpg'  # store image in jpeg format
        image.name = name
        if image is not None:
            obj = Image.objects.create(username=username, image=image)  # create a object of Image type defined in your model
            obj.save()
            context["path"] = obj.image.url  #url to image stored in my server/local device
            context["username"] = obj.username
        else :
            return redirect('/')
        return redirect('any_url')
    return render(request, 'barcode_scanner/scan.html', context=context)  # context is like respose data we are sending back to user, that will be rendered with specified 'html file'.