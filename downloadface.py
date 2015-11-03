import sys, os
import cv2
import urllib2
from urlparse import urlparse

def detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img, file_name):
    i = 0   #   Track how many faces found
    for x1, y1, x2, y2 in rects:
        print "Found " + str(i) + " face!"  #   Tell us what's going on
        cut = img[y1:y2, x1:x2] #   Defines the rectangle containing a face
        file_name = file_name.replace('.jpg','_')   #   Prepare the filename 
        file_name = file_name + str(i) + '.jpg'
        file_name = file_name.replace('\n','')
        print 'Writing ' + file_name
        cv2.imwrite('detected/' + str(file_name), cut)   #   Write the file
        i += 1  #   Increment the face counter

def main():
    #   all.txt contains a list of thumbnail URLs
    #   done.txt contains a list of all processed thumbnails - empty it if you want a fresh run
    for line in open('all.txt'):
        # dirty way to allow resume: if line is in done file, ignore it
        alreadydone = False
        with open('done.txt', 'a+') as f:
                for doneline in f:
                        if line in doneline:
                                alreadydone = True
                                print "Skipping " + line
                                break
        f.close()

        # line has been found, skip to next one
        if alreadydone:
                continue


        file_name = urlparse(line).path.split('/')[-1]
        print "URL is " + line

        handle = urllib2.urlopen(line)
        if (handle.getcode() == 200):
            #   Download to a temp file
            with open(os.path.basename("temp.jpg"), "wb") as local_file:
                local_file.write(handle.read())
            #urllib2.urlretrieve(line, "temp.jpg")
            #   Detect the face(s)
            rects, img = detect("temp.jpg")
            #   Cut and kepp
            box(rects, img, file_name)
            # add record of download
            f = open('done.txt','a')
            f.write(line)
            f.close()
        else:
            print '404 - ' + line


 
if __name__ == "__main__":
    main()
