import sys
import sqlite3
import os
import random
import datetime
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


conn = sqlite3.connect('stock.db')
c = conn.cursor()

conn1 = sqlite3.connect('users.db')
c1 = conn1.cursor()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('database.png'))

        # Set up users table if not exists
        c1.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")
        conn1.commit()
        
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)


        self.label_username = QLabel("Username:", self)
        self.label_username.move(50, 50)
        self.text_username = QLineEdit(self)
        self.text_username.move(150, 50)

        self.label_password = QLabel("Password:", self)
        self.label_password.move(50, 80)
        self.text_password = QLineEdit(self)
        self.text_password.setEchoMode(QLineEdit.Password)
        self.text_password.move(150, 80)

        self.button_login = QPushButton("Login", self)
        self.button_login.move(150, 120)
        self.button_login.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.text_username.text()
        password = self.text_password.text()

        # Check for empty fields
        if not username or not password:
            QMessageBox.warning(self, 'Login Error', 'Username or password cannot be empty.')
            return
        
        # Check for character length
        if len(username) > 12 or len(password) > 12:
            QMessageBox.warning(self, 'Login Error', 'Username and password cannot be longer than 12 characters.')
            return
        
        # Create new connection object and cursor
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # Check login credentials in SQLite database
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        
        if user is None:
            self.statusBar().showMessage("Incorrect username or password.")
            QMessageBox.warning(self, 'Login Error', 'Username and password are incorrect')
            return
        
        role = user[2]
        if role == "admin":
            self.main_window = AdminWindow() 
        elif role == "employee":
            self.main_window = EmployeeWindow()
            
        self.main_window.show()
        self.close()
        
        # Close connection
        conn.close()

