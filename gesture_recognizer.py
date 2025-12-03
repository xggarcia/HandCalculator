"""
Gesture recognition module that analyzes hand landmarks to identify gestures.
Recognizes finger counting (0-9) and specific hand poses for calculator operations.
"""

import time
import math


class GestureRecognizer:
    """Recognizes gestures from hand landmarks."""
    
    def __init__(self, hold_time=3.0):
        """
        Initialize the gesture recognizer.
        
        Args:
            hold_time: Time (in seconds) a gesture must be held before it's confirmed
        """
        self.hold_time = hold_time
        self.current_gesture = None
        self.gesture_start_time = None
        self.last_confirmed_gesture = None
        self.last_confirmed_time = 0
        self.cooldown_time = 1.0  # Time after confirmation before detecting new gesture
    
    def recognize_gesture(self, landmarks):
        """
        Recognize a gesture from hand landmarks. Requires holding gesture for 3 seconds.
        
        Args:
            landmarks: List of (x, y, z) tuples for 21 hand landmarks
            
        Returns:
            Tuple (gesture, hold_progress, is_confirmed) where:
            - gesture: The detected gesture ('0'-'9', '+', '-', '*', '/', '=', 'C') or None
            - hold_progress: Progress from 0.0 to 1.0 of how long gesture has been held
            - is_confirmed: True if gesture has been held for required time
        """
        if landmarks is None or len(landmarks) != 21:
            # No hand detected, reset tracking
            self.current_gesture = None
            self.gesture_start_time = None
            return None, 0.0, False
        
        current_time = time.time()
        
        # Check if we're in cooldown period after last confirmed gesture
        if current_time - self.last_confirmed_time < self.cooldown_time:
            return None, 0.0, False
        
        # Get finger states
        fingers_up = self._count_fingers_up(landmarks)
        
        # Recognize gestures based on finger patterns
        detected_gesture = None
        
        # Numbers 0-5 using one hand
        if fingers_up == 0:
            detected_gesture = '0'
        elif fingers_up == 1:
            # Distinguish between 1 and / (division)
            if self._is_pointing_up(landmarks):
                detected_gesture = '/'
            else:
                detected_gesture = '1'
        elif fingers_up == 2:
            # Distinguish between 2 and * (multiplication - peace sign)
            if self._is_peace_sign(landmarks):
                detected_gesture = '*'
            else:
                detected_gesture = '2'
        elif fingers_up == 3:
            detected_gesture = '3'
        elif fingers_up == 4:
            detected_gesture = '4'
        elif fingers_up == 5:
            # Distinguish between 5 and = (equals - flat palm)
            if self._is_flat_palm(landmarks):
                detected_gesture = '='
            else:
                detected_gesture = '5'
        
        # Check for thumbs up (+) or thumbs down (-)
        if self._is_thumbs_up(landmarks):
            detected_gesture = '+'
        elif self._is_thumbs_down(landmarks):
            detected_gesture = '-'
        
        # Track gesture hold time
        if detected_gesture:
            if self.current_gesture == detected_gesture:
                # Same gesture being held, calculate progress
                hold_duration = current_time - self.gesture_start_time
                hold_progress = min(hold_duration / self.hold_time, 1.0)
                
                # Check if held long enough
                if hold_duration >= self.hold_time:
                    # Gesture confirmed!
                    self.last_confirmed_gesture = detected_gesture
                    self.last_confirmed_time = current_time
                    self.current_gesture = None
                    self.gesture_start_time = None
                    return detected_gesture, 1.0, True
                else:
                    # Still holding, not confirmed yet
                    return detected_gesture, hold_progress, False
            else:
                # New gesture detected, start tracking
                self.current_gesture = detected_gesture
                self.gesture_start_time = current_time
                return detected_gesture, 0.0, False
        else:
            # No gesture detected, reset
            self.current_gesture = None
            self.gesture_start_time = None
            return None, 0.0, False
    
    def _count_fingers_up(self, landmarks):
        """
        Count how many fingers are extended.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Number of fingers up (0-5)
        """
        fingers_up = 0
        
        # Thumb - check if tip is to the right/left of IP joint
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        
        # Calculate if thumb is extended (horizontal distance)
        if abs(thumb_tip[0] - thumb_ip[0]) > abs(thumb_ip[0] - thumb_mcp[0]):
            fingers_up += 1
        
        # Other fingers - check if tip is above PIP joint
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        finger_pips = [6, 10, 14, 18]
        
        for tip_id, pip_id in zip(finger_tips, finger_pips):
            if landmarks[tip_id][1] < landmarks[pip_id][1]:  # y-axis is inverted
                fingers_up += 1
        
        return fingers_up
    
    def _is_thumbs_up(self, landmarks):
        """Check if hand is making thumbs up gesture."""
        fingers_up = self._count_fingers_up(landmarks)
        
        # Only thumb should be up
        if fingers_up != 1:
            return False
        
        # Thumb should be up
        thumb_tip = landmarks[4]
        thumb_mcp = landmarks[2]
        
        # Other fingers should be down
        index_tip = landmarks[8]
        index_mcp = landmarks[5]
        
        return (thumb_tip[1] < thumb_mcp[1] and  # Thumb up
                index_tip[1] > index_mcp[1])      # Index down
    
    def _is_thumbs_down(self, landmarks):
        """Check if hand is making thumbs down gesture."""
        fingers_up = self._count_fingers_up(landmarks)
        
        # Only thumb should be "up" (but pointing down)
        if fingers_up != 1:
            return False
        
        # Thumb should be down
        thumb_tip = landmarks[4]
        thumb_mcp = landmarks[2]
        
        # Other fingers should be curled
        index_tip = landmarks[8]
        index_mcp = landmarks[5]
        
        return (thumb_tip[1] > thumb_mcp[1] and  # Thumb down
                index_tip[1] > index_mcp[1])      # Index down
    
    def _is_peace_sign(self, landmarks):
        """Check if hand is making peace sign (V shape with index and middle)."""
        # Index and middle fingers should be up and apart
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        
        index_pip = landmarks[6]
        middle_pip = landmarks[10]
        ring_pip = landmarks[14]
        
        # Index and middle up, ring down
        index_up = index_tip[1] < index_pip[1]
        middle_up = middle_tip[1] < middle_pip[1]
        ring_down = ring_tip[1] > ring_pip[1]
        
        # Check if fingers are spread apart
        distance = math.sqrt((index_tip[0] - middle_tip[0])**2 + 
                           (index_tip[1] - middle_tip[1])**2)
        
        return index_up and middle_up and ring_down and distance > 0.05
    
    def _is_pointing_up(self, landmarks):
        """Check if index finger is pointing straight up."""
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        
        # Only index should be up, middle should be down
        index_up = index_tip[1] < index_pip[1]
        middle_down = middle_tip[1] > middle_pip[1]
        
        # Check vertical alignment
        horizontal_diff = abs(index_tip[0] - index_pip[0])
        vertical_diff = abs(index_tip[1] - index_pip[1])
        
        return index_up and middle_down and horizontal_diff < vertical_diff * 0.5
    
    def _is_flat_palm(self, landmarks):
        """Check if hand is showing a flat open palm."""
        # All fingers should be extended
        fingers_up = self._count_fingers_up(landmarks)
        if fingers_up != 5:
            return False
        
        # Check if fingers are relatively close together (not spread)
        index_tip = landmarks[8]
        pinky_tip = landmarks[20]
        
        # Distance between index and pinky should be moderate
        distance = abs(index_tip[0] - pinky_tip[0])
        
        # Palm should be relatively flat (check z-coordinates)
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        
        z_diff = abs(wrist[2] - middle_mcp[2])
        
        return distance < 0.25 and z_diff < 0.1
