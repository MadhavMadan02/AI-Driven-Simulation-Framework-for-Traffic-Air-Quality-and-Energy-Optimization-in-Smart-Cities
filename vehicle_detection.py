import cv2
import numpy as np

# Load YOLO pre-trained model for vehicle detection
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load the COCO names file (contains class names)
classes = []
with open("coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Load the image
image_path = r"carOnRoad3.jpg"
image = cv2.imread(image_path)

# Check if the image is loaded correctly
if image is None:
    print("Error: Could not load the image. Check the file path.")
    exit()

# Get image dimensions
height, width, _ = image.shape

# Preprocess the image for YOLO
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)

# Get output layer names
output_layers = net.getUnconnectedOutLayersNames()
detections = net.forward(output_layers)

# Lists to store detected vehicle bounding boxes, confidence scores, and class IDs
boxes = []
confidences = []
class_ids = []

# Loop through detections
for detection in detections:
    for obj in detection:
        scores = obj[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        # Class ID for cars is 2, trucks is 7, buses is 5, motorcycles is 3
        if confidence > 0.5 and class_id in [2, 3, 5, 7]:  
            # Get bounding box coordinates
            center_x = int(obj[0] * width)
            center_y = int(obj[1] * height)
            w = int(obj[2] * width)
            h = int(obj[3] * height)

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            # Append to lists
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply Non-Maximum Suppression (NMS) to remove duplicate overlapping boxes
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Final vehicle count after NMS filtering
vehicle_count = len(indices)

# Draw final bounding boxes
for i in indices.flatten():
    x, y, w, h = boxes[i]
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, "Vehicle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Save the vehicle count to a text file
with open("vehicle_count.txt", "w") as file:
    file.write(str(vehicle_count))

# Display the image with detections
cv2.imshow("Vehicle Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"\nTotal Vehicles Detected: {vehicle_count}")
print("Vehicle count saved to vehicle_count.txt")
