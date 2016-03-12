import cv2
import os
from PIL import Image
from collections import namedtuple
import numpy


CASCADE = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'haarcascade_frontalface_default.xml')
SOONERLATER = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'soonerlater.png')


Coordinate = namedtuple('Coordinate', ['x', 'y'])
_Rectangle = namedtuple('_Rectangle', ['topleft', 'bottomright'])


class Rectangle(_Rectangle):
    @property
    def flattened(self):
        return self.topleft.x, self.topleft.y, self.bottomright.x, self.bottomright.y

    @property
    def width(self):
        return abs(self.bottomright.x - self.topleft.x)

    @property
    def height(self):
        return abs(self.bottomright.y - self.topleft.y)

    @property
    def center(self):
        return Coordinate(self.topleft.x + int(self.height/2),
                          self.topleft.y + int(self.width/2))


def recognize_faces(image, cascade=CASCADE):
    cascade = cv2.CascadeClassifier(cascade)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5,
            minSize=(20, 20), flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    return (Rectangle(Coordinate(x, y), Coordinate(x + w, y + h)) for (x, y, w, h) in faces)


def soonerize(image, sooner=None, pil=False):
    if sooner is None:
        sooner = cv2.imread(SOONERLATER, cv2.CV_LOAD_IMAGE_UNCHANGED)

    faces = recognize_faces(image)

    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    pil_sooner = Image.fromarray(cv2.cvtColor(sooner, cv2.COLOR_BGRA2RGBA), mode='RGBA')

    for rect in faces:
        resized = pil_sooner.copy()
        resized.thumbnail((rect.width, rect.height))

        box = (rect.center.x - int(resized.width/2),
               rect.center.y - int(resized.height/2))

        pil_image.paste(resized, box, resized)

    if pil:
        return pil_image

    return cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)