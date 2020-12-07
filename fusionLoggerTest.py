#Author-Autodesk Research
#Description-Command Map shows your learning history and recommends new commands to use.

import adsk, adsk.core, traceback, json, webbrowser, logging, os

_app = adsk.core.Application.cast(None)
_addin = None
_ui = None
log = None
logger_handler = None
handlers = []

LOG_FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'command-map-addin.log')
PALETTE_ID = 'commandMapPalette'
COMMAND_ID = 'ShowFusionLogger'  #'ShowCommandMapPalette'
PALETTE_URL = 'https://commandmap.autodesk.com/v1/'

def bindEventHandler(event, handler):
    event.add(handler)
    handlers.append(handler)

def unbindEventHandler(event, handler):
    event.remove(handler)
    handlers.remove(handler)

# def CreateOrShowPalette(events):
#     try:
#         ui = adsk.core.Application.get().userInterface
        
#         # Create and display the palette.
#         palette = ui.palettes.itemById(PALETTE_ID)
#         if not palette:
#             # Initial height of 470px to make Autodesk Account login pages look okay
#             palette = ui.palettes.add(PALETTE_ID, 'Command Map', PALETTE_URL, False, True, True, 320, 470)
#             palette.setPosition(30, 620)
#             palette.setMinimumSize(300, 380)
#             palette.setMaximumSize(400, 900)

#             # Dock the palette to the right side of Fusion window.
#             palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight
#             palette.dockingOptions = adsk.core.PaletteDockingOptions.PaletteDockOptionsToVerticalOnly

#             # Add handler to HTMLEvent of the palette.
#             bindEventHandler(palette.incomingFromHTML, events.onHTMLEvent)

#             # Add handler to CloseEvent of the palette.
#             bindEventHandler(palette.closed, events.onClosed)

#             log.warn('Create Command Map palette.')
#             palette.isVisible = True

#         else:
#             log.warn('Show Command Map palette.')
#             palette.isVisible = not palette.isVisible
#     except:
#         log.error(format(traceback.format_exc()))
#         ui.messageBox('Create Command Map palette failed: {}'.format(traceback.format_exc()))


# # Event handler for the commandCreated event.
# class ShowPaletteCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
#     def __init__(self, onHTMLEvent, onClosed):
#         super().__init__()
#         self.onHTMLEvent = onHTMLEvent
#         self.onClosed = onClosed
        
#         log.debug('ShowPaletteCommandCreatedHandler created.')
                     
#     def notify(self, args):
#         CreateOrShowPalette(self)


# # Event handler for the palette close event.
class MyCloseEventHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        pass


# # Event handler for the palette HTML event.                
# class OnHTMLEventHandler(adsk.core.HTMLEventHandler):
#     def __init__(self):
#         super().__init__()
#     def notify(self, args):
#         ui = None

#         try:
#             ui = adsk.core.Application.get().userInterface

#             htmlArgs = adsk.core.HTMLEventArgs.cast(args)            
#             data = json.loads(htmlArgs.data)

#             if htmlArgs.action == 'OpenWebPage':
#                 webbrowser.open(data)
#             elif htmlArgs.action == 'ExecuteCommand':
#                 cmdDef = ui.commandDefinitions.itemById(data)
#                 if cmdDef:
#                     cmdDef.execute()

#             log.debug('HTML Event: {}, {}'.format(htmlArgs.action, data))

#         except:
#             ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))      

     

# Event handler for the commandStarting event.
class CommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        ui = None

        try:
            ui = adsk.core.Application.get().userInterface

            eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
            commandId = eventArgs.commandId
            if commandId == 'SelectCommand':
                return

            # Send the command information to HTML
            palette = ui.palettes.itemById(PALETTE_ID)

            # if palette and commandId:
            #     palette.sendInfoToHTML('StartCommand', json.dumps({ 'id': commandId }))
            if commandId:
                log.info('CommandStaring::id:{}'.format(commandId))

            log.debug('Command started: {}'.format(commandId))
        except:
            pass

# Event handler for the commandStarting event.
class CommandTerminatedHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self,):
        super().__init__()
    def notify(self, args):
        ui = None
        try:
            ui = adsk.core.Application.get().userInterface

            eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
            commandId = eventArgs.commandId
            if commandId == 'SelectCommand':
                return

            # Send the command information to HTML
            palette = ui.palettes.itemById(PALETTE_ID)

            # if palette and commandId:
            #     palette.sendInfoToHTML('TerminateCommand', json.dumps({ 'id': commandId }))

            if commandId:
                log.info('CommandTerminating::id:{}'.format(commandId))

            log.debug('Command terminated: {}'.format(commandId))
        except:
            pass

