from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from cogbattle import CogBattle
from gag import Gag
from cog import Cog
from toon import Toon
from panda3d.core import TextNode
import sys


# Macro-like function used to reduce the amount to code needed to create the on
# screen instructions
def genText(text, i) -> OnscreenText:
    return OnscreenText(
        text=text,
        parent=base.a2dTopLeft,
        pos=(0.07, -0.06 * i - 0.1),
        fg=(1, 1, 1, 1),
        align=TextNode.ALeft,
        shadow=(0, 0, 0, 0.5),
        scale=0.05,
    )


class CogBattleDemo(ShowBase):
    def __init__(self) -> None:
        super().__init__()
        self.cogBattle: CogBattle = CogBattle([Toon()], [Cog()])
        self.generateInstructions()
        self.bindInput()

    def generateInstructions(self):
        genText("ESC: Quit", 0)
        genText("S: Start Cog Battle", 1)
        genText("T: Add Toon", 2)
        genText("C: Add Cog", 3)
        genText("1: Pass", 4)
        genText("2: Use Squirt", 5)
        genText("3: Use Throw", 6)
        genText("7: Target Cog 1", 7)
        genText("8: Target Cog 2", 8)
        genText("9: Target Cog 3", 9)
        genText("0: Target Cog 4", 10)

    def bindInput(self):
        self.accept("escape", sys.exit)
        self.accept("s", self.cogBattle.startCogBattle)
        self.accept("t", self.cogBattle.requestToonJoin, [Toon()])
        self.accept("c", self.cogBattle.requestCogJoin, [Cog()])
        self.accept("1", self.cogBattle.selectGag, [Gag.PASS])
        self.accept("2", self.cogBattle.selectGag, [Gag.SQUIRT])
        self.accept("3", self.cogBattle.selectGag, [Gag.THROW])
        self.accept("7", self.cogBattle.selectTarget, [0])
        self.accept("8", self.cogBattle.selectTarget, [1])
        self.accept("9", self.cogBattle.selectTarget, [2])
        self.accept("0", self.cogBattle.selectTarget, [3])


if __name__ == "__main__":
    demo = CogBattleDemo()
    demo.run()
