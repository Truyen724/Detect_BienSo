from paddleocr import PaddleOCR
import os
import database
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import cv2
import numpy as np
ocr = PaddleOCR(lang="en")
import numpy as np
from keras.models import model_from_json
from lib_detection import load_model, detect_lp, im2single
from os.path import splitext
from lib_detection import load_model, detect_lp, im2single
# Kết nói database

# Dinh nghia cac ky tu tren bien so
char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'
wpod_net_path = "wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)
# Ham fine tune bien so, loai bo cac ki tu khong hop ly
def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString

def load_model(path):
    path = splitext(path)[0]
    with open('%s.json' % path, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json, custom_objects={})
    model.load_weights('%s.h5' % path)
    return model

# Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
Dmax = 608
Dmin = 288
def get_liscent_palate(img):
    # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
    ratio = float(max(img.shape[:2])) / min(img.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, lp_type = detect_lp(wpod_net, im2single(img), bound_dim, lp_threshold=0.5)
    if len(LpImg):
        LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
        txt = get_detect()
    
    return txt
# Lấy chữ trong ảnh
def get_detect(mat):
    result = ocr.ocr(mat)
    boxes = [line[0] for line in result[0]]
    txt = [line[1][0] for line in result[0]]
    scores = [line[1][1] for line in result[0]]
    for box in boxes:
        pts = np.array(box,np.int32)
        pts = pts.reshape((-1, 1, 2))
        mat = cv2.polylines(
            img=mat,
            isClosed=True,
            pts=[pts],
            color = (255, 0, 0)
            )
    out = ""
    if(len(txt) == 2):
        
        for i in txt[0]:
            if(i in char_list):
                out += i 
        for j in txt[1]:
            if(j in char_list):
                out += j 
    if(len(txt) == 1 ):
        for i in txt[0]:
            if(i in char_list):
                out += i 

    return out
list_detect = {}
def play_camera(id):
    vid = cv2.VideoCapture(id)
    while(True):
        ret, frame = vid.read()
        frame = cv2.resize(frame,(640,480))
        if(ret):
        # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
            Dmax = 608
            Dmin = 288
            # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
            ratio = float(max(frame.shape[:2])) / min(frame.shape[:2])
            side = int(ratio * Dmin)
            bound_dim = min(side, Dmax)
            
            try:
                _ , LpImg, lp_type = detect_lp(wpod_net, im2single(frame), bound_dim, lp_threshold=0.5)
                if (len(LpImg)):
                    # Chuyen doi anh bien so
                    LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
                    # Chuyen anh bien so ve gray
                    gray = cv2.cvtColor( LpImg[0], cv2.COLOR_BGR2GRAY)
                    # cv2.imshow("Anh bien so sau chuyen xam", gray)
                    # Ap dung threshold de phan tach so va nen
                    binary = cv2.threshold(gray, 127, 255,
                                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                    text = get_detect(binary)
                    list_detect[text]+=1
                    print(text)
                    
            except:
                pass
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                
                cv2.destroyAllWindows()
                break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # play_camera("../Bien_so.mp4")
    play_camera(0)