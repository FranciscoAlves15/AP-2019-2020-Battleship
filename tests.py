import unittest
import battleship_game as bg

class TestStand(unittest.TestCase):
    def setUp(self):
        self.game = bg.new_game()

    def tearDown(self):
        return super().tearDown()
    
    def __add_player(self, name="Bob"):
        bg.add_player(self.game, name)
    
    def __add_players(self):
        self.__add_player("Bob")
        self.__add_player("Alice")
        self.__add_player("Trudy")

    def __add_players_and_set_match(self):
        self.__add_players()
        bg.start_match(self.game, "Bob", "Alice")
        
    def test_has_player(self):
        self.assertFalse(bg.has_player(self.game, "Bob"))
        self.__add_player()
        self.assertTrue(bg.has_player(self.game, "Bob"))
    
    def test_add_player(self):
        self.assertEqual(len(bg.get_players(self.game)), 0)
        bg.add_player(self.game, "Bob")
        self.assertEqual(len(bg.get_players(self.game)), 1)

    def test_player_in_match(self):
        self.__add_players_and_set_match()
        self.assertTrue(bg.player_in_match(self.game, "Bob"))
        self.assertTrue(bg.player_in_match(self.game, "Alice"))
        self.assertFalse(bg.player_in_match(self.game, "Trudy"))
    
    def test_remove_player(self):
        self.__add_players()
        self.assertTrue(len(bg.get_players(self.game)), 3)
        bg.remove_player(self.game, "Alice")
        self.assertTrue(len(bg.get_players(self.game)), 2)
    
    def test_has_players(self):
        self.assertFalse(bg.has_players(self.game))
        self.__add_players()
        self.assertTrue(bg.has_players(self.game))
    
    def test_get_players(self):
        self.__add_players()
        self.assertEqual(len(bg.get_players(self.game)), 3)
        self.assertIn({
            'name': 'Alice',
            'matches': 0,
            'wins': 0
        }, bg.get_players(self.game))
    
    def test_has_match(self):
        self.assertFalse(bg.has_match(self.game))
        self.__add_players_and_set_match()
        self.assertTrue(bg.has_match(self.game))
    
    def test_start_match(self):
        self.assertFalse(bg.has_match(self.game))
        self.__add_players()
        bg.start_match(self.game, "Alice", "Trudy")
        self.assertTrue(bg.has_match(self.game))


if __name__ == "__main__":
    unittest.main()