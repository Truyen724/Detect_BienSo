from keras.models import model_from_json
from os.path import splitext
import  cv2
def load_model(path):
    path = splitext(path)[0]
    with open('%s.json' % path, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json, custom_objects={})
    model.load_weights('%s.h5' % path)
    return model
model = model_from_json("wpod-net_update1.json")
vid = cv2.VideoCapture(0)
# while(True):
#     ret, frame = vid.read()
#     frame = frame.reshape((1, frame.shape[0], frame.shape[1], frame.shape[2]))
#     model.predict(frame)
    
    