class EmployeeWindow(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()
        self.setWindowIcon(QIcon('database.png'))


    def initUI(self):
        self.setWindowTitle('DBMS v1.0.0')
        self.st = stackedExample()
        helpAct = QAction(QIcon('help_icon.png'), 'Help', self)
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        IDAct = QAction(QIcon('Security.png'), 'Permissions', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        helpAct.setStatusTip('Program Information')
        IDAct.setStatusTip('Security clearance level')
        exitAct.triggered.connect(self.close)
        helpAct.triggered.connect(self.open_popup)
        IDAct.triggered.connect(self.Admin_popup)
        self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)
        toolbar.addAction(helpAct)
        toolbar.addAction(IDAct)
        
        dark_mode_checkbox = QCheckBox('Dark Mode', self)
        dark_mode_checkbox.setChecked(False)
        dark_mode_checkbox.stateChanged.connect(self.toggle_theme)
        toolbar.addWidget(dark_mode_checkbox)

        self.setCentralWidget(self.st)

    def open_popup(self):
        popup = QMessageBox()
        popup.setWindowTitle('Application Information')
        popup.setText('Welcome to the Database management system.\nPlease find additional information here: https://github.com/KashiCode/SimpleDBMS.\nKashiCode 2023©')
        popup.exec_()

        self.show()

    def Admin_popup(self):
        popup = QMessageBox()
        popup.setWindowTitle('Security clearance level')
        popup.setText('Your level of Access is Employee.\nKashiCode 2023©')
        popup.exec_()

        self.show()

    def toggle_theme(self, state):
        if state == Qt.Checked:
            qApp.setStyle(QStyleFactory.create('Fusion'))
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            qApp.setPalette(palette)
        else:
            qApp.setStyle(QStyleFactory.create('Windows'))
            qApp.setPalette(qApp.style().standardPalette())


class stackedExample(QWidget):
    def __init__(self):
        super(stackedExample, self).__init__()

        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Manage stock')
        self.leftlist.insertItem(1, 'Manage orders')
        self.leftlist.insertItem(2, 'View stock')
        self.leftlist.insertItem(3, 'Orders/Transactions')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(500, 350, 200, 200)
        self.show()

    def display(self, i):
        self.Stack.setCurrentIndex(i)
      

    def stack1UI(self):

        layout = QHBoxLayout()
        layout.setGeometry(QRect(0,300,1150,500))
        tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        tabs.addTab(self.tab1, 'Add Stock')
        tabs.addTab(self.tab2, 'Reduce Quantity')
        tabs.addTab(self.tab3, 'Delete Stock')

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        layout.addWidget(tabs)
        self.stack1.setLayout(layout)


   
    def tab1UI(self):
        layout = QFormLayout()


        self.ok = QPushButton('Add Stock', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name = QLineEdit()
        layout.addRow("Stock Name", self.stock_name)

        self.stock_count = QLineEdit()
        layout.addRow("Quantity", self.stock_count)

        self.stock_cost = QLineEdit()
        layout.addRow("Cost of Stock (per item)", self.stock_cost)

        layout.addWidget(self.ok)
        layout.addWidget(cancel)

        self.ok.clicked.connect(self.on_click)

        cancel.clicked.connect(self.stock_name.clear)
        cancel.clicked.connect(self.stock_cost.clear)
        cancel.clicked.connect(self.stock_count.clear)
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        self.ok_red = QPushButton('Reduce Stock', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name_red = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_red)

        self.stock_count_red = QLineEdit()
        layout.addRow("Quantity to reduce", self.stock_count_red)


        layout.addWidget(self.ok_red)
        layout.addWidget(cancel)
        self.tab2.setLayout(layout)
        
        # links the function to reduce stock
        self.ok_red.clicked.connect(self.call_red)
        cancel.clicked.connect(self.stock_name_red.clear)
        cancel.clicked.connect(self.stock_count_red.clear)

    def tab3UI(self):
        layout = QFormLayout()
        self.ok_del = QPushButton('Delete Stock', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name_del = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_del)
        layout.addWidget(self.ok_del)
        layout.addWidget(cancel)
        self.tab3.setLayout(layout)

        self.ok_del.clicked.connect(self.call_del)  
        cancel.clicked.connect(self.stock_name_del.clear)



    def on_click(self):
        now = datetime.datetime.now()
        stock_name_inp = self.stock_name.text().replace(' ','_').lower()[:12]
        stock_count_inp = self.stock_count.text()
        stock_cost_inp = self.stock_cost.text()
    
        if not stock_name_inp.strip() or not stock_count_inp.strip() or not stock_cost_inp.strip():
            QMessageBox.warning(self, "Error", "All fields are required")
            return
    
        try:
            stock_count_inp = int(stock_count_inp)
            stock_cost_inp = int(stock_cost_inp)
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity and cost must be integers")
            return
        
        if stock_count_inp <= 0 or stock_cost_inp <= 0:
            QMessageBox.warning(self, "Error", "Quantity and cost must be greater than zero")
            return
        
        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        d = insert_prod(stock_name_inp, stock_count_inp, stock_cost_inp, stock_add_date_time)
        print(d)



    def call_del(self):
        now = datetime.datetime.now()
        stock_del_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_del.text().replace(' ','_').lower()
        L = remove_stock(stock_name,stock_del_date_time)
        print(L)

    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_red.text().replace(' ','_').lower()
        stock_val_str = self.stock_count_red.text()
    
    # Check if stock name and quantity are not left empty
        if not stock_name:
            QMessageBox.warning(self, 'Error', 'Stock name cannot be left empty.')
            return
        if not stock_val_str:
            QMessageBox.warning(self, 'Error', 'Quantity cannot be left empty.')
            return
    
    # Check if quantity is an integer
        try:
            stock_val = int(stock_val_str)
        
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Quantity must be an integer.')
            return
        
        # Call update_quantity function
        try:
            s = update_quantity(stock_name, -stock_val, stock_red_date_time)
            print(s)
        except Exception:
            print('Exception')


    def call_add(self):
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_add.text().replace(' ','_').lower()
        stock_val = int(self.stock_count_add())
        print(type(stock_value))
        with conn:
            new_quantity = stock_val
            new_name = stock_name
            c.execute("UPDATE stock SET quantity = ? WHERE name = ?",
                  (new_quantity, new_name))
        conn.commit()
        
        
    def stack2UI(self):
        layout = QHBoxLayout()
        layout.setGeometry(QRect(0, 300, 1150, 500))
        tabs = QTabWidget()


        self.tab6 = QWidget() # Add a new tab for adding orders


        tabs.addTab(self.tab6, 'Add Orders') # Add the new tab for adding orders

        self.tab6UI() # Create the UI for the new tab for adding orders

        layout.addWidget(tabs)
        self.stack2.setLayout(layout)
        


    def tab6UI(self):
        layout = QFormLayout()
        self.add_order_button = QPushButton('Add Order', self)
        cancel_button = QPushButton('Cancel', self)
        self.stock_name_edit = QLineEdit()
        layout.addRow("Stock Name to Order", self.stock_name_edit)
        self.quantity_edit = QLineEdit()
        layout.addRow("Quantity to Order", self.quantity_edit)
        self.cost_edit = QLineEdit()
        layout.addRow("Cost of Stock (per item)", self.cost_edit)
        layout.addWidget(self.add_order_button)
        layout.addWidget(cancel_button)
        title_label2 = QLabel("Please note: Only one stock item may be ordered in a single instance")
        layout.addWidget(title_label2)
        

        self.add_order_button.clicked.connect(self.on_order_stock_clicked)
        cancel_button.clicked.connect(self.stock_name_edit.clear)
        cancel_button.clicked.connect(self.quantity_edit.clear)
        cancel_button.clicked.connect(self.cost_edit.clear)
        self.tab6.setLayout(layout)


    def on_order_stock_clicked(self):
        now = datetime.datetime.now()

        # Get input values and sanitize stock_name
        stock_name_inp = self.stock_name_edit.text().replace(' ', '_').lower().strip()
        stock_count_inp = self.quantity_edit.text().strip()
        stock_cost_inp = self.cost_edit.text().strip()

        # Check if any fields are empty
        if not all([stock_name_inp, stock_count_inp, stock_cost_inp]):
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        # Check if stock_count_inp is an integer
        try:
            stock_count = int(stock_count_inp)
        
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Stock quantity must be an integer.')
            return

        # Check if stock_cost_inp is an integer
        
        try:
            stock_cost = int(stock_cost_inp)
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Stock cost must be an integer.')
            return

        # Insert order into database
        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        d = insert_order(stock_name_inp, stock_count, stock_cost, stock_add_date_time)
        print(d)



    def stack3UI(self):

        #table = show_stock()
        #print(table)
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Show Stock")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Enter the search keyword:")
        self.conf_text = QLineEdit()

        self.View.setColumnCount(3)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Stock Name'))
        self.View.setItem(0, 1, QTableWidgetItem('Quantity'))
        self.View.setItem(0, 2, QTableWidgetItem('Cost Per Unit (GBP)'))
        

        layout.addWidget(self.View)
        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.stack3.setLayout(layout)

    def show_search(self):
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = show_stock()
        x = []
        if self.conf_text.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = show_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Viewing Stock Database.')
        else:
            self.lbl3.setText('No valid information in database.')

    def stack4UI(self):
        layout = QVBoxLayout()
        self.srt = QPushButton()
        self.srt.setText("View Transaction History")
        self.Trans = QTableWidget()
        self.lbl4 = QLabel()
        self.lbl_trans_text = QLabel()
        self.lbl_trans_text.setText("Enter the search keyword:")
        self.trans_text = QLineEdit()

        self.Trans.setColumnCount(7)
        self.Trans.setColumnWidth(0, 150)
        self.Trans.setColumnWidth(1, 150)
        self.Trans.setColumnWidth(2, 150)
        self.Trans.setColumnWidth(3, 100)
        self.Trans.setColumnWidth(4, 100)
        self.Trans.setColumnWidth(5, 100)
        self.Trans.setColumnWidth(6, 500)
        self.Trans.insertRow(0)
        self.Trans.setItem(0, 0, QTableWidgetItem('Transaction ID'))
        self.Trans.setItem(0, 1, QTableWidgetItem('Stock Name'))
        self.Trans.setItem(0, 2, QTableWidgetItem('Transaction Type'))
        self.Trans.setItem(0, 3, QTableWidgetItem('Date'))
        self.Trans.setItem(0, 4, QTableWidgetItem('Time'))
        self.Trans.setItem(0, 5, QTableWidgetItem('User Identification'))
        self.Trans.setItem(0, 6, QTableWidgetItem('Transaction Specific'))
        self.Trans.setRowHeight(0, 50)

        layout.addWidget(self.Trans)
        layout.addWidget(self.lbl_trans_text)
        layout.addWidget(self.trans_text)
        layout.addWidget(self.srt)
        layout.addWidget(self.lbl4)
        self.srt.clicked.connect(self.show_trans_history)
        self.stack4.setLayout(layout)
        
        
        
    def show_trans_history(self):
        if self.Trans.rowCount()>1:
            for i in range(1,self.Trans.rowCount()):
                self.Trans.removeRow(1)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'transaction.txt')
        if os.path.exists(path):
            tsearch = open(path, 'r')
            x_c = tsearch.readlines()
            tsearch.close()
            x = []
            if self.trans_text.text() != '':
                key = self.trans_text.text()
                for i in range(0,len(x_c)):
                    if x_c[i]:
                        a = x_c[i].split(" ")
                        name = a[0]
                        action = a[-2]
                        if (key.lower() in name.lower()) or (key.lower() in action.lower()):x.append(a)
            else:
                x = x_c.copy()

            for i in range(0,len(x)):
                x.sort(key=lambda a: a[4])
            #print(x)
            tid = 1900001
            uid = 1001
            for i in range(1,len(x)+1):
                self.Trans.insertRow(i)

                a = x[i-1].split(" ")
                if a[-2] == 'UPDATE':
                    p = 'Quantity of Stock Changed from '+a[1]+' to '+a[2]
                elif a[-2] == 'INSERT':
                    p = 'Stock added with Quantity : '+a[1]+' and Cost(Per Unit in GBP.) : '+a[2]
                elif a[-2] == 'REMOVE':
                    p = 'Stock information deleted.'
                elif a[-2] == 'ORDER':
                    p ='Stock Name: '+a[0]+' has been ordered. Stock ordered with Quantity : '+a[1]+' and Cost(Per Unit in GBP.) : '+a[2]
                else:
                    p = 'None'


                self.Trans.setItem(i, 0, QTableWidgetItem(str(tid)))
                self.Trans.setItem(i, 1, QTableWidgetItem(a[0].replace('_',' ')))
                self.Trans.setItem(i, 2, QTableWidgetItem(a[-2]))
                self.Trans.setItem(i, 3, QTableWidgetItem(a[3]))
                self.Trans.setItem(i, 4, QTableWidgetItem(a[4]))
                self.Trans.setItem(i, 5, QTableWidgetItem(str(uid)))
                self.Trans.setItem(i, 6, QTableWidgetItem(p))
                self.Trans.setRowHeight(i, 50)
                tid += 1
                uid = random.randint(1001, 1012)

            self.lbl4.setText('Viewing Transaction History.')
        else:
            self.lbl4.setText('No valid information found.')

