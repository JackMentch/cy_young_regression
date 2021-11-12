from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
import pandas as pd
import re

start_year = 2000
end_year = 2021

column_names = ["player_id", "votes", "baa", "ops", "strkpct", "bbpct", "wpa",
                "bors", "era",  "strikeouts",
                "era_plus", "fip", "whip", "bb_per_nine", "strikeouts_per_nine"]

df = pd.DataFrame(columns = column_names)


stats = ["standard", "advanced"]

for stat in stats:

    for year in range(start_year, end_year):

        link = f"https://www.baseball-reference.com/leagues/majors/{year}-{stat}-pitching.shtml"

        html = urlopen(link)
        bsObj = BeautifulSoup(html.read(), features="lxml")

        comments = bsObj.findAll(string=lambda text: isinstance(text, Comment))

        for c in comments:
            # convert the comment to BS Object
            c_string = BeautifulSoup(str(c), features="lxml")

            pitchers = c_string.findAll(lambda tag: tag.name == 'tr' and
                                                    tag.get('class') == ['full_table'])

            if pitchers:

                for pitcher in pitchers:

                    name = pitcher.find("td", {"data-stat": "player"}).get_text()
                    id = re.sub('\s+', '', name).replace("*", "").replace(".", "") + str(year)




                    if stat == "advanced":

                        index = df.loc[df['player_id'] == id].index

                        df.at[index,'baa'] = baa = pitcher.find("td", {"data-stat": "adv_pitch_batting_avg"}).get_text()
                        df.at[index,'ops'] = ops = pitcher.find("td", {"data-stat": "adv_pitch_onbase_plus_slugging"}).get_text()

                        df.at[index,'strkpct'] = strkpct = pitcher.find("td", {"data-stat": "adv_pitch_strikeout_perc"}).get_text().replace("%", "")
                        df.at[index,'bbpct'] = bbpct = pitcher.find("td", {"data-stat": "adv_pitch_base_on_balls_perc"}).get_text().replace("%", "")

                        df.at[index,'wpa'] = wpa = pitcher.find("td", {"data-stat": "adv_pitch_wpa_def"}).get_text()
                        df.at[index,'bors'] = bors = pitcher.find("td", {"data-stat": "adv_pitch_re24_def"}).get_text()





                    if stat == "standard":

                        df = df.append({'player_id': id}, ignore_index=True)

                        index = df.loc[df['player_id'] == id].index

                        df.at[index,'era'] = era = pitcher.find("td", {"data-stat": "earned_run_avg"}).get_text()
                        df.at[index,'strikeouts'] = strikeouts = pitcher.find("td", {"data-stat": "SO"}).get_text()
                        df.at[index,'era_plus'] = era_plus = pitcher.find("td", {"data-stat": "earned_run_avg_plus"}).get_text()
                        df.at[index,'fip'] = fip = pitcher.find("td", {"data-stat": "fip"}).get_text()
                        df.at[index,'whip'] = whip = pitcher.find("td", {"data-stat": "whip"}).get_text()
                        df.at[index,'bb_per_nine'] = bb_per_nine = pitcher.find("td", {"data-stat": "bases_on_balls_per_nine"}).get_text()
                        df.at[index,'strikeouts_per_nine'] = strikeouts_per_nine = pitcher.find("td", {"data-stat": "strikeouts_per_nine"}).get_text()


for year in range(start_year, end_year):

    link = f"https://www.baseball-reference.com/awards/awards_{year}.shtml#all_NL_CYA_voting"

    html = urlopen(link)
    bsObj = BeautifulSoup(html.read(), features="lxml")

    comments = bsObj.findAll(string=lambda text: isinstance(text, Comment))

    for c in comments:
        # convert the comment to BS Object
        c_string = BeautifulSoup(str(c), features="lxml")

        leagues = ["AL", "NL"]

        for league in leagues:

            pitchers = c_string.findAll("div", {"id": f"div_{league}_CYA_voting"})

            if pitchers:
                pitchers_string = BeautifulSoup(str(pitchers[0]), features="lxml")
                pitchers_string = pitchers_string.findAll("tr")

                for pitcher in pitchers_string:

                    name = pitcher.find("td", {"data-stat":"player"})


                    if name:
                        name = name.get_text()
                        id = re.sub('\s+', '', name) + str(year)

                        index = df.loc[df['player_id'] == id].index

                        df.at[index,'votes'] = votes = float(pitcher.find("td", {"data-stat":"points_won"}).get_text())

# For all the players that didn't recieve Cy Young votes, fill the value with a 0 not a NaN
df['votes'] = df['votes'].fillna(0)

df.to_csv("data.csv", encoding='utf-8', index=False)