class CommandFusionLoggerAddIn:

    def __init__(self):

        ui = adsk.core.Application.get().userInterface
        try:
            # self.onHTMLEvent = OnHTMLEventHandler()
            self.onClosed = MyCloseEventHandler()
            
            # self.showPaletteCmdDef = ui.commandDefinitions.itemById(COMMAND_ID)
            # if not self.showPaletteCmdDef:
            #     log.debug('Create Show Command Map memu item.')
            #     self.showPaletteCmdDef = ui.commandDefinitions.addButtonDefinition(COMMAND_ID, 'Show Command Map', 'Show the Command Map for Fusion 360 panel.', './resources/icon')
            #     self.onCommandCreated = ShowPaletteCommandCreatedHandler(self.onHTMLEvent, self.onClosed)
            #     bindEventHandler(self.showPaletteCmdDef.commandCreated, self.onCommandCreated)
            self.showFusionLoggerCmdDef = ui.commandDefinitions.itemById(COMMAND_ID)
            if not self.showFusionLoggerCmdDef:
                log.debug('Create Show Command Map memu item.')
                self.showFusionLoggerCmdDef = ui.commandDefinitions.addButtonDefinition(COMMAND_ID, 'Start Logger', 'Start Recording actions in Fusion 360', './resources/icon')
                # bindEventHandler(self.showFusionLoggerCmdDef.commandCreated, self.onCommandCreated)
            # self.showPaletteCmdDef.toolClipFilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), './resources/toolclip.png')

            # Add the command to the toolbar.
            panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
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
                    log.debug('Add Show Command Map to Add-Ins toolbar under CAM.')
                    cmd = panel.controls.addCommand(self.showFusionLoggerCmdDef)
                    cmd.isPromoted = True
                    cmd.isPromotedByDefault = True
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Command Map for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))
        try:
            # Attach a Starting Handler to intercept any command
            log.info('Create Commmand Starting handler.')
            self.onCommandStarting = CommandStartingHandler()
            bindEventHandler(ui.commandStarting, self.onCommandStarting)

            log.info('Create Command Terminated handler.')
            self.onCommandTerminated = CommandTerminatedHandler()
            bindEventHandler(ui.commandTerminated, self.onCommandTerminated)

            # Execute the "Show Command Map pallete" command
            # This must be sent through Fusion instead of calling it directly, otherwise
            # Fusion will crash on startup.
            cmdDef = ui.commandDefinitions.itemById(COMMAND_ID)
            if cmdDef:
                cmdDef.execute()
        except:
            if ui:
                log.error(format(traceback.format_exc()))
                ui.messageBox('Failed to start the Command Map for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))


    def __del__(self):

        ui = adsk.core.Application.get().userInterface

        # Delete command created
        unbindEventHandler(self.showPaletteCmdDef.commandCreated, self.onCommandCreated)

        # Delete the palette created by this add-in.
        palette = ui.palettes.itemById(PALETTE_ID)
        if palette:
            palette.deleteMe()
        
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

        if self.showPaletteCmdDef:
            self.showPaletteCmdDef.deleteMe()

        unbindEventHandler(ui.commandStarting, self.onCommandStarting)
        unbindEventHandler(ui.commandTerminated, self.onCommandTerminated)

# class CommandMapAddIn:

#     def __init__(self):

#         ui = adsk.core.Application.get().userInterface
#         try:
#             self.onHTMLEvent = OnHTMLEventHandler()
#             self.onClosed = MyCloseEventHandler()
            
#             self.showPaletteCmdDef = ui.commandDefinitions.itemById(COMMAND_ID)
#             if not self.showPaletteCmdDef:
#                 log.debug('Create Show Command Map memu item.')
#                 self.showPaletteCmdDef = ui.commandDefinitions.addButtonDefinition(COMMAND_ID, 'Show Command Map', 'Show the Command Map for Fusion 360 panel.', './resources/icon')
#                 self.onCommandCreated = ShowPaletteCommandCreatedHandler(self.onHTMLEvent, self.onClosed)
#                 bindEventHandler(self.showPaletteCmdDef.commandCreated, self.onCommandCreated)

#             # self.showPaletteCmdDef.toolClipFilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), './resources/toolclip.png')

#             # Add the command to the toolbar.
#             panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
#             cntrl = panel.controls.itemById(COMMAND_ID)
#             if not cntrl:
#                 log.debug('Add Show Command Map to Add-Ins toolbar under Solids.')
#                 cmd = panel.controls.addCommand(self.showPaletteCmdDef)
#                 cmd.isPromoted = True
#                 cmd.isPromotedByDefault = True

#             panel = ui.allToolbarPanels.itemById('CAMScriptsAddinsPanel')
#             if panel:
#                 cntrl = panel.controls.itemById(COMMAND_ID)
#                 if not cntrl:
#                     log.debug('Add Show Command Map to Add-Ins toolbar under CAM.')
#                     cmd = panel.controls.addCommand(self.showPaletteCmdDef)
#                     cmd.isPromoted = True
#                     cmd.isPromotedByDefault = True

#             # Attach a Starting Handler to intercept any command
#             log.info('Create Commmand Starting handler.')
#             self.onCommandStarting = CommandStartingHandler()
#             bindEventHandler(ui.commandStarting, self.onCommandStarting)

#             log.info('Create Command Terminated handler.')
#             self.onCommandTerminated = CommandTerminatedHandler()
#             bindEventHandler(ui.commandTerminated, self.onCommandTerminated)

#             # Execute the "Show Command Map pallete" command
#             # This must be sent through Fusion instead of calling it directly, otherwise
#             # Fusion will crash on startup.
#             cmdDef = ui.commandDefinitions.itemById(COMMAND_ID)
#             if cmdDef:
#                 cmdDef.execute()
#         except:
#             if ui:
#                 log.error(format(traceback.format_exc()))
#                 ui.messageBox('Failed to start the Command Map for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))


#     def __del__(self):

#         ui = adsk.core.Application.get().userInterface

#         # Delete command created
#         unbindEventHandler(self.showPaletteCmdDef.commandCreated, self.onCommandCreated)

#         # Delete the palette created by this add-in.
#         palette = ui.palettes.itemById(PALETTE_ID)
#         if palette:
#             palette.deleteMe()
        
#         # Delete controls and associated command definitions created by this add-ins
#         panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
#         cmd = panel.controls.itemById(COMMAND_ID)
#         if cmd:
#             cmd.deleteMe()

#         panel = ui.allToolbarPanels.itemById('CAMScriptsAddinsPanel')
#         if panel:
#             cmd = panel.controls.itemById(COMMAND_ID)
#             if cmd:
#                 cmd.deleteMe()

#         if self.showPaletteCmdDef:
#             self.showPaletteCmdDef.deleteMe()

#         unbindEventHandler(ui.commandStarting, self.onCommandStarting)
#         unbindEventHandler(ui.commandTerminated, self.onCommandTerminated)

def run(context):
    global  _app, _ui, handlers, log, logger_handler, LOG_FILE_NAME#, _addin

    ui = None
    try:
        log = logging.getLogger(__name__)
        logger_handler = logging.FileHandler(LOG_FILE_NAME)
        logger_handler.setLevel(logging.INFO)
        logger_formatter = logging.Formatter('%(asctime)s %(message)s')
        logger_handler.setFormatter(logger_formatter)
        log.addHandler(logger_handler)
        log.setLevel(logging.INFO)
        log.warn('Started Command Map add-in.')
        _app = adsk.core.Application.get()
        _ui = _app.userInterface
        # _addin = CommandMapAddIn()
        _addin = CommandFusionLoggerAddIn()

        ui = adsk.core.Application.get().userInterface

    except:
        if ui:
            log.error(format(traceback.format_exc()))
            ui.messageBox('Failed to start the Command Map for Fusion 360 add-in:\n\n{}'.format(traceback.format_exc()))


def stop(context):
    global _addin, _ui, handlers, log, logger_handler, LOG_FILE_NAME
    ui = None
    
    try:
        log.warn('Stopped Command Map add-in.')
        log.warn('------------------------------------------------------------')
        log.removeHandler(logger_handler)
        del log
        os.remove(LOG_FILE_NAME)
        ui = adsk.core.Application.get().userInterface  
        del _addin

    except:
        pass
