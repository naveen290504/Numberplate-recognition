import numpy as np
import requests
import cv2

regions = ["mx", "us-ca"]

capture_video = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

demo = ''


def detect(frame):
    image = 'output.jpg'
    fin = cv2.imread(image, 1)
    xmin = 0
    ymin = 0
    xmax = 0
    ymax = 0
    score = 0
    plate = 0
    try:
        with open(image, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),
                files=dict(upload=fp),
                headers={'Authorization': 'Token b744e98e8687873b409d45f96f80087372f27617'})

        resp = response.json()
        b = 0
        result = resp['results']
        for i in result:
            b = i.get('box')
        xmin = b.get('xmin')
        ymin = b.get('ymin')
        xmax = b.get('xmax')
        ymax = b.get('ymax')
        pl = ''
        for i in result:
            pl = i.get('plate')
        plate = pl.upper()
        score = 0
        for i in result:
            score = i.get('score')
    except:
        print('License Image Not Here')
    img = image
    imagepath = img
    imagefile = img
    image_input = cv2.imread(imagepath)

    cv2.rectangle(image_input, (xmin, ymin - 20), (xmax, ymax), color=(36, 255, 12), thickness=2)
    if xmax and ymin and ymax and xmin is not None:
        cv2.putText(image_input, f'Licence Plate: {plate} & Accuracy Score: {score}', (xmin, ymin),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
    cv2.imshow('LicenceDetect', image_input)
    return demo


while (True):
    ret, frame = capture_video.read()
    if ret == True:
        # frame = cv2.flip(frame, 1)
        # write the flipped frame
        demo = cv2.imwrite('output.jpg', frame)
    frame = detect(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture_video.release()
cv2.destroyAllWindows()
