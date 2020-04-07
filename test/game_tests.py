import unittest
from unittest import mock
from main import init_game, do_turn


class PathTests(unittest.TestCase):
    def test_game_plays_ok(self):
        console_input = iter([
            "2 2 1",
            "..",
            "..",
            "0 0 1 1 1 1 1 1",
            "",
            "",
            "0 0 1 1 1 1 1 1",
            "",
            ""
        ])

        mock.builtins.input = lambda: next(console_input)

        init_game()
        do_turn()
        do_turn()

    # Turn params
    # x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown

    def test_game_plays_ok_torpedo(self):
        console_input = iter([
            "15 15 1",
            "....xx.........",
            "....xx.........",
            "........xxx.xxx",
            "........xxx.xxx",
            "........xxx....",
            "...............",
            "...xx..........",
            "..xxx..........",
            "..xxx......xx..",
            "..xxx......xx..",
            "..xxx..........",
            "..xxx..........",
            "...xx.....xx...",
            "..........xx...",
            "...............",
            "0 0 1 1 1 1 1 1",
            "",
            "",
            "0 0 1 1 0 1 1 1",
            "",
            "",
            "0 0 1 1 5 1 1 1",
            "",
            ""
        ])

        mock.builtins.input = lambda: next(console_input)

        init_game()
        do_turn()
        do_turn()
        do_turn()

    def test_game_plays_ok_enemy_surface(self):
        console_input = iter([
            "15 15 1",
            "....xx.........",
            "....xx.........",
            "........xxx.xxx",
            "........xxx.xxx",
            "........xxx....",
            "...............",
            "...xx..........",
            "..xxx..........",
            "..xxx......xx..",
            "..xxx......xx..",
            "..xxx..........",
            "..xxx..........",
            "...xx.....xx...",
            "..........xx...",
            "...............",
            "0 0 1 1 1 1 1 1",
            "",
            "SURFACE 1",
            "0 0 1 1 1 1 1 1",
            "",
            "",
            "0 0 1 1 1 1 1 1",
            "",
            ""
        ])

        mock.builtins.input = lambda: next(console_input)

        init_game()
        do_turn()
        do_turn()
        do_turn()

    def test_game_plays_ok_big_map(self):
        console_input = iter([
            "15 15 1",
            "....xx.........",
            "....xx.........",
            "........xxx.xxx",
            "........xxx.xxx",
            "........xxx....",
            "...............",
            "...xx..........",
            "..xxx..........",
            "..xxx......xx..",
            "..xxx......xx..",
            "..xxx..........",
            "..xxx..........",
            "...xx.....xx...",
            "..........xx...",
            "...............",
            "0 0 1 1 1 1 1 1",
            "",
            "",
            "0 0 1 1 1 1 1 1",
            "",
            ""
        ])

        mock.builtins.input = lambda: next(console_input)

        init_game()
        do_turn()
        do_turn()
