from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe

cap = cv2.VideoCapture(0)
mpHands = mediapipe.solutions.hands
hands = mpHands.Hands(max_num_hands=1)        
mpDraw = mediapipe.solutions.drawing_utils

def mean(data):
    return sum(data) / len(data)



app = Flask(__name__)

@app.route("/")
def main():
    return render_template("s.html")

def generate_frames():
    while True:
            
        success,img=cap.read()
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            meanx,meany = 0,0
            if results.multi_hand_landmarks is not None:   
                x_values = []
                y_values = []        
                for hand in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)
                for identity, landmark in enumerate(hand.landmark):
                    
                    height, width, channels = img.shape
                    centerx, centery = int(landmark.x * width), int(landmark.y * height)

                    x_values.append(centerx)
                    y_values.append(centery)
                    
                meanx = int(mean(x_values))
                meany = int(mean(y_values))            
            flipped = cv2.flip(img, 1)
            ret,buffer=cv2.imencode('.jpg',flipped)
            img=buffer.tobytes()
            
            yield img, meanx, meany
                
            
        

    
@app.route('/video')
def video():
    def generate():
        for frame_bytes, meanx, meany in generate_frames():
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes +
                   b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mean')
def get_mean():
    for _, meanx, meany in generate_frames():
        data = {'Meanx': meanx, 'Meany': meany}
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug = True, host = '192.168.18.22')
    
    
    
    





# def main():
#     run = True
#     while run:
#         _, img = cap.read()
        
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = hands.process(imgRGB)
#         if results.multi_hand_landmarks is not None:           
#             for hand in results.multi_hand_landmarks:
#                 mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)

#         flipped = cv2.flip(img, 1)
#         cv2.imshow("Image", flipped)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cv2.destroyAllWindows()
#     cap.release()