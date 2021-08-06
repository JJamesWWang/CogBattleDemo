from main import CogBattleDemo
from cogbattle import CogBattle, CogBattleFSM, CogBattleState
from panda3d.core import loadPrcFileData
import unittest


class TestCogBattle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loadPrcFileData("", "window-type offscreen")
        cls.demo = CogBattleDemo()

    def setUp(self):
        self.cogBattle = CogBattle()
        self.cogBattleFSM = self.cogBattle.cogBattleFSM

    def test_initial_fsm_state(self):
        self.assertEqual(self.cogBattleFSM.state, "Off")

    def test_start_cog_battle_state(self):
        self.cogBattle.startCogBattle()
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.GAG_SELECT)


if __name__ == "__main__":
    unittest.main()
