import functionFIles as bruh

bruh.clear_terminal()

inputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\In-situ-monitoring-of-powder-bed-fusion-additive-manufacturing\system_development\Damascus\V0.4\software development\Recordings"
outputPath = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-2\Processed Data\Footage"
outputPathCSV = r"C:\Users\mayhe\OneDrive\Documents\GitHub\Dataset-battery-tab-laser-welding\data\Dataset-2\Processed Data\Thermal Radiation CSV"

fileNames = bruh.gimmeFileNames(inputPath)
filePaths = bruh.buildFilePaths(inputPath)

for i, path in enumerate(filePaths):
    bruh.saveVideo(filePaths[i], fileNames[i], outputPath)

