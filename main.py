"""
Hand Gesture Calculator - Main Application
Control a calculator using hand gestures detected via webcam.
"""

import cv2
import sys
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from calculator import Calculator
from ui_renderer import UIRenderer


def main():
    """Main application loop."""
    print("Hand Gesture Calculator")
    print("=" * 50)
    print("Initializing camera and hand tracking...")
    
    # Initialize components
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Initialize modules
    hand_tracker = HandTracker(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    gesture_recognizer = GestureRecognizer(hold_time=3.0)
    calculator = Calculator()
    ui_renderer = UIRenderer(frame_width=640, frame_height=480)
    
    print("Camera initialized successfully!")
    print("\nGesture Controls:")
    print("  0-5: Show corresponding number of fingers")
    print("  +: Thumbs up")
    print("  -: Thumbs down")
    print("  *: Peace sign (V with index and middle fingers)")
    print("  /: Point index finger up")
    print("  =: Open palm flat")
    print("  C: Closed fist (hold for 1 second)")
    print("\nPress 'q' to quit")
    print("=" * 50)
    
    # Main loop
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to read frame")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect hands
        frame = hand_tracker.find_hands(frame)
        landmarks = hand_tracker.get_hand_landmarks()
        
        # Draw hand landmarks
        frame = hand_tracker.draw_landmarks(frame)
        
        # Recognize gesture
        current_gesture = None
        hold_progress = 0.0
        
        if landmarks:
            current_gesture, hold_progress, is_confirmed = gesture_recognizer.recognize_gesture(landmarks)
            
            # Process gesture with calculator only if confirmed (held for 3 seconds)
            if is_confirmed:
                if calculator.process_gesture(current_gesture):
                    print(f"Gesture confirmed: {current_gesture} -> {calculator.get_display_text()}")
        
        # Render UI (pass hold progress for visual feedback)
        frame = ui_renderer.render_ui(frame, calculator, current_gesture, hold_progress)
        frame = ui_renderer.render_instructions(frame)
        
        # Display frame
        cv2.imshow('Hand Gesture Calculator', frame)
        
        # Check for quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 'q' or ESC
            break
    
    # Cleanup
    print("\nShutting down...")
    hand_tracker.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        cv2.destroyAllWindows()
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        cv2.destroyAllWindows()
        sys.exit(1)
