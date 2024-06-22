import io
from django.http import HttpResponse
from barcode import Code39
from barcode.writer import ImageWriter
from .models import GeneratedBarcode
from django.shortcuts import render


def generate_barcode(request, code):
    code_obj = Code39(code, writer=ImageWriter())
    buffer = io.BytesIO()
    code_obj.write(buffer)
    buffer.seek(0)
    barcode_obj, created = GeneratedBarcode.objects.get_or_create(code=code)

    if created:
        barcode_obj.image.save(f'{code}.png', buffer, save=True)
        action_performed = "created"
    else:
        action_performed = "fetched"

    myResponse = f'Barcode "{code}" {action_performed} successfully! <a href="{barcode_obj.image.url}">IMAGE LINK</a>'

    return HttpResponse(myResponse)

def generate_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        # Add your logic to handle the code here
        return HttpResponse(f'Code {code} generated successfully!')
    return render(request, 'barcode reader/generate.html')