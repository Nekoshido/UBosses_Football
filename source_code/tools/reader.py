import json
import os
from pathlib import Path

import pandas as pd
from pandas.io.json import json_normalize  # package for flattening json in pandas df

from source_code.tools.models.reader_utils import make_forward, make_midfield, make_centerback


def read_json(path) -> pd.DataFrame:
    first = True
    dataframe = None
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)
            if file.endswith('.json'):
                with open(os.path.join(root, file)) as json_file:
                    data = json.load(json_file)
                    team = json_normalize(data)
                    if first:
                        dataframe = team
                        first = False
                    else:
                        dataframe = dataframe.append(team)
                json_file.close()
    return dataframe


def read_csv(path):
    dataframe = pd.read_csv(path)
    return dataframe


def save_df_csv(dataframe: pd.DataFrame, path: str, name: str):
    # encoding='latin1'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    print(path + name)
    dataframe.to_csv(path + name + ".csv", sep=',', encoding='utf-8', index=False)


if __name__ == "__main__":
    file_name = 'final2022.csv'

    name = 'Ziyech'

    origin_path = f"{Path(__file__).parent.parent}/scraper/whoscored_scraper/files/"
    path_to_save = f"{Path(__file__).parent.parent}/scraper/whoscored_scraper/files/players/"

    dataframe = pd.read_csv(origin_path + file_name, encoding='utf-8')

    df_player, df_quantile_05, df_quantile_95 = make_forward(dataframe, name)
    # df_player, df_quantile_05, df_quantile_95 = make_midfield(dataframe, name, is_merged=True)
    # df_player, df_quantile_05, df_quantile_95 = make_fullback(dataframe, name)
    # df_player, df_quantile_05, df_quantile_95 = make_centerback(dataframe, name)

    # df_player = find_top_midfield_player(dataframe)
    # df_player = find_top_forward_player(dataframe)

    save_df_csv(df_player, path_to_save, name)
