from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def get_finger_states(hand_landmarks, handedness):
    finger_states = []
    is_right_hand = (handedness.classification[0].label == 'Right')

    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

    if is_right_hand:
        finger_states.append(1 if thumb_tip.x > thumb_mcp.x and thumb_tip.y < thumb_ip.y else 0)
    else:
        finger_states.append(1 if thumb_tip.x < thumb_mcp.x and thumb_tip.y < thumb_ip.y else 0)

    finger_tips_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for tip_id, pip_id in zip(finger_tips_ids, pip_ids):
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[pip_id]
        finger_states.append(1 if tip.y < pip.y else 0)

    return finger_states

def dist(lm1, lm2):
    return np.sqrt((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2)

def are_fingers_spread(tips, wrist, base):
    avg_dist = np.mean([dist(tips[i], tips[i+1]) for i in range(len(tips)-1)])
    return avg_dist > dist(wrist, base) * 0.25

def get_gesture(finger_states, hand_landmarks, handedness):
    t, i, m, r, p = finger_states
    is_right_hand = (handedness.classification[0].label == 'Right')

    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if t == i == m == r == p == 0:
        return "Fist"
    if t == i == m == r == p == 1:
        if are_fingers_spread([index_tip, middle_tip, ring_tip, pinky_tip], wrist, index_mcp):
            return "Stop Sign"
        return "Open Hand"
    if t == 1 and i == m == r == p == 0:
        if thumb_tip.y < wrist.y:
            return "Thumbs Up"
        elif thumb_tip.y > wrist.y:
            return "Thumbs Down"
    if t == 0 and i == 1 and m == r == p == 0:
        return "Pointing"
    if t == 0 and i == 1 and m == 1 and r == p == 0:
        if dist(index_tip, middle_tip) > dist(index_mcp, middle_tip) * 0.3:
            return "Peace"
        return "Two Fingers"
    if i == m == r == p == 1:
        if dist(thumb_tip, index_tip) < dist(index_mcp, index_tip) * 0.2:
            return "OK"
    if t == 1 and i == m == r == 0 and p == 1:
        return "Shaka"
    if t == 1 and i == 1 and m == r == p == 0:
        return "Gun"
    if i == 1 and m == r == 0 and p == 1:
        return "Rock On"
    if t == 1 and i == 1 and m == r == p == 0:
        if is_right_hand and thumb_tip.x < thumb_mcp.x:
            return "L-Shape"
        elif not is_right_hand and thumb_tip.x > thumb_mcp.x:
            return "L-Shape"
    if t == 1 and i == 1 and m == r == 0 and p == 1:
        return "Spider-Man"
    if t == 0 and i == 1 and m == r == p == 0:
        return "Number 1"
    if t == 0 and i == 1 and m == 1 and r == p == 0:
        return "Number 2"
    if t == 1 and i == 1 and m == 1 and r == p == 0:
        return "Number 3"
    if t == 0 and i == 1 and m == 1 and r == 1 and p == 1:
        return "Number 4"
    if t == i == m == r == p == 1:
        return "Number 5"

    return "Unknown"

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Webcam not accessible.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        gesture_map = {}

        if result.multi_hand_landmarks and result.multi_handedness:
            for idx, (hand_landmarks, handedness) in enumerate(zip(result.multi_hand_landmarks, result.multi_handedness)):
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_states = get_finger_states(hand_landmarks, handedness)
                gesture = get_gesture(finger_states, hand_landmarks, handedness)
                wrist_lm = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                h, w, _ = frame.shape
                cx, cy = int(wrist_lm.x * w), int(wrist_lm.y * h)
                cv2.putText(frame, f"{handedness.classification[0].label}: {gesture}", (cx - 50, cy - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                gesture_map[handedness.classification[0].label] = hand_landmarks

            if len(result.multi_hand_landmarks) == 2:
                l_hand = gesture_map.get("Left")
                r_hand = gesture_map.get("Right")
                if l_hand and r_hand:
                    l_index_tip = l_hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    r_index_tip = r_hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    l_thumb_tip = l_hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    r_thumb_tip = r_hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    if dist(l_index_tip, r_index_tip) < 0.08 and dist(l_thumb_tip, r_thumb_tip) < 0.08:
                        cv2.putText(frame, "Heart ❤️", (frame.shape[1] // 2 - 100, 80),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
