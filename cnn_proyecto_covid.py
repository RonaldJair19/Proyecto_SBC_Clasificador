import sys
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Flatten, Dense, Activation, Convolution2D, MaxPooling2D
from tensorflow.keras import backend as K 
from tensorflow.keras.optimizers import Adam

K.clear_session()

#Especificando las rutas del data set para los archivos de entrenamiento y de validadion de la red neuronal
path_entrenamiento = 'E:/Documentos/UTP/Cuarto_Anio/Sistemas_basados_en_el_conocimiento/Proyecto/DataSet/img_entrenamiento'
path_validacion = 'E:/Documentos/UTP/Cuarto_Anio/Sistemas_basados_en_el_conocimiento/Proyecto/DataSet/img_validacion'

#Declarando los parametros de la red neuronal
epocas = 20
altura, longitud = 250, 250
batch_size = 20
pasos = 1000
pasos_de_validacion = 200
FConv1 = 32
FConv2 = 64
tam_fil1 = (3,3)
tam_fil2 = (2,2)
tam_pool = (2,2)
clases = 2
lr = 0.0005

#Funciones para el preprocesamiento de imagenes
data_gen_entrenamiento = ImageDataGenerator(
	rescale = 1./255,
	shear_range = 0.3,
	zoom_range = 0.3,
	horizontal_flip = True
)

data_gen_validacion = ImageDataGenerator(
	rescale = 1./225
	)


imagen_entrenamiento = data_gen_entrenamiento.flow_from_directory(
	path_entrenamiento,
	target_size = (altura, longitud),
	batch_size = batch_size,
	class_mode = 'categorical'
	)

imagen_validacion = data_gen_validacion.flow_from_directory(
	path_validacion,
	target_size = (altura, longitud),
	batch_size = batch_size,
	class_mode = 'categorical'
	)

#Se crea la red convolucional
cnn = Sequential()
#Primera capa
cnn.add(Convolution2D(FConv1, tam_fil1, padding = 'same', input_shape = (altura, longitud,3), activation = 'relu'))
#Segunda Capa
cnn.add(MaxPooling2D(pool_size = tam_pool))
#Tercera capa
cnn.add(Convolution2D(FConv2, tam_fil2, padding = 'same', activation = 'relu'))
#Cuarta capa
cnn.add(MaxPooling2D(pool_size = tam_pool))
#Quinta Capa, aplana la imagen
cnn.add(Flatten())
#Sexta capa densa
cnn.add(Dense(256, activation = 'relu'))
#Septima capa, capa de apagado
cnn.add(Dropout(0.5))
#Octava capa densa
cnn.add(Dense(clases, activation = 'softmax'))
#Copilacin
cnn.compile(loss = 'categorical_crossentropy', optimizer = optimizers.Adam(lr = lr, beta_1 = 0.5 ), metrics = ['accuracy'])

cnn.fit(imagen_entrenamiento, steps_per_epoch = pasos, epochs = epocas, validation_data = imagen_validacion, validation_steps = pasos_de_validacion)


#Guardando el modelo
dir = 'E:/Documentos/UTP/Cuarto_Anio/Sistemas_basados_en_el_conocimiento/Proyecto/Modelo'

if not os.path.exists(dir):
	os.mkdir(dir)

cnn.save('E:/Documentos/UTP/Cuarto_Anio/Sistemas_basados_en_el_conocimiento/Proyecto/Modelo/modelo_prueba.h5')
cnn.save_weights('E:/Documentos/UTP/Cuarto_Anio/Sistemas_basados_en_el_conocimiento/Proyecto/Modelo/pesos_modelo.h5')

