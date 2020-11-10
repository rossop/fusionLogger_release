# Author- rossop
# Description - 

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import sys
import logging

# Set up fusionLogger
try:
    app = adsk.core.Application.get()
    ui  = app.userInterface
    user = 'hicksb'
    filename = 'fusion360_' + user + '.log'
    
    fusion_logger = logging.getLogger(__name__)
    fusion_logger.setLevel(logging.INFO)

    LOG_FORMAT = '%(asctime)s|%(msecs)03d|%(process)d|%(filename)s|%(levelname)s|%(message)s'
    formatter = logging.Formatter(LOG_FORMAT)
    
    if sys.platform == 'win32' or sys.platform == 'win64':
        desktop = os.path.expanduser("~\Desktop")
    elif sys.platform == 'darwin':
        desktop = os.path.expanduser("~/Desktop")
    PATH = os.path.join(desktop, filename)


    ui.messageBox(PATH)

    file_handler = logging.FileHandler(PATH)
    file_handler.setFormatter(formatter)

    fusion_logger.addHandler(file_handler)
    
except:
    if ui:
        ui.messageBox('Error:\n{}'.format(traceback.format_exc()))

# Global variable used to maintain a reference to all event handlers.
try:
    app = adsk.core.Application.get()
    ui  = app.userInterface
    mouse = adsk.core.MouseEvent
    camera = app.cameraChanged

    # Global variable used to maintain a reference to all event handlers.
    handlers = []
    command_var = adsk.core.Command

    _userId = app.userId
    _userName = app.userName
    _version = app.version

except:
    if ui:
        ui.messageBox('Error:\n{}'.format(traceback.format_exc()))


# Event handler for the Comand start event
class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
        app =adsk.core.Application.get()
        ui = app.userInterface
    

    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)

        # Code to react to the event.
        try:
            objectType = str(eventArgs._get_objectType())
            commandId = str(eventArgs._get_commandId())
            editObj = str(app.activeEditObject)
            
            INFO = f'{_userId}|{_userName}|{_version}|{self.__class__}|{editObj}|{objectType}|{commandId}'
            fusion_logger.info(INFO)
            # obj_list = [method_name for method_name in dir(eventArgs)
            #           if callable(getattr(eventArgs, method_name))]
            # fusion_logger.info('obj list:{}'.format(str(obj_list)))

        except:
            error_message = 'Logger failed:\n{}'.format(traceback.format_exc())
            ui.messageBox(error_message)   


class MyCameraChangedHandler(adsk.core.CameraEventHandler):
    def __init__(self):
        super().__init__()
        app =adsk.core.Application.get()
        ui = app.userInterface

    def notify(self, args):
        eventArgs = adsk.core.CameraEventArgs.cast(args)

        try:
            objectType = str(eventArgs._get_objectType())
            viewport = str(eventArgs.viewport)
            editObj = str(app.activeEditObject)

            INFO = f'{_userId}|{_userName}|{_version}|{self.__class__}|{editObj}|{objectType}|{viewport}'
            fusion_logger.info(INFO)

        except:
            ui = adsk.core.Application.get().userInterface
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        INFO = f'{_userId}|{_userName}|{_version}|session start'
        fusion_logger.info(INFO)
        ui.messageBox('Fusion Logger Started')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # clearLoggingHandlers()
        INFO = f'{_userId}|{_userName}|{_version}|session end'
        fusion_logger.info(INFO)
        ui.messageBox('Fusion Logger Stopped')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# setup handlers to trigger loggers
try:
    # "userInterface_var" is a variable referencing a UserInterface object.
    onCommandStarting = MyCommandStartingHandler()
    ui.commandStarting.add(onCommandStarting)
    handlers.append(onCommandStarting)

    onCameraChanged = MyCameraChangedHandler()
    camera.add(onCameraChanged)
    handlers.append(onCameraChanged)


except:
    ui.messageBox('Handlers not set: \n{}'.format(traceback.format_exc())) 