#Admin menu:

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setWindowIcon(QIcon('database.png'))

    def initUI(self):
        self.setWindowTitle('DBMS v1.0.0')
        self.stacked_widget = MyStackedWidget()
        self.help_action = QAction(QIcon('help_icon.png'), 'Help', self)
        self.exit_action = QAction(QIcon('exit_icon.png'), 'Exit', self)
        self.id_action = QAction(QIcon('Security.png'), 'Permissions', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.help_action.setStatusTip('Program Information')
        self.id_action.setStatusTip('Security clearance level')
        self.exit_action.triggered.connect(self.close)
        self.help_action.triggered.connect(self.open_popup)
        self.id_action.triggered.connect(self.admin_popup)
        self.status_bar = self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.exit_action)
        toolbar.addAction(self.help_action)
        toolbar.addAction(self.id_action)
        
        self.dark_mode_checkbox = QCheckBox('Dark Mode', self)
        self.dark_mode_checkbox.setChecked(False)
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_theme)
        toolbar.addWidget(self.dark_mode_checkbox)

        self.setCentralWidget(self.stacked_widget)

    def open_popup(self):
        popup = QMessageBox()
        popup.setWindowTitle('Application Information')
        popup.setText('Welcome to the Database management system.\nPlease find additional information here: https://github.com/KashiCode/SimpleDBMS.\nKashiCode 2023©')
        popup.exec_()

        self.show()

    def admin_popup(self):
        popup = QMessageBox()
        popup.setWindowTitle('Security clearance level')
        popup.setText('Your level of Access is Admin.\nKashiCode 2023©')
        popup.exec_()

        self.show()

    def toggle_theme(self, state):
        if state == Qt.Checked:
            qApp.setStyle(QStyleFactory.create('Fusion'))
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            qApp.setPalette(palette)
        else:
            qApp.setStyle(QStyleFactory.create('Windows'))
            qApp.setPalette(qApp.style().standardPalette())

