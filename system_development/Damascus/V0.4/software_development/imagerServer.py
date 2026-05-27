import threading 
import cv2
import functions as fun

HOST = "127.0.0.1"
commandPort = 5000
videoPort = 5100

fun.clear_terminal()

stopFeed = threading.Event()
imager = fun.connect()
client = fun.CameraClient(imager)

socketThread = threading.Thread(
    target=fun.runSocketServer,
    args= (client, HOST, commandPort, stopFeed, imager),
    daemon=True
    )

socketThread.start()

fun.seePreview(client, imager, stopFeed, HOST, videoPort)

cv2.destroyAllWindows()
imager.stopRunning()


