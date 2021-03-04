WHITE_DEFAULT_NAME = 'allwhite.bmp'
from PIL import Image, ImageDraw

f_hstretch = 2 #DMD pixels have double spacing in horizontal direction (see Melih thesis)

"""
    Saves ellipse .bmp generated from blank canvas from allwhite_filename.

    Args:
    eX, eY: integer lengths of horizontal and vertical ellipse axes. Default params creates what appears as a circle on the DMD.
    shiftx, shifty: integer displacements of ellipse center from center of image
"""
def create_ellipse_image(eX=300, eY=590, shiftx=0, shifty=0, allwhite_filename=WHITE_DEFAULT_NAME):
    im = Image.open(allwhite_filename)
    x, y = im.size
    print(x,y)
    shiftx *= f_hstretch
    bbox = (x / 2 - eX / 2 + shiftx, y / 2 - eY / 2 + shifty,
            x / 2 + eX / 2 + shiftx, y / 2 + eY / 2 + shifty)
    draw = ImageDraw.Draw(im)
    draw.ellipse(bbox, fill=0)
    del draw
    im.show() #this is how the image on DMD will look

    #unstretch the image, the outputted image will look wrong on the computer but correct on DMD
    new_im = im.resize((int(x/f_hstretch), y))
    new_im.save("ellipse.bmp")

"""
    Saves bar .bmp generated from blank canvas from allwhite_filename.

    Args:
    l_bar, w_bar: integer lengths of horizontal and vertical ellipse axes
    shiftx, shifty: integer displacements of bar center from center of image
"""

def create_bar_image(l_bar=1, w_bar=600, shiftx=0, shifty=0, allwhite_filename=WHITE_DEFAULT_NAME):
    # get an image
    im = Image.open(allwhite_filename)
    x, y = im.size
    bbox = (x / 2 - l_bar / 2 + shiftx, y / 2 - w_bar / 2 + shifty,
            x / 2 + l_bar / 2 + shiftx, y / 2 + w_bar / 2 + shifty)
    draw = ImageDraw.Draw(im)
    draw.rectangle(bbox, fill=0)
    del draw
    im.show()
    new_im = im.resize((int(x/f_hstretch), y))
    new_im.save("bar.bmp")


def create_dark_image(allwhite_filename=WHITE_DEFAULT_NAME):
    """
    Saves dark .bmp generated from blank canvas from allwhite_filename.
    """
    import PIL.ImageOps

    image = Image.open(allwhite_filename)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.show()
    inverted_image.save('alldark.bmp')

def create_USAFtarget_image(resize_factor = 1, allwhite_filename=WHITE_DEFAULT_NAME, usaf_filename="1951usaf_test_target.bmp",
    shiftx=0, shifty=0):
    background_im = Image.open(allwhite_filename)
    xb, yb = background_im.size
    usaf_im = Image.open(usaf_filename)
    x, y = usaf_im.size
    usaf_im = usaf_im.resize((round(x*resize_factor), round(y*resize_factor)), resample=PIL.Image.LANCZOS)
    x, y = usaf_im.size
    corner = (round((xb - x)/2), round((yb - y)/2))
    background_im.paste(usaf_im, corner)
    background_im.show()
    new_im = background_im.resize((int(xb/f_hstretch), yb))
    background_im.save('usaf.bmp')

def create_triangle_image(shiftx=0, allwhite_filename=WHITE_DEFAULT_NAME):
    im = Image.open(allwhite_filename)
    x, y = im.size
    draw = ImageDraw.Draw(im)
    draw.polygon(((y/2 + x/2 + shiftx, 0), (x/2-y/2 + shiftx,y), (x/2+y/2 + shiftx, y)), fill=0, outline=0)
    del draw
    im.show()
    new_im = im.resize((int(x/f_hstretch), y))
    new_im.save('triangle.bmp')



# create_ellipse_image(eX=100, eY=100)
# create_ellipse_image(eX=100, eY=200)
# create_ellipse_image(eX=30, eY=60)
# create_dark_image()
# create_bar_image(l_bar = 50, w_bar=100)
# create_triangle_image()
create_bar_image(l_bar = 500, w_bar = 900, shiftx = 250)
# create_USAFtarget_image(1)
