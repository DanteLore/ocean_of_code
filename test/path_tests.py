import unittest
from unittest import mock
from main import GameMap, build_map, Navigator


class PathTests(unittest.TestCase):
    def test_create_navigator(self):
        console_input = iter([
            "2 2 1",
            "x.",
            ".x"
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        nav = Navigator(gm)
        self.assertIsNotNone(nav)

    def test_two_moves_on_a_square(self):
        console_input = iter([
            "2 2 1",
            "..",
            ".."
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()
        gm.start_coords()
        nav = Navigator(gm)

        for _ in range(2):
            nav.next_move()

    def test_simple_route(self):
        console_input = iter([
            "5 5 1",
            ".....",
            ".....",
            ".....",
            ".....",
            "....."
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()
        gm.player_pos = (0, 0) # Force player pos
        nav = Navigator(gm)

        route = nav.plan_route_to((4,4))
        print(route)
        self.assertEqual(len(route), 8)

    def test_impossible_route(self):
        console_input = iter([
            "5 5 1",
            ".x...",
            ".x...",
            ".x...",
            ".x...",
            ".x..."
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()
        gm.player_pos = (0, 0) # Force player pos
        nav = Navigator(gm)

        route = nav.plan_route_to((4,4))
        print(route)
        self.assertIsNone(route)

    def test_avoid_obstacles(self):
        console_input = iter([
            "5 5 1",
            ".....",
            ".....",
            ".....",
            ".xxxx",
            "....."
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()
        gm.player_pos = (0, 0) # Force player pos
        nav = Navigator(gm)

        route = nav.plan_route_to((4,4))
        print(route)
        self.assertListEqual(route, ['S', 'S', 'S', 'S', 'E', 'E', 'E', 'E'])

    def test_snake(self):
        console_input = iter([
            "5 5 1",
            ".....",
            "xxxx.",
            ".....",
            ".xxxx",
            "....."
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()
        gm.player_pos = (0, 0) # Force player pos
        nav = Navigator(gm)

        route = nav.plan_route_to((4,4))
        print(route)
        self.assertEqual(len(route), 16)

    def test_spiral(self):
        console_input = iter([
            "5 5 1",
            ".....",
            "xxxx.",
            "...x.",
            ".xxx.",
            "....."
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()
        gm.player_pos = (0, 0) # Force player pos
        nav = Navigator(gm)

        route = nav.plan_route_to((2,2))
        print(route)
        self.assertEqual(len(route), 16)

    def test_spiral_outwards(self):
        console_input = iter([
            "5 5 1",
            ".....",
            "xxxx.",
            "...x.",
            ".xxx.",
            "....."
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()
        gm.player_pos = (2, 2) # Force player pos
        nav = Navigator(gm)

        route = nav.plan_route_to((0,0))
        print(route)
        self.assertEqual(len(route), 16)
