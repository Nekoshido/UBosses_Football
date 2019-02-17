class Player(object):
    def __init__(self):
        """player model_class

        :rtype: object
        """       
        self.name = None
        self.team = None
        self.season = None
        self.birth = None
        self.position = None
        self.height = None
        self.weight = None
        self.nationality = None
        self.url = None
        self.number = None
        self.id = None
        self.competition = None

        # summary:

        self.appearances = None
        self.minutes_played = None
        self.goals = None
        self.assists = None
        self.yellow_cards = None
        self.red_cards = None
        self.shots_per_game = None
        self.pass_success_percentage = None
        self.aerials_duels_won_per_game = None
        self.man_of_the_match = None
        self.rating = None

        #defensive:
        
        self.tackles_per_game = None
        self.interceptions_per_game = None
        self.fouls_per_game = None
        self.offside_won_per_game = None
        self.clarances_per_game = None
        self.dribbled_past_per_game = None # /_player gets dribbled
        self.outfielder = None #/block_per_game
        self.own_goals = None

        #offesive:
        
        self.key_passes_per_game = None
        self.dribbles_per_game = None
        self.fouled_per_game = None
        self.offsides_per_game = None
        self.dispossessed_per_game = None
        self.bad_control_per_game = None

        #passing
        self.average_passes_per_game = None
        self.pass_success_percentage = None
        self.crosses_per_game = None
        self.long_balls_per_game = None
        self.through_balls_per_game = None

        #detailed [total]:
        self.total_tackles_won = None
        self.player_gets_dribbled = None
        self.total_tackle_attempts = None
        self.total_tackles_won_per90 = None
        self.player_gets_dribbled_per90 = None
        self.total_tackle_attempts_per90 = None

        self.interceptions = None
        self.interceptions_per90 = None

        self.fouled = None
        self.fouls = None
        self.fouled_per90 = None
        self.fouls_per90 = None

        self.total_yellow_cards = None
        self.total_red_cards = None
        self.total_yellow_cards_per90 = None
        self.total_red_cards_per90 = None

        self.caught_offside = None
        self.caught_offside_per90 = None

        self.total_clearances = None
        self.total_clearances_per90 = None

        self.blocked_shots = None
        self.blocked_crosses = None
        self.blocked_passes = None
        self.blocked_shots_per90 = None
        self.blocked_crosses_per90 = None
        self.blocked_passes_per90 = None

        self.gk_totalsaves = None
        self.gk_saves_insix_yard_box = None
        self.gk_saves_in_penalty_area = None
        self.gk_saves_from_outside_of_the_box = None
        self.gk_totalsaves_per90 = None
        self.gk_saves_insix_yard_box_per90 = None
        self.gk_saves_in_penalty_area_per90 = None
        self.gk_saves_from_outside_of_the_box_per90 = None

        self.total_shots = None
        self.shots_from_outside_the_penalty_area = None
        self.shots_from_inside_thesix_yard_box = None
        self.shots_from_inside_the_penalty_area = None #excludingsix yard box
        self.total_shots_per90 = None
        self.shots_from_outside_the_penalty_area_per90 = None
        self.shots_from_inside_thesix_yard_box_per90 = None
        self.shots_from_inside_the_penalty_area_per90 = None

        self.shot_open_play = None
        self.shot_counter = None
        self.shot_setpiece = None
        self.shot_penalty_taken = None
        self.shot_offtarget = None
        self.shot_onpost = None
        self.shot_ontarget = None
        self.shot_blocked = None
        self.shot_right_foot = None
        self.shot_left_foot = None
        self.shot_head = None
        self.shot_other = None

        self.shot_open_play_per90 = None
        self.shot_counter_per90 = None
        self.shot_setpiece_per90 = None
        self.shot_penalty_taken_per90 = None
        self.shot_offtarget_per90 = None
        self.shot_onpost_per90 = None
        self.shot_ontarget_per90 = None
        self.shot_blocked_per90 = None
        self.shot_right_foot_per90 = None
        self.shot_left_foot_per90 = None
        self.shot_head_per90 = None
        self.shot_other_per90 = None

        self.total_goal = None
        self.goals_from_inside_thesix_yard_box = None
        self.goals_from_inside_the_penalty_area = None# excludingsix yard box
        self.goals_from_outside_the_penalty_area = None
        self.total_goal_per90 = None
        self.goals_from_inside_thesix_yard_box_per90 = None
        self.goals_from_inside_the_penalty_area_per90 = None  # excludingsix yard box
        self.goals_from_outside_the_penalty_area_per90 = None

        self.goal_open_play = None
        self.goal_counter = None
        self.goal_setpiece = None
        self.goal_penaltyscored = None
        self.goal_own = None
        self.goal_normal = None
        self.goal_right_foot = None
        self.goal_left_foot = None
        self.goal_head = None
        self.goal_other = None
        self.goal_open_play_per90 = None
        self.goal_counter_per90 = None
        self.goal_setpiece_per90 = None
        self.goal_penaltyscored_per90 = None
        self.goal_own_per90 = None
        self.goal_normal_per90 = None
        self.goal_right_foot_per90 = None
        self.goal_left_foot_per90 = None
        self.goal_head_per90 = None
        self.goal_other_per90 = None

        self.unsuccessful_dribbles = None
        self.successful_dribbles = None
        self.total_dribbles = None
        self.unsuccessful_dribbles_per90 = None
        self.successful_dribbles_per90 = None
        self.total_dribbles_per90 = None

        self.unsuccessful_touches = None
        self.total_dispossessed = None
        self.unsuccessful_touches_per90 = None
        self.total_dispossessed_per_90 = None

        self.total_aerial_duels = None
        self.total_aerials_duels_won = None
        self.aerial_duels_lost = None
        self.total_aerial_duels_per_90 = None
        self.total_aerials_duels_won_per_90 = None
        self.aerial_duels_lost_per_90 = None


        self.total_passes = None
        self.accurate_long_balls = None
        self.inaccurate_long_balls = None
        self.accurate_short_passes = None
        self.inaccurate_short_passes = None
        self.total_passes_per_90 = None
        self.accurate_long_balls_per_90 = None
        self.inaccurate_long_balls_per_90 = None
        self.accurate_short_passes_per_90 = None
        self.inaccurate_short_passes_per_90 = None

        self.accurate_cross_passes = None
        self.inaccurate_cross_passes = None
        self.accurate_corner_passes = None
        self.inaccurate_corner_passes = None
        self.accurate_freekicks = None
        self.inaccurate_freekicks = None
        self.accurate_cross_passes_per_90 = None
        self.inaccurate_cross_passes_per_90 = None
        self.accurate_corner_passes_per_90 = None
        self.inaccurate_corner_passes_per_90 = None
        self.accurate_freekicks_per_90 = None
        self.inaccurate_freekicks_per_90 = None

        self.total_key_pass = None
        self.long_key_pass = None
        self.short_key_pass = None
        self.total_key_pass_per_90 = None
        self.long_key_pass_per_90 = None
        self.short_key_pass_per_90 = None

        self.key_pass_cross = None
        self.key_pass_corner = None
        self.key_pass_throughball = None
        self.key_pass_freekick = None
        self.key_pass_throwin = None
        self.key_passes_others = None
        self.key_pass_cross_per_90 = None
        self.key_pass_corner_per_90 = None
        self.key_pass_throughball_per_90 = None
        self.key_pass_freekick_per_90 = None
        self.key_pass_throwin_per_90 = None
        self.key_passes_others_per_90 = None

        self.cross_assist = None
        self.corner_assist = None
        self.throughball_assist = None
        self.freeckick_assist = None
        self.throw_in_assist = None
        self.other_assist = None
        self.cross_assist_per_90 = None
        self.corner_assist_per_90 = None
        self.throughball_assist_per_90 = None
        self.freeckick_assist_per_90 = None
        self.throw_in_assist_per_90 = None
        self.other_assist_per_90 = None

        self.total_assist_per_game = None
        self.total_assist_per_game_per_90 = None

    def __str__(self):
        return "Name: " + str(self.name) + "\n" + "Position: " + str(self.position) + "\n" + "Birth: " \
               + str(self.birth) + "\n" + "Height: " + str(self.height) + "\n" + "Weight: " + str(self.weight) \
               + "\n" + "Url: " + str(self.url) + "\n" + "Number: " + str(self.number) + "\n" + "ID: " + str(self.id)\
               + "\n" + "Team: " + str(self.team) + "\n" + "Season: " + str(self.season) + "\n" \
               + "Appearances: " + str(self.appearances) + "\n" + "Minutes_played: " + str(self.minutes_played) + "\n" \
               + "Goals: " + str(self.goals) + "\n" + "Assists: " + str(self.assists) + "\n" \
               + "Yellow_cards: " + str(self.yellow_cards) + "\n" + "Red_cards: " + str(self.red_cards) + "\n" \
               + "Shots_per_game: " + str(self.shots_per_game) + "\n" + "Pass_success_percentage: " + str(self.pass_success_percentage) + "\n"\
               + "Aerials_duels_won_per_game: " + str(self.aerials_duels_won_per_game) + "\n" + "Man_of_the_match: " + str(self.man_of_the_match) + "\n"\
               + "Tackles_per_game: " + str(self.tackles_per_game) + "\n" + "Tnterceptions_per_game: " + str(self.interceptions_per_game) + "\n" \
               + "Fouls_per_game: " + str(self.fouls_per_game) + "\n" + "Offside_won_per_game: " + str(self.offside_won_per_game) + "\n" \
               + "Clarances_per_game: " + str(self.clarances_per_game) + "\n" + "Dribbled_past_per_game: " + str(self.dribbled_past_per_game) + "\n" \
               + "Outfielder: " + str(self.outfielder) + "\n" + "Own_goals: " + str(self.own_goals) + "\n" \
               + "Key_passes_per_game: " + str(self.key_passes_per_game) + "\n" + "Dribbles_per_game: " + str(
                self.dribbles_per_game) + "\n" \
               + "Fouled_per_game: " + str(self.fouled_per_game) + "\n" + "Offsides_per_game: " + str(
                self.offsides_per_game) + "\n" \
               + "Dispossessed_per_game: " + str(self.dispossessed_per_game) + "\n" + "Bad_control_per_game: " + str(self.bad_control_per_game) + "\n" \
               + "Average_passes_per_game: " + str(self.average_passes_per_game) + "\n" + "Pass_success_percentage: " + str(
                self.pass_success_percentage) + "\n" \
               + "Crosses_per_game: " + str(self.crosses_per_game) + "\n" + "Long_balls_per_game: " + str(
                self.long_balls_per_game) + "\n" \
               + "Through_balls_per_game: " + str(self.through_balls_per_game) + "\n" + "Total_tackles_won: " + str(self.total_tackles_won) + "\n" \
               + "Player_gets_dribbled: " + str(self.player_gets_dribbled) + "\n" + "Total_tackle_attempts: " + str(
               self.total_tackle_attempts) + "\n" + "Interceptions: " + str(
               self.interceptions) + "\n" + "Fouled: " + str(
               self.fouled) + "\n" + "Fouls: " + str(
               self.fouls) + "\n" + "caught_offside: " + str(
               self.caught_offside) + "\n" + "total_clearances: " + str(
               self.total_clearances) + "\n" + "blocked_shots: " + str(
               self.blocked_shots) + "\n" + "blocked_passes: " + str(
               self.blocked_passes) + "\n" + "blocked_crosses: " + str(
               self.blocked_crosses) + "\n" + "gk_totalsaves: " + str(
               self.gk_totalsaves) + "\n" + "gk_saves_insix_yard_box: " + str(
               self.gk_saves_insix_yard_box) + "\n" + "gk_saves_in_penalty_area: " + str(
               self.gk_saves_in_penalty_area) + "\n" + "gk_saves_from_outside_of_the_box: " + str(
               self.gk_saves_from_outside_of_the_box) + "\n" + "shots_from_outside_the_penalty_area: " + str(
               self.shots_from_outside_the_penalty_area) + "\n" + "shots_from_inside_thesix_yard_box: " + str(
               self.shots_from_inside_thesix_yard_box) + "\n" + "shots_from_inside_the_penalty_area: " + str(
               self.shots_from_inside_the_penalty_area) + "\n" + "goals_from_inside_thesix_yard_box: " + str(
               self.goals_from_inside_thesix_yard_box) + "\n" + "goals_from_inside_the_penalty_area: " + str(
               self.goals_from_inside_the_penalty_area) + "\n" + "goals_from_outside_the_penalty_area: " + str(
               self.goals_from_outside_the_penalty_area) + "\n" + "unsuccessful_dribbles: " + str(
               self.unsuccessful_dribbles) + "\n" + "total_dribbles: " + str(
               self.total_dribbles) + "\n" + "unsuccessful_touches: " + str(
               self.unsuccessful_touches) + "\n" + "total_aerial_duels: " + str(
               self.total_aerial_duels) + "\n" + "aerial_duels_lost: " + str(
               self.aerial_duels_lost) + "\n" + "total_passes: " + str(
               self.total_passes) + "\n" + "aerial_duels_lost: " + str(
               self.aerial_duels_lost) + "\n" + "inaccurate_long_balls: " + str(
               self.inaccurate_long_balls) + "\n" + "accurate_short_passes: " + str(
               self.accurate_short_passes) + "\n" + "inaccurate_short_passes: " + str(
               self.inaccurate_short_passes) + "\n" + "long_key_pass: " + str(
               self.long_key_pass) + "\n" + "short_key_pass: " + str(
               self.short_key_pass) + "\n" + "cross_assist: " + str(
               self.cross_assist) + "\n" + "corner_assist: " + str(
               self.corner_assist) + "\n" + "throughball_assist: " + str(
               self.throughball_assist) + "\n" + "freeckick_assist: " + str(
               self.freeckick_assist) + "\n" + "throw_in_assist: " + str(
               self.throw_in_assist) + "\n" + "other_assist: " + str(
               self.other_assist) + "\n" + "total_assist_per_game: " + str(
               self.total_assist_per_game) + "\n"
