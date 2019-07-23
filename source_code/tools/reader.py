import json
import pandas as pd
from pandas.io.json import json_normalize  # package for flattening json in pandas df
import glob, os

from sklearn import preprocessing

path = 'C:/Users/Hecto/PycharmProjects/UBosses_Football/source_code/scraper/whoscored_scraper/data/*/*/*/*'

dataframe = None
first = True
path = 'C:/Users/Hecto/PycharmProjects/UBosses_Football/source_code/scraper/whoscored_scraper/data/archive2'
coef_total_xG = 7971.108875359432 / 82665.99898016188
coef_inside_yard_box_xG = 1758.502254655629 / 5674.666768052864
coef_inside_penalty_area_xG = 5659.5889985826325 / 42973.62233200068
coef_outside_penalty_area_xG = 1147.9944651285803 / 33031.919089974275


def read_json(path):
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


def save_df_csv(dataframe, path):
    dataframe.to_csv(path, sep=',', encoding='latin1', index=False)


def make_midfield(dataframe, name=None):
    if name:
        dataframe = dataframe.loc[dataframe['name'].str.contains(name)]
    df_midfield = dataframe.loc[dataframe['position'].str.contains("DMC|Midfielder|M\(C")]
    df_midfield["custom_passing"] = ((df_midfield["accurate_long_balls"] + df_midfield["accurate_short_passes"]) / (
            df_midfield["accurate_long_balls"] + df_midfield["accurate_short_passes"] + df_midfield[
        "inaccurate_long_balls"] + df_midfield["inaccurate_short_passes"])) * 100
    # accurate_long_balls_per_90
    # custom_passing
    # chances_created = total_key_pass_per_90
    # key_pass_throughball_per_90
    # scoring contribution
    df_midfield["tt_goal_wP_per_90"] = ((df_midfield["goals"] - df_midfield["goal_penaltyscored"]) / df_midfield[
        "minutes_played"]) * 90.0
    df_midfield["scoring_contribution"] = df_midfield["tt_goal_wP_per_90"] + df_midfield["total_assist_per_game_per_90"]
    # successful_dribbles_per90
    # total_dispossessed_per_90
    # fouls_per90
    df_midfield["fouls_per90"] = (df_midfield["fouls"] / df_midfield["minutes_played"]) * 90.0
    # Tackles/was dribbled * 100 = total_tackles_won_per90/player_gets_dribbled_per90 * 100
    df_midfield["tackles_accuracy"] = (df_midfield["total_tackles_won"] / df_midfield["total_tackle_attempts"]) * 100
    # total_tackles_won_per90
    # interceptions_per90
    df_midfield["interceptions_per90"] = (df_midfield["interceptions"] / df_midfield["minutes_played"]) * 90.0
    important_columns = ["scoring_contribution", "key_pass_throughball_per_90", "total_key_pass_per_90",
                         "custom_passing", "accurate_long_balls_per_90", "interceptions_per90",
                         "total_tackles_won_per90", "tackles_accuracy", "fouls_per90",
                         "total_dispossessed_per_90", "successful_dribbles_per90"]

    variables = ("Scoring contribution", "Through ball", "Chances created",
                 "% Passing", "Long Balls", "Interceptions",
                 "Tackles", "Tackles accuracy", "Fouls",
                 "Dispossessed", "Successful Dribbles")

    tag_columns = ["name", "team", "season", "competition", "minutes_played"]
    df_midfield_return = df_midfield[tag_columns + important_columns]
    df_quantile_05 = df_midfield[important_columns].quantile(.05)
    df_quantile_95 = df_midfield[important_columns].quantile(.95)
    return df_midfield_return, df_quantile_05, df_quantile_95


