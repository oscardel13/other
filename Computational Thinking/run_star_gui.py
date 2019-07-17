# Grace Muzny
# CSCI 1200 - spring 2018
# Starter code for Homework 9 - Star Collector!
# This is the file that you will run to show the game!

import tkinter as tk
import game
import player as player1

# if you want to test out different teams against each other, change
# this line. For example, I have 1 Player object saved as player.py and another
# saved as player2.py. I would cahnge this line to:
# import player2 as player2
import player as player2  

class StarCollectorGUI:
    
    def __init__(self, master):
        # you can change this number to change the size of the field!
        # Will work for odd sizes from 7 to 25
        size = 9  
        
        # This is where we make our teams
        p1 = player1.Player(1)
        p2 = player1.Player(1)
        p3 = player1.Player(1)
        p4 = player2.Player(2)
        p5 = player2.Player(2)
        p6 = player2.Player(2)
        t1 = [p1, p2, p3]
        t2 = [p4, p5, p6]

        # Instantiate the game        
        self.my_game = game.Game(t1, t2, size=size)
        self.turns = 0
        
        # setting up the GUI
        self.master = master
        
        self.play_button = tk.Button(master, text = "Auto play", command=lambda: self.play_game())
        self.play_button.pack()

        self.step_button = tk.Button(master, text = "Take turn", command=lambda: self.update_game())
        self.step_button.pack()
        
        self.my_game_display = tk.StringVar()
        self.my_game_display.set("Points:\nTeam 1:\nTeam2:\n")
        self.label = tk.Label(self.master, textvariable=self.my_game_display)
        self.label.pack()
        
        can_size = (size * 10) + 100        
        self.canvas = tk.Canvas(master, width=can_size * 2, height=can_size * 1.5)
        # in the format x1, y1, x2, y2, x3, y3, etc
        self.star_base = (10, 40, 40, 40, 50, 10, 60, 40, 90, 40, 65, 60, 75, 90, 50, 70, 25, 90, 35, 60)
        factor = .15
        self.star_base = [(v * factor) for v in self.star_base]

        self.canvas.pack()

        # initialize the shapes on our board
        self.squares = []
        self.stars = []
        y = 10
        for i in range(self.my_game.height):
            row = []
            x = 75
            for j in range(self.my_game.width):
                x1 = x + (j * 10)
                y1 = y + (i * 10)
    
                if self.my_game.is_star(i, j):
                    coords = []
                    for k in range(0, len(self.star_base), 2):
                        coords.append(self.star_base[k] + x1 - 2)
                        coords.append(self.star_base[k + 1] + y1 - 2)
                    id = self.canvas.create_polygon(coords, fill = "black")
                    self.stars.append((i, j))
                elif self.my_game.is_base(i, j):
                    id = self.canvas.create_oval((x1, y1, x1 + 10, y1 + 10))
                else:
                    id = self.canvas.create_rectangle((x1, y1, x1 + 10, y1 + 10))
                row.append(id)
                x += 10
            self.squares.append(row)
            y += 10
            
        # more informational labels
        self.bonus_info = tk.StringVar()
        self.bonus_info.set("")
        self.label_bonus_info = tk.Label(self.master, textvariable=self.bonus_info)
        self.label_bonus_info.pack()
        
        self.stealing_info = tk.StringVar()
        self.stealing_info.set("")
        self.label_stealing_info = tk.Label(self.master, textvariable=self.stealing_info)
        self.label_stealing_info.pack()
        
        # finally, update the GUI
        self.update_gui()
        
        
    # Updates the graphical representation to accurately show the 
    # current state of the game
    def update_gui(self):
        self.master.title("StarCollector! Turn: %i" % self.turns)
        # then display the state of the game
        colors = self.my_game.to_display_colors()
        for i in range(self.my_game.height):
            for j in range(self.my_game.width):
                color = colors[i][j]
                if (i, j) in self.stars:
                    if not self.my_game.is_star(i, j):
                        # put in a rectangle instead
                        self.canvas.delete(self.squares[i][j]) # remove star
                        x1 = (75 + j * 10) + (j * 10)
                        y1 = (10 + i * 10) + (i * 10)
                        id = self.canvas.create_rectangle((x1, y1, x1 + 10, y1 + 10))
                        self.squares[i][j] = id
                        # remove from star list
                        self.stars.remove((i, j))
                self.canvas.itemconfig(self.squares[i][j], fill=color, outline="black")
        # update points info
        points_s = "Stars:\nTeam 1: %i\nTeam 2: %i" % (self.my_game.get_points(1), self.my_game.get_points(2))
        self.my_game_display.set(points_s + "\n")
        if (self.my_game.game_over()):
            self.my_game_display.set(points_s + "\nWinner: %s" % self.my_game.get_winner()) 
            
        # update other info like how many treasures are left,
        # and how many treasures each team's players are holding
        tt = self.my_game.get_treasures_left()
        t1_t = self.my_game.get_treasures_held_by_team(1)
        t2_t = self.my_game.get_treasures_held_by_team(2)
        onboard_t = tt - t1_t - t2_t
        bonus_s = "Total stars left: %i\nStars on board: %i\nHeld by team 1: %i\nHeld by team 2: %i" % (tt, onboard_t, t1_t, t2_t)
        self.bonus_info.set(bonus_s)
        
        # Update info about how many treasures have been stolen, etc.
        s = ""
        for i in [1, 2]:
            s += "\nTeam %i:" % i
            t_stolet1 = self.my_game.get_stolen_count(i, 1)
            t_stolet2 = self.my_game.get_stolen_count(i, 2)
            s += "\nStolen (no drop) - team 1: %i, team 2: %i" % (t_stolet1, t_stolet2)
            t_stoledt1 = self.my_game.get_stolen_and_dropped_count(i, 1)
            t_stoledt2 = self.my_game.get_stolen_and_dropped_count(i, 2)
            s += "\nStolen (drop first) - team 1: %i, team 2: %i" % (t_stoledt1, t_stoledt2)
        self.stealing_info.set(s)


    # Updates the underluing game if it is not over yet, increments turn counters
    def update_game(self):       
        if not self.my_game.game_over():
            self.turns += 1
            self.my_game.take_turn()
        self.update_gui()
        
    # helps auto update continue updating the game every 200 ms
    def update_auto_wrapper(self):
        self.update_game()
        self.master.after(200, self.update_auto_wrapper)
        
    # Sets off the auto update of the game every 200 ms
    def play_game(self):
        self.master.after(200, self.update_auto_wrapper)
        
def main():
    root = tk.Tk()
    gui = StarCollectorGUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
