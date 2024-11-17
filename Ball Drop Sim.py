import tkinter as tk
import math
import threading
import time

class BallSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Ball Gravity Simulator")
        
        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        # Ball properties
        self.radius = 20
        self.x = 300
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0.5  # gravity acceleration

        # Ball shape (circle)
        self.ball = self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill="blue")
        
        # Mouse drag and collision detection
        self.dragging = False
        self.last_x = 0
        self.last_y = 0
        self.mouse_collision = False  # Flag to ensure only one bounce per contact

        # Flag to track if 'H' is pressed for motion prediction
        self.show_prediction = False
        self.prediction_line = None

        # Create text items for the speedometer and FPS
        self.speed_text = self.canvas.create_text(580, 20, anchor="ne", font=("Arial", 12), text="Speed: 0.0 px/s", fill="black")
        self.fps_text = self.canvas.create_text(580, 40, anchor="ne", font=("Arial", 12), text="FPS: 0", fill="black")

        # Update rate for speedometer (every 10th frame)
        self.speed_update_counter = 0

        # Track FPS
        self.frames = 0
        self.fps = 0
        self.fps_counter = time.time()

        # Event narration window
        self.narrator_window = tk.Toplevel(self.root)
        self.narrator_window.title("Event Narrator")
        self.narrator_text = tk.Text(self.narrator_window, width=50, height=15, wrap=tk.WORD, font=("Arial", 12))
        self.narrator_text.pack(padx=10, pady=10)
        self.narrator_text.insert(tk.END, "Event Narrator Started...\n")
        self.narrator_text.config(state=tk.DISABLED)

        # Thread control
        self.running = True
        self.physics_thread = threading.Thread(target=self.run_physics)
        self.physics_thread.start()

        # Update the GUI periodically
        self.root.after(20, self.update_gui)

        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_ball)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

        # Bind key events
        self.root.bind("<h>", self.toggle_prediction)  # Toggle prediction when 'H' is pressed
        self.root.bind("<KeyRelease-h>", self.toggle_prediction)  # Stop prediction when 'H' is released

    def start_drag(self, event):
        """Start dragging the ball when mouse is pressed."""
        self.dragging = True
        self.last_x = event.x
        self.last_y = event.y
        self.add_narrator_event("Dragging the ball...")

    def drag_ball(self, event):
        """Update the ball's position when dragging."""
        if self.dragging:
            # Calculate the velocity based on mouse movement
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.vx = dx * 0.1  # Adjust the multiplier for sensitivity
            self.vy = dy * 0.1  # Adjust the multiplier for sensitivity

            self.x += dx
            self.y += dy
            self.canvas.moveto(self.ball, self.x - self.radius, self.y - self.radius)
            self.last_x = event.x
            self.last_y = event.y

    def stop_drag(self, event):
        """Stop dragging the ball when mouse button is released."""
        self.dragging = False
        self.add_narrator_event(f"Ball released at position ({self.x:.2f}, {self.y:.2f}) with speed ({self.vx:.2f}, {self.vy:.2f})")

    def toggle_prediction(self, event):
        """Toggle the motion prediction when 'H' key is pressed or released."""
        self.show_prediction = not self.show_prediction

    def update_gui(self):
        """Update the GUI elements like the speedometer, predicted path, and FPS."""
        if self.show_prediction:
            self.show_predicted_path()

        # Update speedometer text
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        self.canvas.itemconfig(self.speed_text, text=f"Speed: {speed:.2f} px/s")

        # Update FPS every second
        current_time = time.time()
        self.frames += 1
        if current_time - self.fps_counter >= 1.0:
            self.fps = self.frames
            self.frames = 0
            self.fps_counter = current_time
            self.canvas.itemconfig(self.fps_text, text=f"FPS: {self.fps}")

        # Schedule the next GUI update
        self.root.after(20, self.update_gui)

    def run_physics(self):
        """This runs the physics updates in a separate thread."""
        while self.running:
            if not self.dragging:
                # Apply gravity to the vertical velocity
                self.vy += self.ay  # gravity effect
                self.vx *= 0.99  # small drag (friction) on horizontal velocity to simulate air resistance

                # Update position based on velocity
                self.x += self.vx
                self.y += self.vy

                # Collision with the ground (bounce)
                if self.y + self.radius >= 600:
                    self.y = 600 - self.radius  # place it on the ground
                    self.vy *= -0.8  # reverse velocity and apply damping factor for bounce
                    self.add_narrator_event(f"Ball bounced on the ground with speed ({self.vx:.2f}, {self.vy:.2f})")

                # Collision with the walls (bounce)
                if self.x - self.radius <= 0 or self.x + self.radius >= 600:
                    self.vx *= -0.9  # reverse velocity and apply damping factor for bounce
                    if self.x - self.radius <= 0:
                        self.x = self.radius
                    elif self.x + self.radius >= 600:
                        self.x = 600 - self.radius
                    self.add_narrator_event(f"Ball bounced off the wall with speed ({self.vx:.2f}, {self.vy:.2f})")

                # Mouse collision (bounce when ball touches mouse pointer)
                mouse_x, mouse_y = self.root.winfo_pointerx(), self.root.winfo_pointery()
                mouse_x -= self.root.winfo_rootx()
                mouse_y -= self.root.winfo_rooty()

                # Check if the ball is close to the mouse pointer
                distance = math.sqrt((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2)
                if distance <= self.radius:
                    if not self.mouse_collision:  # Ensure that the bounce happens only once
                        # Calculate the angle from the ball to the mouse
                        angle = math.atan2(self.y - mouse_y, self.x - mouse_x)
                        # Reflect the ball's velocity off the mouse position
                        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)  # current speed of the ball
                        self.vx = math.cos(angle) * speed * -1  # reverse direction along the angle
                        self.vy = math.sin(angle) * speed * -1

                        # Apply some repulsion force
                        self.vx *= 1.2  # amplify velocity after collision to make the bounce more pronounced
                        self.vy *= 1.2
                        
                        # Set the flag to prevent continuous bouncing
                        self.mouse_collision = True
                        self.add_narrator_event(f"Ball bounced off the mouse pointer with speed ({self.vx:.2f}, {self.vy:.2f})")

                # If the ball is far enough from the mouse, allow further interactions
                if distance > self.radius:
                    self.mouse_collision = False

                # Use the after method to update the ball position on the canvas (in main thread)
                self.root.after(0, self.update_ball_position)

            # Wait a small amount of time (simulating 50 FPS update rate)
            time.sleep(0.02)

    def update_ball_position(self):
        """Update the ball's position on the canvas."""
        self.canvas.moveto(self.ball, self.x - self.radius, self.y - self.radius)

    def add_narrator_event(self, event_message):
        """Add an event message to the narrator window."""
        self.narrator_text.config(state=tk.NORMAL)
        self.narrator_text.insert(tk.END, f"{event_message}\n")
        self.narrator_text.config(state=tk.DISABLED)
        self.narrator_text.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    ball_simulator = BallSimulator(root)
    root.mainloop()
