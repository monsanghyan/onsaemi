import datetime
import cv2
from ultralytics import YOLO
import requests

CONFIDENCE_THRESHOLD = 0.6
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

model = YOLO('./best.pt')

cap = cv2.VideoCapture('https://192.168.0.51:8080/video')
# 내 핸드폰: "https://192.168.0.51:8080/video"

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    start = datetime.datetime.now()

    ret, frame = cap.read()
    if not ret:
        print('Cam Error')
        break

    detection = model(frame)[0]

    for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
        confidence = float(data[4])
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        label = int(data[5])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
        cv2.putText(frame, class_list[label]+' '+str(round(confidence, 2)), (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)

        # print(class_list, label)

        if class_list[label] == 'on':
            response = requests.get("http://127.0.0.1:8000/re")
            print(response.json())

    end = datetime.datetime.now()

    total = (end - start).total_seconds()
    print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')

    fps = f'FPS: {1 / total:.2f}'
    cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()