class MyStackedWidget(QWidget):
    def __init__(self):
        super(MyStackedWidget, self).__init__()

        self.userList = QListWidget()
        self.userList.setFixedWidth(250)
        self.userList.insertItem(0, 'Manage Users')
        self.userList.insertItem(1, 'View Users')

        self.userStack = QWidget()
        self.viewUser = QWidget() 

        self.setupUserStack()
        self.setupViewUser()

        self.mainStack = QStackedWidget(self)
        self.mainStack.addWidget(self.userStack)
        self.mainStack.addWidget(self.viewUser)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.userList)
        hbox.addWidget(self.mainStack)
   

        self.setLayout(hbox)
        self.userList.currentRowChanged.connect(self.display)
        self.setGeometry(500, 350, 200, 200)
        self.show()

    def display(self, index):
        self.mainStack.setCurrentIndex(index)

    def setupUserStack(self):
        layout = QHBoxLayout()
        layout.setGeometry(QRect(0,300,1150,500))
        tabs = QTabWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        tabs.addTab(self.tab4, 'Add User')
        tabs.addTab(self.tab5, 'Remove User')

        self.tab4UI()
        self.tab5UI()

        layout.addWidget(tabs)
        self.userStack.setLayout(layout)

    def tab4UI(self):
         layout = QFormLayout()

         self.ok = QPushButton('Add User', self)
         cancel = QPushButton('Cancel', self)

         self.username = QLineEdit()
         layout.addRow("Username", self.username)

         self.password = QLineEdit()
         layout.addRow("Password", self.password)

         self.role = QComboBox()
         self.role.addItems(['admin', 'employee'])
         layout.addRow("Role", self.role)

         layout.addWidget(self.ok)
         layout.addWidget(cancel)

         self.ok.clicked.connect(self.on_add_user)

         cancel.clicked.connect(self.username.clear)
         cancel.clicked.connect(self.password.clear)
         if self.role is not None:
             cancel.clicked.connect(lambda: self.role.setCurrentIndex(0))
         self.tab4.setLayout(layout)

    def setupViewUser(self):

        #table = show_users()
        #print(table)
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Show Users")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Enter the search keyword:")
        self.conf_text = QLineEdit()

        self.View.setColumnCount(3)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Username'))
        self.View.setItem(0, 1, QTableWidgetItem('Password'))
        self.View.setItem(0, 2, QTableWidgetItem('Role'))
        

        layout.addWidget(self.View)
        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.viewUser.setLayout(layout)

    def show_search(self):
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = show_users()
        x = []
        if self.conf_text.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = show_users()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Viewing User Database.')
        else:
            self.lbl3.setText('No valid information in database.')

    
    
    def on_add_user(self):
        username_inp = self.username.text()
        password_inp = self.password.text()
        role_inp = self.role.currentText()
        
        if len(username_inp) <= 12 and len(password_inp) <= 12:
            if username_inp.strip() and password_inp.strip():
                if any(char.isdigit() for char in password_inp):
                    Y = insert_user(username_inp, password_inp, role_inp)
                    print(Y)
                else:
                    msg_box16 = QMessageBox()
                    msg_box16.setIcon(QMessageBox.Warning)
                    msg_box16.setWindowTitle("Error")
                    msg_box16.setText("Password must contain at least one integer value.")
                    msg_box16.exec_()
                    print("Error: Password must contain at least one integer value.")
            else:
                msg_box17 = QMessageBox()
                msg_box17.setIcon(QMessageBox.Warning)
                msg_box17.setWindowTitle("Error")
                msg_box17.setText("Username and password cannot be empty.")
                msg_box17.exec_()
                print("Error: Username and password cannot be empty.")
        else:
            msg_box18 = QMessageBox()
            msg_box18.setIcon(QMessageBox.Warning)
            msg_box18.setWindowTitle("Error")
            msg_box18.setText(" Username and password must be less than or equal to 12 characters.")
            msg_box18.exec_()
            print("Error: Username and password must be less than or equal to 12 characters.")



    def tab5UI(self):
        layout = QFormLayout()
        self.ok_del = QPushButton('Delete User', self)
        cancel = QPushButton('Cancel', self)
        
        self.username_del = QLineEdit()
        layout.addRow("Username", self.username_del)
        layout.addWidget(self.ok_del)
        layout.addWidget(cancel)
        self.tab5.setLayout(layout)

        self.ok_del.clicked.connect(self.call_del1)  
        cancel.clicked.connect(self.username_del.clear)


    def call_del1(self):
        username = self.username_del.text()
        if username.strip():
            L = remove_user(username)
            print(L)
        else:
            msg_box19 = QMessageBox()
            msg_box19.setIcon(QMessageBox.Warning)
            msg_box19.setWindowTitle("Error")
            msg_box19.setText(" Username cannot be empty.")
            msg_box19.exec_()
            print("Error: Username cannot be empty.")

