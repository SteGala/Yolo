from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Load YOLO model and configure
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Manually specify the output layer indices (YOLOv3 specific)
output_layers = [82, 94, 106]

# Function to perform object detection
def detect_objects(frame):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.3:  # Adjust confidence threshold as needed
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-maxima suppression to remove overlapping boxes
    # indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    # # Prepare results in JSON format
    # results = []
    # for i in indices:
    #     i = i[0]
    #     box = boxes[i]
    #     x, y, w, h = box
    #     label = f'Class {class_ids[i]}'
    #     confidence = confidences[i]
    #     results.append({'name': label, 'confidence': confidence, 'xmin': x, 'ymin': y, 'xmax': x + w, 'ymax': y + h})

    # Prepare results in JSON format
    results = []
    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        label = f'Class {class_ids[i]}'
        confidence = confidences[i]
        results.append({'name': label, 'confidence': confidence, 'xmin': x, 'ymin': y, 'xmax': x + w, 'ymax': y + h})

    return results

@app.route('/process_frames', methods=['POST'])
def process_frames():
    if 'frames' not in request.files:
        return jsonify({'error': 'No frames found in request'}), 400

    # Read input frames
    frames = request.files.getlist('frames')

    results = []
    for frame in frames:
        # Convert frame to numpy array
        npimg = np.fromstring(frame.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Perform object detection
        detections = detect_objects(img)

        results.append(detections)

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
