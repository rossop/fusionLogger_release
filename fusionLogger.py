# Author- rossop
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import logging

# Global variable used to maintain a reference to all event handlers.
handlers = []

try:
    # Started a debug logger
    debugLogger = logging.getLogger(__name__)
    debugLogger.setLevel(logging.DEBUG)

    debugFormatter = logging.Formatter('%(levelname)s::%(name)s::%(message)s')

    file_handler = logging.FileHandler('debug.log')
    file_handler.setFormatter(debugFormatter)

    debugLogger.addHandler(file_handler)
except:
    debugLogger = None

try:
    # Initialise Fusion Logger
    # TODO Set logger name to user name or to part name
    fusionLogger = logging.getLogger(__name__)
    fusionLogger.setLevel(logging.INFO)

    fusionFormatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s')

    file_handler = logging.FileHandler('fusion.log')  # TODO set name to user info
    file_handler.setFormatter(fusionFormatter)

    fusionLogger.addHandler(file_handler)
except:
    fusionLogger = None


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Hello addin')

        if debugLogger:
            debugLogger.debug('Add in started')
            ui.messageBox('Logger initialised')

        else:
            ui.messageBox('Logger not started')

        if fusionLogger:
            ui.messageBox('Fusion Logger initialised')
            ee = eventsLog('somestuff')
            ui.messageBox('Failed:\n{}'.format(ee))

        else:
            ui.messageBox('Fusion Logger not intialised')

        # a = propCommandExecuteHandler()

        # mouseEvent_var = adsk.core.MouseEvent
        # returnValue = mouseEvent_var.add(self, loggerMouseEventHandler)

        # cmdDefs = ui.commandDefinitions
    except:
        debugLogger.debug('Loggernotstarted')

        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Stop addin')
        debugLogger.debug('Add in ended')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class eventsLog():
    def __init__(self, eventData=None, first=eventData, last=eventData):
        self.eventData = eventData
        self.first = first
        self.last = last

        a = propCommandExecuteHandler()

        fusionLogger.info('Command: {} '.format(self.event))
        fusionLogger.info('Details: {} - {}'.format(self.fullname, self.email))

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
