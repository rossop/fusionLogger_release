# Author- rossop
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import logging

# Global variable used to maintain a reference to all event handlers.
handlers = []

try:
    # Started a debug logger
    debugLogger = logging.getLogger(__name__)
    debugLogger.setLevel(logging.DEBUG)

    debugFormatter = logging.Formatter('%(levelname)s::%(name)s::%(message)s')

    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'debug.log')
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(debugFormatter)

    debugLogger.addHandler(file_handler)
except:
    debugLogger = None


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Hello addin')
        debugLogger.debug('Hello addin')

        if debugLogger:
            debugLogger.debug('Add in started')
            ui.messageBox('Debug logger initialised')

        else:
            ui.messageBox('Logger not started')

        try:
            eLog = eventsLog()
            eLog.log()
            ui.messageBox('eLog started')
            debugLogger.debug('eLog started')
        except:
            debugLogger.debug('elog not functioning')
            if ui:
                ui.messageBox('Failed elog:\n{}'.format(traceback.format_exc()))



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
    def __init__(self):
        ui = None
        try:

            app = adsk.core.Application.get()
            ui = app.userInterface

            # Initialise Fusion Logger
            # TODO Set logger name to user name or to part name
            fusionLogger = logging.getLogger(__name__)
            fusionLogger.setLevel(logging.INFO)

            fusionFormatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s')
            self.fusionFormatter = fusionFormatter # is this necessary?

            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fusion.log')
            file_handler = logging.FileHandler(filename)  # TODO set name to user info
            file_handler.setFormatter(fusionFormatter)

            fusionLogger.addHandler(file_handler)
            self.fusionLogger = fusionLogger
        except:
            fusionLogger = None

        if fusionLogger:
            ui.messageBox('Fusion Logger Class initialised')
        else:
            ui.messageBox('Fusion Logger not intialised')

    def log(self, eventData='something', first=None, last=None):

        try:
            self.eventData = eventData
            self.first = first
            self.last = last

            #a = propCommandExecuteHandler()

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