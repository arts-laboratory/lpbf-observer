import threading 
import cv2
import functions as fun

HOST = "127.0.0.1"
PORT = 5000

fun.clear_terminal()

stopFeed = threading.Event()
imager = fun.connect()
client = fun.CameraClient(imager)

socketThread = threading.Thread(
    target=fun.runSocketServer,
    args= (client, HOST, PORT, stopFeed, imager),
    daemon=True
    )

socketThread.start()

fun.seePreview(client, imager, stopFeed)

cv2.destroyAllWindows()
imager.stopRunning()


