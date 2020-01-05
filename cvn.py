import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Activation,Flatten,Conv2D,MaxPooling2D
import pickle

from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt

assert hasattr(tf, "function")

# Chargement des données mnist
mnist = tf.keras.datasets.mnist
(train_images,train_targets), (test_images, test_targets) = mnist.load_data()


#arr = np.arange(taille)
#np.random.shuffle(arr)
#train_images = train_images[arr]
#test_images = test_images[arr]


#train_images = train_images[:10000]

# NORMALISATION DES DONNEES

print(" Moyenne, ecart type", train_images.mean(), train_images.std())

scaler = StandardScaler()
train_images_scaled = scaler.fit_transform( train_images.reshape(-1,28*28))
test_images_scaled = scaler.transform(test_images.reshape(-1,28*28))

train_images_scaled = train_images_scaled.reshape(-1,28,28,1)
test_images_scaled = test_images_scaled.reshape(-1,28,28,1)

print(" Moyenne, ecart type", train_images_scaled.mean(), train_images_scaled.std())

print(train_images_scaled.shape)
print(test_images_scaled.shape)

#for item in train_images_scaled:
 #   print(item.shape)

train_dataset = tf.data.Dataset.from_tensor_slices((train_images_scaled, train_targets))
valid_dataset = tf.data.Dataset.from_tensor_slices((test_images_scaled, test_targets))


#epoch = 1
#batch_size = 192

#for images_batch, targets_batch in train_dataset.repeat(epoch).batch(batch_size):
 #   print(images_batch[0].shape, targets_batch[0])




plt.imshow(train_images[0].reshape(28,28), cmap="binary")
plt.show()



class ModeleConvolutionnel(tf.keras.Model):
    def __init__(self):
        super(ModeleConvolutionnel,self).__init__()

        self.conv1 = tf.keras.layers.Conv2D(32,4, activation='relu', name="conv1")
        self.conv2 = tf.keras.layers.Conv2D(64,3, activation='relu', name="conv2")
        self.conv3 = tf.keras.layers.Conv2D(128, 3, activation='relu', name="conv3")

        self.flatten = tf.keras.layers.Flatten(name="flatten")

        self.dl = tf.keras.layers.Dense(128,activation='relu', name="dl")
        self.out = tf.keras.layers.Dense(10,activation='softmax', name="output")

    def call(self, image):
        conv1 = self.conv1(image)
        #print(conv1)
        conv2 = self.conv2(conv1)
        #print(conv2)
        conv3 = self.conv3(conv2)
        #print(conv3)
        flatten = self.flatten(conv3)
        #print(flatten)
        dl = self.dl(flatten)
        #print(dl)
        output = self.out(dl)
        print(output)
        return output


print(train_images_scaled.shape)
model = ModeleConvolutionnel()
model.predict(train_images_scaled[0:1])

loss_object = tf.keras.losses.SparseCategoricalCrossentropy()
optimizer = tf.keras.optimizers.Adam()

# Perte
train_loss = tf.keras.metrics.Mean(name='train_loss')
valid_loss = tf.keras.metrics.Mean(name='valid_loss')

# Précision
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')
valid_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='valid_accuracy')

def train_step(image, targets):
    with tf.GradientTape() as tape:
        predictions = model(image)
        loss = loss_object(targets, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients,model.trainable_variables))

    train_loss(loss)
    train_accuracy(targets,predictions)


def valid_step(image, targets):
    predictions = model(image)
    t_loss = loss_object(targets,predictions)
    valid_loss(t_loss)
    valid_accuracy(targets,predictions)




epoch = 10
batch_size = 192
b = 0
for epoch in range(epoch):
    # Training set
    for images_batch, targets_batch in train_dataset.batch(batch_size):
        train_step(images_batch, targets_batch)
        template = '\r Batch {}/{}, Loss: {}, Accuracy: {}'
        print(template.format(
            b, len(train_targets), train_loss.result(),
            train_accuracy.result()*100
        ), end="")
        b += batch_size
    # Validation set
    for images_batch, targets_batch in valid_dataset.batch(batch_size):
        valid_step(images_batch, targets_batch)

    template = '\nEpoch {}, Valid Loss: {}, Valid Accuracy: {}'
    print(template.format(
        epoch+1,
        valid_loss.result(),
        valid_accuracy.result()*100)
    )
    valid_loss.reset_states()
    valid_accuracy.reset_states()
    train_accuracy.reset_states()
    train_loss.reset_states()


