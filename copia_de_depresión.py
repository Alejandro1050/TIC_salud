# -*- coding: utf-8 -*-
"""Copia de Depresión.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rqgCZb76H1DfwXmT7PAM8Olh7kHwsxOu

# Análisis de la depresión en estudiantes.

https://www.kaggle.com/datasets/hopesb/student-depression-dataset
"""

# Importación de librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importación del dataset desde kagle
df = pd.read_csv('/content/data.csv')
df.head()

"""# Exploración de los datos"""

df.info()

df.describe()

df.duplicated().sum()

df.isnull().sum()

df.Gender.value_counts()

data = df.copy()
data = data.drop('id', axis=1)
data.plot.box(rot=90)

"""#Limpieza de Datos

Dado que la columna Financial Stress, cuenta con 3 valores nulos, por lo cual optamos por imputar los datos, sacando la media y llenar los datos dulos con la media.
"""

median_financia = data['Financial Stress'].median()
median_financia

data['Financial Stress'].fillna(median_financia, inplace=True)

"""Verificamos que el proceso se haya realizado de manera correcta, en este caso ya no contamos con datos nulos."""

data.isnull().sum()

"""Verificamos que la columna Gnender solo cuente con 2 valores unicos, en este caso podemos ver que efectivamente solo contamos con 2 valores unicos, lo cual es correcto."""

data['Gender'].unique()

"""Verificamos el tipo de datos de la columna Age,esta debe de ser de tipo entero,ya que no hay edades con valores flotantes.

Como podemos observa tenemos que cambiar del tipo de dato float a entero
"""

data['Age'].info()

"""Verificamos que el tipo de dato se haya realizado de manera correcta, este debe de ser entero."""

data['Age'] = data['Age'].astype(int)
data['Age'].info()

"""Verificamos que no contamos con datos duplicados."""

data.duplicated().sum()

"""# Procesamiento de Datos

Realizamos la codificación de variables categóricas a través del método one-hot encoding
"""

data = pd.get_dummies(data, columns=['Gender', 'City', 'Profession'], drop_first=True)

"""Convertimos  la variable 'Sleep Duration', que originalmente contiene rangos de tiempo en formato de texto a valores numéricos."""

data['Sleep Duration'] = data['Sleep Duration'].str.extract('(\d+)-(\d+)').astype(float).mean(axis=1)

print(data['Depression'].unique())

data['Depression'] = data['Depression'].astype(bool)

"""Aplicamos la normalización a las columnas numéricas del conjunto de datos, utilizando el MinMaxScaler de scikit-learn"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
numeric_columns = ['Age', 'Financial Stress', 'CGPA', 'Sleep Duration', 'Work Pressure', 'Academic Pressure', 'Study Satisfaction', 'Job Satisfaction']
data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

"""División del dataset en conjunto de entrenamiento y prueba"""

from sklearn.model_selection import train_test_split

X = data.drop('Depression', axis=1)
y = data['Depression']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)