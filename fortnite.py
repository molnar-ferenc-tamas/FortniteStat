from lxml import html
import requests

class Platform:
    pc = "pc"

class Mode:
    solo = "p2"
    squad = "p9"
    duo = "p10"
    season3solo = "curr_p2"
    season3squad = "curr_p9"
    season3duo = "curr_p10"

class Category:
    wins = "Top1"
    kills = "Kills"
    score = "Score"

class GamerStat:
    def __init__(self, name, platform = Platform.pc, mode = Mode.solo, category = Category.wins):
        self.name = name
        self.platform = platform
        self.mode = mode
        self.category = category

    def getStat(self):
        pageNum = 1
        baseUrl = "https://fortnitetracker.com/leaderboards/{platform}/{category}?page={page}&platform={platform}&mode={mode}"
        url = baseUrl.format(platform = self.platform, category = self.category, page = pageNum, mode = self.mode)

        page = requests.get(url)
        tree = html.fromstring(page.content)

        xpathOfGamerPosition = "//td[a='{name}']/a[1]/@name".format(name=self.name)
        hasResult = (len( tree.xpath("//html/head[title != 'Error']")) > 0)

        while hasResult:
            gamer = tree.xpath( xpathOfGamerPosition)
            if len(gamer) > 0:
                return "Position of {name} is {pos}".format(name=self.name, pos=int(gamer[0]))

            pageNum += 1
            print(".", end="", flush=True)
            url = baseUrl.format(platform = self.platform, category = self.category, page = pageNum, mode = self.mode)

            page = requests.get(url)
            tree = html.fromstring(page.content)

            hasResult = (len( tree.xpath("//html/head[title != 'Error']")) > 0)

        return "No result for {name}".format(name=self.name)


    name = ""
    platform = ""
    mode = ""
    category = ""


#gamerStatList = [GamerStat("Ninja"), GamerStat("Uns3an3r"), GamerStat("DS_GhostTrapper")]
gamerStatList = [GamerStat("FantouGames")]
for gs in gamerStatList:
    print( gs.getStat())