import random
import sys


# Pathfinding "borrowed" from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, direction=None):
        self.parent = parent
        self.position = position
        self.direction = direction

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class GameMap:
    def __init__(self, width, height, player_id, map_data):
        self.player_pos = (-1, -1)
        self.width = width
        self.height = height
        self.player_id = player_id
        self.map_data = map_data
        self.my_life = 0
        self.opp_life = 0
        self.torpedo_cooldown = 0
        self.sonar_cooldown = 0
        self.silence_cooldown = 0
        self.mine_cooldown = 0

    def is_valid(self, row, col):
        return 0 <= row < self.width and 0 <= col < self.height

    def is_land(self, row, col):
        return self.map_data[col][row] == 'x'

    def is_sea(self, row, col):
        return self.map_data[col][row] == '.'

    def start_coords(self):
        candidates = [(x, y) for y in range(self.height) for x in range(self.width) if self.is_sea(x, y)]
        self.player_pos = random.choice(candidates)
        return self.player_pos

    def update(self, x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown):
        self.player_pos = (x, y)
        self.my_life = my_life
        self.opp_life = opp_life
        self.torpedo_cooldown = torpedo_cooldown
        self.sonar_cooldown = sonar_cooldown
        self.silence_cooldown = silence_cooldown
        self.mine_cooldown = mine_cooldown


class Navigator:
    moves = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    sector_centres = {
        1: (2,  2),
        2: (7,  2),
        3: (12, 2),
        4: (2,  7),
        5: (7,  7),
        6: (12, 7),
        7: (2,  12),
        8: (7,  12),
        9: (12, 12),
    }

    curr_move = "W"

    def __init__(self, game_map):
        self.game_map = game_map
        self.history = [game_map.player_pos]
        self.opponent_sector = None
        self.plan = []

    def plan_route_to(self, target, ignore_history=False):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(position=self.game_map.player_pos)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(position=target)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = [start_node]
        closed_list = []
        # count = 0

        # Loop until you find the end
        while len(open_list) > 0:
            # Get the current node - use the one with the lowest value of f
            current_node = min(open_list, key=lambda x: x.f)

            # count += 1
            # print(count)
            # print(current_node.position)
            # print("Open list: {0}".format(",".join([str(x.position) for x in open_list])))
            # print("Closed list: {0}".format(",".join([str(x.position) for x in closed_list])))

            # Pop current off open list, add to closed list
            open_list = [x for x in open_list if x != current_node]
            closed_list.append(current_node)

            # WINNER!
            if current_node == end_node:
                return self.unwind_path(current_node)

            # Generate children
            candidates = [(m, (current_node.position[0] + x, current_node.position[1] + y)) for (m, (x, y)) in
                          self.moves.items()]
            children = [Node(parent=current_node, position=p, direction=m) for (m, p) in candidates if
                        self.move_is_ok(p, ignore_history=ignore_history)]

            # Loop through children
            for child in children:
                # Don't add children in the open list
                if not any([x for x in closed_list if x == child]):
                    # Create the f, g, and h values
                    child.g = current_node.g + 1
                    child.h = abs(child.position[0] - end_node.position[0]) + abs(
                        child.position[1] - end_node.position[1])
                    child.f = child.g + child.h

                    # Child is already in the open list
                    if not any([x for x in open_list if x == child and child.g < x.g]):
                        open_list.append(child)

    def unwind_path(self, current_node):
        path = []
        current = current_node
        # Don't include the current position in the route
        while current is not None and current.position != self.game_map.player_pos:
            path.append(current.direction)
            current = current.parent
        return path[::-1]  # Return reversed path

    def move_random(self):
        me = self.game_map.player_pos
        moves = [(m, (me[0] + x, me[1] + y)) for (m, (x, y)) in self.moves.items()]
        moves = [m for (m, coords) in moves if self.move_is_ok(coords)]

        if moves:
            return random.choice(moves)
        else:
            return None

    def next_move(self):
        self.history.append(self.game_map.player_pos)

        if self.opponent_sector and not self.plan:
            target = self.sector_centres[self.opponent_sector]
            if self.move_is_ok(target, ignore_history=True) and target != self.game_map.player_pos:
                if(target in self.history):
                    print('Target is in history. Surfacing to reset', file=sys.stderr)
                    return self.surface()

                # It's possible to route there, so try
                self.plan = self.plan_route_to(target)
                if self.plan:
                    print('Targeting: {0} New plan: {1}'.format(target, ",".join(self.plan)), file=sys.stderr)
                else:
                    print("Couldn't find route", file=sys.stderr)
            else:
                print('Duff target', file=sys.stderr)
                # Duff target (maybe it's land?) don't bother for now
                self.opponent_sector = None

        if self.plan:
            m = self.plan.pop(0)
        else:
            m = self.move_random()

        if m:
            return self.move(m)
        else:
            return self.surface()

    def move(self, m):
        return "MOVE {0}".format(m)

    def surface(self):
        self.history = [self.game_map.player_pos]
        return "SURFACE"

    def move_is_ok(self, coords, ignore_history=False):
        return self.game_map.is_valid(*coords) \
               and self.game_map.is_sea(*coords) \
               and (ignore_history or coords not in self.history)

    def process_opponent_orders(self, opponent_orders):
        orders = opponent_orders.split()
        if orders and orders[0] == 'SURFACE':
            print('FOUND IN SECTOR {0}'.format(orders[1]), file=sys.stderr)
            self.opponent_sector = int(orders[1])


class Gunner:
    def __init__(self, game_map, navigator):
        self.game_map = game_map
        self.navigator = navigator

    def action(self):
        return "TORPEDO"

    def fire(self):
        return "TORPEDO {0} {1}".format(*self.target())

    def ready(self):
        return self.game_map.torpedo_cooldown == 0 and self.target()

    def target(self):
        (mx, my) = self.game_map.player_pos
        squares = [(x, y) for x in range(self.game_map.width) for y in range(self.game_map.height)]
        squares = [(x, y) for (x, y) in squares if 2 < (abs(mx - x) + abs(my - y)) <= 4]
        squares = [c for c in squares if self.game_map.is_valid(*c)]
        squares = [c for c in squares if self.game_map.is_sea(*c)]

        random.shuffle(squares)
        for coords in squares:
            route = self.navigator.plan_route_to(coords)
            if route and len(route) <= 4:
                print(",".join(route), file=sys.stderr)
                return squares[0]

        return None


def build_map():
    width, height, my_id = [int(i) for i in input().split()]
    map_data = [list(input()) for _ in range(height)]
    return GameMap(width, height, my_id, map_data)


i = 0
gm = None
sc = None
nav = None
gun = None


def init_game():
    global i, gm, sc, nav, gun

    gm = build_map()
    sc = gm.start_coords()
    nav = Navigator(gm)
    gun = Gunner(gm, nav)

    print("{0} {1}".format(*sc))


def do_turn():
    global i
    i += 1
    # print("TURN {0}".format(i), file=sys.stderr)
    gm.update(*[int(i) for i in input().split()])
    sonar_result = input()
    opponent_orders = input()
    nav.process_opponent_orders(opponent_orders)

    if gun.ready():
        print(gun.fire())
    else:
        print("{0} {1}".format(nav.next_move(), gun.action()))


if __name__ == '__main__':
    init_game()

    while True:
        do_turn()