# Stock manipulation functions.

def insert_user(username, password, role):
    with conn1:
        c1.execute("SELECT * FROM users WHERE username = :username", {'username': username})
        check = c1.fetchone()

    if check is None:
        with conn1:
            c1.execute("INSERT INTO users VALUES (:username, :password, :role)", {'username': username, 'password': password, 'role': role})
        msg_box = QMessageBox()
        # Set the window title and message text
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText("User creation confirmed")
        msg_box.exec_()
        return 'User added to the database'
    else:
        msg_box1 = QMessageBox()
        msg_box1.setIcon(QMessageBox.Warning)
        msg_box1.setWindowTitle("Error")
        msg_box1.setText("User already exists.")
        msg_box1.exec_()
        return 'User with same username already exists'
    

def remove_user(username):
    with conn1:
        c1.execute("SELECT COUNT(*) FROM users WHERE username = :username",
                    {'username': username})
        result = c1.fetchone()[0]
        if result == 0:
            msg_box2 = QMessageBox()
            msg_box2.setWindowTitle("ERROR")
            msg_box2.setText("User does not exist or already removed.")
            msg_box2.exec_()
            print(f"Error: User '{username}' does not exist")
        else:
            c1.execute("DELETE from users WHERE username = :username",
                        {'username': username})
            msg_box3 = QMessageBox()
            msg_box3.setWindowTitle("Confirmation")
            msg_box3.setText("User removal confirmed")
            msg_box3.exec_()
            print(f"User '{username}' removed successfully")

