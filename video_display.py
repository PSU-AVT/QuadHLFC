import pika, cv, pickle, time

connection = pika.BlockingConnection(pika.ConnectionParameters(
host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='video_stream_test3')

cv.NamedWindow("There", cv.CV_WINDOW_AUTOSIZE)

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    frame_data = pickle.loads(body)
    print(time.time() - frame_data[4])
    frame = cv.CreateImage(frame_data[0], frame_data[1], frame_data[2])
    cv.SetData(frame, frame_data[3])
    cv.ShowImage("There", frame)
    cv.WaitKey(10)

channel.basic_consume(callback,queue='hello',no_ack=True)

channel.start_consuming()