def make_fullback(dataframe, name=None):
    if name:
        dataframe = dataframe.loc[dataframe['name'].str.contains(name)]
    dataframe = dataframe.loc[dataframe['minutes_played'] > 300.0]
    df_fullback = dataframe.loc[dataframe['position'].str.contains("D\(L|D\(R|D\(CR|D\(CR|D\(CL")]
    df_fullback = df_fullback.assign(
        passing_percentage=(((df_fullback["accurate_long_balls"] + df_fullback["accurate_short_passes"]) / (
                df_fullback["accurate_long_balls"] + df_fullback["accurate_short_passes"] + df_fullback[
            "inaccurate_long_balls"] + df_fullback["inaccurate_short_passes"])) * 100))

    # df_fullback = df_fullback.assign(crossing_percentage=((df_fullback["accurate_cross_passes"] / df_fullback[
    #     "inaccurate_cross_passes"]) * 100.0))

    df_fullback.loc[df_fullback.inaccurate_cross_passes != 0, 'crossing_percentage'] = ((df_fullback["accurate_cross_passes"] / (df_fullback[
        "inaccurate_cross_passes"] + df_fullback["accurate_cross_passes"])) * 100.0)

    df_fullback.loc[df_fullback.inaccurate_cross_passes == 0, 'crossing_percentage'] = 0.0

    # df_fullback = df_fullback.assign(crossing_percentage=((df_fullback["accurate_cross_passes"] / df_fullback[
    #     "minutes_played"]) * 90.0))

    df_fullback = df_fullback.assign(fouls_per90=((df_fullback["fouls"] / df_fullback["minutes_played"]) * 90.0))
    # Tackles/was dribbled * 100 = total_tackles_won_per90/player_gets_dribbled_per90 * 100
    # df_fullback = df_fullback.assign(tackles_accuracy=((df_fullback["total_tackles_won"] / df_fullback["total_tackle_attempts"]) * 100))

    df_fullback.loc[df_fullback.total_tackle_attempts != 0, 'tackles_accuracy'] = ((df_fullback["total_tackles_won"] / df_fullback["total_tackle_attempts"]) * 100)

    df_fullback.loc[df_fullback.total_tackle_attempts == 0, 'tackles_accuracy'] = 0.0

    df_fullback = df_fullback.assign(interceptions_per90=(df_fullback["interceptions"] / df_fullback["minutes_played"]) * 90.0)
    important_columns = ["total_tackles_won_per90", "tackles_accuracy", "interceptions_per90",
                         "passing_percentage", "total_key_pass_per_90", "accurate_cross_passes_per_90",
                         "crossing_percentage", "successful_dribbles_per90", "total_dispossessed_per_90",
                         "total_aerials_duels_won_per_90", "player_gets_dribbled_per90", "fouls_per90", ]

    tag_columns = ["name", "team", "season", "competition", "minutes_played"]
    # print(df_fullback.columns.values)
    # min_max_scaler = preprocessing.MinMaxScaler()
    # scaled_array = min_max_scaler.fit_transform(df_fullback[important_columns])
    # df_normalized = pd.DataFrame(scaled_array)
    df_quantile_01 = df_fullback[important_columns].quantile(.01)
    df_quantile_99 = df_fullback[important_columns].quantile(.99)
    df_fullback[important_columns] = (df_fullback[important_columns] - df_quantile_01[important_columns]) / (df_quantile_99[important_columns] - df_quantile_01[important_columns])
    df_fullback_return = df_fullback[tag_columns + important_columns]
    return df_fullback_return


    df_quantile_05 = df_fullback[important_columns].quantile(.05)
    df_quantile_95 = df_fullback[important_columns].quantile(.95)
    return df_fullback_return, df_quantile_05, df_quantile_95