def insert_order(stock_name, quantity, cost, date):
    with open("transaction.txt", "r") as myfile:
        orders = myfile.readlines()
    for order in orders:
        if order.startswith(stock_name.upper()):
            msg_box14 = QMessageBox()
            msg_box14.setIcon(QMessageBox.Warning)
            msg_box14.setWindowTitle("ERROR")
            msg_box14.setText("Order with the same item already exists.")
            msg_box14.exec_()
            print("Order already exists.")
            return
    a = stock_name.upper() + ' ' + str(quantity) + ' ' + str(cost) + ' ' + str(date) + ' ' + 'ORDER ' + "\n"
    with open("transaction.txt", "a") as myfile:
        myfile.write(a)
        msg_box9 = QMessageBox()
        msg_box9.setIcon(QMessageBox.Warning)
        msg_box9.setWindowTitle("Confirmation")
        msg_box9.setText("Order created sucessfully.")
        msg_box9.exec_()
        print("Order added successfully.")

def insert_prod(name,q,cost,date):
    with conn:
        c.execute("SELECT quantity FROM stock WHERE name = :name",{'name':name})
        check = c.fetchone()
        #print(check)
    if check is None:
        with conn:
            #print('yes')
            c.execute("INSERT INTO stock VALUES (:name, :quantity, :cost)", {'name': name, 'quantity': q, 'cost': cost})
            a = name.upper() +' ' +str(q)+' '+str(cost)+' '+str(date) + ' ' + 'INSERT '+"\n"
            with open("transaction.txt", "a") as myfile:
                myfile.write(a)
            msg_box6 = QMessageBox()
            msg_box6.setIcon(QMessageBox.Warning)
            msg_box6.setWindowTitle("Confirmation")
            msg_box6.setText("Stock added to the database sucessfully.")
            msg_box6.exec_()
        return 'Inserted the stock in DataBase'
    else:
        msg_box8 = QMessageBox()
        msg_box8.setIcon(QMessageBox.Warning)
        msg_box8.setWindowTitle("Error")
        msg_box8.setText("Stock with the same name already present")
        msg_box8.exec_()
        return 'Stock with same name already present.'
    
