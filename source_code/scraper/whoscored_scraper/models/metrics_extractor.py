from typing import Tuple

from source_code.scraper.common import whoscored_models
from source_code.scraper.whoscored_scraper.models import constants_whoscored


def _clean_float(number):
    return 0 if number == "-" or number == 'N/A ' or number == 'N/A' else float(number)


def get_player_name(player_row):
    return player_row.find_element_by_class_name('player-link').get_attribute("innerText").strip('\t').split('\n')[1]


def get_player_list(browser, index: int):
    try:
        return browser.find_elements_by_id("player-table-statistics-body")[index].find_elements_by_tag_name('tr')
    except Exception as e:
        print("Exception: ", e)
        return None


def create_player(soup, player_row, competition):
    new_player = whoscored_models.Player()
    name = player_row.find('a', {'class': 'player-link'}).text.split("\t")[1]
    new_player.name = ''.join([i for i in name if not i.isdigit()])
    new_player.url = player_row.find('a', {'class': 'player-link'})['href']
    new_player.id = new_player.url.split('/')[2]
    new_player.nationality = player_row.find_all('td')[1].find('span')['class'][2].split('-')[1]
    new_player.season = int(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
    new_player.birth = int(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]) - int(
        player_row.find_all('span', {'class': 'player-meta-data'})[0].text)
    new_player.team = soup.find('span', {'class': 'team-header-name'}).text
    new_player.position = player_row.find_all('span', {'class': 'player-meta-data'})[1].text.split(' ')[2]
    new_player.height = _clean_float(player_row.find_all("td")[2].text)
    new_player.weight = _clean_float(player_row.find_all("td")[3].text)
    new_player.appearances = player_row.find_all("td")[4].text
    new_player.minutes_played = _clean_float(player_row.find_all("td")[5].text.strip('\t'))
    new_player.goals = _clean_float(player_row.find_all("td")[6].text.strip('\t'))
    new_player.assists = _clean_float(player_row.find_all("td")[7].text.strip('\t'))
    new_player.yellow_cards = _clean_float(player_row.find_all("td")[8].text.strip('\t'))
    new_player.red_cards = _clean_float(player_row.find_all("td")[9].text.strip('\t'))
    new_player.shots_per_game = _clean_float(player_row.find_all("td")[10].text.strip('\t'))
    new_player.pass_success_percentage_per_game = _clean_float(
        player_row.find_all("td")[11].text.strip('\t'))
    new_player.aerials_duels_won_per_game = _clean_float(player_row.find_all("td")[12].text.strip('\t'))
    new_player.man_of_the_match = _clean_float(player_row.find_all("td")[13].text.strip('\t'))
    new_player.rating = _clean_float(player_row.find_all("td")[14].text.strip('\t'))
    new_player.competition = competition.split('-')[0]
    return new_player


def defensive(player, player_row):
    player.tackles_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.interceptions_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.fouls_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.offside_won_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.clarances_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.dribbled_past_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
    player.outfielder = _clean_float(
        player_row.find_elements_by_tag_name("td")[12].get_attribute("innerHTML").strip('\t'))
    player.own_goals = _clean_float(
        player_row.find_elements_by_tag_name("td")[13].get_attribute("innerHTML").strip('\t'))
    return player


def offensive(player, player_row):
    player.key_passes_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.dribbles_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.fouled_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
    player.offsides_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[12].get_attribute("innerHTML").strip('\t'))
    player.dispossessed_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[13].get_attribute("innerHTML").strip('\t'))
    player.bad_control_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[14].get_attribute("innerHTML").strip('\t'))
    return player


def passing(player, player_row):
    player.average_passes_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.pass_success_percentage = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.crosses_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.long_balls_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
    player.through_balls_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[12].get_attribute("innerHTML").strip('\t'))
    return player


def tackles(player, player_row):
    player.total_tackles_won = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerText").strip('\t'))
    player.player_gets_dribbled = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerText").strip('\t'))
    player.total_tackle_attempts = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerText").strip('\t'))
    player.total_tackles_won_per90 = player.total_tackles_won / (player.minutes_played / 90.0)
    player.player_gets_dribbled_per90 = player.player_gets_dribbled / (player.minutes_played / 90.0)
    player.total_tackle_attempts_per90 = player.total_tackle_attempts / (player.minutes_played / 90.0)
    return player


