from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from cogbattle import CogBattle
from gag import Gag
from cog import Cog
from panda3d.core import TextNode
import sys


# Macro-like function used to reduce the amount to code needed to create the on
# screen instructions
def genText(text, i):
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

    def __init__(self):
        super().__init__()
        self.cogBattle = CogBattle(Cog())
        self.generateInstructions()
        self.bindInput()

    def generateInstructions(self):
        genText("ESC: Quit", 0)
        genText("S: Start Cog Battle", 1)
        genText("1: Pass", 2)
        genText("2: Use Squirt", 3)
        genText("3: Use Throw", 4)

    def bindInput(self):
        self.accept("escape", sys.exit)
        self.accept("s", self.cogBattle.startCogBattle)
        self.accept("1", self.cogBattle.selectGag, [Gag.PASS])
        self.accept("2", self.cogBattle.selectGag, [Gag.SQUIRT])
        self.accept("3", self.cogBattle.selectGag, [Gag.THROW])



if __name__ == "__main__":
    demo = CogBattleDemo()
    demo.run()
