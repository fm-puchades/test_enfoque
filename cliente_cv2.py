import cv2
import requests
import numpy as np

def fetch_frame(stream_url):
    """
    Fetch a single frame from the MJPEG stream.

    Args:
        stream_url (str): The URL of the MJPEG stream.

    Returns:
        np.ndarray: The frame as an OpenCV image (BGR format).
    """
    resolucion = (640, 480)
    frame = cv2.imread("cartaajuste.png")
    frame = cv2.resize(frame, resolucion)
    response = requests.get(stream_url, stream=True, auth=("cameraman", "cam46610"))
    
    if response.status_code != 200:
        raise RuntimeError(f"Failed to connect to stream: {response.status_code}")

    bytes_data = b''
    for chunk in response.iter_content(chunk_size=1024):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # JPEG start
        b = bytes_data.find(b'\xff\xd9')  # JPEG end
        if a != -1 and b != -1:
            jpg = bytes_data[a:b + 2]
            bytes_data = bytes_data[b + 2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            return frame

if __name__ == "__main__":
    stream_url = "http://10.10.51.211:8000/stream.mjpg"

    while True:
        try:
            frame = fetch_frame(stream_url)
            if frame is not None:
                # Process the frame (e.g., apply OpenCV operations here)
                processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Display the processed frame
                cv2.imshow("Processed Frame", processed_frame)

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"Error fetching frame: {e}")
            break

    cv2.destroyAllWindows()
