"""
Hand tracking module using MediaPipe Hands solution.
Provides hand detection and landmark extraction from video frames.
"""

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    """Wrapper for MediaPipe Hands to detect and track hands in video frames."""
    
    def __init__(self, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Initialize the hand tracker.
        
        Args:
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.results = None
    
    def find_hands(self, frame):
        """
        Process a frame to detect hands.
        
        Args:
            frame: BGR image from OpenCV
            
        Returns:
            Processed frame with hand landmarks drawn
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        self.results = self.hands.process(rgb_frame)
        
        return frame
    
    def draw_landmarks(self, frame):
        """
        Draw hand landmarks on the frame.
        
        Args:
            frame: OpenCV frame to draw on
            
        Returns:
            Frame with landmarks drawn
        """
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return frame
    
    def get_hand_landmarks(self):
        """
        Get normalized hand landmarks.
        
        Returns:
            List of landmarks for the first detected hand, or None if no hand detected.
            Each landmark is a tuple (x, y, z) with normalized coordinates.
        """
        if not self.results or not self.results.multi_hand_landmarks:
            return None
        
        # Get first hand
        hand_landmarks = self.results.multi_hand_landmarks[0]
        
        # Convert to list of (x, y, z) tuples
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.append((landmark.x, landmark.y, landmark.z))
        
        return landmarks
    
    def get_hand_label(self):
        """
        Get the handedness label (Left or Right).
        
        Returns:
            String 'Left' or 'Right', or None if no hand detected
        """
        if not self.results or not self.results.multi_handedness:
            return None
        
        return self.results.multi_handedness[0].classification[0].label
    
    def close(self):
        """Release resources."""
        self.hands.close()
