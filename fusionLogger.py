# Author- rossop
# Description - 

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import logging
app = adsk.core.Application.get()
ui = app.userInterface
ui.messageBox('Hello 0')



ui.messageBox('Hello 3')
def run(context):
    ui = None
    try:

        #global app, ui
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions
      
        # Create a button command definition.
        button = cmdDefs.addButtonDefinition('FusionLoggerID', 
                                                'Start Logger', 
                                                   'Records',
                                                   './scr/rec')
                                                   
        
        # Connect to the command created event.
        CommandCreated = CommandCreatedEventHandler()
        button.commandCreated.add(CommandCreated)
        handlers.append(CommandCreated)
        
        # Get the ADD-INS panel in the model workspace. 
        addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        
        # Add the button to the bottom of the panel.
        buttonControl = addInsPanel.controls.addCommand(button)

        # Get the solid create panel in the model workspace. 
        addInsPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        
        # Add the button to the bottom of the panel.
        buttonControl = addInsPanel.controls.addCommand(button)
        buttonControl.isPromotedByDefault = True

        #Adds a toolbar for the MicroChannels
        workSpace = ui.workspaces.itemById('FusionSolidEnvironment')
        tbPanels = workSpace.toolbarPanels
        

        tbPanel = tbPanels.itemById('MicroPanel')
        if tbPanel:
            tbPanel.deleteMe()
        tbPanel = tbPanels.add('MicroPanel', 'Fusion360 Logger', 'SelectPanel', False)

        # Add the button to the bottom of the panel.
        Microtool = tbPanel.controls.addCommand(button)
        Microtool.isPromotedByDefault = True


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

ui.messageBox('Hello 4')
def stop(context):
    ui = None
    app =adsk.core.Application.get()
    ui = app.userInterface
    
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        if tbPanel:
            tbPanel.deleteMe()

        if button:
            button.deleteMe()

        if Microtool:
            Microtool.deleteMe()
            
        ui.messageBox('Logger Ended')
        debugLogger.debug('Logger ended')

    except:
        debugLogger.debug('Logger failed to end')
        debugLogger.debug('Failed:\n{}'.format(traceback.format_exc()))
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))