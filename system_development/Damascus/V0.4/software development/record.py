import functions as fun
import datetime
import time
import cv2

fun.clear_terminal()

imager = fun.connect()

print("Current focus position:", imager.getFocusMotorPosition())

client = fun.CameraClient(imager)

imager.runAsync()  # starts grabbing frames in background

recording = False       
writer = None
record_start = None

cv2.namedWindow('Thermal Camera')
cv2.createTrackbar('Focus', 'Thermal Camera', int(imager.getFocusMotorPosition()), 100, lambda x: imager.setFocusMotorPosition(x))

while True:
    image = client.getImage()

    if image is not None:
        cv2.imshow('Thermal Camera (Press "q" to stop)', image)
    
        if recording:
            writer.write(image)
            elapsed = time.time() - record_start
            if elapsed >= 15:
                recording = False
                writer.release()
                writer = None
                print("Recording saved!")

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        new_pos = max(0, imager.getFocusMotorPosition() - 1)
        imager.setFocusMotorPosition(new_pos)
        cv2.setTrackbarPos('Focus', 'Thermal Camera', int(new_pos))
    elif key == ord('d'):
        new_pos = min(100, imager.getFocusMotorPosition() + 1)
        imager.setFocusMotorPosition(new_pos)
        cv2.setTrackbarPos('Focus', 'Thermal Camera', int(new_pos))
    elif key == ord('z'):
        new_pos = max(0, imager.getFocusMotorPosition() - 10)
        imager.setFocusMotorPosition(new_pos)
        cv2.setTrackbarPos('Focus', 'Thermal Camera', int(new_pos))
    elif key == ord('c'):
        new_pos = min(100, imager.getFocusMotorPosition() + 10)
        imager.setFocusMotorPosition(new_pos)
        cv2.setTrackbarPos('Focus', 'Thermal Camera', int(new_pos))    
    elif key == ord('r') and not recording:
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Recordings/{date}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(filename, fourcc, imager.getActiveOperationMode().getFramerate(), (imager.getWidth(), imager.getHeight()))
        recording = True
        record_start = time.time()
        print("Recording started!")

cv2.destroyAllWindows()
imager.stopRunning()
