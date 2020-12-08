# Author- Peter Rosso  - rosso.io - Design and Manufacture Futures Lab
# Description-Fusion Logger shows your learning history and recommends new commands to use.
# LOG File by AdbA Icons ❤️ from the Noun Project
# stop sign by Michael Finney from the Noun Project

import adsk, adsk.core, traceback, json, webbrowser, logging, os

_app = adsk.core.Application.cast(None)
_addin = None
_ui = None
_userId = None
_userName = None
_version = None
_stopButton = None

log = None
logger_handler = None
handlers = []

LOG_FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Fusion-logger-addin.log')
PALETTE_ID = 'commandMapPalette'
COMMAND_ID = 'StartFusionLogger'
COMMAND_ID_STOP = 'StopFusionLogger'
PALETTE_URL = 'https://commandmap.autodesk.com/v1/'

def bindEventHandler(event, handler):
    event.add(handler)
    handlers.append(handler)

def unbindEventHandler(event, handler):
    event.remove(handler)
    handlers.remove(handler)


# # Event handler for the palette close event.
class MyCloseEventHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        pass


# Event handler for the commandStarting event.
class CommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        ui = None
        app = adsk.core.Application.get()
        ui = app.userInterface

        try:
            eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
            
            
            objectType = eventArgs.objectType
            commandId = eventArgs.commandId
            editObj = app.activeEditObject.objectType
            document = app.activeDocument.name
            workspace = ui.activeWorkspace.name
            workspaceID = ui.activeWorkspace.id
            className = str(self.__class__).split("_py.")
            className = className[-1]

            if commandId:
                INFO = f'{_userId}|{_userName}|{_version}|{className}|{document}|{editObj}|w:{workspace}|{workspaceID}|{objectType}|CommandStarting|{commandId}'
                log.info(INFO)
                
            log.debug('Command started: {}'.format(commandId))
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))


# Event handler for the commandStarting event.
class CommandTerminatedHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self,):
        super().__init__()
    def notify(self, args):
        ui = None
        app = adsk.core.Application.get()
        ui = app.userInterface
        try:
            eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
            
            
            objectType = eventArgs.objectType
            commandId = eventArgs.commandId
            editObj = app.activeEditObject.objectType
            document = app.activeDocument.name
            workspace = ui.activeWorkspace.name
            workspaceID = ui.activeWorkspace.id
            className = str(self.__class__).split("_py.")
            className = className[-1]
            

            if commandId:
                INFO = f'{_userId}|{_userName}|{_version}|{className}|{document}|{editObj}|w:{workspace}|{workspaceID}|{objectType}|CommandTerminating|{commandId}'
                log.info(INFO)

            log.debug('Command terminated: {}'.format(commandId))
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))


class CommandFusionLoggerAddIn:
    # TODO: modify so that when the button is pressed it pops a window communicating the status of the logger. if running or it restarts it if needed

    def __init__(self):

        ui = adsk.core.Application.get().userInterface
        try:
            # self.onHTMLEvent = OnHTMLEventHandler()
            self.onClosed = MyCloseEventHandler()
            
            self.showFusionLoggerCmdDef = ui.commandDefinitions.itemById(COMMAND_ID)
            if not self.showFusionLoggerCmdDef:
                log.debug('Create Show Fusion Logger memu item.')
                self.showFusionLoggerCmdDef = ui.commandDefinitions.addButtonDefinition(COMMAND_ID, 'Start Logger', 'Start Recording actions in Fusion 360', './resources/icon')

            # Add the command to the toolbar.
            panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
            if panel:
                cntrl = panel.controls.itemById(COMMAND_ID)
                if not cntrl:
                    log.debug('Add Show Fusion Logger to Add-Ins toolbar under Solids.')
                    cmd = panel.controls.addCommand(self.showFusionLoggerCmdDef)
                    cmd.isPromoted = True
                    cmd.isPromotedByDefault = True

            panel = ui.allToolbarPanels.itemById('CAMScriptsAddinsPanel')
            if panel:
                cntrl = panel.controls.itemById(COMMAND_ID)
                if not cntrl:
                    log.debug('Add Show Fusion Logger to Add-Ins toolbar under CAM.')
                    cmd = panel.controls.addCommand(self.showFusionLoggerCmdDef)
                    cmd.isPromoted = True
                    cmd.isPromotedByDefault = True
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))
        try:
            # Attach a Starting Handler to intercept any command
            log.info('Create Commmand Starting handler.')
            self.onCommandStarting = CommandStartingHandler()
            bindEventHandler(ui.commandStarting, self.onCommandStarting)

            log.info('Create Command Terminated handler.')
            self.onCommandTerminated = CommandTerminatedHandler()
            bindEventHandler(ui.commandTerminated, self.onCommandTerminated)

            # This must be sent through Fusion instead of calling it directly, otherwise
            # Fusion will crash on startup.
            cmdDef = ui.commandDefinitions.itemById(COMMAND_ID)
            if cmdDef:
                cmdDef.execute()
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))

    def __del__(self):
        try:
            ui = adsk.core.Application.get().userInterface

            # Delete command created
            # unbindEventHandler(self.startFusionLoggerCmdDef.commandCreated, self.onCommandCreated)
            
            # Delete controls and associated command definitions created by this add-ins
            panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
            cmd = panel.controls.itemById(COMMAND_ID)
            if cmd:
                cmd.deleteMe()

            panel = ui.allToolbarPanels.itemById('CAMScriptsAddinsPanel')
            if panel:
                cmd = panel.controls.itemById(COMMAND_ID)
                if cmd:
                    cmd.deleteMe()


            unbindEventHandler(ui.commandStarting, self.onCommandStarting)
            unbindEventHandler(ui.commandTerminated, self.onCommandTerminated)
        
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))

