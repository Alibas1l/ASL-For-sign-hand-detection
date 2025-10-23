"""
Professional Sign Language Detection Application
Real-time hand sign detection and text conversion
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import queue
from datetime import datetime
import os

# Try to import TensorFlow and MediaPipe
try:
    import tensorflow as tf
    import mediapipe as mp
except ImportError:
    print("Warning: TensorFlow or MediaPipe not installed. Some features may not work.")
    tf = None
    mp = None


class SignLanguageDetector:
    """Main application class for sign language detection"""
    
    def __init__(self, root, model_path=None):
        self.root = root
        self.root.title("Sign Language Alphabet Recognition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2C3E50')
        
        # Application state
        self.is_running = False
        self.cap = None
        self.detected_text = ""
        self.last_prediction = ""
        self.prediction_stability = 0
        self.stability_threshold = 5  # Number of consistent frames needed
        
        # Model setup
        self.model = None
        self.model_path = model_path
        if model_path and os.path.exists(model_path):
            try:
                self.model = tf.keras.models.load_model(model_path)
                print(f"Model loaded from {model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
        
        # Hand detection setup
        if mp:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.mp_draw = mp.solutions.drawing_utils
        else:
            self.hands = None
        
        # Class labels for ASL alphabet
        self.class_labels = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'Delete', 'Space'
        ]
        
        # Create UI
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Camera feed
        left_panel = tk.Frame(main_frame, bg='#34495E', relief=tk.RAISED, borderwidth=2)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Camera feed label
        camera_label = tk.Label(left_panel, text="Camera Feed", 
                               font=('Arial', 14, 'bold'), 
                               bg='#34495E', fg='white')
        camera_label.pack(pady=10)
        
        # Video display
        self.video_label = tk.Label(left_panel, bg='black')
        self.video_label.pack(padx=10, pady=10)
        
        # Prediction display
        pred_frame = tk.Frame(left_panel, bg='#34495E')
        pred_frame.pack(pady=10, fill=tk.X, padx=10)
        
        tk.Label(pred_frame, text="Current Detection:", 
                font=('Arial', 12, 'bold'), 
                bg='#34495E', fg='white').pack()
        
        self.prediction_label = tk.Label(pred_frame, text="-", 
                                        font=('Arial', 48, 'bold'), 
                                        bg='#1ABC9C', fg='white',
                                        relief=tk.RAISED, borderwidth=3,
                                        width=5)
        self.prediction_label.pack(pady=5)
        
        # Confidence display
        self.confidence_label = tk.Label(pred_frame, text="Confidence: 0%", 
                                        font=('Arial', 10), 
                                        bg='#34495E', fg='#BDC3C7')
        self.confidence_label.pack()
        
        # Right panel - Controls and output
        right_panel = tk.Frame(main_frame, bg='#34495E', relief=tk.RAISED, borderwidth=2)
        right_panel.grid(row=0, column=1, sticky='nsew')
        
        # Alphabet reference
        ref_label = tk.Label(right_panel, text="ASL Alphabet Reference", 
                            font=('Arial', 14, 'bold'), 
                            bg='#34495E', fg='white')
        ref_label.pack(pady=10)
        
        # Alphabet grid
        self.create_alphabet_grid(right_panel)
        
        # Text output section
        output_label = tk.Label(right_panel, text="Detected Text", 
                               font=('Arial', 14, 'bold'), 
                               bg='#34495E', fg='white')
        output_label.pack(pady=(20, 5))
        
        # Text display
        text_frame = tk.Frame(right_panel, bg='#34495E')
        text_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        self.text_display = tk.Text(text_frame, 
                                   font=('Arial', 14), 
                                   height=6, 
                                   wrap=tk.WORD,
                                   bg='white', 
                                   relief=tk.SUNKEN,
                                   borderwidth=2)
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.text_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_display.config(yscrollcommand=scrollbar.set)
        
        # Control buttons
        button_frame = tk.Frame(right_panel, bg='#34495E')
        button_frame.pack(pady=20)
        
        # Start/Stop button
        self.start_button = tk.Button(button_frame, 
                                      text="Start Camera", 
                                      command=self.toggle_camera,
                                      font=('Arial', 12, 'bold'),
                                      bg='#27AE60', 
                                      fg='white',
                                      width=15,
                                      height=2,
                                      relief=tk.RAISED,
                                      cursor='hand2')
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Clear button
        clear_button = tk.Button(button_frame, 
                                text="Clear All", 
                                command=self.clear_text,
                                font=('Arial', 12, 'bold'),
                                bg='#F39C12', 
                                fg='white',
                                width=15,
                                height=2,
                                relief=tk.RAISED,
                                cursor='hand2')
        clear_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Save button
        save_button = tk.Button(button_frame, 
                               text="Save to Text File", 
                               command=self.save_to_file,
                               font=('Arial', 12, 'bold'),
                               bg='#3498DB', 
                               fg='white',
                               width=15,
                               height=2,
                               relief=tk.RAISED,
                               cursor='hand2')
        save_button.grid(row=1, column=0, padx=5, pady=5)
        
        # Quit button
        quit_button = tk.Button(button_frame, 
                               text="Quit", 
                               command=self.on_closing,
                               font=('Arial', 12, 'bold'),
                               bg='#E74C3C', 
                               fg='white',
                               width=15,
                               height=2,
                               relief=tk.RAISED,
                               cursor='hand2')
        quit_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#1ABC9C', relief=tk.SUNKEN, borderwidth=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(status_frame, 
                                     text="Ready - Click 'Start Camera' to begin", 
                                     font=('Arial', 10),
                                     bg='#1ABC9C', 
                                     fg='white',
                                     anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
    
    def create_alphabet_grid(self, parent):
        """Create a grid showing ASL alphabet"""
        grid_frame = tk.Frame(parent, bg='white', relief=tk.SUNKEN, borderwidth=2)
        grid_frame.pack(pady=5, padx=10, fill=tk.BOTH)
        
        # Create grid of alphabet labels
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                  'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S',
                  'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                  'Del', 'Space']
        
        row = 0
        col = 0
        for letter in letters:
            label = tk.Label(grid_frame, 
                           text=letter, 
                           font=('Arial', 10, 'bold'),
                           bg='#ECF0F1',
                           fg='#2C3E50',
                           relief=tk.RAISED,
                           borderwidth=1,
                           width=6,
                           height=2)
            label.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(7):
            grid_frame.grid_columnconfigure(i, weight=1)
    
    def toggle_camera(self):
        """Start or stop the camera"""
        if not self.is_running:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start camera capture"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera")
                return
            
            self.is_running = True
            self.start_button.config(text="Stop Camera", bg='#E74C3C')
            self.status_label.config(text="Camera running - Show hand signs to detect")
            
            # Start video processing thread
            self.video_thread = threading.Thread(target=self.process_video, daemon=True)
            self.video_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def stop_camera(self):
        """Stop camera capture"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.start_button.config(text="Start Camera", bg='#27AE60')
        self.status_label.config(text="Camera stopped")
        self.video_label.config(image='')
    
    def process_video(self):
        """Process video frames"""
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror view
            frame = cv2.flip(frame, 1)
            
            # Process frame
            processed_frame, prediction, confidence = self.process_frame(frame)
            
            # Update prediction with stability check
            if prediction:
                if prediction == self.last_prediction:
                    self.prediction_stability += 1
                else:
                    self.prediction_stability = 0
                    self.last_prediction = prediction
                
                # Add to text if stable
                if self.prediction_stability >= self.stability_threshold:
                    self.add_prediction_to_text(prediction)
                    self.prediction_stability = 0
                
                # Update UI
                self.root.after(0, self.update_prediction_display, prediction, confidence)
            
            # Convert frame for display
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_pil = frame_pil.resize((640, 480), Image.Resampling.LANCZOS)
            frame_tk = ImageTk.PhotoImage(frame_pil)
            
            # Update display
            self.root.after(0, self.update_video_display, frame_tk)
    
    def process_frame(self, frame):
        """Process a single frame for hand detection and classification"""
        h, w, _ = frame.shape
        prediction = None
        confidence = 0.0
        
        # Detect hands using MediaPipe
        if self.hands:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
                    
                    # Get bounding box
                    x_coords = [lm.x for lm in hand_landmarks.landmark]
                    y_coords = [lm.y for lm in hand_landmarks.landmark]
                    
                    x_min, x_max = int(min(x_coords) * w), int(max(x_coords) * w)
                    y_min, y_max = int(min(y_coords) * h), int(max(y_coords) * h)
                    
                    # Add padding
                    padding = 30
                    x_min = max(0, x_min - padding)
                    y_min = max(0, y_min - padding)
                    x_max = min(w, x_max + padding)
                    y_max = min(h, y_max + padding)
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 165, 0), 2)
                    
                    # Extract hand region
                    hand_img = frame[y_min:y_max, x_min:x_max]
                    
                    # Classify if model is available
                    if self.model and hand_img.size > 0:
                        prediction, confidence = self.classify_hand(hand_img)
        
        # Add instructions on frame
        cv2.putText(frame, "Show hand sign to camera", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame, prediction, confidence
    
    def classify_hand(self, hand_img):
        """Classify the hand sign using the model"""
        try:
            # Resize image to model input size (adjust based on your model)
            img_size = 64  # Adjust this based on your model
            hand_img_resized = cv2.resize(hand_img, (img_size, img_size))
            hand_img_rgb = cv2.cvtColor(hand_img_resized, cv2.COLOR_BGR2RGB)
            
            # Normalize
            hand_img_normalized = hand_img_rgb / 255.0
            
            # Add batch dimension
            hand_img_batch = np.expand_dims(hand_img_normalized, axis=0)
            
            # Predict
            predictions = self.model.predict(hand_img_batch, verbose=0)
            class_idx = np.argmax(predictions[0])
            confidence = predictions[0][class_idx]
            
            # Get class label (adjust based on your model's classes)
            if class_idx < len(self.class_labels):
                prediction = self.class_labels[class_idx]
            else:
                prediction = chr(65 + class_idx) if class_idx < 26 else 'Unknown'
            
            return prediction, confidence
        except Exception as e:
            print(f"Classification error: {e}")
            return None, 0.0
    
    def update_video_display(self, frame_tk):
        """Update video display in GUI"""
        self.video_label.config(image=frame_tk)
        self.video_label.image = frame_tk
    
    def update_prediction_display(self, prediction, confidence):
        """Update prediction display"""
        self.prediction_label.config(text=prediction)
        self.confidence_label.config(text=f"Confidence: {confidence*100:.1f}%")
    
    def add_prediction_to_text(self, prediction):
        """Add prediction to text display"""
        if prediction == "Space":
            self.text_display.insert(tk.END, " ")
        elif prediction == "Delete" or prediction == "Del":
            current_text = self.text_display.get("1.0", tk.END)
            if len(current_text) > 1:
                self.text_display.delete("end-2c", "end-1c")
        else:
            self.text_display.insert(tk.END, prediction)
        
        self.text_display.see(tk.END)
    
    def clear_text(self):
        """Clear all detected text"""
        self.text_display.delete("1.0", tk.END)
        self.status_label.config(text="Text cleared")
    
    def save_to_file(self):
        """Save detected text to a file"""
        text = self.text_display.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sign_language_output_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(text)
            messagebox.showinfo("Success", f"Text saved to {filename}")
            self.status_label.config(text=f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            self.stop_camera()
        if self.hands:
            self.hands.close()
        self.root.destroy()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Optional: Specify path to your trained model
    model_path = None  # Set to your model path, e.g., "model.h5" or "model.keras"
    
    # Check if model file exists in workspace
    possible_models = ['model.h5', 'model.keras', 'asl_model.h5', 'sign_language_model.h5']
    for model_file in possible_models:
        if os.path.exists(model_file):
            model_path = model_file
            break
    
    app = SignLanguageDetector(root, model_path=model_path)
    root.mainloop()


if __name__ == "__main__":
    main()
