# Author- rossop
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import logging


# Global variable used to maintain a reference to all event handlers.
try:
    app = adsk.core.Application.get()
    ui  = app.userInterface
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
    ui.messageBox('NO LOGGER')


class eventsLogger():
    def __init__(self):
        ui = None

        app = adsk.core.Application.get()
        ui = app.userInterface

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
            if ui:
                ui.messageBox('Failed logger.log():\n{}'.format(traceback.format_exc()))

        self.fusionFormatter = fusionFormatter
        self.fusionLogger = fusionLogger

    def log(self, eventData='something', first=None, last=None):

        try:
            self.eventData = eventData
            self.first = first
            self.last = last


            self.fusionLogger.info('Command: {} '.format(self.event))
            self.fusionLogger.info('Details: {} - {}'.format(self.fullname, self.email))

        except:
            if ui:
                ui.messageBox('Failed logger.log():\n{}'.format(traceback.format_exc()))

    @property
    def event(self):
        try:
            formatter = '{} happened'.format(self.eventData)
        except:
            fusionLogger.exception('EventNotLogged')
        else:
            if formatter:
                return formatter

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)


try:
    eLog = eventsLogger()
    eLog.log('START')
except:
    debugLogger.debug('eLog not functioning')


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Started Logger ADDIn')

    except:
        debugLogger.debug('Logger not started')
        debugLogger.debug('Failed:\n{}'.format(traceback.format_exc()))
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    #global debugLogger
    #global eLog


def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Logger Ended')
        debugLogger.debug('Logger ended')

    except:
        debugLogger.debug('Logger failed to end')
        debugLogger.debug('Failed:\n{}'.format(traceback.format_exc()))
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the commandCreated event.
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
            eLog.log('Logged!!')
            ui.messageBox('In MyCommandStartingHandler event handler.\nDo some logging')
        except:
            error_message = 'Logger failed:\n{}'.format(traceback.format_exc())
            ui.messageBox(error_message)
            debugLogger(error_message)


try:
    onCommandStarting = MyCommandStartingHandler()
    ui.commandStarting.add(onCommandStarting)
    handlers.append(onCommandStarting)
    ui.messageBox('here')
except:
    ui.messageBox('here2')
    debugLogger.debug('Handlers not set: \n{}'.format(traceback.format_exc()))
    ui.messageBox('here3??')
    ui.messageBox('Handlers not set: \n{}'.format(traceback.format_exc()))