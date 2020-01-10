# Author- rossop
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import logging


# Global variable used to maintain a reference to all event handlers.
handlers = []
app = adsk.core.Application.get()
ui = app.userInterface

# Global Variables
try:
    command_var = adsk.core.Command
    #Event
except:
    ui.messageBox('ERROR')

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

class MyCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        # Code to react to event.
        eventArgs = adsk.core.CommandEventArgs.cast(args)
        app = adsk.core.Application.get()
        ui = app.userInterface

        elog.log('Logged!!')
        ui.messageBox('In MyExecuteHandler event handler.')


try:
    eLog = eventsLogger()
    eLog.log('START')
except:
    debugLogger.debug('elog not functioning')


try:
    userInterface_var = ui  # adsk.core.UserInterface.get()
    # "userInterface_var" is a variable referencing a UserInterface object.s
    # if None:
    #     onCommandStarting = MyCommandStartingHandler()
    #     userInterface_var.commandStarting.add(onCommandStarting)
    #     onCommandTerminated = MyCommandTerminatedHandler()
    #     userInterface_var.commandTerminated.add(onCommandTerminated)S
    onCommandExecute = MyCommandExecuteHandler()

    try:
        objs = [command_var, command_var.execute]
        for obj in objs:
            try:
                object_methods = [method_name for method_name in dir(obj)
                          if callable(getattr(obj, method_name))]
                debugLogger.debug(str(object_methods))
            except:
                debugLogger.debug('Error')
    except:
        debugLogger.debug('Error')

    command_var._get_activate.add(onCommandExecute)
    handlers.append(onCommandExecute)

except:
    debugLogger.debug('Failed elog:\n{}'.format(traceback.format_exc()))
    if ui:
        ui.messageBox('Failed elog:\n{}'.format(traceback.format_exc()))