#
#
#
# dataframe["total_goal_withoutPenalty"] = dataframe["goals"] - (
#             dataframe["goal_penaltyscored"] * dataframe["minutes_played"] / 90.0)
# dataframe["total_goals_from_inside_thesix_yard_box"] = dataframe["goals_from_inside_thesix_yard_box"] * dataframe[
#     "minutes_played"] / 90.0
# dataframe["total_goals_from_inside_the_penalty_area"] = dataframe["goals_from_inside_the_penalty_area"] * dataframe[
#     "minutes_played"] / 90.0
# dataframe["total_goals_from_outside_the_penalty_area"] = dataframe["goals_from_outside_the_penalty_area"] * dataframe[
#     "minutes_played"] / 90.0
#
# dataframe["total_shots"] = dataframe["total_shots_per_90"] * dataframe["minutes_played"] / 90.0
# dataframe["total_shots_from_inside_thesix_yard_box"] = dataframe["shots_from_inside_thesix_yard_box"] * dataframe[
#     "minutes_played"] / 90.0
# dataframe["total_shots_from_inside_the_penalty_area"] = (dataframe["shots_from_inside_the_penalty_area"] * dataframe[
#     "minutes_played"] / 90.0) - (dataframe["shot_penalty_taken"] * dataframe["minutes_played"] / 90.0)
# dataframe["total_shots_from_outside_the_penalty_area"] = dataframe["shots_from_outside_the_penalty_area"] * dataframe[
#     "minutes_played"] / 90.0
#
# coef_total_xG = 7971.108875359432 / 82665.99898016188
# coef_inside_yard_box_xG = 1758.502254655629 / 5674.666768052864
# coef_inside_penalty_area_xG = 5659.5889985826325 / 42973.62233200068
# coef_outside_penalty_area_xG = 1147.9944651285803 / 33031.919089974275
#
# dataframe["xG"] = (dataframe["total_shots_from_inside_thesix_yard_box"] * coef_inside_yard_box_xG) + (
#             dataframe["total_shots_from_inside_the_penalty_area"] * coef_inside_penalty_area_xG) + (
#                               dataframe["total_shots_from_outside_the_penalty_area"] * coef_outside_penalty_area_xG)
#
# dataframe["custom_passing"] = ((dataframe["accurate_long_balls"] + dataframe["accurate_short_passes"]) / (
#             dataframe["accurate_long_balls"] + dataframe["accurate_short_passes"] + dataframe["inaccurate_long_balls"] +
#             dataframe["inaccurate_short_passes"])) * 100
#

#
# final_df_forward = df_forward[['name', 'total_goal_withoutPenalty', 'xG']]

def make_forward(dataframe, name=None):
    if name:
        dataframe = dataframe.loc[dataframe['name'].str.contains(name)]
    # dataframe = dataframe.loc[dataframe['minutes_played'] > 1000.0]
    # dataframe = dataframe.loc[dataframe['season'] > 2016]
    df_forward = dataframe.loc[dataframe['position'].str.contains("AM|FW")]
    # "% Passing"\
    df_forward["custom_passing"] = ((df_forward["accurate_long_balls"] + df_forward["accurate_short_passes"]) / (
            df_forward["accurate_long_balls"] + df_forward["accurate_short_passes"] + df_forward[
        "inaccurate_long_balls"] +
            df_forward["inaccurate_short_passes"])) * 100
    # "% Shooting" \
    df_forward["shot_percentage"] = (df_forward["total_shots"] - df_forward["shot_offtarget"]) / df_forward[
        "total_shots"]
    # "Shots", total_shots_per90
    # "Non-Penalty Goals",\
    df_forward["xG"] = (df_forward["shots_from_inside_thesix_yard_box"] * coef_inside_yard_box_xG) + (
            df_forward["shots_from_inside_the_penalty_area"] * coef_inside_penalty_area_xG) + (
                               df_forward["shots_from_outside_the_penalty_area"] * coef_outside_penalty_area_xG)
    df_forward["xG_per90"] = (df_forward["xG"] / df_forward["minutes_played"]) * 90.0
    # "% Goal Conversion",\
    df_forward["goal_conversion"] = df_forward["xG_per90"] / df_forward["total_shots_per90"]
    # "Successful Dribbles", successful_dribbles_per90
    # "Dispossessed" \ total_dispossessed_per_90
    # "Int+Tackles"\ interceptions_per90 +total_tackles_won_per90
    df_forward["interceptions_per90"] = (df_forward["interceptions"] / df_forward["minutes_played"]) * 90.0
    df_forward["total_tackles_won_per90"] = (df_forward["total_tackles_won"] / df_forward["minutes_played"]) * 90.0
    df_forward["tackles_interceptions_per90"] = df_forward["interceptions_per90"] + df_forward[
        "total_tackles_won_per90"]
    # "Throughballs"-> total_aerials_duels_won_per_90 // key_pass_throughball_per_90
    # "Key Passes"\ total_key_pass_per_90
    # "Assists" \ total_assist_per_game_per_90

    variables = ("% Passing", "% Shooting", "Shots",
                 "Non-Penalty Goals", "% Goal Conversion", "Successful Dribbles",
                 "Dispossessed", "Int+Tackles", "Throughballs",
                 "Key Passes", "Assists")

    important_columns = ["custom_passing", "shot_percentage", "total_shots_per90",
                         "xG_per90", "goal_conversion", "successful_dribbles_per90",
                         "total_dispossessed_per_90", "tackles_interceptions_per90", "key_pass_throughball_per_90",
                         "total_key_pass_per_90", "total_assist_per_game_per_90"]

    tag_columns = ["name", "team", "season", "competition", "minutes_played"]
    df_forward_return = df_forward[tag_columns + important_columns]
    df_quantile_05 = df_forward[important_columns].quantile(.05)
    df_quantile_95 = df_forward[important_columns].quantile(.95)
    return df_forward_return, df_quantile_05, df_quantile_95


