WHITE_DEFAULT_NAME = 'allwhite.bmp'


def create_ellipse_image(eX=300, eY=590, shiftx=0, shifty=0, allwhite_filename=WHITE_DEFAULT_NAME):
    """
    Saves ellipse .bmp generated from blank canvas from allwhite_filename.

    Args:
    eX, eY: integer lengths of horizontal and vertical ellipse axes. Default params creates what appears as a circle on the DMD.
    shiftx, shifty: integer displacements of ellipse center from center of image
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from PIL import Image, ImageDraw

    im = Image.open(allwhite_filename)
    x, y = im.size
    #

    bbox = (x / 2 - eX / 2 + shiftx, y / 2 - eY / 2 + shifty,
            x / 2 + eX / 2 + shiftx, y / 2 + eY / 2 + shifty)
    draw = ImageDraw.Draw(im)
    draw.ellipse(bbox, fill=0)
    del draw
    im.show()
    im.save("ellipse.bmp")


def create_bar_image(l_bar=1, w_bar=600, shiftx=0, shifty=0, allwhite_filename=WHITE_DEFAULT_NAME):
    """
    Saves bar .bmp generated from blank canvas from allwhite_filename.

    Args:
    l_bar, w_bar: integer lengths of horizontal and vertical ellipse axes
    shiftx, shifty: integer displacements of bar center from center of image
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from PIL import Image, ImageDraw

    # get an image
    im = Image.open(allwhite_filename)
    x, y = im.size
    bbox = (x / 2 - l_bar / 2 + shiftx, y / 2 - w_bar / 2 + shifty,
            x / 2 + l_bar / 2 + shiftx, y / 2 + w_bar / 2 + shifty)
    draw = ImageDraw.Draw(im)
    draw.rectangle(bbox, fill=0)
    del draw
    im.show()
    im.save("bar.bmp")


def create_dark_image(allwhite_filename=WHITE_DEFAULT_NAME):
    """
    Saves dark .bmp generated from blank canvas from allwhite_filename.
    """
    from PIL import Image
    import PIL.ImageOps

    image = Image.open(allwhite_filename)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.show()
    inverted_image.save('alldark.bmp')

def create_USAFtarget_image(resize_factor = 1, allwhite_filename=WHITE_DEFAULT_NAME, usaf_filename="1951usaf_test_target_stretch.bmp",
	shiftx=0, shifty=0):
	from PIL import Image
	import PIL

	background_im = Image.open(allwhite_filename)
	xb, yb = background_im.size
	usaf_im = Image.open(usaf_filename)
	x, y = usaf_im.size
	usaf_im = usaf_im.resize((round(x*resize_factor), round(y*resize_factor)), resample=PIL.Image.LANCZOS)
	x, y = usaf_im.size
	corner = (round((xb - x)/2), round((yb - y)/2))
	background_im.paste(usaf_im, corner)
	background_im.show()
	background_im.save('usaf.bmp')

# create_ellipse_image(eX=100, eY=200)
# create_dark_image()
# create_bar_image()

create_USAFtarget_image(1)
