import unittest
from unittest import mock
from main import GameMap, build_map


class MapTests(unittest.TestCase):
    def test_create_map(self):
        gm = GameMap(10, 10, 1, [])
        self.assertIsNotNone(gm)

    def test_not_square(self):
        console_input = iter([
            "4 2 1",
            "x...",
            "...x"
        ])
        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        self.assertEqual(gm.height, 2)
        self.assertEqual(gm.width, 4)

    def test_map_correct_size(self):
        console_input = iter([
            "2 2 1",
            "x.",
            ".x"
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        self.assertEqual(gm.player_id, 1)
        self.assertEqual(gm.height, 2)
        self.assertEqual(gm.width, 2)

    def test_map_land(self):
        console_input = iter([
            "2 2 1",
            "x.",
            ".x"
        ])

        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        self.assertEqual(gm.is_land(0, 0), True)
        self.assertEqual(gm.is_land(1, 0), False)
        self.assertEqual(gm.is_land(0, 1), False)
        self.assertEqual(gm.is_land(1, 1), True)

    def test_map_sea(self):
        console_input = iter([
            "4 2 1",
            "x...",
            "...x"
        ])
        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        self.assertEqual(gm.is_sea(0, 0), False)
        self.assertEqual(gm.is_sea(1, 0), True)
        self.assertEqual(gm.is_sea(2, 1), True)
        self.assertEqual(gm.is_sea(3, 1), False)

    def test_valid_coords(self):
        console_input = iter([
            "2 2 1",
            "..",
            ".."
        ])
        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        self.assertEqual(gm.is_valid(0, 0), True)
        self.assertEqual(gm.is_valid(-1, 0), False)
        self.assertEqual(gm.is_valid(0, -1), False)
        self.assertEqual(gm.is_valid(1, 1), True)
        self.assertEqual(gm.is_valid(2, 0), False)
        self.assertEqual(gm.is_valid(0, 2), False)

    def test_start_coords(self):
        console_input = iter([
            "2 2 1",
            "xx",
            ".x"
        ])
        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        (x, y) = gm.start_coords()

        self.assertEqual(x, 0)
        self.assertEqual(y, 1)

    def test_start_coords_sets_my_position(self):
        console_input = iter([
            "2 2 1",
            "xx",
            ".x"
        ])
        mock.builtins.input = lambda: next(console_input)
        gm = build_map()

        (x, y) = gm.start_coords()

        self.assertEqual(gm.player_pos, (x, y))



