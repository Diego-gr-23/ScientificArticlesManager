from PyQt6 import QtCore, QtGui, QtWidgets
from hashFNV1 import TablaHash
import json
import os

DB_FILE = "articulos_db.txt"

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(1256, 820)

        # Fondo
        self.Fondo = QtWidgets.QLabel(parent=Window)
        self.Fondo.setGeometry(QtCore.QRect(0, 0, 1256, 820))
        self.Fondo.setText("")
        self.Fondo.setPixmap(QtGui.QPixmap("MainWindow.png"))
        self.Fondo.setScaledContents(False)

        # Inputs
        self.lineEditTitle = QtWidgets.QLineEdit(parent=Window)
        self.lineEditTitle.setGeometry(QtCore.QRect(330, 110, 471, 31))
        self.lineEditTitle.setPlaceholderText("Título")
        self.lineEditTitle.setStyleSheet("background-color: skyblue")

        self.lineEditAuthor = QtWidgets.QLineEdit(parent=Window)
        self.lineEditAuthor.setGeometry(QtCore.QRect(330, 160, 471, 31))
        self.lineEditAuthor.setPlaceholderText("Autor")
        self.lineEditAuthor.setStyleSheet("background-color: skyblue")

        self.lineEditYear = QtWidgets.QLineEdit(parent=Window)
        self.lineEditYear.setGeometry(QtCore.QRect(330, 210, 471, 31))
        self.lineEditYear.setPlaceholderText("Año")
        self.lineEditYear.setStyleSheet("background-color: skyblue")

        self.lineEditContent = QtWidgets.QLineEdit(parent=Window)
        self.lineEditContent.setGeometry(QtCore.QRect(360, 250, 471, 31))
        self.lineEditContent.setPlaceholderText("Contenido del artículo")
        self.lineEditContent.setStyleSheet("background-color: skyblue")

        self.lineEditSearch = QtWidgets.QLineEdit(parent=Window)
        self.lineEditSearch.setGeometry(QtCore.QRect(360, 340, 471, 31))
        self.lineEditSearch.setPlaceholderText("Buscar por título")
        self.lineEditSearch.setStyleSheet("background-color: skyblue")

        # Botones
        self.pushButtonAdd = QtWidgets.QPushButton(parent=Window)
        self.pushButtonAdd.setGeometry(QtCore.QRect(880, 170, 121, 61))
        self.pushButtonAdd.setStyleSheet("background-color: transparent; border: none;")

        self.pushButtonSearch = QtWidgets.QPushButton(parent=Window)
        self.pushButtonSearch.setGeometry(QtCore.QRect(850, 340, 101, 31))
        self.pushButtonSearch.setStyleSheet("background-color: transparent; border: none;")

        self.pushButtonDelet = QtWidgets.QPushButton(parent=Window)
        self.pushButtonDelet.setGeometry(QtCore.QRect(970, 320, 51, 61))
        self.pushButtonDelet.setStyleSheet("background-color: transparent; border: none;")

        # Tabla
        self.tableWidget = QtWidgets.QTableWidget(parent=Window)
        self.tableWidget.setGeometry(QtCore.QRect(200, 470, 871, 241))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Título", "Autor", "Año", "Nombre Archivo", "Contenido"])
        self.tableWidget.setStyleSheet("background-color: skyblue")

        # Ajustar ancho de columnas
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i, 210)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Gestor De Articulos Científicos"))


class MainApp(QtWidgets.QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tabla = TablaHash()
        self.load_database()

        # Conectar botones
        self.pushButtonAdd.clicked.connect(self.agregar_articulo)
        self.pushButtonSearch.clicked.connect(self.buscar_articulo)
        self.pushButtonDelet.clicked.connect(self.eliminar_articulo)

    def agregar_articulo(self):
        titulo = self.lineEditTitle.text().strip()
        autor = self.lineEditAuthor.text().strip()
        anio = self.lineEditYear.text().strip()
        contenido = self.lineEditContent.text().strip()

        if titulo and autor and anio and contenido:
            hash_id = hash(contenido)
            filename = f"{hash_id}.txt"

            # Guardar el artículo en archivo independiente
            with open(filename, "w", encoding="utf-8") as f:
                f.write(contenido)

            # Insertar en la tabla hash
            self.tabla.insert(hash_id, titulo, autor, anio, filename)

            # Actualizar base de datos
            self.save_database()

            # Refrescar tabla visual
            self.refrescar_tabla()

            # Limpiar inputs
            self.lineEditTitle.clear()
            self.lineEditAuthor.clear()
            self.lineEditYear.clear()
            self.lineEditContent.clear()

    def eliminar_articulo(self):
        selected = self.tableWidget.currentRow()
        if selected >= 0:
            filename = self.tableWidget.item(selected, 3).text()
            hash_id = int(filename.replace(".txt", ""))

            # Eliminar del backend
            self.tabla.eliminar(hash_id)

            # Eliminar archivo físico
            if os.path.exists(filename):
                os.remove(filename)

            # Guardar cambios en DB
            self.save_database()

            # Refrescar tabla visual
            self.refrescar_tabla()

    def buscar_articulo(self):
        query = self.lineEditSearch.text().strip().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)  # Buscar por título
            if item:
                self.tableWidget.setRowHidden(row, query not in item.text().lower())

    def refrescar_tabla(self):
        self.tableWidget.setRowCount(0)
        for i in range(self.tabla.size):
            current = self.tabla.tabla[i]
            while current:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(current.title))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(current.authors))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(current.year)))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(current.filename))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem("Ver contenido"))
                current = current.next

    def save_database(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            for i in range(self.tabla.size):
                current = self.tabla.tabla[i]
                while current:
                    line = f"{current.hash_id}|{current.title}|{current.authors}|{current.year}|{current.filename}\n"
                    f.write(line)
                    current = current.next

    def load_database(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        hash_id, titulo, autor, anio, filename = parts
                        self.tabla.insert(int(hash_id), titulo, autor, anio, filename)
        self.refrescar_tabla()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = MainApp()
    ventana.show()
    sys.exit(app.exec())
