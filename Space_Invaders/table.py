import pandas as pd
import pygame_menu
from screen import Screen


class Table:

    data = {
        "name": [],
        "score": [],
    }
    name = 'noname'
    score = 0
    scores = []
    names = []

    def __init__(self):
         pass


    def write_score(self):
        self.add()
        if self.check(): #check if the player already exists in the CSV file
            df = pd.DataFrame.from_dict(self.data)
            df.to_csv("scoreboard.csv", mode="a", index=False, header=False)
        self.clear()

    def check(self):
        df = pd.read_csv("scoreboard.csv")
        check = True
        for x in df['name']:
            if x == self.name:
                index = df["name"].tolist().index(x)
                if self.score < df["score"].tolist()[index]:
                    check = False

        return check



    def add(self):
        if self.name == '':
            self.name = 'noname'
        self.data["name"].append(self.name)
        self.data["score"].append(self.score)

    def clear(self):
        self.data["name"].clear()
        self.data["score"].clear()


    def read(self):
        df = pd.read_csv("scoreboard.csv")
        while len(self.names) < 5:
            max = df["score"].max()
            score_list = df["score"].tolist()
            name_list = df["name"].tolist()
            index = score_list.index(max)
            if not self.names.__contains__(name_list[index]):
                self.names.append(name_list[index])
                self.scores.append(score_list[index])
            df = df.drop(df.index[index])

    def show_scoreboard(self, function, surface):
        scoreboard_menu = pygame_menu.Menu('', 750, 750, theme=Screen.MY_THEME)
        scoreboard_menu.add.button('Back', function)

        # Table
        table = scoreboard_menu.add.table(table_id='my_table', font_size=35, font_color=(255, 255, 255))
        table.default_cell_padding = 10
        table.add_row(['Player', 'High Score', ], cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)
        self.read()
        for i in range(len(self.scores)):
            table.add_row([self.names[i], self.scores[i]], cell_align=pygame_menu.locals.ALIGN_CENTER)

        scoreboard_menu.mainloop(surface)
