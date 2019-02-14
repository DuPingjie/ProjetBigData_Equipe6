import boto3
import sys 
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

def Encrypt(filename):         
    data = ''
    # 二进制只读打开文件，读取文件数据
    with open(filename, 'rb') as f:
        data = f.read()
    with open(filename, 'wb') as out_file:
        # 收件人秘钥 - 公钥
        recipient_key = RSA.import_key(open('my_rsa_public.pem').read())
        #一个 16 字节的会话密钥
        session_key = get_random_bytes(16)
        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        out_file.write(cipher_rsa.encrypt(session_key))
        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
       
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        out_file.write(cipher_aes.nonce)
        out_file.write(tag)
        out_file.write(ciphertext)


#params = sys.argv[1]
params='dataset.csv'
#sqs= boto3.resource('sqs',region_name='us-east-1',aws_access_key_id='ASIARAT5KFXEZXWSZZ2F',aws_secret_access_key='g4If7bezCnnb2tU7KljIK6FNq8kuGeezh6qUV7Ve',
       #  aws_session_token= 'FQoGZXIvYXdzELL//////////wEaDLxyigmS5J4ykAMSziLwAoFz38IDSOfmQhvsOCjsorDvmWvg2x/S0FUHOXh9zMvci+Urn21H+JwrE40mf7iTzznbp1s71UbOcxFwIb6Um/XoO5tQzCufYmb4bajMEIIOipqXHw7Oo5oadJhv5Uu2xTxWcvFMxDrLgIMS18xCcp51EaBOxXXFNsIE5tdDXEsemfnb/7fbMxodSwGRZRzJAvY1BERz4yALQBMZqWplWgtMv61/atfWR9pkdLp3NktJYoFQ9/zhtoZWcp69tV4RHf/zh8HVZXD3avtJphIOJu7qAAL8CLescQQiJlG3oxoBot7J4LMNQP1hOoAEu3fVmGV6EO9azmf69q9rVabkbsPUE3QMiDsr+Akak26OCr6i54YTFIURokYAKKfIGPNOhhp2sO3Yy2jRfCKr7R3QSVEB4xLR1YgVFLeQdVd8NzVC+3NdquhjTuMupr6xzZyQOSoRsJHyTvajbCRtW4KqSxsPpvh9/NMg+Ux7fjOREIKaKNDw8uEF')
#s3 = boto3.resource('s3',region_name='us-east-1',aws_access_key_id='ASIARAT5KFXEZXWSZZ2F',aws_secret_access_key='g4If7bezCnnb2tU7KljIK6FNq8kuGeezh6qUV7Ve',
 #        aws_session_token= 'FQoGZXIvYXdzELL//////////wEaDLxyigmS5J4ykAMSziLwAoFz38IDSOfmQhvsOCjsorDvmWvg2x/S0FUHOXh9zMvci+Urn21H+JwrE40mf7iTzznbp1s71UbOcxFwIb6Um/XoO5tQzCufYmb4bajMEIIOipqXHw7Oo5oadJhv5Uu2xTxWcvFMxDrLgIMS18xCcp51EaBOxXXFNsIE5tdDXEsemfnb/7fbMxodSwGRZRzJAvY1BERz4yALQBMZqWplWgtMv61/atfWR9pkdLp3NktJYoFQ9/zhtoZWcp69tV4RHf/zh8HVZXD3avtJphIOJu7qAAL8CLescQQiJlG3oxoBot7J4LMNQP1hOoAEu3fVmGV6EO9azmf69q9rVabkbsPUE3QMiDsr+Akak26OCr6i54YTFIURokYAKKfIGPNOhhp2sO3Yy2jRfCKr7R3QSVEB4xLR1YgVFLeQdVd8NzVC+3NdquhjTuMupr6xzZyQOSoRsJHyTvajbCRtW4KqSxsPpvh9/NMg+Ux7fjOREIKaKNDw8uEF')

sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
bucket = s3.Bucket('mybucketdataset')


inboxQueue = sqs.get_queue_by_name(QueueName='inboxQueue')
outboxQueue = sqs.get_queue_by_name(QueueName='outboxQueue')
questionQueue = sqs.get_queue_by_name(QueueName='questionQueue')
answerQueue = sqs.get_queue_by_name(QueueName='answerQueue')
resultQueue = sqs.get_queue_by_name(QueueName='resultQueue')

strAnswer=""
isMatch=False
#receive the question that has in the queue.
question_received=questionQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)

for question in question_received:
	#send the answer
	print("==============================")
	print("You can upload the dataset only when you give the right answer.")
	print("==============================")
	strAnswer = input(question.body+" : ")
	print("==============================")
	answer = answerQueue.send_message(MessageBody=strAnswer)
	time.sleep(1)
	#receive the result.
	result_received=resultQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
	for result in result_received:
		#if the answer is correct
		if(result.body=="match"):
			print("The answer is correct!")
			print("==============================")
			print("Begin to upload the "+params)
			print("==============================")
			strDataset = params
			strKey=strDataset
			isMatch=True
			Encrypt(strKey)
			with open(strDataset, 'rb') as data:
				bucket.upload_fileobj(data, strKey)

			request = inboxQueue.send_message(MessageBody=strKey)
			question.delete() #delete the question if the answer is correct.
			print(params+" has uploaded!")
			print("Wait for the result...")
			print("==============================")
			while True: #if correct,wait for the file predict.csv.
				message_received=outboxQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
				hasfound=False
				for message in message_received:
					for obj in bucket.objects.filter(Prefix=message.body):
						if obj.key == message.body:
							with open(message.body, 'wb') as data:
								bucket.download_fileobj(message.body, data)
							print(message.body+" has downloaded.")
							print("==============================")
							message.delete()
							hasfound=True
							break
				if hasfound:
					break

		#if it's not correct.
		else:
			isMatch=False
			print("The answer is not correct.")
			
		result.delete()



