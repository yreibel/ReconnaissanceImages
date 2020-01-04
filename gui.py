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

        # On crée une image de la zone de gui en format RGB32
        self.image = QImage(self.size(), QImage.Format_RGB32)

        # On remplit l'image de blanc
        self.image.fill(Qt.white)

        self.isDrawing = False # si est en train de dessiner

        # Caractéristiques du pinceau
        self.taillePinceau = 10
        self.couleurPinceau = Qt.red

        # Création de points pour le dessin
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
            self.pointPrecedent.setX(self.pointPrecedent.x() *1.3)

    # Actions effectuées durant le mouvement de la souris
    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.isDrawing:
            surface = QPainter(self.image)
            surface.setPen(QPen(self.couleurPinceau, self.taillePinceau, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            #surface.translate(self.pointPrecedent.x(),0)
            self.pointSuivant = event.pos()
            self.pointSuivant.setX(self.pointSuivant.x() * 1.3)

            surface.drawLine(self.pointPrecedent, self.pointSuivant)

            self.pointPrecedent = (event.pos())
            self.pointPrecedent.setX(self.pointPrecedent.x() * 1.3)
            self.update()

    # Action effectuée lorsque le clic est laché
    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.isDrawing = False

# Application principale
class GUIApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Reconnaissance d\'images'
       # self.width = 1000
       # self.height = 500

        self.setWindowTitle(self.title)
        self.resize(1000,500)
        self.centrer()

        # On crée un objet Zone Canva contenant notre zone de dessin
        self.zoneCanva = ZoneCanva()

        # Création d'un bouton pour lancer la détection du résultat
        self.btnDetection = QPushButton('Détection ...', self)
        self.btnDetection.setToolTip('Détecter la représentation de l\'image')

        # On lie le bouton de détection à un handler d'évènement
        self.btnDetection.clicked.connect(self.actionBtnDetection)

        # Création d'un bouton pour nettoyer la zone de dessin
        self.btnClear = QPushButton('Clear Canva', self)
        self.btnClear.setToolTip('Nettoyer la zone de dessin')

        # On lie le bouton de nettoyage à sa fonction évènement
        self.btnClear.clicked.connect(self.actionBtnClear)


        # Label pour l'affiche du résultat
        self.labelResultat = QLabel()
        self.labelResultat.setText("En attente de détection ...")

        # Layout vertical pour ordonner les widgets appliqués
        layoutVResultat = QVBoxLayout()
        layoutVResultat.addWidget(self.btnDetection)
        layoutVResultat.addWidget(self.labelResultat)
        layoutVResultat.addWidget(self.btnClear)

        # Layout horizontal intégrant le canva et la partie détection-résultat
        layoutHorizontal = QHBoxLayout()
        layoutHorizontal.addWidget(self.zoneCanva)
        layoutHorizontal.addLayout(layoutVResultat)

        # Création d'un widget pour appliquer le layout qui englobe tout
        ecran = QWidget()
        ecran.setLayout(layoutHorizontal)
        self.setCentralWidget(ecran)
        # On affiche la fenêtre principale
        self.show()

    # Méthode pour centrer la fenêtre principale
    def centrer(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    # Déclenchement lorsque le bouton de détection est appuyé
    def actionBtnDetection(self):
        # On crée une modification de l'image
        self.imageModifiee = self.zoneCanva.image
        # On sauvegarde la modification de l'image en niveau de gris
        self.imageModifiee = self.imageModifiee.convertToFormat(QImage.Format_Grayscale8)
        # On applique une remise à l'échelle
        self.imageModifiee = self.imageModifiee.scaled(28,28)
        # On sauvegarde l'image
        self.imageModifiee.save("dessin.png")

    # Nettoyage de la zone de dessin
    def actionBtnClear(self):
        # On remplit la zone de canva de blanc
        self.zoneCanva.image.fill(Qt.white)
        # Mise à jour de la zone de dessin
        self.zoneCanva.update()


# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUIApp()
    sys.exit(app.exec_())
