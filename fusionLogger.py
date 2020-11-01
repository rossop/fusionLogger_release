# Author- rossop
# Description - 

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import logging

# Set up fusionLogger
try:
    user = 'rossop'
    
    fusion_logger = logging.getLogger(__name__)
    fusion_logger.setLevel(logging.INFO)

    LOG_FORMAT = '%(asctime)s::%(msecs)03d::%(process)d::%(filename)s::%(levelname)s::%(message)s'
    formatter = logging.Formatter(LOG_FORMAT)
    
    file_handler = logging.FileHandler('C:/Users/pr13905/fusion_log_' + user + '.log')
    file_handler.setFormatter(formatter)

    fusion_logger.addHandler(file_handler)
    
    #log_filename = user + '_info.log'



    # logging.basicConfig(name='fusion_logger',
    #                     level = logging.INFO,
    #                     format = LOG_FORMAT,
    #                     datefmt='%Y-%m-%d,%H:%M:%S',
    #                     filename = 'C:\Users\pr13905\fusion_log_' + user + '.log',
    #                     filemode='a')
    
    # fusion_logger = logging.getLogger('fusion_logger')
except:
    if ui:
        ui.messageBox('Error:\n{}'.format(traceback.format_exc()))

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


# Event handler for the Comand start event
class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
        app =adsk.core.Application.get()
        ui = app.userInterface

    def setup_logger(self, logger):
        try:
            self.logger = fusion_logger
        except:
            ui.messageBox('Error:\n{}'.format(traceback.format_exc()))        

    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
        try:
            fusion_logger.info('In MyCommandStartingHandler event handler.')
            ui.messageBox('In MyCommandStartingHandler event handler.')
        except:
            ui.messageBox('Error:\n{}'.format(traceback.format_exc()))  

        # Code to react to the event.
        try:
            obj_list = [method_name for method_name in dir(eventArgs)
                      if callable(getattr(eventArgs, method_name))]
            loggedData = str(eventArgs._get_commandDefinition())
            fusion_logger.info'commandDefinition:\n{}'.format(loggedData))
            #eLog.log('obj_list:\n{}'.format(str(obj_list)))

            loggedData = str(eventArgs._get_commandId())
         S  fusion_logger.info('commandId:\n{}'.format(loggedData))

            loggedData = str(eventArgs._get_objectType())
            fusion_logger.info('objectType:\n{}'.format(loggedData))

            loggedData = str(eventArgs._get_firingEvent())
            fusion_logger.info('eventArgs:\n{}'.format(loggedData))

            loggedData = str(eventArgs.__module__)
            fusion_logger.info('module:\n{}'.format(loggedData))

            loggedData = str(eventArgs.__class__)
            fusion_logger.info('class:\n{}'.format(loggedData))

            loggedData = str(eventArgs.__dir__())
            fusion_logger.info('dir:\n{}'.format(loggedData))

            loggedData = type(eventArgs)
            fusion_logger.info('type:\n{}'.format(loggedData))

        except:
            error_message = 'Logger failed:\n{}'.format(traceback.format_exc())
            ui.messageBox(error_message)   


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


# setup handlers to trigger loggers
try:
    # "userInterface_var" is a variable referencing a UserInterface object.
    onCommandStarting = MyCommandStartingHandler()
    ui.commandStarting.add(onCommandStarting)
    handlers.append(onCommandStarting)

    ui.messageBox(app.userId)
    ui.messageBox(app.userName)
    ui.messageBox(app.version)
except:
    ui.messageBox('Handlers not set: \n{}'.format(traceback.format_exc())) 