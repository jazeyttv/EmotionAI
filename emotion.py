import cv2
from deepface import DeepFace

def analyze_emotion(frame):
    """Analyze the dominant emotion in a frame using DeepFace."""
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return analysis[0]['dominant_emotion']
    except:
        return "neutral"

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access webcam. Make sure it is connected and not used by another app.")
        return

    print("Starting Emotion-Based Coding Assistant...")
    print("Press 'Q' to quit.")

    last_emotion = "neutral"
    last_suggestion = "Keep going, you're doing great 👍"
    frame_count = 0
    update_interval = 20  # Update emotion every 20 frames (~2 seconds)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Only analyze emotion every few frames
        if frame_count % update_interval == 0:
            emotion = analyze_emotion(frame)
            last_emotion = emotion

            # Suggestions based on emotion
            if emotion in ["angry", "sad", "fear"]:
                last_suggestion = "You look stressed! Take a short break ☕"
            elif emotion == "happy":
                last_suggestion = "You're crushing it! Next challenge unlocked 🚀"
            else:
                last_suggestion = "Keep going, you're doing great 👍"

        # Display last known emotion and suggestion
        cv2.putText(frame, f"Emotion: {last_emotion}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, last_suggestion, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Emotion Assistant", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
