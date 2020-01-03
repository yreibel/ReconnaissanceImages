#Imports nécessaires

from PyQt5.QtGui import QPainter, QPen, QPixmap, QBrush, QImage
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, \
    QDesktopWidget
import sys

# Zone de dessin
class ZoneCanva(QWidget):
    def __init__(self):
        super().__init__()

        # On crée une image de la zone de gui
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.isDrawing = False # si est en train de dessiner
        self.taillePinceau = 10
        self.couleurPinceau = Qt.black

        self.pointPrecedent = QPoint()
        self.pointSuivant = QPoint()

    def paintEvent(self, event):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    # Action effectuée lorsque la souris est pressée
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isDrawing = True
            self.pointPrecedent = (event.pos())
            self.pointPrecedent.setX(self.pointPrecedent.x() * 2)

    # Action effectuée durant le mouvement de la souris
    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.isDrawing:
            surface = QPainter(self.image)
            surface.setPen(QPen(self.couleurPinceau, self.taillePinceau, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            #surface.translate(self.pointPrecedent.x(),0)
            self.pointSuivant = event.pos()
            self.pointSuivant.setX(self.pointSuivant.x() * 2)
            surface.drawLine(self.pointPrecedent, self.pointSuivant)
            #surface.drawLine(self.pointPrecedent, (event.pos()))
            self.pointPrecedent = (event.pos())
            self.pointPrecedent.setX(self.pointPrecedent.x() * 2)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.isDrawing = False


class GUIApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Reconnaissance d\'images'
        self.left = 100
        self.top = 50
        self.width = 1000
        self.height = 500

        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(700,500)
        self.centrer()


        # Création d'un bouton pour lancer la détection du résultat
        self.btnDetection = QPushButton('Détection ...', self)
        self.btnDetection.setToolTip('Détecter la représentation de l\'image')

        # Label pour l'affiche du résultat
        self.labelResultat = QLabel()
        self.labelResultat.setText("En attente de détection ...")

        # Layout vertical pour ordonner les widgets appliqués
        layoutVResultat = QVBoxLayout()
        layoutVResultat.addWidget(self.btnDetection)
        layoutVResultat.addWidget(self.labelResultat)

        # Layout horizontal intégrant le canva et la partie détection-résultat
        layoutHorizontal = QHBoxLayout()
        layoutHorizontal.addWidget(ZoneCanva())
        layoutHorizontal.addLayout(layoutVResultat)

        # Création d'un widget pour appliquer le layout qui englobe tout
        ecran = QWidget()
        ecran.setLayout(layoutHorizontal)
        self.setCentralWidget(ecran)

        self.show()

    # Méthode pour centrer la fenêtre principale
    def centrer(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUIApp()
    sys.exit(app.exec_())
