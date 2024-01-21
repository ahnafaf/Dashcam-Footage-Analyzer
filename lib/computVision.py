import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

video_path = 'NO20230618-115845-000309F.MP4'
extracted_text = []

def extract_text(file_name):
    video = cv2.VideoCapture(file_name)
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Perform text extraction using Tesseract OCR
        text = pytesseract.image_to_string(gray)
        extracted_text.append(text)
        print(text)
    video.release()

# Call the function to extract text from the video
extract_text(video_path)

# Print the extracted text from each frame
 
