import cv2
from flask import Flask, Response,render_template
app = Flask(__name__)
# RTSP URL
rtsp_url1 = "rtsp://admin:123456@192.168.2.132:554/stream1"
rtsp_url2 = "rtsp://admin:123456@192.168.2.133:554/stream1"
rtsp_url3 = "rtsp://admin:123456@192.168.2.131:554/stream1"
rtsp_url4 = "rtsp://admin:123456@192.168.2.130:554/stream1"

def gen_frames(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Unable to open RTSP stream")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')    
    cap.release()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed1')
def video_feed1():
    return Response(gen_frames(rtsp_url1), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2')
def video_feed2():
    return Response(gen_frames(rtsp_url2), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed3')
def video_feed3():
    return Response(gen_frames(rtsp_url3), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed4')
def video_feed4():
    return Response(gen_frames(rtsp_url4), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0',port=8000)