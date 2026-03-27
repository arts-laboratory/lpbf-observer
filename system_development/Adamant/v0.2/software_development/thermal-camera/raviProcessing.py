import time 
import functionFIles as bruh

bruh.clear_terminal()

inputPath = r"C:\Users\mayhe\OneDrive\Documents\Thermal stuff\3_13_2026"
outputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Footage"
outputPathCSV = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-1\Thermal Radiation CSV"
calibrationFile1 = r"C:\Users\mayhe\OneDrive\Documents\GitHub\In-situ-monitoring-of-powder-bed-fusion-additive-manufacturing\system_development\Adamant\v0.2\software_development\thermal-camera\Calibration Files\Xi 400 SN25114061\Kennlinie-25114061-18-150-900.prn"
calibrationFile2 = r"C:\Users\mayhe\OneDrive\Documents\GitHub\In-situ-monitoring-of-powder-bed-fusion-additive-manufacturing\system_development\Adamant\v0.2\software_development\thermal-camera\Calibration Files\Xi 400 SN25114061\Kennlinie-25114061-18-0-250.prn"
calibrationFile3 = r"C:\Users\mayhe\OneDrive\Documents\GitHub\In-situ-monitoring-of-powder-bed-fusion-additive-manufacturing\system_development\Adamant\v0.2\software_development\thermal-camera\Calibration Files\Xi 400 SN25114061\Kennlinie-25114061-18-M20-100.prn"

raviFileNames = bruh.gimmeFileNames(inputPath)
raviFiles = bruh.buildFilePaths(inputPath)

for i, file in enumerate(raviFileNames):
    print(f"{i}: {file}")
    capture = bruh.captureVideo(raviFiles[i])
    bruh.makeVideo(capture, outputPath, raviFileNames[i], True, 188, 90, 125, 125, calibrationFile1, calibrationFile2, calibrationFile3)
    bruh.saveFrameCSV(capture, outputPathCSV, raviFileNames[i], 314, calibrationFile1, calibrationFile2, calibrationFile3)

print("FINALLY DONE!")