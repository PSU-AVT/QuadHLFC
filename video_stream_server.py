import cv, sys, pika, pickle, time
from threading import Thread

class Camera:

    def __init__(self):
        self.init_pubsub(host_name = 'localhost')
         
        
        #cv.NamedWindow("Here", cv.CV_WINDOW_AUTOSIZE)
        self.capture = cv.CaptureFromCAM(0)
        self.run()

    def run(self):
        while(True):
            self.repeat()

    def repeat(self):
        
        frame = cv.QueryFrame(self.capture)
        cv.ShowImage("Here", frame)
        c = cv.WaitKey(10)

        temp = cv.CreateImageHeader((frame.width, frame.height), frame.depth, frame.nChannels)
        
        frame_data = ((frame.width, frame.height), frame.depth, frame.nChannels, frame.tostring(), time.time())
        print(frame_data[0]) 
        self.channel.basic_publish(exchange='',routing_key='hello',body=pickle.dumps(frame_data))

    def init_pubsub(self, host_name):
        print("initializing pubsub server connection...")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='video_stream_test3')

    def send_message(self, message, routing_name):
        pass

if __name__ == "__main__":
    cam = Camera()
