import logging
logging.basicConfig(level=logging.INFO)

# Paketler projeye dahil edilir.
from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
import numpy as np
import cv2


def print_log(text, hdmi_out):
    outframe = hdmi_out.newframe()
    x = 100
    y = 200   
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(outframe, text, (x,y), font, 0.6, (255, 255, 255), 1)
    hdmi_out.writeframe(outframe)
    logging.info(text)
    del outframe

    
# Hdmi cikis konfigurasyonlari yapilir.
base = BaseOverlay("base.bit")
Mode = VideoMode(1920,1080,24)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(Mode,PIXEL_BGR)
hdmi_out.start()

print_log("Program baslatiliyor.", hdmi_out)

# Monitor cikti arabellek boyutu belirlenir.
frame_out_w = 1920
frame_out_h = 1080
# Kamera girdi boyutu belirlenir.
frame_in_w = 640
frame_in_h = 480

# OpenCV kullanarak kamerayi baslatir.
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_in_w);
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_in_h);

print_log("Kamera durumu: " + str(webcam.isOpened()), hdmi_out)

print_log("Yuz tanima paketleri ve yuzler ekleniyor.", hdmi_out)

import face_recognition
ilayda_image = face_recognition.load_image_file("database/ilayda/1.png")
ilayda_face_encoding = face_recognition.face_encodings(ilayda_image)[0]

huseyin_image = face_recognition.load_image_file("database/huseyin/1.png")
huseyin_face_encoding = face_recognition.face_encodings(huseyin_image)[0]

kadir_image = face_recognition.load_image_file("database/kadir/1.jpg")
kadir_face_encoding = face_recognition.face_encodings(kadir_image)[0]

huseyin_hoca_image = face_recognition.load_image_file("database/huseyin_hoca/1.png")
huseyin_hoca_face_encoding = face_recognition.face_encodings(huseyin_hoca_image)[0]

ali_hoca_image = face_recognition.load_image_file("database/ali_hoca/1.png")
ali_hoca_face_encoding = face_recognition.face_encodings(ali_hoca_image)[0]


known_face_encodings = [
    ilayda_face_encoding,
    huseyin_face_encoding,
    kadir_face_encoding,
    huseyin_hoca_face_encoding,
    ali_hoca_face_encoding
]

known_face_names = [
    "Ilayda",
    "Huseyin",
    "Kadir",
    "Huseyin Acar",
    "Ali Arserim"
]

face_locations = []
face_encodings = []
face_names = []

print_log("Tum yuzler sisteme basariyla tanimlandi.", hdmi_out)

print_log("Yuz tanima baslatiliyor.", hdmi_out)

# 0 numarali buton sistemi durdurmak icin tanimlandi.
stopButton = base.buttons[0]

frame_counter = 0
ret, frame = webcam.read()

while True:
    ret, frame = webcam.read()
    
    inputBGR = cv2.resize(frame, (0,0),fx=0.25, fy=0.25)
    rgb_small_frame = inputBGR[:,:,::-1]
    
    if stopButton.read():
        print_log("Program durduruldu.", hdmi_out)
        break
    
    # Her 5 frameden biri icin yuz tanima algoritmasi calisacaktir.
    if frame_counter%30==0:
    # if process_this_frame:
        # Frame icindeki yuzleri ve lokasyonlari bulur.
        face_locations = face_recognition.face_locations(rgb_small_frame)
        logging.info(f"{len(face_locations)} adet yuz bulundu.")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Sisteme tanimlanmis oldugumuz yuzler ile framede bulduklarini karsilastirir.
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Bilinmiyor"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)

    # Sonuclari ekranda gosterir.
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Yuz tanimayi 1/4 oraninda yaptigimiz icin yuz konumlarini tekrardan eski orana cevirir.
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Yuzu belirten bir dikdortgen cizer.
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Cizilen dikdortgenin yanina yuzun adini yazar.
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left, bottom - 10), font, 1.0, (255, 255, 255), 1)

    outframe = hdmi_out.newframe()
    outframe[0:480,0:640,:] = frame[0:480,0:640,:]
    hdmi_out.writeframe(outframe)
    frame_counter+=1

print_log("Sistem kapatiliyor.", hdmi_out)

# Tanimlanmis olan camera degiskeni ve hdmi cikisi silinir.
webcam.release()
hdmi_out.stop()
del hdmi_out
