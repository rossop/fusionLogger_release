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
    handlers = []
    command_var = adsk.core.Command
except:
    if ui:
        ui.messageBox('Error:\n{}'.format(traceback.format_exc()))

try:
    # Started a debug logger
    debugLogger = logging.getLogger('DebuggerFusion')
    debugLogger.setLevel(logging.DEBUG)

    debugFormatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s')


    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'debug.log')
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(debugFormatter)

    debugLogger.addHandler(file_handler)

except:
    debugLogger = None
    ui.messageBox('NO DEBUG LOGGER')


class eventsLogger():
    def __init__(self):
        # ui = None
        # app = adsk.core.Application.get()
        # ui = app.userInterface

        try:
            fusionFormatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s')

            logName = 'fusion.log'
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), logName)
            file_handler = logging.FileHandler(filename)  # TODO set name to user info
            file_handler.setFormatter(fusionFormatter)

            # Initialise Fusion Logger
            # TODO Set logger name to user name or to part name
            name = 'partName'
            fusionLogger = logging.getLogger(name)
            fusionLogger.setLevel(logging.INFO)
            fusionLogger.addHandler(file_handler)

        except:
            fusionLogger = None
            fusionFormatter = None
            debugLogger.log('Failed logger.log():\n{}'.format(traceback.format_exc()))
            # if ui:
            #     ui.messageBox('Failed logger.log():\n{}'.format(traceback.format_exc()))

        self.fusionFormatter = fusionFormatter
        self.fusionLogger = fusionLogger

    def log(self, eventData='something'):
        try:
            self.event = eventData
            self.fusionLogger.info('Command: {} '.format(self.event))
        except:
            debugLogger.debug('Failed logger.log():\n{}'.format(traceback.format_exc()))

try:
    eLog = eventsLogger()
    eLog.log('START')
except:
    debugLogger.debug('eLog not functioning')
    #global debugLogger
    #global eLog
    ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



# Event handler for the commandCreated event.
class CommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        app = adsk.core.Application.get()
        ui  = app.userInterface

        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)

            message = 'Started Logger ADDIn'
            ui.messageBox(message)
            debugLogger.debug(message)

        except:
            debugLogger.debug('Logger not started')
            debugLogger.debug('Failed:\n{}'.format(traceback.format_exc()))
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
        app =adsk.core.Application.get()
        ui = app.userInterface

    def setup_logger(self, logger):
        self.logger = logger


    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
        eLog = eventsLogger()
        # Code to react to the event.
        try:
            obj_list = [method_name for method_name in dir(eventArgs)
                      if callable(getattr(eventArgs, method_name))]
            loggedData = str(eventArgs._get_commandDefinition())
            eLog.log('commandDefinition:\n{}'.format(loggedData))
            #eLog.log('obj_list:\n{}'.format(str(obj_list)))

            loggedData = str(eventArgs._get_commandId())
            eLog.log('commandID:\n{}'.format(loggedData))

            loggedData = str(eventArgs._get_objectType())
            #eLog.log('objectType:\n{}'.format(loggedData))

            loggedData = str(eventArgs._get_firingEvent())
            #eLog.log('eventArgs:\n{}'.format(loggedData))

            loggedData = str(eventArgs.__module__)
            #eLog.log('module:\n{}'.format(loggedData))

            loggedData = str(eventArgs.__class__)
            eLog.log('class:\n{}'.format(loggedData))

            loggedData = str(eventArgs.__dir__())
            # eLog.log('dir:\n{}'.format(loggedData))

            loggedData = type(eventArgs)
            eLog.log('type:\n{}'.format(loggedData))

            # ui.messageBox('In MyCommandStartingHandler event handler.\nDo some logging')
        except:
            error_message = 'Logger failed:\n{}'.format(traceback.format_exc())
            ui.messageBox(error_message)
            debugLogger.debug(error_message)


try:
    onCommandStarting = MyCommandStartingHandler()
    ui.commandStarting.add(onCommandStarting)
    ui.messageBox(app.userId)
    ui.messageBox(app.userName)
    ui.messageBox(app.version)
    # ui.messageBox(app.activeDocument)
    # #banana = adsk.core.HTMLEvent()
    # # banana = ui.commandStarting()
    # # banana.add(onCommandStarting)
    # mouse.add(onCommandStarting)
    # handlers.append(onCommandStarting)

except:
    debugLogger.debug('Handlers not set: \n{}'.format(traceback.format_exc()))
    ui.messageBox('Handlers not set: \n{}'.format(traceback.format_exc())) 