# ProjetBigDataEquipe6
·DU Pingjie
·YANG Di
·EZZAGH Hicham
#Importation des bibliotheques

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#Import dataset
df = pd.read_csv('dataset.csv')

#Exploration des donnees


df.head()    ## cette ligne c'est pour voir la structure des donnees
df.info()    ## cette ligne c'est pour savoir les colonnes et lignes et types des donnees

# verifier la distribution de Target 
sns.countplot("TARGET",data=df)

	################## MISSING DATA ########################



# on a creer une loupe et une liste vide pour la remplir avec les indices des colonnes qui ne sont pas remplis
mv = []
for i in range (len(df.columns)):
    if df[df.columns[i]].isna().sum() != 0:
        mv.append(i)
print(mv)


# on a creer une loupe et une liste vide pour la remplir avec les noms des colonnes qui ne sont pas remplis
cmv = []
for i in range (len(mv)):
    cmv.append(df.columns[mv[i]])


# on a creer une loupe et une liste vide pour la remplir avec les indices des colonnes de type integer qui ne sont pas remplis
imv = []
for i in range (len(cmv)):
    if df[cmv[i]].dtype == 'int64':
        imv.append(i)
print(imv)

# on a creer une loupe et une liste vide pour la remplir avec les indices des colonnes de type float qui ne sont pas remplis
fmv = []
for i in range (len(cmv)):
    if df[cmv[i]].dtype == 'float64':
        fmv.append(cmv[i])
print(fmv)

# on a creer une loupe et une liste vide pour la remplir avec les indices des colonnes de type object qui ne sont pas remplis
omv = []
for i in range (len(mv)):
    if df[cmv[i]].dtype == 'object':
        omv.append(cmv[i])
print(omv)

# remplir les cases vides des colonnes de type float par la moyenne 
for i in range (len(fmv)):
    df[fmv[i]].fillna(value=df[fmv[i]].mean(),inplace=True)

# remplir les cases vides des colonnes de type float par la valeur la plus commune
for i in range (len(omv)):
    df[omv[i]].fillna(value=df[omv[i]].value_counts().idxmax(),inplace=True)

# une liste qui contient les noms des colonnes de type object
oc = []
for i in range (len(df.columns)):
    if df[df.columns[i]].dtype == 'object':
        oc.append(df.columns[i])
print(oc)

                               ############################### Feature Scaling ##############################

# une liste des colonnes de type float ou integer
ifc = []
for i in range (len(df.columns)):
    if df[df.columns[i]].dtype != 'object':
        ifc.append(df.columns[i])
print(len(ifc))

js = df[ifc]

# utiliser la finction MinMaxSxaler pour faire scaling de tous les colonnes de type numerique
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
sab = scaler.fit_transform(js)

# construire une dataframe dans laquelle il ya tous les colonnes numerique en mode scaling et joinnant ces colonnes avec la colonnes target

kil = pd.DataFrame(sab,columns=ifc).drop('TARGET',axis=1)
kil_100 = kil.join(df['TARGET'])

# myta contient une dataframe avec tous les colonnes de type object
myta = df[oc]

# kil_myta c'est une dataframe qui fait une jointure des colonnes texte avec les colonnes de type numerique qu'on a deja scaling
kil_myta = kil_100.join(myta)

                             ################################## Categorical DATA ################################

# coder le donnees de type texte 
dataset = pd.get_dummies(kil_myta,columns=oc,drop_first=True)


#splitting dataset 
from sklearn.model_selection import train_test_split

X = dataset.drop('TARGET',axis=1)
y = dataset['TARGET']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=101)


#training model with UNBALANCED DATA
# utilisation de modele Decision Tree 

from sklearn.tree import DecisionTreeClassifier
dtree = DecisionTreeClassifier()
dtree.fit(X_train,y_train)

#Predictions and Evaluation of Decision Tree

predictions = dtree.predict(X_test)
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test,predictions))


                               ############################ReSampling - Under Sampling###########################
# compter tous les occurences pour target = 1

number_of_1 = len(dataset[dataset.TARGET == 1])
One_indices = np.array(dataset[dataset.TARGET == 1].index)

# Choisir les indices de TARGET = 0
Zero_indices = dataset[dataset.TARGET == 0].index

# Parmi les indices que nous avons choisis, s閘ectionnez au hasard un nombre "x" (number_of_1)
random_Zero_indices = np.random.choice(Zero_indices, number_of_1, replace = False)
random_Zero_indices = np.array(random_Zero_indices)

# Ajouter les 2 indices
under_sample_indices = np.concatenate([One_indices,random_Zero_indices])

# Under sample dataset
under_sample_data = dataset.iloc[under_sample_indices,:]

X_undersample = under_sample_data.ix[:, under_sample_data.columns != 'TARGET']
y_undersample = under_sample_data.ix[:, under_sample_data.columns == 'TARGET']

# Montrant le ratio
print("Percentage of zero Target: ", len(under_sample_data[under_sample_data.TARGET == 0])/len(under_sample_data))
print("Percentage of One Target: ", len(under_sample_data[under_sample_data.TARGET == 1])/len(under_sample_data))
print("Total number of Target in resampled data: ", len(under_sample_data))



from sklearn.cross_validation import train_test_split

# Undersampled dataset
X_train_undersample, X_test_undersample, y_train_undersample, y_test_undersample = train_test_split(X_undersample
                                                                                                   ,y_undersample
                                                                                                   ,test_size = 0.3
                                                                                                   ,random_state = 0)
print("")
print("Number loans train dataset: ", len(X_train_undersample))
print("Number loans test dataset: ", len(X_test_undersample))
print("Total number of loans: ", len(X_train_undersample)+len(X_test_undersample))


# Training a Decision Tree Model after undersampling
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train_undersample,y_train_undersample)
#Predictions and Evaluation of Decision Tree
predictions = classifier.predict(X_test_undersample)
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test_undersample,predictions))

# RANDOM FOREST
from sklearn.ensemble import RandomForestClassifier
classifier1 = RandomForestClassifier(n_estimators = 400, criterion = 'entropy', random_state = 0)
classifier1.fit(X_train_undersample, y_train_undersample)

# Predicting the Test set results
y_pred = classifier1.predict(X_test_undersample)

# Making the Confusion Matrix
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test_undersample,y_pred))


# Fitting Kernel SVM to the Training set
from sklearn.svm import SVC
classifier5 = SVC(kernel = 'linear', C=100)
classifier5.fit(X_train_undersample, y_train_undersample)

# Predicting the Test set results
y_pred5 = classifier5.predict(X_test_undersample)

# Making the Confusion Matrix
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test_undersample,y_pred5))



# Applying PCA pour reduire les dimmensions afin d'augmenter la precision en garadant seulement les features qui sont plus significatifs
from sklearn.decomposition import PCA
pca = PCA(n_components = 30)
X_train_undersample = pca.fit_transform(X_train_undersample)
X_test_undersample = pca.transform(X_test_undersample)
explained_variance = pca.explained_variance_ratio_

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier4 = LogisticRegression(random_state = 0)
classifier4.fit(X_train_undersample, y_train_undersample)

# Predicting the Test set results
y_pred4 = classifier4.predict(X_test_undersample)

# Making the Confusion Matrix
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test_undersample,y_pred4))


#Resultat finale

y_pred_rendu = pd.DataFrame(y_pred,columns=['TARGET'])
predict = df[:14515].drop('TARGET',axis=1).join(y_pred_rendu)
predict.to_csv('predict.csv')


