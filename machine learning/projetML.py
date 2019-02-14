#Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
#from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

#Import dataset
def algoML(filename):

	df = pd.read_csv(filename)




										


	# looking for the position of the column that have missing values
	mv = []
	for i in range (len(df.columns)):
	    if df[df.columns[i]].isna().sum() != 0:
	        mv.append(i)


	# list comtain the name of all cilumn that are missing
	cmv = []
	for i in range (len(mv)):
	    cmv.append(df.columns[mv[i]])

	# looking for the position of columns integer that have missing values
	imv = []
	for i in range (len(cmv)):
	    if df[cmv[i]].dtype == 'int64':
	        imv.append(i)

	# looking for the position of columns float that have missing values
	fmv = []
	for i in range (len(cmv)):
	    if df[cmv[i]].dtype == 'float64':
	        fmv.append(cmv[i])


	# looking for the position of columns object that have missing values
	omv = []
	for i in range (len(mv)):
	    if df[cmv[i]].dtype == 'object':
	        omv.append(cmv[i])


	# filling the missing values of float columns by the mean
	for i in range (len(fmv)):
	    df[fmv[i]].fillna(value=df[fmv[i]].mean(),inplace=True)

	# filling the missing values of text columns by the mean
	for i in range (len(omv)):
	    df[omv[i]].fillna(value=df[omv[i]].value_counts().idxmax(),inplace=True)

	# looking for the columns object 
	oc = []
	for i in range (len(df.columns)):
	    if df[df.columns[i]].dtype == 'object':
	        oc.append(df.columns[i])


	                               ############################### Feature Scaling ##############################

	# looking for the columns float and integer  
	ifc = []
	for i in range (len(df.columns)):
	    if df[df.columns[i]].dtype != 'object':
	        ifc.append(df.columns[i])
	print(len(ifc))

	js = df[ifc]

	scaler = MinMaxScaler()
	sab = scaler.fit_transform(js)

	kil = pd.DataFrame(sab,columns=ifc).drop('TARGET',axis=1)
	kil_100 = kil.join(df['TARGET'])

	myta = df[oc]

	kil_myta = kil_100.join(myta)

	                             ################################## Categorical DATA ################################

	# Categorical Features
	dataset = pd.get_dummies(kil_myta,columns=oc,drop_first=True)


	#splitting dataset 

	X = dataset.drop('TARGET',axis=1)
	y = dataset['TARGET']
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=101)




	                               ############################ReSampling - Under Sampling###########################

	number_of_1 = len(dataset[dataset.TARGET == 1])
	One_indices = np.array(dataset[dataset.TARGET == 1].index)

	# Picking the indices of the normal classes
	Zero_indices = dataset[dataset.TARGET == 0].index

	# Out of the indices we picked, randomly select "x" number (number_of_1)
	random_Zero_indices = np.random.choice(Zero_indices, number_of_1, replace = False)
	random_Zero_indices = np.array(random_Zero_indices)

	# Appending the 2 indices
	under_sample_indices = np.concatenate([One_indices,random_Zero_indices])

	# Under sample dataset
	under_sample_data = dataset.iloc[under_sample_indices,:]

	X_undersample = under_sample_data.ix[:, under_sample_data.columns != 'TARGET']
	y_undersample = under_sample_data.ix[:, under_sample_data.columns == 'TARGET']






	# Undersampled dataset
	X_train_undersample, X_test_undersample, y_train_undersample, y_test_undersample = train_test_split(X_undersample
	                                                                                                   ,y_undersample
	                                                                                                   ,test_size = 0.3
	                                                                                                   ,random_state = 0)





	# RANDOM FOREST
	classifier1 = RandomForestClassifier(n_estimators = 300, criterion = 'entropy', random_state = 0)
	classifier1.fit(X_train_undersample, y_train_undersample)

	# Predicting the Test set results
	y_pred = classifier1.predict(X_test_undersample)

	# Making the Confusion Matrix

	# Fitting Kernel SVM to the Training set




	#Resultat finale

	y_pred_rendu = pd.DataFrame(y_pred,columns=['TARGET'])
	predict = df[:14515].drop('TARGET',axis=1).join(y_pred_rendu)
	predict.to_csv('predict.csv')


