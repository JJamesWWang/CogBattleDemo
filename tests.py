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

    def setUp(self):
        self.cogBattle = CogBattle([Toon()], [Cog()], deterministic=True)
        self.cogBattleFSM = self.cogBattle.cogBattleFSM
        self.cogBattle.startCogBattle()

    def test_start_cog_battle_state(self):
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.GAG_SELECT)

    def test_correct_toon_number(self):
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
        for _ in range(8):
            self.cogBattle.selectGag(Gag.PASS)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.COGS_WON)

    def test_cog_dies_squirt(self):
        for _ in range(3):
            self.cogBattle.selectGag(Gag.SQUIRT)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)

    def test_cog_dies_throw(self):
        for _ in range(2):
            self.cogBattle.selectGag(Gag.THROW)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)

    def test_cog_dies_combo(self):
        self.cogBattle.selectGag(Gag.SQUIRT)
        self.cogBattle.selectGag(Gag.THROW)
        self.cogBattle.selectGag(Gag.SQUIRT)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)

    # def test_toon_joins_only_during_gag_select(self): -> Can't test this
    # because of timing issues (gag execute and cogs attack is instant)

    # def test_cog_joins_only_during_gag_select(self): -> See above

    def test_triple_squirt_kills(self):
        for _ in range(2):
            self.cogBattle.requestToonJoin(Toon())
            taskMgr.step()
        for _ in range(3):
            self.cogBattle.selectGag(Gag.SQUIRT)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)
        self.assertEqual(self.cogBattle.toons[0].health, 15)

    def test_double_throw_kills(self):
        self.cogBattle.requestToonJoin(Toon())
        taskMgr.step()
        for _ in range(2):
            self.cogBattle.selectGag(Gag.THROW)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)
        self.assertEqual(self.cogBattle.toons[0].health, 15)

    def test_two_cogs_attack(self):
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()
        for _ in range(4):
            self.cogBattle.selectGag(Gag.PASS)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.COGS_WON)

    def test_four_cogs_attack(self):
        for _ in range(3):
            self.cogBattle.requestCogJoin(Cog())
            taskMgr.step()
        for _ in range(2):
            self.cogBattle.selectGag(Gag.PASS)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.COGS_WON)

    def test_additional_gags_do_nothing(self):
        for _ in range(3):
            self.cogBattle.requestToonJoin(Toon())
            taskMgr.step()
            self.cogBattle.selectGag(Gag.SQUIRT)
        self.cogBattle.selectGag(Gag.THROW)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.TOONS_WON)

    def test_targeting_works(self):
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()
        self.cogBattle.selectGag(Gag.SQUIRT)
        self.cogBattle.selectTarget(1)
        self.assertEqual(self.cogBattle.cogs[1].health, 8)

    def test_multitargeting_works(self):
        for _ in range(3):
            self.cogBattle.requestToonJoin(Toon())
            taskMgr.step()
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()
        for _ in range(3):
            self.cogBattle.selectGag(Gag.THROW)
            self.cogBattle.selectTarget(1)
        self.cogBattle.selectGag(Gag.THROW)
        self.cogBattle.selectTarget(0)
        self.assertEqual(len(self.cogBattle.cogs), 1)
        self.assertEqual(self.cogBattle.cogs[0].health, 6)

    def test_selecting_nonexistent_cog_does_nothing(self):
        self.cogBattle.requestCogJoin(Cog())
        taskMgr.step()

        self.cogBattle.selectGag(Gag.SQUIRT)
        self.cogBattle.selectTarget(2)
        self.assertEqual(self.cogBattleFSM.state, CogBattleState.GAG_SELECT)


if __name__ == "__main__":
    unittest.main()
