# Grace Muzny
# CSCI 1200 - spring 2018
# Starter code for Homework 9 - Star Collector!

import random

class Square:
    
    # Instantiates a square
    # Parameters - occupant (string)
    #    optional - display (string color this will be displayed as)
    #    optional - team (int team this square belongs to)
    def __init__(self, occupant, display = "white", team = None):
        self.occ = occupant
        self.display = display
        self.team = team

    # Returns the string color representation of this square
    def __str__(self):
        return self.display

class Game:

    # Instantiates a game by laying out the playing field
    # including starting player positions and starting star positions
    # All positions for stars and players are reflected across the x-axis
    #
    # Parameters - players1 (list of Players on the first team)
    #            - players2 (list of Players on the second team)
    #    optional - size (int size grid to play on. Best with odd [7 - 25])
    def __init__(self, players1, players2, size = 11):
        self.players1 = players1
        self.players2 = players2
        self.width = size
        self.height = size
        self.contents = []
        self.positions = []
        self.team_points = {1: 0, 2: 0}
        self.stolen = {1: {1: 0, 2: 0}, 2: {1: 0, 2: 0}}
        self.stolen_and_dropped = {1: {1: 0, 2: 0}, 2: {1: 0, 2: 0}}

        for i in range(self.height):
            self.contents.append([Square("") for j in range(self.width)])
            
        # create scoring regions
        t1_home = (1, self.width // 2)
        t2_home = (self.height - 2, self.width // 2)

        # let all the players see the team info
        for p in self.players1:
            p.set_home_location(t1_home)
        for p in self.players2:
            p.set_home_location(t2_home)

        self.contents[t1_home[0]][t1_home[1]] = Square("home", display = "red", team = 1)
        self.contents[t2_home[0]][t2_home[1]] = Square("home", display = "blue", team = 2)
        
        # assign players to their starting positions
        for i in range(self.height):
            self.positions.append([None for j in range(self.width)])
        self.setup_team(t1_home)

        # put out treasures
        self.treasure_bank = TreasureBank()
        count = 0
        while count < int(self.width * self.height / 6):
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            inverse = (self.height - row - 1, self.width - col - 1)
            if not self.is_occupied((row, col)) and not self.is_occupied(inverse):
                k = self.treasure_bank.get_treasure_key()
                self.contents[row][col] = Square(k, display = "yellow")
                if (row, col) != inverse:
                    k = self.treasure_bank.get_treasure_key()
                    self.contents[inverse[0]][inverse[1]] = Square(k, display = "yellow")
                count += 1
    
    # Helper method that places players on the playing field so that
    # team positions begin in equal configurations
    # Parameters - home - (tuple of ints (row, col) position of team 1's home base)
    def setup_team(self, home):
        for i in range(len(self.players1)):
            # random unoccupied position near the home
            target = home
            while self.is_occupied(target):
                downness = random.randint(-1, self.height // 4)
                leftness = random.randint(0, self.width // 2)
                rightness = random.randint(0, self.width // 2)
                target = (home[0] + downness, home[1] + (leftness - rightness))
            self.positions[target[0]][target[1]] = self.players1[i]
            self.players1[i].set_position(target)
            inv = (self.height - target[0] - 1, self.width - target[1] - 1)
            self.positions[inv[0]][inv[1]] = self.players2[i]
            self.players2[i].set_position(inv)

    # Returns True if the target square is any of: home base, star, player
    # Parameters - target (tuple of ints (row, col) position)
    def is_occupied(self, target):
        if self.contents[target[0]][target[1]].occ != "":
            return True
        return self.positions[target[0]][target[1]] is not None

    # Returns player occupant of square if player is positioned there, otherwise
    # string occupant if the target square
    # Parameters - target (tuple of ints (row, col) position)
    def get_occupant(self, target):
        if self.positions[target[0]][target[1]] is not None:
            return self.positions[target[0]][target[1]]
        else:
            return self.contents[target[0]][target[1]]
        
        
    # Determines which of two attacks won. Case insensitive.
    # Parameters - a1 (string should be "rock", "paper", or "scissors")
    #            - a2 (string should be "rock", "paper", or "scissors")
    # Returns 1 if a1 won, 2 if a2 won, and 0 in case of tie.
    # Returns -1 if attacks weren't in correct format
    def beats(self, a1, a2):
        if a1.lower() == a2.lower():
            return 0
        elif a1.lower() == "rock":
            if a2.lower() == "scissors":
                return 1
            return 2
        elif a1.lower() == "paper":
            if a2.lower() == "rock":
                return 1
            return 2
        elif a1.lower() == "scissors":
            if a2.lower() == "paper":
                return 1
            return 2
        return -1  # should never happen

    # Take one turn in the game by:
    # asking players for moves
    # disallowing illegal moves
    # letting players put stars in their home bases
    # resolving conflicts
    # letting players collect stars
    def take_turn(self):
        # first, get all player moves
        moves = {p: p.get_move() for p in self.players1 + self.players2}

        # make sure all moves are legal moves
        for p in moves:
            if moves[p][0] < 0 or moves[p][0] >= self.height or \
            moves[p][1] < 0 or moves[p][1] >= self.width:
                moves[p] = p.get_position()  # illegal move = no move

        # also make sure that no one is trying to move more than one square
        for p in moves:
            prev = p.get_position()
            curr = moves[p]
            diff1 = abs(prev[0] - curr[0]) # should be 0 or 1
            diff2 = abs(prev[1] - curr[1]) # should be 0 or 1
            if diff1 + diff2 > 1:
                moves[p] = p.get_position()

        # players interact with home bases
        for p in moves:
            if self.contents[moves[p][0]][moves[p][1]].occ == "home":
                self.interact(self.contents[moves[p][0]][moves[p][1]], p)
                moves[p] = p.get_position() # don't let players stand on the home bases

        # make sure that there are no players there
        # resolve any conflicts
        for p in moves:
            m = moves[p]
            for p2 in moves:
                m2 = moves[p2]
                # test to see if two players are going to collide
                prev1 = p.get_position()
                prev2 = p2.get_position()
                switchies = prev1 == m2 and prev2 == m
                if (m == m2 or switchies) and p != p2:
                    attack1 = p.get_attack(str(p2))
                    attack2 = p2.get_attack(str(p))
                    result = self.beats(attack1, attack2)
    
                    # distribute treasure
                    if result == 1 and p2.has_star():
                        # p takes treasure from p2
                        if p.has_star():
                            self.treasure_bank.remove_star(p.remove_star())
                            self.stolen_and_dropped[p.get_team()][p2.get_team()] += 1
                        else:
                            self.stolen[p.get_team()][p2.get_team()] += 1
                        p.set_star(p2.remove_star())
                    elif result == 2 and p.has_star():
                        # p2 takes treasure from p
                        if p2.has_star():
                            self.treasure_bank.remove_star(p2.remove_star())
                            self.stolen_and_dropped[p2.get_team()][p.get_team()] += 1
                        else:
                            self.stolen[p2.get_team()][p.get_team()] += 1
                        p2.set_star(p.remove_star())
                    # if one of them is stationary or battle was a draw, then neither player moves
                    if p.get_position() == m or p2.get_position() == m2 or result == 0:
                        moves[p] = p.get_position()
                        moves[p2] = p2.get_position()
                    # otherwise, decide who gets to go there:
                    elif result == 1:
                        # p2 moves back to where they are
                        moves[p2] = p2.get_position()
                    elif result == 2:
                        # p moves back to where they are
                        moves[p] = p.get_position()

        # players interact with squares for treasure
        for p in moves:
            self.interact(self.contents[moves[p][0]][moves[p][1]], p)

        # actually move the players
        for p in moves:
            prev = p.get_position()
            if self.positions[prev[0]][prev[1]] == p:
                self.positions[prev[0]][prev[1]] = None
            p.set_position(moves[p])
            self.positions[moves[p][0]][moves[p][1]] = p
    

    # Interacts a square and a player for squares that contain things
    # If a player is carrying a star and visits the home base, they score
    # If a player moves onto a star, that player picks up the star and
    # the square is cleared.
    def interact(self, sq, player):
        if sq.occ == "home":
            if player.has_star():
                # drop off treasures
                t = player.remove_star()
                # then have this team score
                if self.treasure_bank.is_valid(t) and sq.team == player.get_team():
                    self.team_points[player.get_team()] += 1
                # no one gets points if you put it in the wrong bin
                self.treasure_bank.remove_star(t)
        elif sq.occ != "":
            if player.has_star():
                self.treasure_bank.remove_star(player.remove_star())
            # give treasure to player
            player.set_star(sq.occ)
            # remove it from the board
            sq.occ = ""
            sq.display = "white"
        # otherwise empty

    # Returns True if there are no more treasures that are on the board
    # or carried by players.
    def game_over(self):
        # game is over when all treasures are collected and no players are holding any treasures
        if self.treasure_bank.get_treasures_left() == 0:
            for p in self.players1 + self.players2:
                if p.has_star():
                    return False
            return True
        return False
    
    # Compares team point values to determine winner.
    # Returns "1" if team 1 won, "2" if team 2 did, and "Tie!" otherwise
    def get_winner(self):
        if self.game_over():
            if self.team_points[1] > self.team_points[2]:
                return "1"
            elif self.team_points[2] > self.team_points[1]:
                return "2"
            else:
                return "Tie!"
        return None
    
    # Returns a two-dimensional array of the colors to display
    # the playing field in
    def to_display_colors(self):
        colors = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                occ = self.get_occupant((i, j))
                row.append(str(occ))
            colors.append(row)
        return colors
    
    # returns the int number of points this team has
    # parameters - team_num (int num of the team)
    def get_points(self, team_num):
        return self.team_points[team_num]
    
    # returns the int number of stars left on the board
    def get_treasures_left(self):
        return self.treasure_bank.get_treasures_left()
    
    # returns the int number of stars players from the team currently hold
    # parameters - team_num (int num of the team)
    def get_treasures_held_by_team(self, team):
        players = self.players1
        if team == 2:
            players = self.players2
        count = 0
        for p in players:
            if p.has_star():
                count += 1
        return count
    
    # returns the int number of points the 1st team has stolen from the 2nd
    # parameters - team_num (int num of the stealing team)
    #            - team_num (int num of the stolen from team)
    def get_stolen_count(self, team, team_from):
        return self.stolen[team][team_from]
    
    # returns the int number of points the 1st team has stolen from the 2nd
    # that  has cause the first team to drop a star
    # parameters - team_num (int num of the stealing team)
    #            - team_num (int num of the stolen from team)
    def get_stolen_and_dropped_count(self, team, team_from):
        return self.stolen_and_dropped[team][team_from]
    
    # returns true if this square is a star
    # parameters - row (int)
    #            - col (int)
    def is_star(self, row, col):
        return self.treasure_bank.is_valid(self.contents[row][col].occ)
    
    # returns true if this square is a team base
    # parameters - row (int)
    #            - col (int)
    def is_base(self, row, col):
        return self.contents[row][col].occ == "home"
        
    # returns a string representation of the playing field
    # by combining the strings of all the current occupants of the field
    def __str__(self):
        s = ""
        for i in range(self.height):
            for j in range(self.width):
                s += str(self.get_occupant((i, j)))
            s += "\n"
        s += "Team 1: " + str(self.team_points[1]) + "\n"
        s += "Team 2: " + str(self.team_points[2]) + "\n"
        return s


class TreasureBank:

    # initializes a treasure bank so that it can generate
    # unique and very difficult to guess keys for our treasures
    def __init__(self, seed = None):
        self.seed = seed
        random.seed(a = self.seed)
        self.bank = []

    # generates and returns a new treasure key
    # this is a string representation of a float in [0, 1)
    def get_treasure_key(self):
        key = str(random.random())
        while key in self.bank:
            key = str(random.random())
        self.bank.append(key)
        return key
    
    # returns true if this key is a valid treasure
    # parameters - k (string potential key)
    def is_valid(self, k):
        return k in self.bank

    # returns the number of treasures left in the bank
    def get_treasures_left(self):
        return len(self.bank)
    
    # removes this key from the bank
    # parameters - k (string key)
    def remove_star(self, k):
        self.bank.remove(k)


