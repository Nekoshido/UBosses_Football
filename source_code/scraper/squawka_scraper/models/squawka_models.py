# -*- coding: utf-8 -*-


class Player(object):
    def __init__(self):
        self.name = ''
        self.ID = 0
        self.position_sw = ''
        self.position_trnfmrkt = ''
        self.team = ''

        self.age = ''
        self.height = ''
        self.weight = ''
        self.year = ''

        self.swn_score = ''
        self.swn_score_list = []

        self.app_tot = ''
        self.app_full = ''
        self.app_sub_on = ''
        self.app_sub_off = ''

        self.goals = []
        self.goal_tot = 0
        self.goal_right = 0
        self.goal_left = 0
        self.goal_head = 0
        self.goal_other = 0

        self.shot_acc = 0
        self.shot_on = 0
        self.shot_off = 0
        self.shot_block = 0
        self.shot_conv = 0
        self.shot_fail = 0

        self.tt_chances_created = 0
        self.assist = 0
        self.key_passes = 0
        self.tt_chan_pitch = []

        self.avg_pass_acc = 0
        self.succ_pass = 0
        self.unsucc_pass = 0
        self.succ_long_balls = 0
        self.unsucc_long_balls = 0
        self.succ_head_pass = 0
        self.unsucc_head_pass = 0
        self.succ_through_ball = 0
        self.unsucc_through_ball = 0
        self.succ_cross_ball = 0
        self.unsucc_cross_ball = 0
        self.pass_forward = 0
        self.pass_backward = 0

        self.avg_pass_length = 0
        self.avg_long_ball_length = 0
        self.avg_back_pass_length = 0
        self.avg_forw_pass_length = 0

        self.avg_duels_won = 0
        self.succ_tackle = 0
        self.unsucc_tackle = 0
        self.suff_foul = 0
        self.comm_foul = 0
        self.succ_take_on = 0
        self.unsucc_take_on = 0
        self.succ_head_duel = 0
        self.unsucc_head_duel = 0

        self.avg_def_act = 0
        self.def_clear = 0
        self.interception = 0
        self.block = 0

        self.total_def_err = 0
        self.led_attempt_goal = 0
        self.led_goal = 0

        self.tot_yel_card = 0
        self.viol_yel_card = 0
        self.tack_yel_card = 0
        self.verb_yel_card = 0
        self.oth_yel_card = 0
        self.tot_red_card = 0
        self.viol_red_card = 0
        self.tack_red_card = 0
        self.verb_red_card = 0
        self.oth_red_card = 0

    def __unicode__(self):
        string = 'Name: ' + self.name + '\n'
        string = string + 'Appearance: ' + str(self.app_tot) + '\n'
        string = string + 'Goals: ' + str(self.goal_tot) + '\n'
        string = string + 'Shot Accuracy: ' + str(self.shot_acc) + '\n'
        string = string + 'Total Chances: ' + str(self.tt_chances_created) + '\n'
        string = string + 'Pass Accuracy: ' + str(self.avg_pass_acc) + '\n'
        string = string + 'Pass length: ' + str(self.avg_pass_length) + '\n'
        string = string + 'Duels Won: ' + str(self.avg_duels_won) + '\n'
        string = string + 'Defensive Actions: ' + str(self.avg_def_act) + '\n'
        string = string + 'Defensive Errors: ' + str(self.total_def_err) + '\n'
        string = string + 'Yellow/Red Cards: ' + str(self.tot_yel_card) + '/' + str(self.tot_red_card) + '\n'
        return string


class Goalkeeper(object):
    def __init__(self):
        self.name = ''
        self.ID = 0
        self.position_sw = ''
        self.position_trnfmrkt = ''
        self.team = ''

        self.age = ''
        self.height = ''
        self.weight = ''
        self.year = ''

        self.swn_score = ''
        self.swn_score_list = []

        self.app_tot = ''
        self.app_full = ''
        self.app_sub_on = ''
        self.app_sub_off = ''

        self.clean_sheets = 0
        self.goal_conceed = []
        self.total_goal_conceed = 0

        self.avg_goals_conceed = 0
        self.goals_corner = 0
        self.goals_set_piece_crosses = 0
        self.goals_direct_free_kicks = 0
        self.goals_open_play = 0
        self.goals_open_play_outside_box = 0
        self.goals_others = 0
        self.total_goal_conceed2 = 0
        self.goals_zone = []

        self.avg_saves_per_game = 0
        self.saves_per_game_list = []
        self.num_saves = 0
        self.saves_position_list = []
        self.num_saves2 = 0
        self.penalties_conceded = 0
        self.penalties_saved = 0
        self.penalties_list = []

        self.avg_saves_per_goal = 0
        self.saves_per_goal_list = []
        self.total_saves_goal = 0

        self.avg_claims_success = 0
        self.claims_success_list = []
        self.tot_claims_success = 0
        self.claims_fail_list = []
        self.tot_claims_fail = 0

        self.avg_punches = 0
        self.punches_success_list = []
        self.tot_punches_success = 0
        self.punches_fail_list = []
        self.tot_punches_fail = 0

        self.avg_dist_succ = 0
        self.succ_goal_kicks = 0
        self.unsucc_goal_kicks = 0
        self.succ_kicks_from_hands = 0
        self.unsucc_kicks_from_hands = 0
        self.succ_threw_out = 0
        self.unsucc_threw_out = 0
        self.succ_other = 0
        self.unsucc_other = 0

        self.dis_length = 0
        self.goal_kicks_length = 0
        self.kicks_from_hands = 0
        self.threw_out_length = 0
        self.other_length = 0

        self.tot_yel_card = 0
        self.viol_yel_card = 0
        self.tack_yel_card = 0
        self.verb_yel_card = 0
        self.oth_yel_card = 0
        self.tot_red_card = 0
        self.viol_red_card = 0
        self.tack_red_card = 0
        self.verb_red_card = 0
        self.oth_red_card = 0

    def __unicode__(self):
        string = 'Name: ' + self.name + '\n'
        string = string + 'Appearance: ' + str(self.app_tot) + '\n'
        string = string + 'Clean Sheets: ' + str(self.clean_sheets) + '\n'
        string = string + 'Avg Goals Conceed: ' + str(self.avg_goals_conceed) + '\n'
        string = string + 'Avg Saves per Game: ' + str(self.avg_saves_per_game) + '\n'
        string = string + 'Avg Saves per Goal: ' + str(self.avg_saves_per_goal) + '\n'
        string = string + 'Avg Claim Success: ' + str(self.avg_claims_success) + '\n'
        string = string + 'Avg Punches: ' + str(self.avg_punches) + '\n'
        string = string + 'Dist Success: ' + str(self.avg_dist_succ) + '\n'
        string = string + 'Dist Length: ' + str(self.dis_length) + '\n'
        string = string + 'Yellow/Red Cards: ' + str(self.tot_yel_card) + '/' + str(self.tot_red_card) + '\n'
        return string
