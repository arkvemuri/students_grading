import pika
import six.moves.urllib as urllib
from pika import BlockingConnection
#from pika.handlers import IncomingMessageHandler


#server = 'amqps://RootManageSharedAccessKey:' + urllib.parse.quote(key) + '@swayam2test.servicebus.windows.net/swayameventhub'
#server = 'amqps://RootManageSharedAccessKey:' + urllib.parse.quote(key) + '@swayam2test.servicebus.windows.net/swayameventhub'
ADDRESS = "amqps://swayam2test.servicebus.windows.net"

#USER = "RootManageSharedAccessKey"
#KEY = "/8thDkXqpv5ynS99ludS9a+vwTCjWlgpwYJiQYcpcCs="
USER='admin'
KEY='admin'
SERVER='localhost'
QUEUE='hello'

credentials = pika.PlainCredentials(USER, KEY)
parameters = pika.ConnectionParameters(credentials=credentials)

queue = 'swayameventhub'

connection = pika.BlockingConnection(pika.ConnectionParameters(SERVER,credentials=credentials))
channel = connection.channel()
channel.basic_publish(exchange='',
                      routing_key=QUEUE,
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

#conn = BlockingConnection(server, allowed_mechs="PLAIN")9
#sender = conn.create_sender(queue)
#sender.send(Message(body="Hello World!"))
connection.close()

#connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#channel = connection.channel()


#channel.queue_declare(queue='hello')

#channel.basic_publish(exchange='',
#                      routing_key='hello',
#                      body='Hello World!')
#print(" [x] Sent 'Hello World!'")
#connection.close()

