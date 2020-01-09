# Get the UserInterface object and the CommandDefinitions collection.
ui = app.userInterface
cmdDefs = ui.commandDefinitions

# Create a button command definition.
buttonExample = cmdDefs.addButtonDefinition('MyButtonDefId', 'Sample Button',
                                            'Sample button tooltip',
                                            './/Resources//Sample')

# Connect to the command created event.
buttonExampleCreated = ButtonExampleCreatedEventHandler()
buttonExample.commandCreated.add(buttonExampleCreated)
handlers.append(buttonExampleCreated)

# Get the ADD-INS panel in the model workspace.
addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')

# Add the button to the bottom.
buttonControl = addInsPanel.controls.addCommand(buttonExample)

# Make the button available in the panel.
buttonControl.isPromotedByDefault = True
buttonControl.isPromoted = True
