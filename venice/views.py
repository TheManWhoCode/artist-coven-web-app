from django.shortcuts import render
from .models import User, UserGallery
import hashlib
from PIL import Image, ExifTags

# Create your views here.
def rotate_image(filepath):
  try:
    image = Image.open(filepath)
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
    image.save(filepath)
    image.close()
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    pass

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
def handle_uploaded_file(f,image_name):
    format = "jpg"
    with open("venice/static/images/"+image_name+"."+format, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def dashboard(request):

    user = User.objects.select_related().filter()
    context = {'user_list': user}
    return render(request,'dashboard.html',context = context)

def signup(request):
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['password'].encode())
        updated_password = hashed_password.hexdigest()
        update_user_db = User.objects.create(username=data['username'],password=updated_password)
        if update_user_db:
            return render(request,'signup_200.html')
        else:
            return render(request,'signup_404.html')
    return render(request,'sign_up.html')


def upload_art(request):
    if request.method=="POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['password'].encode())
        updated_password = hashed_password.hexdigest()
        queried_id = (User.objects.values_list('id').get(password=updated_password))[0]
        handle_uploaded_file(request.FILES['artwork'],data['title'])
        format = "jpg"
        path ="venice/static/images/"+ data['title'] + "." + format
        rotate_image(path)
        update_gallery = UserGallery.objects.create(title=data['title'],
                                                    user_id=queried_id,
                                                    artwork = convertToBinaryData(path)
                                                    )
        if update_gallery:
            return render(request,'upload_200.html')
        else:
            return render(request,'upload_404.html')
    return render(request,'upload_art.html')

def see_art(request):
    user_gallery = UserGallery.objects.select_related('user').filter()
    context = {'user_gallery': user_gallery}
    return render(request,'see_art.html',context=context)