class CommandStopFusionLogger: 
    # TODO: modify so that when the button is pressed it pops a window communicating the status of the logger. if running or it stops it if needed
    # The stop method can be simply unbindEventHandler removing logger from monitored handlers.
    def __init__(self):

        ui = adsk.core.Application.get().userInterface
        try:
            self.onClosed = MyCloseEventHandler()

            self.stopFusionLoggerCmdDef = ui.commandDefinitions.itemById(COMMAND_ID_STOP)
            if not self.stopFusionLoggerCmdDef:
                log.debug('Create Stop Fusion Logger menu Item.')
                self.stopFusionLoggerCmdDef = ui.commandDefinitions.addButtonDefinition(COMMAND_ID_STOP, 'Stop Logger', 'Stop Recording actions in Fusion 360', './resources/stop')

                        # Add the command to the toolbar.
            panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
            if panel:
                cntrl = panel.controls.itemById(COMMAND_ID_STOP)
                if not cntrl:
                    log.debug('Add Stop Fusion Logger to Add-Ins toolbar under Solids.')
                    cmd = panel.controls.addCommand(self.stopFusionLoggerCmdDef)
                    cmd.isPromoted = True
                    cmd.isPromotedByDefault = True

            panel = ui.allToolbarPanels.itemById('CAMScriptsAddinsPanel')
            if panel:
                cntrl = panel.controls.itemById(COMMAND_ID_STOP)
                if not cntrl:
                    log.debug('Add Stop Fusion Logger to Add-Ins toolbar under CAM.')
                    cmd = panel.controls.addCommand(self.stopFusionLoggerCmdDef)
                    cmd.isPromoted = True
                    cmd.isPromotedByDefault = True
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))
    def __del__(self):
        pass


def run(context):
    global  _app, _ui, handlers, log, logger_handler, LOG_FILE_NAME, _userId, _userName, _version , _addin, _stopButton

    ui = None
    ui = adsk.core.Application.get().userInterface

    try:
        log = logging.getLogger(__name__)
        logger_handler = logging.FileHandler(LOG_FILE_NAME)
        logger_handler.setLevel(logging.INFO)
        logger_formatter = logging.Formatter('%(asctime)s %(message)s')
        logger_handler.setFormatter(logger_formatter)
        log.addHandler(logger_handler)
        log.setLevel(logging.INFO)
        log.warn('Started Fusion Logger add-in.')
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        _userId = _app.userId
        _userName = _app.userName
        _version = _app.version   

        _addin = CommandFusionLoggerAddIn()
        _stopButton = CommandStopFusionLogger()
        ui.messageBox('Started Fusion Logger add-in')
        

    except:
        if ui:
            log.error(format(traceback.format_exc()))
            ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))


def stop(context):
    global _app, _ui, handlers, log, logger_handler, LOG_FILE_NAME, _userId, _userName, _version , _addin, _stopButton
    ui = None
    ui = adsk.core.Application.get().userInterface
    
    try:
        log.warn('Stopped Fusion Logger add-in.')
        log.warn('------------------------------------------------------------')
        log.removeHandler(logger_handler)
        del log
    
          
        del _addin
        ui.messageBox('Stopped Fusion Logger add-in')
    except:
        if ui:
            log.error(format(traceback.format_exc()))
            ui.messageBox('Failed to start the Fusion Logger for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))