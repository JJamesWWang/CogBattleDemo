from main import CogBattleDemo
from cogbattle import CogBattle, CogBattleFSM, CogBattleState
from toon import Toon, ToonCombatant
from cog import Cog, CogCombatant
from gag import Gag
from panda3d.core import loadPrcFileData
import unittest
from direct.task.TaskManagerGlobal import taskMgr


class TestCogBattle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loadPrcFileData("", "window-type offscreen")
        cls.demo = CogBattleDemo()

    def setUp1v1(self):
        self.cogBattle = CogBattle([Toon()], [Cog()], deterministic=True)
        self.cogBattleFSM = self.cogBattle.cogBattleFSM
        self.cogBattle.startCogBattle()

    def test_start_cog_battle_state(self):
        self.setUp1v1()
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.GAG_SELECT)

    def test_correct_toon_number(self):
        self.setUp1v1()
        self.assertEqual(len(self.cogBattle.toons), 1)
        self.cogBattle.requestToonJoin(Toon())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.toons), 2)
        self.cogBattle.requestToonJoin(Toon())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.toons), 3)
        self.cogBattle.requestToonJoin(Toon())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.toons), 4)
        self.cogBattle.requestToonJoin(Toon())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.toons), 4)

    def test_correct_cog_number(self):
        self.setUp1v1()
        self.assertEqual(len(self.cogBattle.cogs), 1)
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.cogs), 2)
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.cogs), 3)
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.cogs), 4)
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()
        self.assertEqual(len(self.cogBattle.cogs), 4)

    def test_toon_dies(self):
        self.setUp1v1()
        for _ in range(8):
            self.cogBattle.selectGag(Gag.PASS)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.COGS_WON)

    def test_cog_dies_squirt(self):
        self.setUp1v1()
        for _ in range(3):
            self.cogBattle.selectGag(Gag.SQUIRT)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)

    def test_cog_dies_throw(self):
        self.setUp1v1()
        for _ in range(2):
            self.cogBattle.selectGag(Gag.THROW)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)

    def test_cog_dies_combo(self):
        self.setUp1v1()
        self.cogBattle.selectGag(Gag.SQUIRT)
        self.cogBattle.selectGag(Gag.THROW)
        self.cogBattle.selectGag(Gag.SQUIRT)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)


if __name__ == "__main__":
    unittest.main()
