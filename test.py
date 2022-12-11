import numpy as np
from keras.models import model_from_json
import cv2 
from os.path import splitext
from lib_detection import load_model, detect_lp, im2single
def load_model(path):
    path = splitext(path)[0]
    with open('%s.json' % path, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json, custom_objects={})
    model.load_weights('%s.h5' % path)
    return model
wpod_net_path = "wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)
vid = cv2.VideoCapture(0)
while(True):
    ret, frame = vid.read()
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
                cv2.imshow("Anh bien so sau chuyen xam", gray)
                # Ap dung threshold de phan tach so va nen
                binary = cv2.threshold(gray, 127, 255,
                                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                cv2.imshow("Anh bien so sau threshold", binary)
                # Nhan dien bien so. Cau hinh --psm 7 la de nhan dien 1 line only
                # text = pytesseract.image_to_string(binary, lang="eng", config="--psm 7")
                # Viet bien so len anh
                # cv2.putText(Ivehicle,fine_tune(text),(50, 50), cv2.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 255), lineType=cv2.LINE_AA)
                # Hien thi anh va luu anh ra file output.png
                cv2.imshow("Anh input", frame)
                # cv2.imwrite("output.pqng",frame)
                # the 'q' button is set as the
                # quitting button you may use any
                # desired button of your choice
        except:
            pass
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            
            cv2.destroyAllWindows()
            break
cv2.destroyAllWindows()