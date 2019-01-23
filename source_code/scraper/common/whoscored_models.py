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

        #detailed [per 90 mins]:
        
        self.total_tackles_won = None
        self.player_gets_dribbled = None
        self.total_tackle_attempts = None
        self.interceptions = None
        self.fouled = None
        self.fouls = None
        self.caught_offside = None
        self.total_clearances = None
        self.blocked_shots = None
        self.blocked_passes = None
        self.blocked_crosses = None
        self.gk_totalsaves = None
        self.gk_saves_insix_yard_box = None
        self.gk_saves_in_penalty_area = None
        self.gk_saves_from_outside_of_the_box = None
        self.shots_from_outside_the_penalty_area = None
        self.shots_from_inside_thesix_yard_box = None
        self.shots_from_inside_the_penalty_area = None #excludingsix yard box
        self.goals_from_outside_the_penalty_area = None
        self.goals_from_inside_thesix_yard_box = None
        self.goals_from_inside_the_penalty_area = None# excludingsix yard box
        self.unsuccessful_dribbles = None
        self.total_dribbles = None
        self.total_aerial_duels = None
        self.aerial_duels_lost = None
        self.total_passes = None
        self.inaccurate_long_balls = None
        self.accurate_short_passes = None
        self.inaccurate_short_passes = None
        self.long_key_pass = None
        self.short_key_pass = None
        self.cross_assist = None
        self.corner_assist = None
        self.throughball_assist = None
        self.freeckick_assist = None
        self.throw_in_assist = None
        self.other_assist = None
        self.total_assist_per_game = None