file_name = 'final_s2019.csv'
path = 'C:/Users/Hecto/PycharmProjects/UBosses_Football/source_code/scraper/whoscored_scraper/data/'
dataframe = pd.read_csv(path + file_name, encoding='latin-1')

values_list = list(dataframe.columns.values)

float_list = ['accurate_corner_passes', 'accurate_corner_passes_per_90', 'accurate_cross_passes',
              'accurate_cross_passes_per_90', 'accurate_freekicks', 'accurate_freekicks_per_90', 'accurate_long_balls',
              'accurate_long_balls_per_90', 'accurate_short_passes', 'accurate_short_passes_per_90',
              'aerial_duels_lost', 'aerial_duels_lost_per_90', 'aerials_duels_won_per_game', 'assists',
              'average_passes_per_game', 'bad_control_per_game', 'birth', 'blocked_crosses', 'blocked_crosses_per90',
              'blocked_passes', 'blocked_passes_per90', 'blocked_shots', 'blocked_shots_per90', 'caught_offside',
              'caught_offside_per90', 'clarances_per_game', 'corner_assist', 'corner_assist_per_90',
              'cross_assist', 'cross_assist_per_90', 'crosses_per_game', 'dispossessed_per_game',
              'dribbled_past_per_game', 'dribbles_per_game', 'fouled', 'fouled_per90', 'fouled_per_game', 'fouls',
              'fouls_per90', 'fouls_per_game', 'freeckick_assist', 'freeckick_assist_per_90',
              'gk_saves_from_outside_of_the_box', 'gk_saves_from_outside_of_the_box_per90', 'gk_saves_in_penalty_area',
              'gk_saves_in_penalty_area_per90', 'gk_saves_insix_yard_box', 'gk_saves_insix_yard_box_per90',
              'gk_totalsaves', 'gk_totalsaves_per90', 'goal_counter', 'goal_counter_per90', 'goal_head',
              'goal_head_per90', 'goal_left_foot', 'goal_left_foot_per90', 'goal_normal', 'goal_normal_per90',
              'goal_open_play', 'goal_open_play_per90', 'goal_other', 'goal_other_per90', 'goal_own', 'goal_own_per90',
              'goal_penaltyscored', 'goal_penaltyscored_per90', 'goal_right_foot', 'goal_right_foot_per90',
              'goal_setpiece', 'goal_setpiece_per90', 'goals', 'goals_from_inside_the_penalty_area',
              'goals_from_inside_the_penalty_area_per90', 'goals_from_inside_thesix_yard_box',
              'goals_from_inside_thesix_yard_box_per90', 'goals_from_outside_the_penalty_area',
              'goals_from_outside_the_penalty_area_per90', 'height', 'inaccurate_corner_passes',
              'inaccurate_corner_passes_per_90', 'inaccurate_cross_passes', 'inaccurate_cross_passes_per_90',
              'inaccurate_freekicks', 'inaccurate_freekicks_per_90', 'inaccurate_long_balls',
              'inaccurate_long_balls_per_90', 'inaccurate_short_passes', 'inaccurate_short_passes_per_90',
              'interceptions', 'interceptions_per90', 'interceptions_per_game', 'key_pass_corner',
              'key_pass_corner_per_90', 'key_pass_cross', 'key_pass_cross_per_90', 'key_pass_freekick',
              'key_pass_freekick_per_90', 'key_pass_throughball', 'key_pass_throughball_per_90', 'key_pass_throwin',
              'key_pass_throwin_per_90', 'key_passes_others', 'key_passes_others_per_90', 'key_passes_per_game',
              'long_balls_per_game', 'long_key_pass', 'long_key_pass_per_90', 'man_of_the_match', 'minutes_played',
              'offside_won_per_game', 'offsides_per_game', 'other_assist',
              'other_assist_per_90', 'outfielder', 'own_goals', 'pass_success_percentage', 'player_gets_dribbled',
              'player_gets_dribbled_per90', 'rating', 'red_cards', 'season', 'short_key_pass',
              'short_key_pass_per_90', 'shot_blocked', 'shot_blocked_per90', 'shot_counter', 'shot_counter_per90',
              'shot_head', 'shot_head_per90', 'shot_left_foot', 'shot_left_foot_per90', 'shot_offtarget',
              'shot_offtarget_per90', 'shot_onpost', 'shot_onpost_per90', 'shot_ontarget', 'shot_ontarget_per90',
              'shot_open_play', 'shot_open_play_per90', 'shot_other', 'shot_other_per90', 'shot_penalty_taken',
              'shot_penalty_taken_per90', 'shot_right_foot', 'shot_right_foot_per90', 'shot_setpiece',
              'shot_setpiece_per90', 'shots_from_inside_the_penalty_area', 'shots_from_inside_the_penalty_area_per90',
              'shots_from_inside_thesix_yard_box', 'shots_from_inside_thesix_yard_box_per90',
              'shots_from_outside_the_penalty_area', 'shots_from_outside_the_penalty_area_per90', 'shots_per_game',
              'successful_dribbles', 'successful_dribbles_per90', 'tackles_per_game', 'through_balls_per_game',
              'throughball_assist', 'throughball_assist_per_90', 'throw_in_assist', 'throw_in_assist_per_90',
              'total_aerial_duels', 'total_aerial_duels_per_90', 'total_aerials_duels_won',
              'total_aerials_duels_won_per_90', 'total_assist_per_game', 'total_assist_per_game_per_90',
              'total_clearances', 'total_clearances_per90', 'total_dispossessed', 'total_dispossessed_per_90',
              'total_dribbles', 'total_dribbles_per90', 'total_goal', 'total_goal_per90', 'total_key_pass',
              'total_key_pass_per_90', 'total_passes', 'total_passes_per_90', 'total_red_cards',
              'total_red_cards_per90', 'total_shots', 'total_shots_per90', 'total_tackle_attempts',
              'total_tackle_attempts_per90', 'total_tackles_won', 'total_tackles_won_per90', 'total_yellow_cards',
              'total_yellow_cards_per90', 'unsuccessful_dribbles', 'unsuccessful_dribbles_per90',
              'unsuccessful_touches', 'unsuccessful_touches_per90', 'weight', 'yellow_cards']

#
#
dataframe[float_list] = dataframe[float_list].replace(['-'], '0')
dataframe[float_list] = dataframe[float_list].astype(float)

name = "Correa"
df_player, df_quantile_05, df_quantile_95 = make_forward(dataframe, name)
#df_player, df_quantile_05, df_quantile_95 = make_midfield(dataframe, name)
# df_player, df_quantile_05, df_quantile_95 = make_fullback(dataframe, name)

# print("Quantile 5% Worst")
# print(df_quantile_05)
# print("Quantile 5% Best")
# print(df_quantile_95)

print(df_player)

df_player.to_csv(
    'C:/Users/Hecto/PycharmProjects/UBosses_Football/source_code/scraper/whoscored_scraper/data/players/' + name + '.csv',
    sep=',', index=False)
