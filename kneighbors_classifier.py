from sklearn.datasets import *
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import cv2

# Afficher l'image
def afficheImageTest(imgDessin):
    plt.imshow(imgDessin, cmap="gray")
    plt.show()

# Afficher les images du dataset fourni
def afficheImageDataSet(i):
    plt.imshow(digit['images'][i], cmap='Greys_r')
    plt.show()


# Chargement des données
digit = load_digits()
dig = pd.DataFrame(digit['data'][0:1700])
#print(digit['target'][1733])

train_x = digit.data # les input variables
train_y = digit.target # les étiquettes (output variable)

print(train_x.shape)

# Découpage du jeu de données
x_train,x_test,y_train,y_test=train_test_split(train_x,train_y,test_size=0.25) #0.25 pour indiquer 25% de jeu de test


# On crée un classifier de k voisins
KNN = KNeighborsClassifier(1) # 1 classifier
# On entraîne notre jeu de données
KNN.fit(x_train, y_train)
# Evaluation du résultat
print(KNN.score(x_test,y_test))


# Tests de prédiction sur image issue du dessin (gui.py)

imgDessin = cv2.imread("dessin.png", cv2.IMREAD_GRAYSCALE)
afficheImageTest(imgDessin)
# On inverse les bits de couleurs (blanc et noir) pour les faire correspondre au dataset
inversion_image = cv2.bitwise_not(imgDessin)
afficheImageTest(inversion_image)
# Reshape de l'image pour l'aplatir sous forme de vecteur
inversion_image = inversion_image.reshape(1,-1)


# Prédiction du résultat
print("Résultat prédit", KNN.predict(inversion_image))

afficheImageDataSet(9)


