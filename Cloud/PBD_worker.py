import boto3
import statistics
import time
import random
import projetML
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

def Descrypt(filename):
    code = 'nooneknows'
    with open(filename, 'rb') as fobj:
        # Import private key
        private_key = RSA.import_key(open('my_private_rsa_key.bin').read(), passphrase=code)
        # Session key, random number, message authentication code, confidential data
        enc_session_key, nonce, tag, ciphertext = [ fobj.read(x) 
                                                    for x in (private_key.size_in_bytes(), 
                                                    16, 16, -1) ]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        # Decrypt
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    with open(filename, 'wb') as wobj:
        wobj.write(data)


sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
bucket = s3.Bucket('mybucketdataset')

inboxQueue = sqs.get_queue_by_name(QueueName='inboxQueue')
outboxQueue = sqs.get_queue_by_name(QueueName='outboxQueue')
questionQueue = sqs.get_queue_by_name(QueueName='questionQueue')
answerQueue = sqs.get_queue_by_name(QueueName='answerQueue')
resultQueue = sqs.get_queue_by_name(QueueName='resultQueue')
questions=["What's your first name?","What's your favorite color?","What's your last name?"]
answers=["pingjie","blue","du"]
matchQA=False
randIdx=random.randint(0,2)


question_received=questionQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
for question in question_received:
    question.delete()

#Firstly,send a question.
question = questionQueue.send_message(MessageBody=questions[randIdx])

print("Worker begins.")
while True:
    time.sleep(1)
    #receive the answer if it's in the queue
    answer_received=answerQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
    for answer in answer_received:

        if(answers[randIdx]==answer.body):  #if the answer is correct
            resultQueue.send_message(MessageBody="match")
            matchQA=True
            randIdx=random.randint(0,2)
            question = questionQueue.send_message(MessageBody=questions[randIdx])
        else:   #if the answer is not correct
            resultQA = resultQueue.send_message(MessageBody="notMatch")
            matchQA=False
            print("the answer is not correct.")
            print("=========================================")
        answer.delete()


    if(matchQA):

        print("the answer is correct. Wait for the dateset.")
        #receive the infos of the file uploaded.
        message_received=inboxQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
        for message in message_received:

            for obj in bucket.objects.filter(Prefix=message.body):
                if obj.key == message.body:
                    with open(message.body, 'wb') as data:
                        bucket.download_fileobj(message.body, data)

            print("The dataset has been downloaded!")

            Descrypt(message.body)
            
            projetML.algoML(message.body)

            with open("predict.csv", 'rb') as data:
                bucket.upload_fileobj(data, "predict.csv")
            responce = outboxQueue.send_message(MessageBody="predict.csv")
            matchQA=False
            print("predict.csv"+" has uploaded.")
            print("=========================================")
            message.delete()

