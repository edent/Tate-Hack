import os
import sys
import cv2
import numpy as np

if __name__ == "__main__":

    # Requires path to training image folder, and image we want to find.
    # Each subfolder should be of the same subject.
    """
     Eg:
    |-path
      |-Alice
      | |-0.jpg
      | |-1.jpg
      |
      |-Bob
      | |-0.jpg
      |
      |-Carly
      ...
    """
   
    if len(sys.argv) < 4:
        print "USAGE: recognise.py </path/to/images> sampleImage.jpg threshold"
        print "threshold is an float. Choose 100.0 for an extremely close match.  Choose 100000.0 for a fuzzier match."
        print str(len(sys.argv))
        sys.exit()

    # Create an Eign Face recogniser
    t = float(sys.argv[3])
    model = cv2.createEigenFaceRecognizer(threshold=t)

    # Load the model
    model.load("eigenModel.xml")

    # Read the image we're looking for
    sampleImage = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
    sampleImage = cv2.resize(sampleImage, (256,256))

    # Look through the model and find the face it matches
    [p_label, p_confidence] = model.predict(sampleImage)

    # Print the confidence levels
    print "Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence)

    # If the model found something, print the file path
    if (p_label > -1):
        count = 0
        for dirname, dirnames, filenames in os.walk(sys.argv[1]):
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                if (count == p_label):
                    for filename in os.listdir(subject_path):
                        print subject_path

                count = count+1
