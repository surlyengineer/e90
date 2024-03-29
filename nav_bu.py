import cv2
import numpy as np
import nav#anglefinder

GAMMA_CORR = 5 #this will change with lighting conditions
GAUSS_BLUR_RAD = 15

def find_beacon(img):
    img = cv2.GaussianBlur(img, (GAUSS_BLUR_RAD, GAUSS_BLUR_RAD), 0)
    (minVal, maxVal, min_loc, max_loc) = cv2.minMaxLoc(img)
    image = img.copy()
    cv2.circle(image, max_loc, GAUSS_BLUR_RAD, (255, 0, 0), 2)
    return max_loc

def gamma_correction(img, correction):
    """
    http://py-fu.blogspot.com/2014/04/
    simple-gamma-correction-with-opencv.html
    """
    img = img/255.0
    img = cv2.pow(img, correction)
    return np.uint8(img*255)

def find_circs(imag):
    bw = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
    circs = cv2.HoughCircles(
            bw,
            cv2.cv.CV_HOUGH_GRADIENT,
            2, 
            10,
            minRadius=100,
            maxRadius=750)
    imag = imag.copy()
    try:
        for c in circs:
            circle = c[0]
            cv2.circle(imag, (circle[0], circle[1]), 10, (0,0,255), 2)
    except:
        return False
    #cv2.imshow("Found center", imag)
    #cv2.waitKey()
    return (circle[0], circle[1]), circle[2]

def find_angles_for(dots, center):
    dot_centers = {}
    angle_to = {}
    for dot in dots:
        dot_centers[dot] = find_beacon(dots[dot])
    for dot_center in dot_centers:
        beacon = dot_centers[dot_center]
        angle =  np.arctan2((beacon[0]-center[0]), 
                -1*(beacon[1]-center[1]))
        #if np.degrees(angle) < 0:
        #    angle += np.radians(360)
        angle_to[dot_center] = angle #print(angle_to)
    return(angle_to, dot_centers)

def operate_on(image, dome_center, dome_radius, gamma=GAMMA_CORR):
    #dome_center = find_circs(image)
    working_copy = image.copy()
    display = image.copy()
    blank = np.zeros(image.shape, dtype=np.uint8)
    cv2.circle(blank, dome_center, int(dome_radius), (1,1,1), -1)
    working_copy = cv2.multiply(blank, working_copy)
    gci = gamma_correction(working_copy, gamma)
    b,g,r = cv2.split(gci)
    bb = cv2.GaussianBlur(b, (15,15), 0)
    rb = cv2.GaussianBlur(r, (15,15), 0)
    gb = cv2.GaussianBlur(g, (15,15), 0)

    b = cv2.subtract(b, rb)
    b = cv2.subtract(b, gb)
    r = cv2.subtract(r, bb)
    r = cv2.subtract(r, gb)
    g = cv2.subtract(g, rb)
    g = cv2.subtract(g, bb)

    cv2.imshow("blue", b)
    cv2.imshow("red", r)
    cv2.imshow("green", g)
    dot_dict = {}
    dot_dict['blue'] = b
    dot_dict['red'] = r
    dot_dict['green'] = g
    angle_to, dots = find_angles_for(dot_dict, dome_center)
    color_dict = {
            'blue':(255,0,0),
            'green':(0,255,0),
            'red':(0,0,255)}
    for pt in dots:
        cv2.circle(display, dots[pt], 10, color_dict[pt], 2) 
    cv2.imshow("display", display)
    print([[color,np.degrees(angle_to[color])] for color in angle_to])
    location = nav.guess_position_from(angle_to)
    x = location[0]
    y = location[1]
    t = np.degrees(location[2]) 
    print("{} {} {}".format(x,y,t))
    return gci

def main():
    imag = cv2.imread('robust_test.jpg')
    blank = np.zeros(imag.shape, dtype=np.uint8)
    dome_center, radius = find_circs(imag)
    cv2.circle(blank, dome_center, int(radius-40), (1, 1, 1), -1)
    imag = cv2.multiply(blank, imag)
    gci = gamma_correction(imag, GAMMA_CORR)
    #cv2.imshow("gamma", gci)
    #cv2.waitKey()
    b,g,r = cv2.split(gci)
    cv2.imshow("blue", b)
    cv2.waitKey()
    dot_dict = {}
    dot_dict['blue'] = b
    dot_dict['red'] = r
    dot_dict['green'] = g
    find_angles_for(dot_dict, dome_center)
main()
