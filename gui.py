#Imports nécessaires

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QPixmap, QBrush, QImage
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class GUIApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Reconnaissance d\'images'
        self.left = 100
        self.top = 50
        self.width = 640
        self.height = 480

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # On crée une image de la zone de gui
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.isDrawing = False
        self.taillePinceau = 10
        self.couleurPinceau = Qt.black

        self.pointPrecedent = QPoint()

        # Affichage de la fenêtre graphique
        self.show()

    def paintEvent(self, event):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    # Action effectuée lorsque la souris est pressée
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isDrawing = True
            self.pointPrecedent = event.pos()

    # Action effectuée durant le mouvement de la souris
    # On enregistre
    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.isDrawing:

            painter = QPainter(self.image)
            painter.setPen(QPen(self.couleurPinceau, self.taillePinceau, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.pointPrecedent, event.pos())
            self.pointPrecedent = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.isDrawing = False



# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUIApp()
    sys.exit(app.exec_())
