"""
Calculator logic module for processing gestures and performing arithmetic operations.
"""


class Calculator:
    """Manages calculator state and operations."""
    
    def __init__(self):
        """Initialize calculator state."""
        self.current_number = ""
        self.operation = None
        self.operand1 = None
        self.result = None
        self.history = []
        self.error = None
    
    def process_gesture(self, gesture):
        """
        Process a recognized gesture and update calculator state.
        
        Args:
            gesture: Single character representing the gesture ('0'-'9', '+', '-', '*', '/', '=', 'C')
            
        Returns:
            Boolean indicating if state was updated
        """
        if gesture is None:
            return False
        
        self.error = None
        
        # Handle number input (only single digit allowed)
        if gesture.isdigit():
            # Only accept if we don't already have a number
            if not self.current_number:
                self.current_number = gesture
                return True
            else:
                # Already have a number, ignore
                return False
        
        # Handle clear
        if gesture == 'C':
            self.clear()
            return True
        
        # Handle operations
        if gesture in ['+', '-', '*', '/']:
            self._handle_operation(gesture)
            return True
        
        # Handle equals
        if gesture == '=':
            self._calculate_result()
            return True
        
        return False
    
    def _handle_operation(self, op):
        """Handle arithmetic operation input."""
        if self.current_number:
            # If we have a current number, store it
            if self.operand1 is None:
                self.operand1 = float(self.current_number)
                self.current_number = ""
                self.operation = op
            else:
                # Calculate intermediate result
                self._calculate_result()
                if self.error is None:
                    self.operation = op
        elif self.result is not None:
            # Use previous result as operand1
            self.operand1 = self.result
            self.result = None
            self.operation = op
    
    def _calculate_result(self):
        """Calculate the result of the current operation."""
        if self.operand1 is None or self.operation is None:
            return
        
        if not self.current_number:
            return
        
        operand2 = float(self.current_number)
        
        try:
            if self.operation == '+':
                self.result = self.operand1 + operand2
            elif self.operation == '-':
                self.result = self.operand1 - operand2
            elif self.operation == '*':
                self.result = self.operand1 * operand2
            elif self.operation == '/':
                if operand2 == 0:
                    self.error = "Division by zero"
                    self.clear()
                    return
                self.result = self.operand1 / operand2
            
            # Add to history
            expression = f"{self.operand1} {self.operation} {operand2} = {self.result}"
            self.history.append(expression)
            
            # Reset state
            self.operand1 = None
            self.operation = None
            self.current_number = ""
            
        except Exception as e:
            self.error = str(e)
            self.clear()
    
    def clear(self):
        """Clear all calculator state."""
        self.current_number = ""
        self.operation = None
        self.operand1 = None
        self.result = None
        self.error = None
    
    def get_display_text(self):
        """
        Get the text to display on the calculator screen.
        
        Returns:
            String representing current calculator state
        """
        if self.error:
            return f"Error: {self.error}"
        
        if self.result is not None:
            # Format result nicely
            if self.result == int(self.result):
                return str(int(self.result))
            return f"{self.result:.4f}".rstrip('0').rstrip('.')
        
        if self.current_number:
            return self.current_number
        
        if self.operand1 is not None and self.operation:
            op1_str = str(int(self.operand1)) if self.operand1 == int(self.operand1) else str(self.operand1)
            return f"{op1_str} {self.operation}"
        
        return "0"
    
    def get_history(self, max_items=5):
        """
        Get recent calculation history.
        
        Args:
            max_items: Maximum number of history items to return
            
        Returns:
            List of history strings (most recent first)
        """
        return list(reversed(self.history[-max_items:]))
