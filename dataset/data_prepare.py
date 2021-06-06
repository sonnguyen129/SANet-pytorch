import numpy as np
import cv2
import time
import os

vid_path = '/media/server2/2506d886-07a4-47e8-846b-9ece25dfe8c7/home/server2/son_env_disk2/video_content/'
for vid in os.listdir(vid_path):
    cap = cv2.VideoCapture(vid_path + vid)
# vid = '/media/server2/2506d886-07a4-47e8-846b-9ece25dfe8c7/home/server2/son_env_disk2/video_content/210329_06B_Bali_1080p_005.mp4'
# cap = cv2.VideoCapture(vid)
    print('Starting capture '+ vid.split("/")[-1] + "\n")
    i=0
    while(i < 1061):
        
        # Capture frame-by-frame
        i+=1
        ret, frame = cap.read()
        if not ret:
            continue
        # frame = cv2.resize(frame, dsize=None,fx=0.3,fy=0.3)

        # Hiển thị
        cv2.imshow('frame',frame)

        # Lưu dữ liệu
        if i>=60:
            print("Số ảnh capture = ",i-60)
            # Tạo thư mục nếu chưa có
            if not os.path.exists('video_frame'):
                os.mkdir('video_frame')

            cv2.imwrite('video_frame/' + vid.split("/")[-1].replace('.mp4','') + "_" + str(i-60) + ".jpg",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()