# TSE-INFO2-Projet-BigData

Equipe : Hicham Ezzagh - Pingjie Du - Di Yang

## Introduction

- We have realised a data analysis with Machine Learning and Cloud Computing service (AWS) on Python3.
- We also used MongoDB service for the local storage.(Java with API mongodb-driver and javacsv).

## Installation 

- Update the pip3 tool :

  sudo pip3 install --upgrade pip 
Install the required Python3 packages :
  pip3 install boto3
  sudo pip3 install --upgrade ipython numpy pandas seaborn matplotlib scipy scikit-learn 
- Install TK for Python 3 (used by Matplotlib) :

  sudo apt install python3-tk

  tous le code python sont déjà commenté
  
## Storage

- The result file - predict.csv is in storage/src/main/resources/  

- Run main.java the file predict.csv will be imported in local MongoDB.

## Cloud

- Postion of files

  "PBD_worker.csv" and "my_private_rsa_key.bin" is on the VM in the cloud.
  
  "PBD_client.py" and "my_rsa_public.pem" is in the local computer.
  
  "projetML.py" is the code of the machine-learning part.
  
  "crypto.py" is used for create the private key and the public key.
  

- Implementation process

  Firstly, run "python3 PBD_worker.py" on the VM in the cloud.
  
  Then, run "python3 PBD_client.py" on the local computer.It will encrypt the "dataset.csv" and automatically upload the "dataset.csv" to the cloud and download the "predict.csv" from the cloud.
  
