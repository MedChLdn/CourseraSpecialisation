from zipfile import ZipFile
import PIL
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np


# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

list_files = []
def ext_zip(zip_file):
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('Project')
        list_files = zip_ref.namelist().copy()
        print(list_files)
    return list_files

def path(file):
    path = 'Project'
    return '{}/{}'.format(path, file)

def faces_sheet(lst_files):
    from PIL import Image
    from PIL import ImageDraw   
    
    for file in lst_files:
        img = cv.imread(path(file))
        #create grey scale
        grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #create a PIL image object
        pil_img = Image.open(path(file))
        #resized_pil_img = pil_img.resize((round(pil_img.size[0]*0.5), round(pil_img.size[1]*0.5)))
        #binary_img = cv.threshold(img,140,255,cv.THRESH_BINARY)[1]
        get_faces = face_cascade.detectMultiScale(grey_img, 1.2, 6)

        #pil_img = pil_img.convert('RGB')
        #drawing = ImageDraw.Draw(pil_img)
        #print(get_faces)

        list_faces = []
        for x, y, w, h in get_faces:
            crop_img = pil_img.crop((x, y, x+w, y+h))
            crop_img.thumbnail((100, 100))
            cv.rectangle(img, (x, y), (x+w, y+h),(255, 0, 0), 2)
            #drawing.rectangle((x, y, x+w, y+h))
            #faces = [x] + [y] + [w] + [h]
            #cv.imshow("img", img)
            #cv.waitkey()
            list_faces.append(crop_img)
        if len(list_faces) == 0:
            print("Results found in file {}".format(file))
            print("But there were no faces in that file!")
            continue
        else:
            contact_sheet = PIL.Image.new(list_faces[0].mode, (list_faces[0].width*5,list_faces[0].height*2))
        #x1, y1, w1, h1 = list_faces[0]
        #first_face = pil_img.crop((x1, y1, w1, h1))
        #contact_sheet = PIL.Image.new(first_face.mode, (first_face.width*5,first_face.height*2))
            

        a = 0
        b = 0
        if list_faces != 0:
            for face in list_faces:
                contact_sheet.paste(face, (a, b))
                if a+100 == contact_sheet.width:
                    a=0
                    b=b+100
                else:
                    a=a+100
            print("Results found in file {}".format(file))
            display(contact_sheet)       

def word_srch(list_files, word):
    list_pic_name = []
    for f in list_files:
        str_text = pytesseract.image_to_string(path(f))
        if word in str_text:
            list_pic_name.append(f)
    print(list_pic_name)
    return faces_sheet(list_pic_name)


h = ext_zip("readonly/images.zip")
text = input("Enter the word here: ")
word_srch(h, text)
#faces_sheet(["a-3.png"])
