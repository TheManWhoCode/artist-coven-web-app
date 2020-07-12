from django.shortcuts import render
from .models import User, UserGallery
import hashlib
from PIL import Image, ExifTags
from django.db import connection
import sqlite3

from sqlite3 import Error

# Create your views here.

def get_id(db_conn, password):
    cur = db_conn.cursor()
    cur.execute("select id from venice_user where password = ?", (password,))
    rows = cur.fetchall()

    for row in rows:
        return row

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

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
    dir_name= "C:\\Users\HoangChuong\\fromHeroku\mongoteri\\venice\static\images\\"
    format = "jpg"
    print("path is ",dir_name+image_name+"."+format)
    with open(dir_name+image_name+"."+format, 'wb+') as destination:
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
        print("password is ",data['password'])
        hashed_password = hashlib.sha256(data['password'].encode())
        updated_password = hashed_password.hexdigest()
        print(type(updated_password))
        print("updated password is ",updated_password)


        dir_name_db = "C:\\Users\HoangChuong\\fromHeroku\mongoteri\db.sqlite3"
        dir_name = "C:\\Users\HoangChuong\\fromHeroku\mongoteri\\venice\static\images\\"

        dbConnection = create_connection(dir_name_db)
        queried_id = get_id(dbConnection,updated_password)
        queried_id = queried_id[0]
        print("queried id is ",queried_id)
        handle_uploaded_file(request.FILES['artwork'],data['title'])
        format = "jpg"
        path = dir_name + data['title'] + "." + format
        print("path is ",path)
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