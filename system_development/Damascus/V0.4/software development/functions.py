import sys
import optris.otcsdk as otc
import os
import numpy as np


def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def connect(serialNumber=0):
    otc.Sdk.init(otc.Verbosity_Info, otc.Verbosity_Off, sys.argv[0])
    otc.EnumerationManager.getInstance().addEthernetDetector("192.168.0.0/24")
    
    imager = otc.IRImagerFactory.getInstance().create('native')
    imager.connect(serialNumber)

    
    return imager

class CameraClient(otc.IRImagerClient):

    def __init__(self, imager):
        super().__init__()
        self._imager = imager
        self._imager.addClient(self)
        self._latest_frame = None
        self._frame_updated = False
        self._builder = otc.ImageBuilder(colorFormat=otc.ColorFormat_BGR, widthAlignment=otc.WidthAlignment_OneByte)
    
    def onFrame(self, evt):
        self._latest_frame = evt.clone()
        self._frame_updated = True

    def getImage(self):
        if self._latest_frame is None or not self._frame_updated:
            return None
    
        self._builder.setThermalFrame(thermalFrame=self._latest_frame.thermalFrame)
        self._builder.convertTemperatureToPaletteImage()
        
        image = np.empty((self._builder.getHeight(), self._builder.getWidth(), 3), dtype=np.uint8)
        self._builder.copyImageDataTo(image)
        self._frame_updated = False
        
        return image
    




