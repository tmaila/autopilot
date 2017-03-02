import tensorflow as tf
import scipy.misc
import model
import cv2
from subprocess import call
import time
import logger

sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "save/model.ckpt")

img = cv2.imread('steering_wheel_image.jpg',0)
rows,cols = img.shape

# Initialize variables
smoothed_angle = 0.0
degrees = 0.0
i = -1
t = time.time()
t_prev = t

# Create ResultLogger and write initial log entry
log = logger.ResultLogger('logs/runlog.csv')
log.write(i, t, float('nan'), degrees, smoothed_angle)

while(True): #cv2.waitKey(10) != ord('q')):
    i += 1
    full_image = scipy.misc.imread("driving_dataset/" + str(i) + ".jpg", mode="RGB")
    image = scipy.misc.imresize(full_image[-150:], [66, 200]) / 255.0
    degrees = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0] * 180.0 / scipy.pi

    #make smooth angle transitions by turning the steering wheel based on the difference of the current angle
    #and the predicted angle
    smoothed_angle += 0.2 * pow(abs((degrees - smoothed_angle)), 2.0 / 3.0) * (degrees - smoothed_angle) / abs(degrees - smoothed_angle)

    # Measure time, note you want to use time.clock on Windows
    t = time.time()

    # Write to driving log
    log.write(i, t, t-t_prev, degrees, smoothed_angle)
    t_prev = t

    #call("clear")
    #print("Predicted steering angle: " + str(degrees) + " degrees")
    #cv2.imshow("frame", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))


    #M = cv2.getRotationMatrix2D((cols/2,rows/2),-smoothed_angle,1)
    #dst = cv2.warpAffine(img,M,(cols,rows))
    #cv2.imshow("steering wheel", dst)


cv2.destroyAllWindows()
