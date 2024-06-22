from django.shortcuts import render
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from PIL import Image
from generator.models import GeneratedBarcode


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