from __future__ import print_function
import sys
# import all the stuff from mvIMPACT Acquire into the current scope
from mvIMPACT import acquire
# import all the mvIMPACT Acquire related helper function such as 'conditionalSetProperty' into the current scope
# If you want to use this module in your code feel free to do so but make sure the 'Common' folder resides in a sub-folder of your project then
from mvIMPACT.Common import exampleHelper
 
# For systems with NO mvDisplay library support
import ctypes
from PIL import Image
import numpy
def get_pDev():
    devMgr = acquire.DeviceManager()
    
    pDev = devMgr.getDevice(0)
    if pDev == None:
        exampleHelper.requestENTERFromUser()
        sys.exit(-1)
    return pDev
def acquire_image(): 
    devMgr = acquire.DeviceManager()
    # pDev = exampleHelper.getDeviceFromUserInput(devMgr)
    pDev = devMgr.getDevice(0)
    if pDev == None:
        exampleHelper.requestENTERFromUser()
        sys.exit(-1)
    pDev.open()
    
    #print("Please enter the number of buffers to capture followed by [ENTER]: ", end='')
    framesToCapture = 1 #exampleHelper.getNumberFromUser()
    if framesToCapture < 1:
        print("Invalid input! Please capture at least one image")
        sys.exit(-1)
    
    fi = acquire.FunctionInterface(pDev)
    statistics = acquire.Statistics(pDev)
    
    while fi.imageRequestSingle() == acquire.DMR_NO_ERROR:
        #print("Buffer queued")
        pass
    
    pPreviousRequest = None
    
    exampleHelper.manuallyStartAcquisitionIfNeeded(pDev, fi)
    for i in range(framesToCapture):
        requestNr = fi.imageRequestWaitFor(10000)
        if fi.isRequestNrValid(requestNr):
            pRequest = fi.getRequest(requestNr)
            if pRequest.isOK:
                if i%100 == 0:
                    print("Info from " + pDev.serial.read() +
                            ": " + statistics.framesPerSecond.name() + ": " + statistics.framesPerSecond.readS() +
                            ", " + statistics.errorCount.name() + ": " + statistics.errorCount.readS() +
                            ", " + statistics.captureTime_s.name() + ": " + statistics.captureTime_s.readS())
                
                # For systems with NO mvDisplay library support
                cbuf = (ctypes.c_char * pRequest.imageSize.read()).from_address(int(pRequest.imageData.read()))
                channelType = numpy.uint16 if pRequest.imageChannelBitDepth.read() > 8 else numpy.uint8
                arr = numpy.fromstring(cbuf, dtype = channelType)
                arr.shape = (pRequest.imageHeight.read(), pRequest.imageWidth.read(), pRequest.imageChannelCount.read())
                arr = arr.reshape(arr.shape[0],arr.shape[1])
                if pRequest.imageChannelCount.read() == 1:
                    img = Image.fromarray(arr)
                else:
                    img = Image.fromarray(arr, 'RGBA' if alpha else 'RGB')
            if pPreviousRequest != None:
                pPreviousRequest.unlock()
            pPreviousRequest = pRequest
            fi.imageRequestSingle()
            #img.show()
        else:
            # Please note that slow systems or interface technologies in combination with high resolution sensors
            # might need more time to transmit an image than the timeout value which has been passed to imageRequestWaitFor().
            # If this is the case simply wait multiple times OR increase the timeout(not recommended as usually not necessary
            # and potentially makes the capture thread less responsive) and rebuild this application.
            # Once the device is configured for triggered image acquisition and the timeout elapsed before
            # the device has been triggered this might happen as well.
            # The return code would be -2119(DEV_WAIT_FOR_REQUEST_FAILED) in that case, the documentation will provide
            # additional information under TDMR_ERROR in the interface reference.
            # If waiting with an infinite timeout(-1) it will be necessary to call 'imageRequestReset' from another thread
            # to force 'imageRequestWaitFor' to return when no data is coming from the device/can be captured.
            print("imageRequestWaitFor failed (" + str(requestNr) + ", " + acquire.ImpactAcquireException.getErrorCodeAsString(requestNr) + ")")
    exampleHelper.manuallyStopAcquisitionIfNeeded(pDev, fi)
    #exampleHelper.requestENTERFromUser()
    return arr

