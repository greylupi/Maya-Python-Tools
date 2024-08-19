import maya.cmds as cmds

class MR_window(object):
    def __init__(self):
        
        self.window = "MR_window"
        self.title = "UV Transfer Attributes to Multiple Objects"
        self.size = (400,400)
        
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)
        
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=20)
        cmds.text("Objects must be similar. First select the object which has the UV's to be transferred.") 
        cmds.text("Then select all other objects which source UV's are to be transferred to.")
        cmds.separator(height=20)
    
        #create radio buttons for selection
        cmds.separator(height=20)
        self.selectionValue = cmds.radioButtonGrp( label='Sample Space: ', labelArray3=['World', 'Local', 'UV'], numberOfRadioButtons=3 )
        self.selectionValue2 = cmds.radioButtonGrp( shareCollection=self.selectionValue, label='', labelArray2=['Component', 'Topology'], numberOfRadioButtons=2 )
        cmds.separator(height=20)
    
        #creates button to execute command
        self.confirmBtn = cmds.button(label='Transfer', command=self.transferAttribute)

        cmds.showWindow()


    def transferAttribute(self, *args):
        selectionValue = 0
        selectionValue2 = 0
        selection= cmds.ls(sl=True)
        
        selectionValue = cmds.radioButtonGrp(self.selectionValue, query=True, select=True)
        selectionValue2 = cmds.radioButtonGrp(self.selectionValue2, query=True, select=True)
        print(selectionValue)
        print(selectionValue2)
        
        if selectionValue == 1 and len(selection) > 1:
            for i in range(1, len(selection)):
                cmds.transferAttributes(selection[0], selection[i], uvs = 2, sampleSpace = 1)
        elif selectionValue == 2 and len(selection) > 1:
            for i in range(1, len(selection)):
                cmds.transferAttributes(selection[0], selection[i], uvs = 2, sampleSpace = 2)
        elif selectionValue == 3 and len(selection) > 1:
            for i in range(1, len(selection)):
                cmds.transferAttributes(selection[0], selection[i], uvs = 2, sampleSpace = 3)
        elif selectionValue2 == 1 and len(selection) > 1:
            for i in range(1, len(selection)):
                cmds.transferAttributes(selection[0], selection[i], uvs = 2, sampleSpace = 4)
        elif selectionValue2 == 2 and len(selection) > 1:
            for i in range(1, len(selection)):
                cmds.transferAttributes(selection[0], selection[i], uvs = 2, sampleSpace = 5)
        elif selectionValue == 0 and selectionValue2 == 0 :
            cmds.confirmDialog(title='Error Message', message='Sample Space must be selected.', button=['OK'], defaultButton='OK')
        else:
            cmds.confirmDialog(title='Error Message', message='More than one object must be selected.', button=['OK'], defaultButton='OK')
            
        
        
myWindow = MR_window()

