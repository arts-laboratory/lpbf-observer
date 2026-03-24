import numpy as np
import cv2
import functionFIles as ff

ff.clear_terminal()

ravi_file_name = 'Run1.ravi'
input = r"C:\Users\mayhe\OneDrive\Documents\Thermal stuff\3_13_2026"
calibrationFile = r"C:\Users\mayhe\OneDrive\Documents\GitHub\In-situ-monitoring-of-powder-bed-fusion-additive-manufacturing\system_development\Adamant\v0.2\software_development\thermal-camera\Calibration Files\Xi 800 SN25114061\Kennlinie-25114061-18-150-900.prn"

calibrationData = np.loadtxt(calibrationFile)
    
floats = calibrationData[:, 0].astype(int)
temperatures = calibrationData[:, 1]

print(f"Floats: {floats}")
print(f"Temperatures: {temperatures}")