def interceptions(player, player_row):
    player.interceptions = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerText").strip('\t'))
    player.interceptions_per90 = player.interceptions / (player.minutes_played / 90.0)
    return player


def fouls(player, player_row):
    player.fouled = _clean_float(player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.fouls = _clean_float(player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.fouled_per90 = player.fouled / player.minutes_played
    player.fouls_per90 = player.fouls / player.minutes_played
    return player


def cards(player, player_row):
    player.total_yellow_cards = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.total_red_cards = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.total_yellow_cards_per90 = player.total_yellow_cards / (player.minutes_played / 90.0)
    player.total_red_cards_per90 = player.total_red_cards / (player.minutes_played / 90.0)
    return player


def offside(player, player_row):
    player.caught_offside = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.caught_offside_per90 = player.caught_offside / (player.minutes_played / 90.0)
    return player


def clearances(player, player_row):
    player.total_clearances = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.total_clearances_per90 = player.total_clearances / (player.minutes_played / 90.0)
    return player


def blocks(player, player_row):
    player.blocked_shots = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.blocked_crosses = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.blocked_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.blocked_shots_per90 = player.blocked_shots / (player.minutes_played / 90.0)
    player.blocked_crosses_per90 = player.blocked_crosses / (player.minutes_played / 90.0)
    player.blocked_passes_per90 = player.blocked_passes / (player.minutes_played / 90.0)
    return player


def saves(player, player_row):
    player.gk_totalsaves = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.gk_saves_insix_yard_box = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.gk_saves_in_penalty_area = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.gk_saves_from_outside_of_the_box = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.gk_totalsaves_per90 = player.gk_totalsaves / (player.minutes_played / 90.0)
    player.gk_saves_insix_yard_box_per90 = player.gk_saves_insix_yard_box / (player.minutes_played / 90.0)
    player.gk_saves_in_penalty_area_per90 = player.gk_saves_in_penalty_area / (player.minutes_played / 90.0)
    player.gk_saves_from_outside_of_the_box_per90 = player.gk_saves_from_outside_of_the_box / (
            player.minutes_played / 90.0)
    return player


def shot_zones(player, player_row):
    player.total_shots = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.shots_from_outside_the_penalty_area = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.shots_from_inside_thesix_yard_box = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.shots_from_inside_the_penalty_area = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.total_shots_per90 = player.total_shots / (player.minutes_played / 90.0)
    player.shots_from_outside_the_penalty_area_per90 = player.shots_from_outside_the_penalty_area / (
            player.minutes_played / 90.0)
    player.shots_from_inside_thesix_yard_box_per90 = player.shots_from_inside_thesix_yard_box / (
            player.minutes_played / 90.0)
    player.shots_from_inside_the_penalty_area_per90 = player.shots_from_inside_the_penalty_area / (
            player.minutes_played / 90.0)
    return player


def shot_situations(player, player_row):
    player.shot_open_play = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.shot_counter = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.shot_setpiece = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.shot_penalty_taken = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.shot_open_play_per90 = player.shot_open_play / (player.minutes_played / 90.0)
    player.shot_counter_per90 = player.shot_counter / (player.minutes_played / 90.0)
    player.shot_setpiece_per90 = player.shot_setpiece / (player.minutes_played / 90.0)
    player.shot_penalty_taken_per90 = player.shot_penalty_taken / (player.minutes_played / 90.0)
    return player


def shot_accuracy(player, player_row):
    player.shot_offtarget = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.shot_onpost = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.shot_ontarget = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.shot_blocked = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.shot_offtarget_per90 = player.shot_offtarget / (player.minutes_played / 90.0)
    player.shot_onpost_per90 = player.shot_onpost / (player.minutes_played / 90.0)
    player.shot_ontarget_per90 = player.shot_ontarget / (player.minutes_played / 90.0)
    player.shot_blocked_per90 = player.shot_blocked / (player.minutes_played / 90.0)
    return player


def shot_body_parts(player, player_row):
    player.shot_right_foot = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.shot_left_foot = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.shot_head = _clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.shot_other = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.shot_right_foot_per90 = player.shot_right_foot / (player.minutes_played / 90.0)
    player.shot_left_foot_per90 = player.shot_left_foot / (player.minutes_played / 90.0)
    player.shot_head_per90 = player.shot_head / (player.minutes_played / 90.0)
    player.shot_other_per90 = player.shot_other / (player.minutes_played / 90.0)
    return player


def goal_zones(player, player_row):
    player.total_goal = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.goals_from_inside_thesix_yard_box = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.goals_from_inside_the_penalty_area = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.goals_from_outside_the_penalty_area = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.total_goal_per90 = player.total_goal / (player.minutes_played / 90.0)
    player.goals_from_inside_thesix_yard_box_per90 = player.goals_from_inside_thesix_yard_box / (
            player.minutes_played / 90.0)
    player.goals_from_inside_the_penalty_area_per90 = player.goals_from_inside_the_penalty_area / (
            player.minutes_played / 90.0)
    player.goals_from_outside_the_penalty_area_per90 = player.goals_from_outside_the_penalty_area / (
            player.minutes_played / 90.0)
    return player


def goal_situations(player, player_row):
    player.goal_open_play = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.goal_counter = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.goal_setpiece = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.goal_penaltyscored = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.goal_own = _clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
    player.goal_normal = _clean_float(
        player_row.find_elements_by_tag_name("td")[12].get_attribute("innerHTML").strip('\t'))
    player.goal_open_play_per90 = player.goal_open_play / (player.minutes_played / 90.0)
    player.goal_counter_per90 = player.goal_counter / (player.minutes_played / 90.0)
    player.goal_setpiece_per90 = player.goal_setpiece / (player.minutes_played / 90.0)
    player.goal_penaltyscored_per90 = player.goal_penaltyscored / (player.minutes_played / 90.0)
    player.goal_own_per90 = player.goal_own / (player.minutes_played / 90.0)
    player.goal_normal_per90 = player.goal_normal / (player.minutes_played / 90.0)
    return player


def goal_body_parts(player, player_row):
    player.goal_right_foot = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.goal_left_foot = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.goal_head = _clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.goal_other = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.goal_right_foot_per90 = player.goal_right_foot / (player.minutes_played / 90.0)
    player.goal_left_foot_per90 = player.goal_left_foot / (player.minutes_played / 90.0)
    player.goal_head_per90 = player.goal_head / (player.minutes_played / 90.0)
    player.goal_other_per90 = player.goal_other / (player.minutes_played / 90.0)
    return player


def dribbles(player, player_row):
    player.unsuccessful_dribbles = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.successful_dribbles = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.total_dribbles = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.unsuccessful_dribbles_per90 = player.unsuccessful_dribbles / (player.minutes_played / 90.0)
    player.successful_dribbles_per90 = player.successful_dribbles / (player.minutes_played / 90.0)
    player.total_dribbles_per90 = player.total_dribbles / (player.minutes_played / 90.0)
    return player


def possession_loss(player, player_row):
    player.unsuccessful_touches = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.total_dispossessed = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.unsuccessful_touches_per90 = player.unsuccessful_touches / (player.minutes_played / 90.0)
    player.total_dispossessed_per_90 = player.total_dispossessed / (player.minutes_played / 90.0)
    return player


def aerial(player, player_row):
    player.total_aerial_duels = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.total_aerials_duels_won = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.aerial_duels_lost = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.total_aerial_duels_per_90 = player.total_aerial_duels / (player.minutes_played / 90.0)
    player.total_aerials_duels_won_per_90 = player.total_aerials_duels_won / (player.minutes_played / 90.0)
    player.aerial_duels_lost_per_90 = player.aerial_duels_lost / (player.minutes_played / 90.0)
    return player


def pass_length(player, player_row):
    player.total_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.accurate_long_balls = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.inaccurate_long_balls = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.accurate_short_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.inaccurate_short_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.total_passes_per_90 = player.total_passes / (player.minutes_played / 90.0)
    player.accurate_long_balls_per_90 = player.accurate_long_balls / (player.minutes_played / 90.0)
    player.inaccurate_long_balls_per_90 = player.inaccurate_long_balls / (player.minutes_played / 90.0)
    player.accurate_short_passes_per_90 = player.accurate_short_passes / (player.minutes_played / 90.0)
    player.inaccurate_short_passes_per_90 = player.inaccurate_short_passes / (player.minutes_played / 90.0)
    return player


def pass_type(player, player_row):
    player.accurate_cross_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.inaccurate_cross_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.accurate_corner_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.inaccurate_corner_passes = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.accurate_freekicks = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.inaccurate_freekicks = _clean_float(
        player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
    player.accurate_cross_passes_per_90 = player.accurate_cross_passes / (player.minutes_played / 90.0)
    player.inaccurate_cross_passes_per_90 = player.inaccurate_cross_passes / (player.minutes_played / 90.0)
    player.accurate_corner_passes_per_90 = player.accurate_corner_passes / (player.minutes_played / 90.0)
    player.inaccurate_corner_passes_per_90 = player.inaccurate_corner_passes / (player.minutes_played / 90.0)
    player.accurate_freekicks_per_90 = player.accurate_freekicks / (player.minutes_played / 90.0)
    player.inaccurate_freekicks_per_90 = player.inaccurate_freekicks / (player.minutes_played / 90.0)
    return player


def key_passes_length(player, player_row):
    player.total_key_pass = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.long_key_pass = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.short_key_pass = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.total_key_pass_per_90 = player.total_key_pass / (player.minutes_played / 90.0)
    player.long_key_pass_per_90 = player.long_key_pass / (player.minutes_played / 90.0)
    player.short_key_pass_per_90 = player.short_key_pass / (player.minutes_played / 90.0)
    return player


def key_passes_type(player, player_row):
    player.key_pass_cross = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.key_pass_corner = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.key_pass_throughball = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.key_pass_freekick = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.key_pass_throwin = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.key_passes_others = _clean_float(
        player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
    player.key_pass_cross_per_90 = player.key_pass_cross / (player.minutes_played / 90.0)
    player.key_pass_corner_per_90 = player.key_pass_corner / (player.minutes_played / 90.0)
    player.key_pass_throughball_per_90 = player.key_pass_throughball / (player.minutes_played / 90.0)
    player.key_pass_freekick_per_90 = player.key_pass_freekick / (player.minutes_played / 90.0)
    player.key_pass_throwin_per_90 = player.key_pass_throwin / (player.minutes_played / 90.0)
    player.key_passes_others_per_90 = player.key_passes_others / (player.minutes_played / 90.0)
    return player


def assist(player, player_row):
    player.cross_assist = _clean_float(
        player_row.find_elements_by_tag_name("td")[6].get_attribute("innerHTML").strip('\t'))
    player.corner_assist = _clean_float(
        player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
    player.throughball_assist = _clean_float(
        player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
    player.freeckick_assist = _clean_float(
        player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
    player.throw_in_assist = _clean_float(
        player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
    player.other_assist = _clean_float(
        player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
    player.total_assist_per_game = _clean_float(
        player_row.find_elements_by_tag_name("td")[12].get_attribute("innerHTML").strip('\t'))
    player.cross_assist_per_90 = player.cross_assist / (player.minutes_played / 90.0)
    player.corner_assist_per_90 = player.corner_assist / (player.minutes_played / 90.0)
    player.throughball_assist_per_90 = player.throughball_assist / (player.minutes_played / 90.0)
    player.freeckick_assist_per_90 = player.freeckick_assist / (player.minutes_played / 90.0)
    player.throw_in_assist_per_90 = player.throw_in_assist / (player.minutes_played / 90.0)
    player.other_assist_per_90 = player.other_assist / (player.minutes_played / 90.0)
    player.total_assist_per_game_per_90 = player.total_assist_per_game / (player.minutes_played / 90.0)
    return player