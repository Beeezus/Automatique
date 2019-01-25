from PyQt5 import QtWidgets, QtCore, QtGui
from os.path import join, realpath
import configuration
import logging
from utility import create_file_list, read_json_file, save_json_file, get_configuration_path


'''LOG'''
logging.basicConfig(format = '%(asctime)s %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p',
                    filename = 'system.log',
                    level=logging.INFO)

class MenuInterface(QtWidgets.QWidget):
    def __init__(self):
        super(MenuInterface, self).__init__()

        '''Window settings'''
        self.resize(700, 400)
        self.setWindowTitle("")
        self.path = ''
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        '''Path configurations'''
        self.dict_configuration_path = get_configuration_path()
        self.json_templates_path = self.dict_configuration_path["json_templates_path"]
        self.excel_templates_path = self.dict_configuration_path["excel_templates_path"]
        self.json_files_path = self.dict_configuration_path["json_files_path"]
        self.excel_files_path = self.dict_configuration_path["excel_files_path"]
        self.hierarchy_path = self.dict_configuration_path["hierarchy_path"]
        self.post_files_path = self.dict_configuration_path["post_files_path"]

        '''LOAD EXTERNAL CSS STYLESHEET'''
        self.stylesheet = open('stylesheet.css').read()
        self.setStyleSheet(self.stylesheet)

        '''Load external font'''
        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(join("font", "CaviarDreams.ttf"))
        font_family = font_db.applicationFontFamilies(font_id)[0]

        '''Font for widgets'''
        self.font = QtGui.QFont(font_family)
        self.font.setPointSize(20)

        '''Folder path for treeview'''
        self.folder_path_tree_view = ""


        '''Treeview'''
        self.treeview = QtWidgets.QTreeView()
        self.treeview.clicked.connect(self.on_select_treeview)

        file_system = QtWidgets.QFileSystemModel(self.treeview)
        file_system.setReadOnly(True)
        file_system.setRootPath(realpath(''))

        self.treeview.setModel(file_system)
        self.treeview.setRootIndex(file_system.index(self.json_files_path))
        self.treeview.header().resizeSection(0, 800)
        self.treeview.setAnimated(True)

        '''text'''
        self.email_text = QtWidgets.QLineEdit()

        '''Load templates'''
        self.list_json_templates = create_file_list(join(realpath(''), "json_templates"), ".json")

        self.list_check = []

        '''Create checkbox list for templates'''
        for template in self.list_json_templates:
            self.list_check.append(QtWidgets.QCheckBox(template, self)) 

        '''Load hierarchies'''
        self.list_hierarchies = create_file_list(join(realpath(''), "hierarchy"), ".xml")
        
        '''Create checkbox list for herarchies'''
        for hierarchy in self.list_hierarchies:
            self.list_check.append(QtWidgets.QCheckBox(hierarchy, self)) 

        '''Load dict measures'''
        self.dict_measures_id = read_json_file(join(realpath(''), "configuration", "measures_config.json"))

        '''create checkbox list for trend id'''
        for measure_id in self.dict_measures_id.keys():
            self.list_check.append(QtWidgets.QCheckBox(measure_id, self))     

        '''Message box'''
        self.message_box = QtWidgets.QMessageBox()

        '''Layout'''
        self.vertical_box = QtWidgets.QVBoxLayout()
        self.vertical_box_check = QtWidgets.QVBoxLayout()
        self.horizontal_box = QtWidgets.QHBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout()
        self.layout_widget = QtWidgets.QWidget()


    '''Tree clicked function'''
    def on_select_treeview(self, index):
        self.folder_path_tree_view = self.sender().model().filePath(index)


    '''_________________________________________________________________________________________'''


    '''Change Hierarchy path Interface'''   
    def change_path_hierarchy_interface(self):
        self.setWindowTitle("Change Hierarchy path")
        
        button_change_path_hierarchy = QtWidgets.QPushButton("Save")
        button_change_path_hierarchy.setFont(self.font)
        button_change_path_hierarchy.clicked.connect(self.change_path_hierarchy_function)

        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_hierarchy)
        
   
    '''Button clicked function'''
    def change_path_hierarchy_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Change hierarchy path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_hierarchy_path(self.folder_path_tree_view)
            if(response == True):
                logging.info("Hierarchy path changed")
                self.message_box.about(self, "Change hierarchy path", "Changed path!")   
            else:
                logging.info("Hierarchy path changing failed")
                self.message_box.critical(self, "Change hierarchy path", "Error!")
        self.close()


    '''__________________________________________________________________________________________'''
    

    '''Change Hierarchy path Interface'''
    def change_path_template_interface(self):
        self.setWindowTitle("Change Template path")
            
        button_change_path_template = QtWidgets.QPushButton("Save")
        button_change_path_template.setFont(self.font)
        button_change_path_template.clicked.connect(self.change_path_template_function)
        
        '''Vertical layout'''
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_template)
        
        
    def change_path_template_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Change Template path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_template_path(self.folder_path_tree_view)
            if(response == True):
                logging.info("Changed Template path succesfully")
                self.message_box.about(self, "Change Template path", "Changed path!")   
            else:
                self.message_box.critical(self, "Change Template path", "Error!")
                logging.info("Changing Template path failed")
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    '''Change Excel path Interface'''
    def change_path_excel_interface(self):
        self.setWindowTitle("Change Excel path")

        button_change_path_excel = QtWidgets.QPushButton("Save")
        button_change_path_excel.setFont(self.font)
        button_change_path_excel.clicked.connect(self.change_path_excel_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_excel)
        
        
    def change_path_excel_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Change excel_files path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_excel_path(self.folder_path_tree_view)
            if(response == True):
                logging.info("excel path changed")
                self.message_box.about(self, "Change excel_files path", "Changed path!")      
            else:
                logging.info("excel path change failed")
                self.message_box.critical(self, "Change excel_files path", "Error")
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    '''Change Excel Templates path Interface'''
    def change_path_excel_templates_interface(self):
        self.setWindowTitle("Change Excel Templates path")
        
        button_change_path_excel_templates = QtWidgets.QPushButton("Save")
        button_change_path_excel_templates.setFont(self.font)
        button_change_path_excel_templates.clicked.connect(self.change_path_excel_templates_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_excel_templates)
        
    
    '''Button clicked function'''
    def change_path_excel_templates_function(self):
        self.message_box = QtWidgets.QMessageBox()
        button_reply = self.message_box.question(self, 'JasonX', "Change excel_templates path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_excel_templates_path(self.folder_path_tree_view)
            if(response == True):
                logging.info("excel templates path changed")
                self.message_box.about(self, "Change excel_templates path", "Changed path!")      
            else:
                logging.info("excel templates path change failed")
                self.message_box.critical(self, "Change excel_templates path", "Error")
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    '''Change json path file'''
    def change_path_json_file_interface(self):
        self.setWindowTitle("Change Json path")
        
        button_change_path_json_file = QtWidgets.QPushButton("Save")
        button_change_path_json_file.setFont(self.font)
        button_change_path_json_file.clicked.connect(self.change_path_json_file_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_json_file)


    '''Button clicked function'''
    def change_path_json_file_function(self):
        self.message_box = QtWidgets.QMessageBox()
        button_reply = self.message_box.question(self, 'JasonX', "Change json_files path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_json_path(self.folder_path_tree_view)
            if(response == True):
                logging.info("Json file path changed")
                self.message_box.about(self, "Change json_files path", "Changed path!")   
            else:
                logging.info("Json file path changing faied")
                self.message_box.critical(self, "Change json_files path", "Error!")
        self.close()


    '''_______________________________________________________________________________________________________________________________________________________________'''


    '''Change Excel Final path Interface'''
    def change_path_excel_final_interface(self):
        self.setWindowTitle("Change Excel Final path")
    
        button_change_path_excel_final = QtWidgets.QPushButton("Save")
        button_change_path_excel_final.setFont(self.font)
        button_change_path_excel_final.clicked.connect(self.change_path_excel_final_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_excel_final)
    

    '''Button clicked function'''
    def change_path_excel_final_function(self):
        try:
            button_reply = self.message_box.question(self, 'JasonX', "Change excel_final path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
            if button_reply == QtWidgets.QMessageBox.Yes:
                response = configuration.change_excel_final_path(self.folder_path_tree_view)
                if(response == True):
                    logging.info("Final excel path changed")
                    self.message_box.about(self, "Change excel_final path", "Changed path!")      
                else:
                    logging.info("Final excel path changing failed")
                    self.message_box.critical(self, "Change excel_final path", "Error")
            self.close()
        except Exception as e:
            logging.error(e, exc_info=True)


    '''_____________________________________________________________________________________________________________________________________________________________'''


    '''Change ChangePathLogsFileInterface'''
    def change_path_logs_file_interface(self):
        self.setWindowTitle("Change Logs file path")
        
        button_change_path_logs_file = QtWidgets.QPushButton("Save")
        button_change_path_logs_file.setFont(self.font)
        button_change_path_logs_file.clicked.connect(self.change_path_logs_file_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_logs_file)
        

    '''Button clicked function'''
    def change_path_logs_file_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Change logs_file path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_logs_file_path(self.folder_path_tree_view)
            if(response == True):
                logging.info("Logs path changed sucessfuly")
                self.message_box.about(self, "Change logs_file path", "Changed path!")      
            else:
                logging.info("Logs path changing failed")
                self.message_box.critical(self, "Change logs_file path", "Error")
        self.close()


    '''_____________________________________________________________________________________________________________________________________________________________'''


    '''Change Path Post Files Interface'''
    def change_path_post_files_interface(self):
        self.setWindowTitle("Change Post Files path")
        
        button_change_path_post_files = QtWidgets.QPushButton("Save")
        button_change_path_post_files.setFont(self.font)
        button_change_path_post_files.clicked.connect(self.change_path_post_files_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_change_path_post_files)
        

    '''Button clicked function'''
    def change_path_post_files_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Change post_files path?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_post_files_path(self.folder_path_tree_view)
            if(response == True):
                logging.info("Post Files path changed sucessfuly")
                self.message_box.about(self, "Change post_files path", "Changed path!")      
            else:
                logging.info("Post Files path changing failed")
                self.message_box.critical(self, "Change post_files path", "Error")
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    '''Add Template Interface'''
    def add_json_template_interface(self):
        self.setWindowTitle("Add new Json template")
        
        button_add_json_template = QtWidgets.QPushButton("Save")       
        button_add_json_template.setFont(self.font)
        button_add_json_template.clicked.connect(self.add_json_template_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_add_json_template)
    

    '''Button clicked function'''
    def add_json_template_function(self):
        self.message_box = QtWidgets.QMessageBox()
        button_reply = self.message_box.question(self, 'JasonX', "Add JSON Template in json_file directory?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.add_json_template(self.folder_path_tree_view)
            if(response == True):
                self.message_box.about(self, "Add template json", "Template added!") 
            else: 
                self.message_box.critical(self, "Add template json", "Error!")
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    '''Add Hierarchy Interface'''
    def add_hierarchy_interface(self):
        self.setWindowTitle("Add new Hierarchy")
        
        button_add_hierarchy = QtWidgets.QPushButton("Save")
        button_add_hierarchy.setFont(self.font)
        button_add_hierarchy.clicked.connect(self.add_hierarchy_function)
        
        
        self.vertical_box.addWidget(self.tree_view)
        self.vertical_box.addWidget(button_add_hierarchy)
        

    '''Button clicked function'''
    def add_hierarchy_function(self):
        self.message_box = QtWidgets.QMessageBox()
        button_reply = self.message_box.question(self, 'JasonX', "Add XML Hierarchy in hierarchy directory?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.add_file_hierarchy(self.folder_path_tree_view)
            if(response == True):
                self.message_box.about(self, "Add hierarchy xml", "File added!") 
            else:
                self.message_box.critical(self, "Add hierarchy xml", "Error!")              
        self.close()


    '''_____________________________________________________________________________________________________________________________________________________________'''


    '''Delete Template Interface'''
    def delete_json_template_interface(self):
        self.setWindowTitle("Delete JSON template")

        button_delete_json_template = QtWidgets.QPushButton("Delete")       
        button_delete_json_template.setFont(self.font)
        button_delete_json_template.clicked.connect(self.delete_json_template_function)

        
        

        for check_box in self.list_check:
            self.vertical_box_check.addWidget(check_box) 
        
        widget = QtWidgets.QWidget()
        widget.setLayout(self.vertical_box_check)
        widget.setStyleSheet("width:500")
        widget.adjustSize()

        scroll = QtWidgets.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        self.vertical_box.addWidget(scroll)
        self.vertical_box.addWidget(button_delete_json_template)


    '''Button clicked function'''
    def delete_json_template_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Delete JSON templates?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            list_templates_del = []
            for check_box in self.list_check:
                if(check_box.isChecked()):
                    list_templates_del.append(check_box.text())
            response = configuration.delete_json_templates(list_templates_del)
            if(response == True):
                self.message_box.about(self, "Delete template json", "Template deleted!") 
            else: 
                self.message_box.critical(self, "Delete template json", "Error!")
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    '''Delete Hierarchy Interface'''
    def delete_hierarchy_interface(self):
        self.setWindowTitle("Delete Hierarchies")
        
        button_delete_hierarchy = QtWidgets.QPushButton("Delete")       
        button_delete_hierarchy.setFont(self.font)
        button_delete_hierarchy.clicked.connect(self.delete_hierarchy_function)

        
        

        for check_box in self.list_check:
            self.vertical_box_check.addWidget(check_box) 
        
        widget = QtWidgets.QWidget()
        widget.setLayout(self.vertical_box_check)
        widget.setStyleSheet("width:500")
        widget.adjustSize()

        scroll = QtWidgets.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        self.vertical_box.addWidget(scroll)
        self.vertical_box.addWidget(button_delete_hierarchy)
            

    '''Button function'''
    def delete_hierarchy_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Delete Hierarchies?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            list_hierarchies_del = []
            for check_box in self.list_check:
                if(check_box.isChecked()):
                    list_hierarchies_del.append(check_box.text())
            response = configuration.delete_hierarchies(list_hierarchies_del)
            if(response == True):
                self.message_box.about(self, "Delete Hierarchies", "Hierarchies deleted!") 
            else: 
                self.message_box.critical(self, "Delete Hierarchies", "Error!")
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    '''CHANGE MEASURES SET FOR EXCEL'''
    def change_measures_set_interface(self):
        self.setWindowTitle("Change measures set")

        button_change_measures_set = QtWidgets.QPushButton("Save")
        button_change_measures_set.setFont(self.font) 
        button_change_measures_set.clicked.connect(self.change_measures_set_function)      

        for check_box in self.list_check:
            if(self.dict_measures_id[check_box.text()]["active"] == True):
                self.vertical_box_check.addWidget(check_box)
                check_box.setChecked(True)
            else:
                self.vertical_box_check.addWidget(check_box)
                check_box.setChecked(False)      
        
        widget = QtWidgets.QWidget()
        widget.setLayout(self.vertical_box_check)
        widget.setStyleSheet("width:500")
        widget.adjustSize()

        scroll = QtWidgets.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)
        
        self.vertical_box.addWidget(scroll)
        self.vertical_box.addWidget(button_change_measures_set)

        self.setLayout(self.vertical_box)

        
    '''Button function'''
    def change_measures_set_function(self):
        self.message_box = QtWidgets.QMessageBox()
        button_reply = self.message_box.question(self, 'JasonX', "Save changes?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            for check_box in self.list_check:
                self.dict_measures_id[check_box.text()]["active"] = check_box.isChecked()  
            response = save_json_file(join(realpath(''), "configuration", "trendIdConfiguration.json"), self.dict_measures_id)
            if(response == True):
                self.message_box.about(self, "JasonX", "Measures set saved successfully!")           
        self.close()


    '''______________________________________________________________________________________________________________________________'''


    def change_email_interface(self):
        self.setWindowTitle("Change email")
        
        button_change_email = QtWidgets.QPushButton("Save")
        button_change_email.setFont(self.font)
        button_change_email.clicked.connect(self.change_email_function)
        
        email_label = QtWidgets.QLabel()
        email_label.setText("Insert new email")
        email_label.setAlignment(QtCore.Qt.AlignCenter)
        email_label.setFont(self.font)
        
        self.vertical_box = QtWidgets.Qself.vertical_boxLayout()
        self.vertical_box.addWidget(email_label)
        self.vertical_box.addWidget(self.email_text)
        self.vertical_box.addWidget(button_change_email)
        self.setLayout(self.vertical_box)
        
            
    '''Button clicked function'''
    def change_email_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Change email?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = configuration.change_email(self.email_text.text())
            if(response == True):
                self.message_box.about(self, "JasonX", "Email changed!")            
        self.close()