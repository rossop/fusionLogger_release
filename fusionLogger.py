# Author- rossop
# Description - 

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import logging

# Global variable used to maintain a reference to all event handlers.
try:
    app = adsk.core.Application.get()
    ui  = app.userInterface
    mouse = adsk.core.MouseEvent

    # Global variable used to maintain a reference to all event handlers.
    handlers = []
    command_var = adsk.core.Command
except:
    if ui:
        ui.messageBox('Error:\n{}'.format(traceback.format_exc()))

# def checkHandler(self, args):
#     # Code to react to the event.
#     app =adsk.core.Application.get()
#     ui = app.userInterface
#     try:
#         ui.messageBox('In {} event handler.'.fomat(self.__name__)
#     except:
#         ui.messageBox('Error:\n{}'.format(traceback.format_exc()))
#     return None


class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
        app =adsk.core.Application.get()
        ui = app.userInterface

    def setup_logger(self, logger):
        self.logger = logger

    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
        try:
            ui.messageBox('In MyCommandStartingHandler event handler.')
        except:
            ui.messageBox('Error:\n{}'.format(traceback.format_exc()))

# Event handler for the commandTerminated event.
class MyCameraEventdHandler(adsk.core.CameraEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CameraEventArgs.cast(args)

        # Code to react to the event.
        ui.messageBox('In MyCameraEventdHandler event handler.') 

class MyMouseClickHandler(adsk.core.MouseEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        # Code to react to the event.
        ui.messageBox('In MyMouseClickHandler event handler.')


def clearLoggingHandlers():
    """
    Remove uiHandlers from handlers list and ui
    """
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # onCommandStarting.
        ui.commandStarting.remove(onCommandStarting)
        handlers.remove(onCommandStarting)

        # onCommandTerminated.
        ui.commandTerminated.remove(onCommandTerminated)
        handlers.remove(onCommandTerminated)

        # onMarkingMenuDisplaying.
        ui.markingMenuDisplaying.remove(onMarkingMenuDisplaying)
        handlers.remove(onMarkingMenuDisplaying)

        # onWorkspaceActivated.
        ui.workspaceActivated.remove(onWorkspaceActivated)
        handlers.remove(onWorkspaceActivated)
    
    except:
        # create try/except for individual logginf handlers
        ui.messageBox('Handlers not removed: \n{}'.format(traceback.format_exc()))

    return None


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Hello addin')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # clearLoggingHandlers()
        ui.messageBox('Stop addin')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# setup handlers 
try:
    # "userInterface_var" is a variable referencing a UserInterface object.
    onCommandStarting = MyCommandStartingHandler()
    ui.commandStarting.add(onCommandStarting)
    handlers.append(onCommandStarting)

    # "userInterface_var" is a variable referencing a UserInterface object.
    #onCameraActivated = MyCameraEventdHandler()
    #ui.workspaceActivated.add(onCameraActivated)
    #handlers.append(onWorkspaceActivated)

    # "command_var" is a variable referencing a Command object.
    onMouseClick = MyMouseClickHandler()
    mouse.add(onMouseClick)
    handlers.append(onMouseClick)
    
    ui.messageBox(app.userId)
    ui.messageBox(app.userName)
    ui.messageBox(app.version)
except:
    ui.messageBox('Handlers not set: \n{}'.format(traceback.format_exc())) 