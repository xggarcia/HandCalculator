"""
UI rendering module for displaying the calculator interface.
"""

import cv2
import numpy as np


class UIRenderer:
    """Renders the calculator UI on video frames."""
    
    def __init__(self, frame_width=640, frame_height=480):
        """
        Initialize UI renderer.
        
        Args:
            frame_width: Width of video frame
            frame_height: Height of video frame
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # UI colors (BGR format)
        self.bg_color = (40, 40, 40)
        self.text_color = (255, 255, 255)
        self.display_bg = (60, 60, 60)
        self.gesture_color = (100, 255, 100)
        self.error_color = (0, 0, 255)
        self.accent_color = (255, 165, 0)
    
    def render_ui(self, frame, calculator, current_gesture=None, hold_progress=0.0):
        """
        Render the calculator UI on the frame.
        
        Args:
            frame: OpenCV frame to draw on
            calculator: Calculator instance
            current_gesture: Currently recognized gesture
            hold_progress: Progress of holding gesture (0.0 to 1.0)
            
        Returns:
            Frame with UI rendered
        """
        h, w = frame.shape[:2]
        
        # Create overlay for calculator display
        overlay = frame.copy()
        
        # Draw calculator display area (top-right)
        display_x = w - 300
        display_y = 20
        display_w = 280
        display_h = 150
        
        cv2.rectangle(overlay, 
                     (display_x, display_y), 
                     (display_x + display_w, display_y + display_h),
                     self.display_bg, -1)
        cv2.rectangle(overlay, 
                     (display_x, display_y), 
                     (display_x + display_w, display_y + display_h),
                     self.accent_color, 2)
        
        # Display calculator text
        display_text = calculator.get_display_text()
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Adjust font size based on text length
        font_scale = 1.5 if len(display_text) < 10 else 1.0
        
        # Get text size for centering
        text_size = cv2.getTextSize(display_text, font, font_scale, 2)[0]
        text_x = display_x + (display_w - text_size[0]) // 2
        text_y = display_y + display_h - 40
        
        # Display text
        text_color = self.error_color if "Error" in display_text else self.text_color
        cv2.putText(overlay, display_text, (text_x, text_y),
                   font, font_scale, text_color, 2, cv2.LINE_AA)
        
        # Display label
        cv2.putText(overlay, "CALCULATOR", (display_x + 10, display_y + 25),
                   font, 0.6, self.accent_color, 1, cv2.LINE_AA)
        
        # Draw current gesture indicator with progress bar (top-left)
        if current_gesture and hold_progress > 0.0:
            gesture_x = 20
            gesture_y = 20
            gesture_w = 200
            gesture_h = 100
            
            cv2.rectangle(overlay, 
                         (gesture_x, gesture_y), 
                         (gesture_x + gesture_w, gesture_y + gesture_h),
                         self.display_bg, -1)
            cv2.rectangle(overlay, 
                         (gesture_x, gesture_y), 
                         (gesture_x + gesture_w, gesture_y + gesture_h),
                         self.gesture_color, 2)
            
            # Display gesture
            cv2.putText(overlay, "HOLD GESTURE", (gesture_x + 10, gesture_y + 25),
                       font, 0.5, self.gesture_color, 1, cv2.LINE_AA)
            cv2.putText(overlay, current_gesture, (gesture_x + 80, gesture_y + 55),
                       font, 1.5, self.gesture_color, 2, cv2.LINE_AA)
            
            # Draw progress bar
            progress_x = gesture_x + 10
            progress_y = gesture_y + 70
            progress_w = gesture_w - 20
            progress_h = 15
            
            # Background bar
            cv2.rectangle(overlay,
                         (progress_x, progress_y),
                         (progress_x + progress_w, progress_y + progress_h),
                         (50, 50, 50), -1)
            
            # Progress fill
            fill_w = int(progress_w * hold_progress)
            if fill_w > 0:
                # Color changes from yellow to green as it fills
                progress_color = (0, int(255 * hold_progress), int(255 * (1 - hold_progress)))
                cv2.rectangle(overlay,
                             (progress_x, progress_y),
                             (progress_x + fill_w, progress_y + progress_h),
                             progress_color, -1)
        
        # Draw history (bottom-right)
        history = calculator.get_history(3)
        if history:
            history_x = w - 400
            history_y = h - 150
            
            cv2.putText(overlay, "HISTORY:", (history_x, history_y),
                       font, 0.5, self.text_color, 1, cv2.LINE_AA)
            
            for i, entry in enumerate(history):
                y_pos = history_y + 30 + (i * 25)
                cv2.putText(overlay, entry, (history_x, y_pos),
                           font, 0.4, self.text_color, 1, cv2.LINE_AA)
        
        # Blend overlay with frame
        cv2.addWeighted(overlay, 0.9, frame, 0.1, 0, frame)
        
        return frame
    
    def render_instructions(self, frame):
        """
        Render gesture instructions on the frame.
        
        Args:
            frame: OpenCV frame to draw on
            
        Returns:
            Frame with instructions rendered
        """
        h, w = frame.shape[:2]
        
        instructions = [
            "GESTURE CONTROLS:",
            "Hold gesture for 3 seconds!",
            "",
            "0-5: Show fingers",
            "+: Thumbs up",
            "-: Thumbs down",
            "*: Peace sign",
            "/: Point up",
            "=: Open palm",
            "",
            "Press 'q' to quit"
        ]
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        y_start = h - 250
        
        for i, text in enumerate(instructions):
            y_pos = y_start + (i * 20)
            cv2.putText(frame, text, (20, y_pos),
                       font, font_scale, self.text_color, 1, cv2.LINE_AA)
        
        return frame
    
    def render_title(self, frame):
        """
        Render title bar.
        
        Args:
            frame: OpenCV frame to draw on
            
        Returns:
            Frame with title rendered
        """
        h, w = frame.shape[:2]
        
        # Draw title background
        cv2.rectangle(frame, (0, 0), (w, 50), self.bg_color, -1)
        
        # Draw title text
        font = cv2.FONT_HERSHEY_SIMPLEX
        title = "Hand Gesture Calculator"
        cv2.putText(frame, title, (w//2 - 200, 35),
                   font, 1.0, self.accent_color, 2, cv2.LINE_AA)
        
        return frame
