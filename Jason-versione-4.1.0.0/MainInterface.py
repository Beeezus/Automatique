from os.path import join, realpath, isfile, exists
import utility
import sys
from configuration import control_paths, reset_path
import logging
from Jasonx import Jasonx
from activation import initialize_activations, read_credentials, refresh_get, activate_dummy
from subprocess import call
from httpReq import post, get
from json import dumps
from json import dumps
from PyQt5 import QtWidgets, QtGui, QtCore
from MenuInterface import MenuInterface
from webbrowser import open_new


class MainInterface(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainInterface, self).__init__(parent)
        logging.basicConfig(format = '%(asctime)s %(message)s',
                            datefmt = '%m/%d/%Y %I:%M:%S %p',
                            filename = 'syslog.log',
                            level=logging.INFO)

        '''Initialization configurations'''
        control_paths()
        utility.refresh_template_configuration()

        '''Path configurations'''
        self.dict_configuration_path = utility.get_configuration_path()
        self.json_templates_path = self.dict_configuration_path["json_templates_path"]
        self.excel_templates_path = self.dict_configuration_path["excel_templates_path"]
        self.json_files_path = self.dict_configuration_path["json_files_path"]
        self.excel_files_path = self.dict_configuration_path["excel_files_path"]
        self.hierarchy_path = self.dict_configuration_path["hierarchy_path"]
        self.post_files_path = self.dict_configuration_path["post_files_path"]

        '''Window configuration'''
        stylesheet = open('stylesheet.css').read()
        self.setStyleSheet(stylesheet)
        self.setWindowTitle("JasonX powered by Storm")

        self.jasonx_instance = ""
        self.menu_interface_instance = MenuInterface()
        self.list_file_json = []
        self.hierarchy_name = ""
        self.dict_response = {}

        '''configuration measures'''
        self.env_config = utility.read_json_file(join(realpath(''), "configuration", "env_config.json"))

        '''Load external font'''
        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(join("font", "CaviarDreams.ttf"))
        font_family = font_db.applicationFontFamilies(font_id)[0]

        '''Font for widgets'''
        self.font = QtGui.QFont(font_family)
        self.font.setPointSize(20)

        '''Font title'''
        self.font_title = QtGui.QFont(font_family)
        self.font_title.setPointSize(50)

        '''Font for toolbar'''
        self.font_toolbar = QtGui.QFont(font_family)
        self.font_toolbar.setPointSize(15)

        '''Font for menu'''
        self.font_menu = QtGui.QFont(font_family)
        self.font_menu.setPointSize(14)

        '''Message box'''
        self.message_box = QtWidgets.QMessageBox()

        '''Folder path for treeview'''
        self.folder_path_tree_view = ""

        '''Menu settings'''
        menubar = self.menuBar()
        menubar.setObjectName('menubar')
        menubar.setFont(self.font_menu)

        '''Configuration Json path'''
        menu_act_json_files_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "json_dark.png")), 'Json output', self)        
        menu_act_json_files_path.setStatusTip('')
        menu_act_json_files_path.triggered.connect(self.menu_json_files_path_function)

        '''Configuration Hierarchy path'''
        menu_act_hierarchy_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "hierarchy_dark.png")), 'Hierarchy', self)        
        menu_act_hierarchy_path.setStatusTip('')
        menu_act_hierarchy_path.triggered.connect(self.menu_hierarchy_path_function)

        '''Configuration Template path'''
        menu_act_json_templates_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "template_dark.png")), 'Template', self)        
        menu_act_json_templates_path.setStatusTip('')
        menu_act_json_templates_path.triggered.connect(self.menu_json_templates_path_function)  

        '''Configuration Excel path'''
        menu_act_excel_files_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "excel_dark.png")), 'Excel output', self)        
        menu_act_excel_files_path.setStatusTip('')
        menu_act_excel_files_path.triggered.connect(self.menu_excel_files_path_function)

        '''Configuration Excel Templates path'''
        menu_act_excel_templates_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "xls_dark.png")), 'Excel templates', self)        
        menu_act_excel_templates_path.setStatusTip('')
        menu_act_excel_templates_path.triggered.connect(self.menu_excel_templates_path_function)

        '''Configuration Excel Final path'''
        menu_act_excel_append_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "xls_final_dark.png")), 'Excel Final output', self)        
        menu_act_excel_append_path.setStatusTip('')
        menu_act_excel_append_path.triggered.connect(self.menu_excel_append_path_function)
        
        '''Logs'''
        menu_act_log_files_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "log_file")), 'Logs', self)        
        menu_act_log_files_path.setStatusTip('')
        menu_act_log_files_path.triggered.connect(self.menu_log_files_path_function)
        '''Post File path'''
        menu_act_post_files_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "export_dark.png")), 'Post Files output', self)        
        menu_act_post_files_path.setStatusTip('')
        menu_act_post_files_path.triggered.connect(self.menu_post_files_path_function)

        '''Reset paths default'''
        menu_act_reset_path = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "reset_dark.png")), 'Reset Path to Default', self)        
        menu_act_reset_path.setStatusTip('')
        menu_act_reset_path.triggered.connect(self.menu_reset_path_function) 

        '''INFO MENU'''
        '''User Guide'''
        menu_act_user_guide = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu", "guide_dark.png")), 'Open User Guide', self)        
        menu_act_user_guide.setStatusTip('')
        menu_act_user_guide.triggered.connect(self.menu_user_guide_function)

        '''ADD MENU'''
        '''Add template json'''
        menu_act_add_json_templates = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu","json_dark.png")), 'Add Template', self)
        menu_act_add_json_templates.setStatusTip('Add JSON Template')   
        menu_act_add_json_templates.triggered.connect(self.menu_add_json_templates_function)   

        '''Add Hierarchy xml'''
        menu_act_add_hierarchy = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu","xml_dark.png")), 'Add Hierarchy', self)
        menu_act_add_hierarchy.setStatusTip('Add Hierarchy XML')
        menu_act_add_hierarchy.triggered.connect(self.menu_add_hierarchy_function)

        '''DELETE MENU'''
        '''Delete template json'''
        menu_act_delete_json_templates = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu","json_dark_delete.png")), 'Delete Template', self)
        menu_act_delete_json_templates.setStatusTip('Delete JSON Template')   
        menu_act_delete_json_templates.triggered.connect(self.menu_delete_json_templates_function)   

        '''Delete Hierarchy xml'''
        menu_act_delete_hierarchy = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu","xml_dark_delete.png")), 'Delete Hierarchy', self)
        menu_act_delete_hierarchy.setStatusTip('Delete Hierarchy XML')
        menu_act_delete_hierarchy.triggered.connect(self.menu_delete_hierarchy_function)

        '''Software version'''
        menu_act_version = menubar.addMenu('Version 4.0.0.0')
        menu_act_version.setEnabled(False)
        menu_separator = menubar.addMenu('||')
        menu_separator.setEnabled(False)

        '''Change email'''
        menu_act_change_email = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "menu","list_dark.png")), 'Change email address', self)
        menu_act_change_email.setStatusTip('Change email address')
        menu_act_change_email.triggered.connect(self.change_email_function)

        '''set change menu'''
        menu_file_section = menubar.addMenu('&Change Path')
        menu_file_section.setFont(self.font_menu)
        menu_file_section.addAction(menu_act_json_files_path)
        menu_file_section.addAction(menu_act_json_templates_path)
        menu_file_section.addSeparator()
        menu_file_section.addAction(menu_act_hierarchy_path)
        menu_file_section.addSeparator()
        menu_file_section.addAction(menu_act_excel_files_path)
        menu_file_section.addAction(menu_act_excel_templates_path)
        menu_file_section.addAction(menu_act_excel_append_path)
        menu_file_section.addSeparator()
        menu_file_section.addAction(menu_act_log_files_path)
        menu_file_section.addSeparator()
        menu_file_section.addAction(menu_act_post_files_path)
        menu_file_section.addSeparator()
        menu_file_section.addAction(menu_act_reset_path) 
        menu_separator1 = menubar.addMenu('||')
        menu_separator1.setEnabled(False)

        '''set add menu'''
        menu_add_section = menubar.addMenu('&Add')
        menu_add_section.setFont(self.font_menu)
        menu_add_section.addAction(menu_act_add_json_templates)
        menu_add_section.addAction(menu_act_add_hierarchy)
        menu_separator2 = menubar.addMenu('||')
        menu_separator2.setEnabled(False)

        '''set menu delete'''
        menu_delete_section = menubar.addMenu('&Delete')
        menu_delete_section.setFont(self.font_menu)
        menu_delete_section.addAction(menu_act_delete_json_templates)
        menu_delete_section.addAction(menu_act_delete_hierarchy)
        menu_separator3 = menubar.addMenu('||')
        menu_separator3.setEnabled(False)

        '''set menu excel'''
        menu_excel_section = menubar.addMenu('&Excel')
        menu_excel_section.setFont(self.font_menu)
        menu_separator4 = menubar.addMenu('||')
        menu_separator4.setEnabled(False)

        '''set menu email'''
        menu_email_section = menubar.addMenu('&Email')
        menu_email_section.setFont(self.font_menu)
        menu_email_section.addAction(menu_act_change_email)
        menu_separator5 = menubar.addMenu('||')
        menu_separator5.setEnabled(False)
        
        '''set info menu'''
        menu_info_section = menubar.addMenu('&Info')
        menu_info_section.setFont(self.font_menu)
        menu_info_section.addAction(menu_act_user_guide)

        '''Toolbar bottom settings'''
        toolbar_bottom = QtWidgets.QToolBar(self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, toolbar_bottom)
        toolbar_bottom.setObjectName('toolbar_bottom')
        toolbar_bottom.setMovable(False)
        toolbar_bottom.setFont(self.font_toolbar)
        toolbar_bottom.setIconSize(QtCore.QSize(300,30))
        toolbar_bottom.setOrientation(QtCore.Qt.Vertical)
        toolbar_refresh_data = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "icon","refresh_dark.png")), 'Refresh data', self)
        toolbar_bottom.addAction(toolbar_refresh_data)
        toolbar_refresh_data.triggered.connect(self.refresh_window)

        '''Toolbar settings'''
        toolbar = QtWidgets.QToolBar(self)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, toolbar)
        toolbar.setObjectName('toolbar')
        toolbar.setMovable(False)
        toolbar.setFont(self.font_toolbar)
        toolbar.setIconSize(QtCore.QSize(130,160))
        toolbar.setOrientation(QtCore.Qt.Vertical)

        '''Toolbar elements'''
        toolbar_hierarchy_to_json = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "icon","create_json_icon.png")), 'Create JSON files from Hierarchy XML', self)
        toolbar_activate_things = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "icon","activate_thing_icon.png")), 'Activate or deactivate things', self)
        toolbar_create_excel = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "icon","create_excel_icon.png")), 'Create Excel files', self)
        #toolbar_diagnostics = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "icon","diagnostics_icon.png")), 'Diagnostics', self)
        toolbar_create_credentials = QtWidgets.QAction(QtGui.QIcon(join(realpath(''), "image", "icon","create_credentials_image_dark.png")), 'Diagnostics', self)

        '''Add element toolbar'''
        toolbar.addAction(toolbar_hierarchy_to_json)
        toolbar.addAction(toolbar_activate_things)
        toolbar.addAction(toolbar_create_excel)
        #toolbar.addAction(toolbar_diagnostics)
        toolbar.addAction(toolbar_create_credentials)

        '''Toolbar triggered'''
        toolbar_hierarchy_to_json.triggered.connect(self.hierarchy_to_json_main_interface)
        toolbar_activate_things.triggered.connect(self.activate_things_select_interface)
        toolbar_create_excel.triggered.connect(self.create_excel_select_interface)
        #toolbar_diagnostics.triggered.connect(self.diagnosticsMain_interface)
        toolbar_create_credentials.triggered.connect(self.open_create_credential)

        '''Label'''
        self.title_label = QtWidgets.QLabel()
        self.sub_title_label = QtWidgets.QLabel()
        self.logo_label = QtWidgets.QLabel()
        self.username_label = QtWidgets.QLabel()
        self.password_label = QtWidgets.QLabel()
        self.gateway_id_label = QtWidgets.QLabel()
        self.hierarchy_label = QtWidgets.QLabel()
        self.stage_label = QtWidgets.QLabel()
        self.thing_id_label = QtWidgets.QLabel()
        self.excel_output_name_label = QtWidgets.QLabel()
        self.excel_file_label = QtWidgets.QLabel()
        self.modify_period_label = QtWidgets.QLabel()
        self.site_name_label = QtWidgets.QLabel()
        self.set_period_label = QtWidgets.QLabel()
        self.file_name_label = QtWidgets.QLabel()

        '''Label set text'''
        self.title_label.setText("")
        self.logo_label.setText("")
        self.username_label.setText("Username")
        self.password_label.setText("Password")
        self.gateway_id_label.setText("Gateway ID")
        self.hierarchy_label.setText("Hierarchy")
        self.stage_label.setText("Environment")
        self.thing_id_label.setText("Thing ID")
        self.excel_output_name_label.setText("Excel output name")
        self.excel_file_label.setText("Excel file name")
        self.modify_period_label.setText("Modify period")
        self.site_name_label.setText("Site name")
        self.set_period_label.setText("Modify period")
        self.file_name_label.setText("File name")

        '''Label font'''
        self.title_label.setFont(self.font_title)
        self.sub_title_label.setFont(self.font_title)
        self.logo_label.setFont(self.font)
        self.username_label.setFont(self.font)
        self.password_label.setFont(self.font)
        self.gateway_id_label.setFont(self.font)
        self.hierarchy_label.setFont(self.font)
        self.stage_label.setFont(self.font)
        self.thing_id_label.setFont(self.font)
        self.excel_output_name_label.setFont(self.font)
        self.excel_file_label.setFont(self.font)
        self.modify_period_label.setFont(self.font)
        self.site_name_label.setFont(self.font)
        self.set_period_label.setFont(self.font)
        self.file_name_label.setFont(self.font)

        '''QLineEdit'''
        self.username_text = QtWidgets.QLineEdit()
        self.password_text = QtWidgets.QLineEdit()
        self.thing_id_text = QtWidgets.QLineEdit()
        self.excel_output_name_text = QtWidgets.QLineEdit()
        self.modify_period_text = QtWidgets.QLineEdit()
        self.site_name_text = QtWidgets.QLineEdit()
        self.set_period_text = QtWidgets.QLineEdit()
        self.set_period_text.setDisabled(True)

        '''Checkbox'''
        self.set_period_checkbox = QtWidgets.QCheckBox("", self)
        self.set_period_checkbox.clicked.connect(self.visibility_toggle)
        self.set_period_checkbox.setStyleSheet("QCheckBox:indicator{width: 30; height: 30;}")

        '''ComboBox'''
        self.gateway_id_combo_box = QtWidgets.QComboBox()
        self.hierarchy_combo_box = QtWidgets.QComboBox()
        self.stage_combo_box = QtWidgets.QComboBox()
        self.excel_file_combo_box = QtWidgets.QComboBox()

        '''Combobox population'''
        self.gateway_id_combo_box.addItems(list(self.env_config.keys()))
        self.hierarchy_combo_box.addItems(utility.create_file_list(self.hierarchy_path, ".xml"))
        self.stage_combo_box.addItems([_dict["stage"] for _dict in self.env_config.values()])
        self.excel_file_combo_box.addItems(utility.create_file_list(self.excel_files_path, ".xml"))
        
        '''Checkbox list'''
        self.list_check = []

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

        '''Layout
        vertical_box = QtWidgets.QVBoxLayout()
        horizontal_box = QtWidgets.QHBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()
        '''

        self.start_page_interface()


    '''________________________________________________________________________________________________'''

    def on_select_treeview(self, index):
        self.folder_path = self.sender().model().filePath(index) 

    '''________________________________________________________________________________________________'''


    def start_page_interface(self):
        self.title_label.setText("Welcome to JasonX")
        self.sub_title_label.setText("enel x")
        self.logo_label.setPixmap(QtGui.QPixmap(join(realpath(''), "image", "icon", "search_logo.png")).scaled(600, 600))

        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sub_title_label.setAlignment(QtCore.Qt.AlignRight)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        layout_widget = QtWidgets.QWidget()
        vertical_box = QtWidgets.QVBoxLayout()
        vertical_box.addWidget(self.title_label)
        vertical_box.addWidget(self.sub_title_label)
        vertical_box.addWidget(self.logo_label)
        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)


    '''________________________________________________________________________________________________'''


    def hierarchy_to_json_main_interface(self):
        self.title_label.setText("Create Json files")
        self.logo_label.setPixmap(QtGui.QPixmap(join(realpath(''), "image", "icon", "xml_to_json_image.png")).scaled(450, 300))

        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        '''Button'''
        button_open_viewinterface_json = QtWidgets.QPushButton("Send Data")
        button_open_viewinterface_json.setFont(self.font)
        button_open_viewinterface_json.clicked.connect(self.control_input_data)

        vertical_box = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username_text, 0, 1)  
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_text, 1, 1)
        grid_layout.addWidget(self.gateway_id_label, 2, 0)
        grid_layout.addWidget(self.gateway_id_combo_box, 2, 1)
        grid_layout.addWidget(self.hierarchy_label, 3, 0)
        grid_layout.addWidget(self.hierarchy_combo_box, 3, 1)
        vertical_box.addWidget(self.logo_label)
        vertical_box.addWidget(self.title_label)
        vertical_box.addLayout(grid_layout)
        vertical_box.addWidget(button_open_viewinterface_json)
        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)

    def control_input_data(self):
            if(self.username_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', '') != "" and self.password_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', '') != "" and self.gateway_id_combo_box.currentText() != "" and self.hierarchy_combo_box.currentText() != ""):
                try:
                    self.jasonx_instance = Jasonx(self.username_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', ''), self.password_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', ''), self.gateway_id_combo_box.currentText(), self.env_config[self.gateway_id_combo_box.currentText()]["environment_prefix"], self.hierarchy_combo_box.currentText(), True)
                except Exception as e:
                    logging.error(e, exc_info=True)
            else:
                self.message_box.about(self, "Error input data", "Error input data")
                

    def  hierarchy_to_json_view_interface(self):
        button_create_json_file = QtWidgets.QPushButton("Generate JSON")
        button_create_json_file.setFont(self.font)
        button_create_json_file.clicked.connect(self.create_json_files)

        '''Table'''
        table = QtWidgets.QTableWidget()
        table.setRowCount(len(self.jasonx_instance.dict_meter_template))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Meter Name", "Model"])
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.setColumnWidth(0, 800)
        table.setColumnWidth(1, 800)

        try:
            count = 0
            for meter, model in self.jasonx_instance.dict_meter_template.items():
                table.setItems(count, 0, QtWidgets.QTableWidgetItem(meter))
                table.setItems(count, 1, QtWidgets.QTableWidgetItem(model))
                count += 1
        except Exception as e:
            logging.error(e, exc_info=True)

        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()
        grid_layout.addWidget(table, 0, 0)
        grid_layout.addWidget(button_create_json_file, 1, 0)

        layout_widget.setLayout(grid_layout)

        self.setCentralWidget(layout_widget)


    def create_json_files(self):
        if(self.jasonx_instance.dict_meters_not_found != {}):
            button_reply = self.message_box.question(self, 'JasonX', "Some templates are missing, do you want to create?",  self.message_box.Yes | self.message_box.No, self.message_box.No)
            if button_reply == self.message_box.Yes:
                try:
                    response = self.jasonx_instance.create_template()
                    self.hierarchy_to_json_main_interface()
                    if(response == []):
                        self.message_box.about(self, "JasonX", "Templates created!")
                    else:
                        self.message_box.about(self, "JasonX", "Trend_id not found!")
                except Exception as e:
                    logging.error(e, exc_info=True)
            else:
                try:
                    self.jasonx_instance.create_json()
                    self.message_box.about(self, "JasonX", "JSON files created!")
                except Exception as e:
                    logging.error(e, exc_info=True)
        else:
            try:
                self.jasonx_instance.create_json()
                self.message_box.about(self, "JasonX", "JSON files created!")
            except Exception as e:
                logging.error(e, exc_info=True)

    
    '''________________________________________________________________________________________________'''

    def open_create_credential(self):
        try:
            button_reply = self.message_box.question(self, 'Generated credentials now?', " !!!ATTENTION!!!\nOpen VPN. \nCredentials are valid one hour.",  self.message_box.Yes | self.message_box.No, self.message_box.No)
            if button_reply == self.message_box.Yes:
                call(join(realpath(''), "CreateCredential.bat")) 
        except Exception as e:
            logging.error(e, exc_info=True)


    def activate_things_select_interface(self):
        '''Button'''
        button_activate_dummy = QtWidgets.QPushButton("")
        button_open_activate_things = QtWidgets.QPushButton("")
        button_open_deactivate_things = QtWidgets.QPushButton("")
        button_refresh_get = QtWidgets.QPushButton("")

        '''Button font'''
        button_activate_dummy.setFont(self.font_title)
        button_open_activate_things.setFont(self.font_title)
        button_open_deactivate_things.setFont(self.font_title)
        button_refresh_get.setFont(self.font_title)

        '''Button object name'''
        button_activate_dummy.setObjectName("button_activate_dummy")
        button_open_activate_things.setObjectName("button_open_activate_things")
        button_open_deactivate_things.setObjectName("button_open_deactivate_things")
        button_refresh_get.setObjectName("button_refresh_get")

        '''Button icon'''
        button_activate_dummy.setIcon(QtGui.QIcon('image/icon/activate_thing_dummy_image.png'))
        button_open_activate_things.setIcon(QtGui.QIcon('image/icon/activate_thing_image.png'))
        button_open_deactivate_things.setIcon(QtGui.QIcon('image/icon/deactivate_thing_image.png'))
        button_refresh_get.setIcon(QtGui.QIcon('image/icon/refresh_get_image.png'))

        '''Button icon size'''
        button_activate_dummy.setIconSize(QtCore.QSize(390,390))
        button_open_activate_things.setIconSize(QtCore.QSize(400,400))
        button_open_deactivate_things.setIconSize(QtCore.QSize(400,400))
        button_refresh_get.setIconSize(QtCore.QSize(400, 400))

        '''Button function'''
        button_activate_dummy.clicked.connect(self.activate_dummy_interface)
        button_open_activate_things.clicked.connect(self.select_folder_activate_things)
        button_open_deactivate_things.clicked.connect(self.deactivate_things_interface)
        button_refresh_get.clicked.connect(self.select_folder_refresh_get)

        grid_layout = QtWidgets.QGridLayout()
        vertical_box = QtWidgets.QVBoxLayout()
        layout_widget = QtWidgets.QWidget()
        grid_layout.addWidget(button_refresh_get, 0, 0)
        grid_layout.addWidget(button_activate_dummy, 0, 1)
        grid_layout.addWidget(button_open_activate_things, 1, 0)
        grid_layout.addWidget(button_open_deactivate_things, 1, 1)
        vertical_box.addLayout(grid_layout)
        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)

    
    def activate_dummy_interface(self):
        self.title_label.setText("Activate dummy")
        self.logo_label.setPixmap(QtGui.QPixmap(join(realpath(''), "image", "icon", "icon.png")).scaled(350, 300))

        self.title_label.setAlignment(QtCore.Qt.AlignCenter)  
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        button_activate_dummy = QtWidgets.QPushButton("Send Data")
        button_activate_dummy.setFont(self.font)
        button_activate_dummy.clicked.connect(self.control_input_data_dummy)

        vertical_box = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username_text, 0, 1)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_text, 1, 1)
        grid_layout.addWidget(self.gateway_id_label, 2, 0)
        grid_layout.addWidget(self.gateway_id_combo_box, 2, 1)

        vertical_box.addWidget(self.logo_label)
        vertical_box.addChildWidget(self.title_label)
        vertical_box.addLayout(grid_layout)
        vertical_box.addWidget(button_activate_dummy)

        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)


    def control_input_data_dummy(self):
        if(self.username_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', '') != "" and self.password_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', '') != "" and self.gateway_id_combo_box.currentText() != ""):
            try:
                response = activate_dummy(self.username_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', '') != "", self.password_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', '') != "", self.gateway_id_combo_box.currentText() != "", self.env_config[self.gateway_id_combo_box.currentText()])
                self.activate_dummy_view_interface(response)
            except Exception as e:
                logging.error(e, exc_info=True)
        else:
            self.message_box.about(self, "Error input data", "Error input data")

    
    def activate_dummy_view_interface(self, response):
        '''Button settings'''
        button_send_report = QtWidgets.QPushButton("Send Report")
        button_send_report.setFont(self.font)
        button_send_report.clicked.connect(self.send_report_function)

        table = QtWidgets.QTableWidget()
        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()

        table.setRowCount(1)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Status', 'Message'])
        table.setColumnWidth(0, 800)
        table.setColumnWidth(1, 800)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(response[0])))
        table.setItem(0, 1, QtWidgets.QTableWidgetItem(response[1]))

        grid_layout.addWidget(table, 0, 0)
        grid_layout.addWidget(button_send_report)

        layout_widget.setLayout(grid_layout)
        self.setCentralWidget(layout_widget)


    def select_folder_activate_things(self):
        '''Button settings'''
        button_open_activate_thing_main_interface = QtWidgets.QPushButton("Select")
        button_open_activate_thing_main_interface.setFont(self.font)
        button_open_activate_thing_main_interface.clicked.connect(self.open_activate_thing_main_interface)

        vertical_box = QtWidgets.QVBoxLayout()
        layout_widget = QtWidgets.QWidget()
        vertical_box.addWidget(self.treeview)
        vertical_box.addWidget(button_open_activate_thing_main_interface)
        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)


    def open_activate_thing_main_interface(self):
        button_reply = self.message_box.question(self, 'JasonX', "Select json files in this folder?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            self.activateThingMainInterface()
        self.close 


    def activate_thing_main_interface(self):
        '''Button settings'''
        button_activate_thing = QtWidgets.QPushButton("Activate Things")
        button_activate_thing.setFont(self.font)
        button_activate_thing.clicked.connect(self.activate_thing)

        if(isfile(self.folder_path)):
            self.hierarchy_name = utility.get_substring(QtCore.QFileInfo(self.folder_path).absolutePath(), start = '/json_files/', stop = '')
            lis = []
            lis.append(utility.get_substring(self.folder_path, start = self.hierarchy_name + '/', stop = ''))
            self.list_file_json = lis
        else:
            self.list_file_json = utility.create_file_list(self.folder_path , ".json")
            self.name_hierarchy = utility.get_substring(QtCore.QFileInfo(self.folder_path).absoluteFilePath(), start = '/json_files/', stop = '')
        
        table = QtWidgets.QTableWidget()
        layout_widget = QtWidgets.QWidget()
        table.setRowCount(len(self.list_file_json))
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["File JSON"])
        table.setColumnWidth(0, 1000)

        count = 0
        for _file in self.list_file_json:
            table.setItem(count, 0, QtWidgets.QTableWidgetItem(_file))
            count +=1

        vertical_box = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(table, 0, 0)

        vertical_box.addLayout(grid_layout)
        vertical_box.addWidget(self.gateway_id_label)
        vertical_box.addWidget(self.gateway_id_combo_box)
        vertical_box.addWidget(button_activate_thing)

        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)


    def activate_thing(self):
        button_reply = self.message_box.question(self, 'JasonX', "Do you want active these things?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            try:
                self.message_box.about(self, "Activate Things", "Activations in progress.. Switch to console window now") 
                self.dict_response = initialize_activations(self.hierarchy_name, self.list_file_json, self.combo_box_gateway_id.currentText(), self.env_config[self.combo_box_gateway_id.currentText()])
                self.activate_thing_view_interface()
            except Exception as e:
                logging.error(e, exc_info=True)


    def activate_thing_view_interface(self): 
        '''Button settings'''
        button_send_report = QtWidgets.QPushButton("Send Report")
        button_send_report.setFont(self.font)
        button_send_report.clicked.connect(self.send_report_function)

        table = QtWidgets.QTableWidget()
        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()
        table.setRowCount(len(self.dict_response))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Status', 'Message'])
        table.setColumnWidth(0, 500)
        table.setColumnWidth(1, 500)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        '''Table population'''
        count = 0  
        for status, message in self.dict_response.items():
            table.setItem(count, 0, QtWidgets.QTableWidgetItem(status))
            table.setItem(count, 1, QtWidgets.QTableWidgetItem(message))
            count +=1

        grid_layout.addWidget(table, 0, 0)
        grid_layout.addWidget(button_send_report, 1, 0)

        layout_widget.setLayout(layout_widget)
        self.setCentralWidget(layout_widget)


    def send_report_function(self):
        button_reply = self.message_box.question(self, 'JasonX', "Create file logs?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = utility.create_logs(self.dict_response, self.hierarchy_name)
            if(response == True):
                self.message_box.about(self, "JasonX", "File logs created successfully!")


    def deactivate_things_interface(self):
        '''Button settings'''
        button_deactivate_thing = QtWidgets.QPushButton("Deactivate Things")
        button_deactivate_thing.setFont(self.font)
        button_deactivate_thing.clicked.connect(self.deactivate_things_function)

        vertical_box = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()
        grid_layout.addWidget(self.gateway_id_label, 0, 0)
        grid_layout.addWidget(self.gateway_id_combo_box, 0, 1)
        grid_layout.addWidget(self.thing_id_label, 1, 0)
        grid_layout.addWidget(self.thing_id_text, 1, 1)

        vertical_box.addLayout(grid_layout)
        vertical_box.addWidget(button_deactivate_thing)

        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)

    
    def deactivate_thing_function(self):
        try:
            gateway_id = self.gateway_id_combo_box.currentText()
            account = self.env_config[gateway_id]["account"]
            environment_prefix = self.env_config[gateway_id]["environment_prefix"]
            stage = account = self.env_config[gateway_id]["stage"]
            api_id_post = account = self.env_config[gateway_id]["api_id_post"]

            dict_credentials = read_credentials(account)
            dict_credentials["account"] = account

            endpoint = 'https://' + api_id_post + '.execute-api.eu-central-1.amazonaws.com/' + stage + '/v1/gateways/' + gateway_id +'/command'
            data = {
                "command": "deactivate-thing",
                "env_prefix": environment_prefix,
                "gateway_id": gateway_id,
                "parameters": {
                    "thing_id": gateway_id +"_thing"+self.thing_id_text.text()
                    }
                }
            payload = dumps(data, indent = 4)
            response = post(dict_credentials, endpoint, stage, payload)
            self.message_box.about(self, "Deactivate things", str(response))
        except Exception as e:
            logging.error(e, exc_info=True)
            self.message_box.about(self, "Deactivate things", "Error!")

    def select_folder_refresh_get(self):
        '''Button settings'''
        button_open_refresh_get_interface = QtWidgets.QPushButton("Select")
        button_open_refresh_get_interface.setFont(self.font)
        button_open_refresh_get_interface.clicked.connect(self.open_refresh_get_interface)

        vertical_box = QtWidgets.QVBoxLayout()
        layout_widget = QtWidgets.QWidget()
        vertical_box.addWidget(self.treeview)
        vertical_box.addWidget(button_open_refresh_get_interface)
        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)

        
    def open_refresh_get_interface(self):
        button_reply = self.message_box.question(self, 'JasonX', "Select json files in this folder?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            self.refresh_get_interface()
        self.close


    def refresh_get_interface(self):
        '''Button settings'''
        button_refresh_get = QtWidgets.QPushButton("Get ID Thing")
        button_refresh_get.setFont(self.font)
        button_refresh_get.clicked.connect(self.refresh_get)

        if(isfile(self.folder_path)):
            self.hierarchy_name = utility.get_substring(QtCore.QFileInfo(self.folder_path).absolutePath(), start = '/post_files/', stop = '')
            lis = []
            lis.append(utility.get_substring(self.folder_path, start = self.hierarchy_name + '/', stop = ''))
            self.list_file_json = lis
        else:
            self.list_file_json = utility.create_file_list(QtCore.QFileInfo(self.folder_path).absoluteFilePath(), ".json")
            self.hierarchy_name = utility.get_substring(self.folder_path, start = '/post_files/', stop = '')

        table = QtWidgets.QTableWidget()                  
        table.setRowCount(len(self.list_file_json))
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Post reports"])
        table.setColumnWidth(0,1000)  

        vertical_box = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(table, 0, 0)

        vertical_box.addLayout(grid_layout)
        vertical_box.addWidget(self.stage_combo_box)
        vertical_box.addWidget(button_refresh_get)


    def refresh_get(self):
        self.dict_response = {}
        for _file in self.list_file_json:
            self.dict_response[_file] = refresh_get(_file, self.hierarchy_name, self.stage_combo_box.currentText())
        self.refresh_get_view_interface()

    
    def refresh_get_view_interface(self):
        '''Button settings'''
        button_create_log = QtWidgets.QPushButton("Send Report")
        button_create_log.setFont(self.font)
        button_create_log.clicked.connect(self.button_function_create_log_refresh_get)

        table = QtWidgets.QTableWidget()
        grid_layout = QtWidgets.QGridLayout()
        layout_widget = QtWidgets.QWidget()    
        table.setRowCount(len(self.dict_response))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Thing','Status', 'Message'])
        table.setColumnWidth(0, 500)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 500)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        count = 0  
        for thing in self.dict_response.keys():
            status, message = self.dict_response[thing]
            table.setItem(count, 0, QtWidgets.QTableWidgetItem(thing))
            table.setItem(count, 1, QtWidgets.QTableWidgetItem(str(status)))
            table.setItem(count, 2, QtWidgets.QTableWidgetItem(message))
            count +=1

        grid_layout.addWidget(table, 0, 0)
        grid_layout.addWidget(button_create_log, 1, 0)

        layout_widget.setLayout(grid_layout)
        self.setCentralWidget(layout_widget)


    def button_function_create_log_refresh_get(self):
        button_reply = self.message_box.question(self, 'JaSONx', "Create file logs ?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            response = utility.create_logs(self.dict_response, self.hierarchy_name)
            if(response == True):
                self.message_box.about(self, "JaSONx", "Logs files have been created and sent successfully!")
            else:
                self.message_box.about(self, "JaSONx", "Error on logs creating")
        

    '''________________________________________________________________________________________________'''


    def create_excel_select_interface(self):
        button_append_excel = QtWidgets.QPushButton("")
        button_excel_eis = QtWidgets.QPushButton("")
        button_open_excel_datalake = QtWidgets.QPushButton("")

        '''Button font'''
        button_append_excel.setFont(self.font_title)
        button_excel_eis.setFont(self.font_title)
        button_open_excel_datalake.setFont(self.font_title)

        '''Button object name'''
        button_append_excel.setObjectName("button_open_append_excel")
        button_excel_eis.setObjectName("button_open_excel_eis")
        button_open_excel_datalake.setObjectName("button_open_excel_datalake")

        '''Button icon'''
        button_append_excel.setIcon(QtGui.QIcon('image/icon/append_excel_files_image.png'))
        button_excel_eis.setIcon(QtGui.QIcon('image/icon/create_excel_eis_image.png'))
        button_open_excel_datalake.setIcon(QtGui.QIcon('image/icon/excel_datalake_image.png'))

        '''Button icon size'''
        button_append_excel.setIconSize(QtCore.QSize(450,400))
        button_excel_eis.setIconSize(QtCore.QSize(350,400))
        button_open_excel_datalake.setIconSize(QtCore.QSize(350,400))

        '''Button function'''
        button_append_excel.clicked.connect(self.append_excel_files_interface)
        button_excel_eis.clicked.connect(self.create_excel_files_interface)
        button_open_excel_datalake.clicked.connect(self.create_excel_datalake_interface)

        grid_layout = QtWidgets.QGridLayout()
        horizontal_box = QtWidgets.QHBoxLayout()
        layout_widget = QtWidgets.QWidget()
        grid_layout.addWidget(button_excel_eis, 0, 0)
        grid_layout.addWidget(button_open_excel_datalake, 0, 1)
        
        horizontal_box.addWidget(button_append_excel)
        horizontal_box.addLayout(grid_layout)

        layout_widget.setLayout(horizontal_box)
        self.setCentralWidget(layout_widget)

    
    def create_excel_files_interface(self):
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setPixmap(QtGui.QPixmap(join(realpath(''), "image", "title.svg")))

        '''Button settings'''
        button_create_excel = QtWidgets.QPushButton("Create EIS Registry")
        button_create_excel.setFont(self.font)
        button_create_excel.clicked.connect(self.create_excel_files_function)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.site_name_label, 0, 0)
        grid_layout.addWidget(self.site_name_text, 0, 2)
        grid_layout.addWidget(self.set_period_label, 1, 0) 
        grid_layout.addWidget(self.set_period_checkbox, 1, 1)
        grid_layout.addWidget(self.set_period_text, 1, 2)
        grid_layout.addWidget(self.hierarchy_label, 2, 0)
        grid_layout.addWidget(self.hierarchy_combo_box, 2, 2)
        grid_layout.addWidget(self.gateway_id_label, 3, 0)
        grid_layout.addWidget(self.gateway_id_combo_box, 3, 2)

        vertical_box = QtWidgets.QVBoxLayout()
        layout_widget = QtWidgets.QWidget()
        vertical_box.addWidget(self.title_label)
        vertical_box.addLayout(grid_layout)
        vertical_box.addWidget(button_create_excel)

        layout_widget.setLayout(vertical_box)
        self.setCentralWidget(layout_widget)


    def create_excel_files_function(self):
        if(self.site_name_text.text().strip("\n").strip("\r").strip("\r\n").replace(' ', '')):
            if(self.hierarchy_combo_box.currentText() != "" and self.gateway_id_combo_box.currentText() != ""):
                if(exists(join(realpath(''), self.excel_templates_path, "templateLeonardo.xlsx"))):    
                    import Excel
                    self.jasonx_instance = Jasonx("None", "None", self.gateway_id_combo_box.currentText(), self.env_config[self.gateway_id_combo_box.currentText()]["environment_prefix"], self.hierarchy_combo_box.currentText(), False)
                    self.jasonx_instance.create_json()
                    if(self.set_period_checkbox.isChecked()):
                        response = Excel.Excel(self.site_name_text.text(), self.jasonx_instance.hierarchy_name, self.jasonx_instance.environment_prefix, self.jasonx_instance.dict_meters, int(self.set_period_text.text()), self.jasonx_instance.gateway_id)
                    else:
                        response = Excel.Excel(self.site_name_text.text(), self.jasonx_instance.hierarchy_name, self.jasonx_instance.environment_prefix, self.jasonx_instance.dict_meters, 0, self.jasonx_instance.gateway_id)
                    if(response):   
                        self.message_box.about(self, "Create excel", "Excel files created") 
                    else:
                        self.message_box.about(self, "Create excel", "Error!") 
                else:
                    self.message_box.about(self, "JasonX", "Excel template not found!")  
        else:
            self.site_name_text.setStyleSheet("border: 1px solid #502088; border-radius:10px; height:40px; color: #ffffff; font:16pt 'Verdana'; background-color:#ff4b4b") 
            self.site_name_text.setPlaceholderText("Insert site name")  

    
    def visibility_toggle(self):
        if(self.set_period_checkbox.isChecked() == False):
            self.set_period_text.setDisabled(True)
        else:
            self.set_period_text.setDisabled(False)

    
    def append_excel_files_interface(self):
        '''Button settings'''
        button_excel_append = QtWidgets.QPushButton("Append")
        button_excel_append.setFont(self.font)   
        button_excel_append.clicked.connect(self.start_append_excel_function)    

        list_file = utility.create_file_list(self.excel_files_path, ".xlsx")

        for file_name in list_file:
            self.list_check.append(QtWidgets.QCheckBox(file_name, self)) 

        vertical_box_check = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("width:500")
        widget.adjustSize()

        '''Insert checkbox'''
        for check_box in self.list_check:
            vertical_box_check.addWidget(check_box)

        widget.setLayout(vertical_box_check)

        '''Scroll'''
        scroll = QtWidgets.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        vertical_box = QtWidgets.QVBoxLayout()
        layout_widget = QtWidgets.QWidget()
        vertical_box.addWidget(scroll)
        vertical_box.addWidget(self.file_name_label)
        vertical_box.addWidget(self.file_name_text)
        vertical_box.addWidget(button_excel_append)

        layout_widget.addLayout(vertical_box)
        self.setCentralWidget(layout_widget)


    def start_append_excel_function(self, state):
        button_reply = self.message_box.question(self, 'JasonX', "Append Excel files?",  QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No,  QtWidgets.QMessageBox.No)
        if button_reply == QtWidgets.QMessageBox.Yes:
            import ExcelAppend
            response = ExcelAppend.create_excel(self.dict_config, self.list_check, self.file_name_text.text()) 
            if(response == True):
                self.message_box.about(self, "JasonX", "File Excel created successfully!")   
            else:
                self.message_box.about(self, "Jasonx", "Error!")          


    def diagnostics_main_interface(self):
        ''' '''        


    '''________________________________________________________________________________________________________________'''
    
    
    def refresh_window(self):
        try:
            logging.info("Refreshing window")
            button_reply = self.message_box.question(self, 'JasonX', "Refresh application?",  self.message_box.Yes |  self.message_box.No,  self.message_box.No)
            if button_reply ==self.message_box.Yes:            
                self.start_page_interface()
        except Exception as e:
            logging.error(e, exc_info=True)

    
    '''________________________________________________________________________________________________________________'''


    '''Change path items'''
    def menu_hierarchy_path_function(self):
        try:
            logging.info("Changing Path Hierarchy")
            self.dialog = self.menu_interface_instance.change_path_hierarchy_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_json_templates_path_function(self):
        try:
            logging.info("Changing path template")
            self.dialog = self.menu_interface_instance.change_path_template_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_excel_files_path_function(self):
        try:
            logging.info("Changing path to Excel")
            self.dialog = self.menu_interface_instance.change_path_excel_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_excel_templates_path_function(self):
        try:
            logging.info("Changing path to Excel Templates")
            self.dialog = self.menu_interface_instance.change_path_excel_templates_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_excel_append_path_function(self):
        try:
            logging.info("Changing final Excel path")
            self.dialog = self.menu_interface_instance.change_path_excel_final_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)
            

    def menu_json_files_path_function(self):
        try:
            logging.info("Changing Json file path")
            self.dialog = self.menu_interface_instance.change_path_json_file_interface()
            self.dialog.showMaximized()  
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_log_files_path_function(self):
        try:
            logging.info("Changing logs path")
            self.dialog = self.menu_interface_instance.change_path_logs_file_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_post_files_path_function(self):
        try:
            logging.info("Changing post files path")
            self.dialog = self.menu_interface_instance.change_path_post_files_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_reset_path_function(self):
        try:
            logging.info("Reseting default path")
            button_reply = self.message_box.question(self, 'JaSONx', "Reset default path?",  self.message_box.Yes | self.message_box.No, self.message_box.No)
            if button_reply == self.message_box.Yes:
                reset_path()
                logging.info("Reset path sucessfuly")
                self.message_box.about(self, "Reset path", "Reset path to default")      
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_add_json_templates_function(self):
        try:
            logging.info("Adding Template")
            self.dialog = self.menu_interface_instance.add_json_template_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_add_hierarchy_function(self):
        try:
            logging.info("Adding Template")
            self.dialog = self.menu_interface_instance.add_hierarchy_interface()
            self.dialog.showMaximized()
        except Exception as e:
            logging.error(e, exc_info=True)

        
    '''Info items'''
    def menu_user_guide_function(self):
        try:
            logging.info("Opening guide")
            open_new(join(realpath(''), "User Guide.pdf")) 
        except Exception as e:
            logging.error(e, exc_info=True)  


    '''Delete items'''
    def menu_delete_json_templates_function(self):
        try:
            logging.info("Delete Template")
            self.dialog = self.menu_interface_instance.delete_json_template_interface()
            self.dialog.show()
        except Exception as e:
            logging.error(e, exc_info=True)


    def menu_delete_hierarchy_function(self):
        try:
            logging.info("Delete Hierarchy")
            self.dialog = self.menu_interface_instance.delete_hierarchy_interface()
            self.dialog.show()
        except Exception as e:
            logging.error(e, exc_info=True)


    def change_email_function(self):
        try:
            logging.info("Change email address")
            dialog = self.menu_interface_instance.change_email_interface()
            dialog.show()
        except Exception as e:
            logging.error(e, exc_info=True) 


'''Main functions'''
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainInterface()
    main.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()