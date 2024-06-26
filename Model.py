import math


from centroidtracker import CentroidTracker


class Tracker:
    def __init__(self):
        self.center_points = {}
       
        self.id_count = 0


    def update(self, objects_rect):
      
        objects_bbs_ids = []

     
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

          
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:
                    self.center_points[id] = (cx, cy)
#                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

          
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

     
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

     
        self.center_points = new_center_points.copy()


        return objects_bbs_ids

import torch
import numpy as np
import cv2
import time
import queue
output_queue = queue.Queue()


class ObjectDetection:

    def __init__(self, model):

        self.ids = []
        self.model = model
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.count = 0
        self.curr_count = 0
        self.rect = []
        self.tracker = CentroidTracker(maxDisappeared=80, maxDistance=90)
        self.passed_ids = []

        self.new_detected = False

        self.queue = queue
        self.frame = 0




        print("\n\nDevice Used:", self.device)





    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord,

    def class_to_label(self, x):
        return self.classes[int(x)]

    def plot_boxes(self, results, frame, frame_count):
        labels, cord = results
        self.new_detected = False

        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        cv2.line(frame, (0, 102), (x_shape, 102), (0, 0, 255), 3)



        for i in range(n):
            row = cord[i]
            if self.class_to_label(labels[i]) == "person":
             if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                self.new_detected = True



                self.rect.append([x1, y1, x2, y2])
                self.new_rects = self.tracker.update(rects=self.rect)

                center = (int(center_x), int(center_y))
                frame[center[1], center[0]] = (50, 255, 100)


        if isinstance(self.new_rects, dict):
         self.curr_count = len(self.rect)
         for key, val in self.new_rects.items():
             center_y = (val[1] + val[3]) / 2
             cv2.rectangle(frame, (val[0], val[1]), (val[2], val[3]), (0 ,0, 255), 1)
             cv2.putText(frame, str("Total Crossed:"+ str(self.count)), (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
             cv2.putText(frame, str(key), (val[0], val[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
             if key not in(self.passed_ids):
                if center_y >= 100 and center_y <= 105:
                 self.passed_ids.append(key)
                 self.count += 1

         self.rect = []

        return frame




    def __call__(self, frame):
        frame_count = 0

        start_time = time.perf_counter()

        results = self.score_frame(frame)
        frame = self.plot_boxes(results, frame, frame_count)
        frame_count += 1
        end_time = time.perf_counter()

        fps = 1 / np.round(end_time - start_time, 3)

        '''
            cv2.imshow("img", frame)


            if cv2.waitKey(10) & 0xFF == ord('q'):
                break'''
        if self.new_detected == False:
         print(self.new_detected)
        return frame, self.count, self.curr_count, self.new_detected



# Nesneyi seçin ve çerçeve içine sınırlayın
if __name__ == '__main__':
 cap = cv2.VideoCapture(r"video\16.mp4")
 detection = ObjectDetection(torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True))
 detection([])