#function that retrieves all of the stock.
def show_stock():
    with conn:
        c.execute("SELECT * FROM stock")
        
        
    return c.fetchall()

def show_users():
    with conn1:
        c1.execute("SELECT * FROM users")
        
    return c1.fetchall()

def update_cost(name, cost,date):
    with conn:
        c.execute("""UPDATE stock SET cost = :cost
                    WHERE name = :name""",
                  {'name': name, 'cost': cost})
        
def update_quantity(name, val,date):
    with conn:
        c.execute("SELECT quantity FROM stock WHERE name = :name",{'name': name})
        z = c.fetchone()
        print (z)
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE stock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})
        a = name.upper() + ' ' + str(z[0]) + ' ' + str(cost) + ' ' + str(date) +' UPDATE '+"\n"
        with open("transaction.txt", "a") as myfile:
            myfile.write(a)
            msg_box12 = QMessageBox()
            msg_box12.setIcon(QMessageBox.Warning)
            msg_box12.setWindowTitle("Confirmation")
            msg_box12.setText("Stock quantity reduced sucessfuly.")
            msg_box12.exec_()
        print("stock value reduced")
        
def remove_stock(name, date):
    with conn:
        # Check if item is in the database
        c.execute("SELECT * from stock WHERE name = :name", {'name': name})
        item = c.fetchone()
        if item is None:
            msg_box10 = QMessageBox()
            msg_box10.setIcon(QMessageBox.Warning)
            msg_box10.setWindowTitle("ERROR")
            msg_box10.setText("Stock item is not in the database.")
            msg_box10.exec_()
            print(f"{name} is not in the database.")
            return

        # If item exists, remove it
        c.execute("DELETE from stock WHERE name = :name", {'name': name})

        a = name.upper() + ' ' + 'None' + ' ' + 'None'+' ' + str(date) + ' REMOVE '+"\n"

        with open("transaction.txt", "a") as myfile:
            myfile.write(a)
            msg_box11 = QMessageBox()
            msg_box11.setIcon(QMessageBox.Warning)
            msg_box11.setWindowTitle("Confirmation")
            msg_box11.setText("Removed stock item sucessfully.")
            msg_box11.exec_()
            print(f"{name} removed successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
