import socket


def create_ellipse_image(allwhite_filename='allwhite.bmp'):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from PIL import Image, ImageDraw
    # get an image
    im = Image.open(allwhite_filename)

    x, y = im.size
    # Size of Bounding Box for ellipse #this creates what appears as a circle on the DMD
    eX, eY = 300, 590
    # eX, eY = 300, 300
    shiftx, shifty = -45, -40

    bbox = (x / 2 - eX / 2 + shiftx, y / 2 - eY / 2 + shifty,
            x / 2 + eX / 2 + shiftx, y / 2 + eY / 2 + shifty)
    draw = ImageDraw.Draw(im)
    draw.ellipse(bbox, fill=0)
    del draw

    im.save("out.bmp")


class DMD():
    """Communicate with the DMD through the beaglebone board."""

    def __init__(self, PEM_IP):
        self.PEM_IP = PEM_IP
        # working settings from Fermi3
        self.PEM_PORT = 0x5555
        self.BUFFER_SIZE = 1024
        self.pem_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pem_socket.settimeout(8)

    def version_checker(self):
        self.pem_socket.connect((self.PEM_IP, self.PEM_PORT))
        with self.pem_socket as s:
            header = [4, 1, 0, 0, 1, 0]
            # data has N bytes
            data = [0x30]
            checksum = sum(header + data) % 0x100
            command = header + data + [checksum]
            msg = bytes(command)
            s.send(msg)
            recdata = s.recv(self.BUFFER_SIZE)
        self.pem_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(list(recdata[0:6]))
        print(recdata[6:])

    def send_image(self, image_filename):

        def sendData(header, data):
            checksum = sum(header + data) % 0x100
            command = header + data + [checksum]
            msg = bytes(command)
            pem.send(msg)
            try:
                recdata = pem.recv(self.BUFFER_SIZE)
            except socket.timeout:
                print("Timed out on receive")
                return

            resp = list(recdata[0:6])
            if resp[0] == 1:
                print("Error")
                print(int(recdata[6]))
            elif resp[0] != 3:
                print(recdata[6:])

        # header has six bytes
        #[packettype, cmd1, cmd2, flags, payloadlenlsb, payloadlenmsb]
        startheader = [2, 1, 5, 1, 0xff, 0xff]
        midheader = [2, 1, 5, 2, 0xff, 0xff]
        endheader = [2, 1, 5, 3, 0, 0]

        with open(image_filename, "rb") as file:
            with self.pem_socket as pem:
                pem.connect((self.PEM_IP, self.PEM_PORT))
                # header must be compatible with length of data
                # data is an array of bytes
                data = list(file.read(65535))
                sendData(startheader, data)
                while (1):
                    data = list(file.read(65535))
                    if len(data) != 65535:
                        break
                    sendData(midheader, data)

                remainingBytes = len(data)
                endheader[4] = remainingBytes & 0xff
                endheader[5] = (remainingBytes >> 8) & 0xff
                sendData(endheader, data)
        self.pem_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Image successfully sent")


# create_ellipse_image()

PEM_IP = '192.168.1.16'
my_DMD = DMD(PEM_IP)
# my_DMD.version_checker()
my_DMD.send_image('out.bmp')
