import maya.cmds as cmds

class MR_window(object):
    def __init__(self):
        
        self.window = "MR_window"
        self.title = "Rename Quick Tool"
        self.size = (600,400)
        
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)
        
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=20)
        cmds.text("Don't forget to check your n-gon's and tri's")
        cmds.separator(height=20)
        
        #create textfield
        self.descriptionName = cmds.textFieldGrp(label='Description: ')
        cmds.separator(height=20)
        
        #create radio buttons for side selection
        cmds.separator(height=20)
        self.sideValue = cmds.radioButtonGrp( label='Prefix: ', labelArray4=['l', 'm', 'r', 'f'], numberOfRadioButtons=4 )
        self.sideValue2 = cmds.radioButtonGrp( shareCollection=self.sideValue, label='', labelArray3=['bk', 'bt', 'ctr'], numberOfRadioButtons=3 )
        cmds.separator(height=20)
        #create radio buttons for type selection
        self.typeValue = cmds.radioButtonGrp( numberOfRadioButtons=4, label='Types', labelArray4=['grp', 'geo', 'crv', 'img'], select=True )
        self.typeValue2 = cmds.radioButtonGrp( numberOfRadioButtons=3, shareCollection=self.typeValue, label='', labelArray3=['cam', 'jnt', 'lgt'] )
        #create checkbox for numerization
        cmds.separator(height=20)
        
        #self.numerize = cmds.checkBox( label='Suffix with Number (001,002,etc...):', value=1 )
        self.numerize = cmds.checkBoxGrp( numberOfCheckBoxes=2, label='Number Sequence: ', labelArray2=['Yes', 'No'], v2=1 )
        cmds.separator(height=20)
        #creates button to execute command
        self.confirmBtn = cmds.button(label='Confirm Name Change', command=self.renameFunction)
        
        
       
        
        cmds.showWindow()

    def renameFunction(self, *args):
        descriptionName = ""
        sideValue = 0
        selection= cmds.ls(sl=True)
        isValid = 0
        descriptionName= cmds.textFieldGrp(self.descriptionName, query=True, text=True)
        
        sideValue = cmds.radioButtonGrp(self.sideValue, query=True, select=True)
        sideValue2 = cmds.radioButtonGrp(self.sideValue2, query=True, select=True)
        
        if sideValue == 1:
            sideSelection = "l"
        elif sideValue == 2:
            sideSelection = "m"
        elif sideValue == 3: 
            sideSelection = "r"
        elif sideValue == 4: 
            sideSelection = "f"
        elif sideValue2 == 1: 
            sideSelection = "bk"
        elif sideValue2 == 2:
            sideSelection = "bt"
        elif sideValue2 == 3: 
            sideSelection = "ctr"
        else:
            isValid = 1
            
        typeSelect = cmds.radioButtonGrp(self.typeValue, query=True, select=True)
        typeSelect2 = cmds.radioButtonGrp(self.typeValue2, query=True, select=True)
        
        if typeSelect >= 1 and typeSelect == 1:
            selectType = "grp"
        elif typeSelect >= 1 and typeSelect == 2:
            selectType = "geo"
        elif typeSelect >= 1 and typeSelect == 3:
            selectType = "crv"
        elif typeSelect >= 1 and typeSelect == 4:
            selectType = "img"
        elif typeSelect2 >= 1 and typeSelect2 == 1:
            selectType = "cam"
        elif typeSelect2 >= 1 and typeSelect2 == 2:
            selectType = "jnt"
        elif typeSelect2 >= 1 and typeSelect2 == 3:
            selectType = "lgt"

        isNumerize = cmds.checkBoxGrp(self.numerize, query=True, value1=True)
        print(isNumerize)
        
        
        if isValid == 0 and isNumerize == True:
            for i in range(len(selection)):
                new_name = sideSelection + '_' + descriptionName + '_' + str(i+1).zfill(3) + '_' + selectType
                cmds.rename(selection[i], new_name)
        elif isValid == 0 and isNumerize == False:
            for i in range(len(selection)):
                new_name = sideSelection + '_' + descriptionName + '_' + selectType
                cmds.rename(selection[i], new_name)
        elif isValid == 1 and isNumerize == True:
            for i in range(len(selection)):
                new_name = descriptionName + '_' + str(i+1).zfill(3) + '_' + selectType
                cmds.rename(selection[i], new_name)
        else:
            for i in range(len(selection)):
                new_name = descriptionName + '_' + selectType
                cmds.rename(selection[i], new_name)
            
        
        
myWindow = MR_window()