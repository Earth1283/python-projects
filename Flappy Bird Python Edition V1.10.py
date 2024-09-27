# THIS PROJECT IS ABANDONED! FOR A BETTER VERSION, SEE FLAPPY BIRD V2!

# The following script is licensed under the MIT license.
# Flappy Bird Python © 2024 by Earth1283 is licensed under CC BY-NC-SA 4.0.
# This game has been known to be highly addictive, so please play this under your own discreetion
# Game recommended for 0+
# Requirements for playing:
# Hands. Reason: Spacebar
# Eyes. Reasons: Observation

# +===========================+
# +PUBLIC DISTRIBUTION EDITION+
# +===========================+
# PDE Ver 1.11

# Release 1.11 - Enhanced the hitbox warning system
# Release 1.10 - The update which I finally fixed crashes

# Controls:
# [Space] Jump or restart the game
# [G] Show guidance (you still have to mannually play it)
# [H] Show hitboxes, the hitbox of the player gets thicker when it is closer to the pipes
# Info:
# Avoid the green pipes, and jump to avoid them
# The blue dot makes you invincible for 5 seconds (there will be a countdown)
# If you are inside a pipe when the invincibility ends, you will die (lol)

# Code :)

import tkinter as tk
import random

class FlappyBird:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird Python Edition - V1.10")
        
        # Canvas
        self.canvas = tk.Canvas(root, width=400, height=600, bg='sky blue')
        self.canvas.pack()

        # Bird
        self.bird = self.canvas.create_rectangle(50, 250, 70, 270, fill='yellow')

        # Variables
        self.gravity = 0.75
        self.bird_velocity = 0
        self.game_active = True
        self.score = 0
        self.high_score = 0
        self.hitbox_visible = False  # Hitbox indicator flag
        self.optimal_path_visible = False  # Optimal path indicator flag

        # Invincibility buff
        self.invincible = False
        self.invincibility_duration = 5000  # 5 seconds in milliseconds
        self.invincibility_end_time = 0
        self.invincibility_countdown = None
        self.invincibility_glow = None

        # Invincibility item
        self.invincibility_item = None
        self.invincibility_item_exists = False
        self.pipes_passed_since_last_item = 0

        # Difficulty settings
        self.pipe_gap = 200
        self.min_pipe_gap = 120
        self.pipe_gap_decrement = 2

        # Score display
        self.score_text = self.canvas.create_text(200, 50, text=f'Score: {self.score}', font=('Arial', 24), fill='white')
        self.high_score_text = self.canvas.create_text(200, 100, text=f'High Score: {self.high_score}', font=('Arial', 24), fill='white')

        # Pipes
        self.pipes = []
        self.pipe_speed = 5
        self.create_pipes()
        self.pipe_passed = False

        # Key Bindings
        self.root.bind('<space>', self.flap)
        self.root.bind('h', self.toggle_hitbox)  # Toggle hitbox visibility
        self.root.bind('g', self.toggle_optimal_path)  # Toggle optimal path visibility

        # Game Loop
        self.update_game()

    def flap(self, event):
        if self.game_active:
            self.bird_velocity = -10
        else:
            self.restart_game()

    def toggle_hitbox(self, event):
        self.hitbox_visible = not self.hitbox_visible
        if not self.hitbox_visible:
            self.canvas.delete("hitbox")

    def toggle_optimal_path(self, event):
        self.optimal_path_visible = not self.optimal_path_visible
        if not self.optimal_path_visible:
            self.canvas.delete("optimal_path")
            self.canvas.delete("predicted_path")

    def activate_invincibility(self):
        if self.invincibility_end_time:
            self.canvas.after_cancel(self.invincibility_end_time)
        self.invincible = True
        self.invincibility_end_time = self.canvas.after(self.invincibility_duration, self.deactivate_invincibility)
        if not self.invincibility_countdown:
            self.invincibility_countdown = self.canvas.create_text(200, 300, text=f'Invincibility: 5', font=('Arial', 24), fill='blue')
        self.update_invincibility_countdown(5)
        if not self.invincibility_glow:
            self.invincibility_glow = self.canvas.create_oval(self.canvas.coords(self.bird)[0] - 5,
                                                              self.canvas.coords(self.bird)[1] - 5,
                                                              self.canvas.coords(self.bird)[2] + 5,
                                                              self.canvas.coords(self.bird)[3] + 5,
                                                              outline='blue', width=3)

    def update_invincibility_countdown(self, time_left):
        if time_left > 0 and self.invincible:
            if self.canvas.winfo_exists():
                self.canvas.itemconfig(self.invincibility_countdown, text=f'Invincibility: {time_left}')
                self.canvas.after(1000, self.update_invincibility_countdown, time_left - 1)
        else:
            if self.canvas.winfo_exists():
                self.canvas.delete(self.invincibility_countdown)
            self.invincibility_countdown = None

    def deactivate_invincibility(self):
        self.invincible = False
        if self.canvas.winfo_exists():
            self.canvas.delete(self.invincibility_countdown)
            self.canvas.delete(self.invincibility_glow)
        self.invincibility_countdown = None
        self.invincibility_glow = None
        self.invincibility_end_time = None

    def create_pipes(self):
        for i in range(2):
            pipe_x = 400 + i * 200
            self.pipes.append(self.create_pipe(pipe_x))

    def create_pipe(self, pipe_x):
        pipe_height = random.randint(150, 450)
        top_pipe = self.canvas.create_rectangle(pipe_x, 0, pipe_x + 50, pipe_height, fill='green')
        bottom_pipe = self.canvas.create_rectangle(pipe_x, pipe_height + self.pipe_gap, pipe_x + 50, 600, fill='green')
        return top_pipe, bottom_pipe

    def move_pipes(self):
        for pipe_pair in self.pipes:
            for pipe in pipe_pair:
                self.canvas.move(pipe, -self.pipe_speed, 0)

        if self.canvas.coords(self.pipes[0][0])[2] < 0:
            for pipe in self.pipes.pop(0):
                self.canvas.delete(pipe)
            self.pipes.append(self.create_pipe(400))
            self.pipes_passed_since_last_item += 1

    def move_invincibility_item(self):
        if self.invincibility_item_exists:
            self.canvas.move(self.invincibility_item, -self.pipe_speed, 0)
            if self.canvas.coords(self.invincibility_item)[2] < 0:
                self.canvas.delete(self.invincibility_item)
                self.invincibility_item_exists = False

    def check_collision(self):
        bird_coords = self.canvas.coords(self.bird)
        if bird_coords[1] < 0 or bird_coords[3] > 600:
            self.game_active = False
            return

        if not self.invincible:
            for pipe_pair in self.pipes:
                for pipe in pipe_pair:
                    if self.canvas.bbox(pipe) and self.canvas.bbox(self.bird):
                        if self.check_overlap(self.canvas.bbox(pipe), self.canvas.bbox(self.bird)):
                            self.game_active = False
                            return

        # Check collision with invincibility item
        if self.invincibility_item_exists and self.canvas.bbox(self.invincibility_item) and self.canvas.bbox(self.bird):
            if self.check_overlap(self.canvas.bbox(self.invincibility_item), self.canvas.bbox(self.bird)):
                self.activate_invincibility()
                self.canvas.delete(self.invincibility_item)
                self.invincibility_item_exists = False

    def check_overlap(self, box1, box2):
        if (box1 is None) or (box2 is None):
            return False
        return (box1[0] < box2[2] and box1[2] > box2[0] and box1[1] < box2[3] and box1[3] > box2[1])

    def update_game(self):
        if self.game_active:
            self.bird_velocity += self.gravity
            self.canvas.move(self.bird, 0, self.bird_velocity)
            self.move_pipes()
            self.move_invincibility_item()
            self.check_collision()
            self.update_score()

            # Update invincibility glow position
            if self.invincible and self.invincibility_glow:
                bird_coords = self.canvas.coords(self.bird)
                self.canvas.coords(self.invincibility_glow, bird_coords[0] - 5, bird_coords[1] - 5, bird_coords[2] + 5, bird_coords[3] + 5)

            # Draw hitboxes if enabled
            if self.hitbox_visible:
                self.draw_hitboxes()

            # Draw optimal path and predicted path if enabled
            if self.optimal_path_visible:
                self.draw_optimal_path()
                self.draw_predicted_path()

            # Possibly spawn an invincibility item
            self.spawn_invincibility_item()

        self.root.after(30, self.update_game)

    def update_score(self):
        bird_coords = self.canvas.coords(self.bird)
        for pipe_pair in self.pipes:
            pipe_coords = self.canvas.coords(pipe_pair[0])
            if not self.pipe_passed and pipe_coords[0] < bird_coords[0] and pipe_coords[2] < bird_coords[2]:
                self.score += 1
                self.pipe_passed = True
                self.canvas.itemconfig(self.score_text, text=f'Score: {self.score}')
                self.increase_difficulty()
            if pipe_coords[2] < bird_coords[0]:
                self.pipe_passed = False

    def increase_difficulty(self):
        if self.pipe_gap > self.min_pipe_gap:
            self.pipe_gap -= self.pipe_gap_decrement

    def draw_hitboxes(self):
        # Remove existing hitboxes
        self.canvas.delete("hitbox")
        
        # Draw bird hitbox
        bird_coords = self.canvas.coords(self.bird)
        thick = self.is_near_pipe(bird_coords)
        self.canvas.create_rectangle(*bird_coords, outline='red', width=thick, tag="hitbox")
        
        # Draw pipes hitboxes
        for pipe_pair in self.pipes:
            for pipe in pipe_pair:
                pipe_coords = self.canvas.coords(pipe)
                self.canvas.create_rectangle(*pipe_coords, outline='red', tag="hitbox")

    def draw_optimal_path(self):
        # Remove existing optimal path
        self.canvas.delete("optimal_path")

        # Draw new optimal path
        bird_coords = self.canvas.coords(self.bird)
        bird_center_x = (bird_coords[0] + bird_coords[2]) / 2
        bird_center_y = (bird_coords[1] + bird_coords[3]) / 2

        path_points = [(bird_center_x, bird_center_y)]
        
        for pipe_pair in self.pipes:
            pipe_coords = self.canvas.coords(pipe_pair[0])
            pipe_center_x = (pipe_coords[0] + pipe_coords[2]) / 2
            pipe_top = pipe_coords[3]
            pipe_bottom = self.canvas.coords(pipe_pair[1])[1]
            optimal_y = (pipe_top + pipe_bottom) / 2
            path_points.append((pipe_center_x, optimal_y))
        
        for i in range(len(path_points) - 1):
            self.draw_curve(path_points[i], path_points[i + 1])

    def draw_curve(self, point1, point2):
        steps = 20
        x1, y1 = point1
        x2, y2 = point2
        for i in range(steps):
            t = i / steps
            xt = (1 - t) * x1 + t * x2
            yt = (1 - t) * y1 + t * y2
            self.canvas.create_oval(xt, yt, xt + 1, yt + 1, fill='orange', outline='orange', tag="optimal_path")

    def draw_predicted_path(self):
        # Remove existing predicted path
        self.canvas.delete("predicted_path")

        # Draw predicted path
        bird_coords = self.canvas.coords(self.bird)
        bird_center_x = (bird_coords[0] + bird_coords[2]) / 2
        bird_center_y = (bird_coords[1] + bird_coords[3]) / 2
        predicted_y = bird_center_y
        velocity = self.bird_velocity
        path_points = [(bird_center_x, predicted_y)]
        
        for _ in range(30):
            predicted_y += velocity
            velocity += self.gravity
            path_points.append((bird_center_x, predicted_y))

        for i in range(len(path_points) - 1):
            self.canvas.create_line(path_points[i], path_points[i + 1], fill='lime', width=3, tag="predicted_path")

    def is_near_pipe(self, bird_coords):
        for pipe_pair in self.pipes:
            for pipe in pipe_pair:
                pipe_coords = self.canvas.coords(pipe)
                if abs(bird_coords[0] - pipe_coords[2]) < 20 or abs(bird_coords[2] - pipe_coords[0]) < 20:
                    return 3  # Thicker hitbox
        return 1  # Normal hitbox

    def spawn_invincibility_item(self):
        if not self.invincibility_item_exists and self.pipes_passed_since_last_item >= random.randint(7, 10):
            if random.random() < 0.5:  # 50% chance to spawn the item
                item_x = 400
                item_y = self.get_valid_item_y_position()
                self.invincibility_item = self.canvas.create_oval(item_x, item_y, item_x + 20, item_y + 20, fill='blue', outline='blue')
                self.invincibility_item_exists = True
                self.pipes_passed_since_last_item = 0

    def get_valid_item_y_position(self):
        attempts = 0
        max_attempts = 50000  # Prevent infinite loop, however, if you put this number too high it will crash the game
        # For modders: The sweet spot is around 50000 attempts for balance.
        # If the program cannot find a good place to put it, it will stuff it at Y250.
        # Below 10K attempts is for smooth playing, and above 10K is basically for performance
        # If it goes above 100K it might lag the game.
        while attempts < max_attempts:
            item_y = random.randint(100, 500)
            valid_position = True
            for pipe_pair in self.pipes:
                top_pipe_coords = self.canvas.coords(pipe_pair[0])
                bottom_pipe_coords = self.canvas.coords(pipe_pair[1])
                if (top_pipe_coords[1] < item_y < top_pipe_coords[3] or
                        bottom_pipe_coords[1] < item_y < bottom_pipe_coords[3]):
                    valid_position = False
                    break
            if valid_position:
                return item_y
            attempts += 1
        # If no valid position found after max_attempts, return a default position
        return 250
        # This part is critical to prevent crashes
        # Typically, Python spends a long time trying to figure out a valid Y coord.
        # Now, after an x amount of tries, it simply "gives up" and outputs 250 for Y.
        
        # Note to future Earth1283: Opimize this crap by making Python try differient numbers every time
        
# Reset the game to its origional configuration after death
    def restart_game(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.canvas.itemconfig(self.high_score_text, text=f'High Score: {self.high_score}')
        self.canvas.delete("all")
        self.bird = self.canvas.create_rectangle(50, 250, 70, 270, fill='yellow')
        self.score_text = self.canvas.create_text(200, 50, text=f'Score: {self.score}', font=('Arial', 24), fill='white')
        self.high_score_text = self.canvas.create_text(200, 100, text=f'High Score: {self.high_score}', font=('Arial', 24), fill='white')
        self.pipes.clear()
        self.pipe_gap = 215  # Reset the pipe gap
        self.create_pipes()
        self.bird_velocity = 0
        self.score = 0
        self.pipe_passed = False
        self.game_active = True
        self.invincible = False
        self.invincibility_item_exists = False
        self.pipes_passed_since_last_item = 0
        self.invincibility_countdown = None
        self.invincibility_glow = None

if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBird(root)
    root.mainloop()
    
# Copyright Earth1283 2024
