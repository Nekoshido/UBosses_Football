# -*- coding: utf-8 -*-
class Team(object):
    def __init__(self):
        self.name = ''
        self.player_id = 0
        self.full_name = ''

class Player(object):
    def __init__(self):
        """Player model class

        :rtype: object
        """
        self.name = ''
        self.player_id = 0
        self.full_name = ''
        self.birthday = ''
        self.place_of_birth = ''
        self.height = ''
        self.weight = ''
        self.size = ''
        self.value_list = []
        self.main_position = []
        self.other_positions = []
        self.agent = ''
        self.contract_renew = ''
        self.contract_expires = ''
        self.foot = ''
        self.main_nationality = ''
        self.nationalities = []
        self.outfitter = ''
        self.injuries = []

class PlayerPreview(object):
    def __init__(self):
        """Player model class

        :rtype: object
        """
        self.name = None
        self.player_id = None
        self.url = None
        self.birth = None
        self.position = None
        self.value = None
        self.number = None

    def __str__(self):
        return "Name: " + str(self.name) + "\n" + "Position: " + str(self.position) + "\n" + "Value: " \
               + str(self.value) + "\n" + "Birth: " + str(self.birth) + "\n" + "Url: " + str(self.url) + "\n" \
               + "Number: " + str(self.number) + "\n" + "ID: " + str(self.id) + "\n"

class Value(object):
    def __init__(self):
        self.club = ''
        self.player_name = ''
        self.age = ''
        self.date = ''
        self.market_value = ''
        self.currency = ''


class Competition(object):
    def __init__(self):
        self.season = ''
        self.name = ''
        self.matches = ''
        self.goals = ''
        self.assists = ''
        self.own_goals = ''
        self.subs_on = ''
        self.subs_off = ''
        self.yellow_card = ''
        self.yellow_red_card = ''
        self.red_card = ''
        self.penalty_goals = ''
        self.minutes_goal = ''
        self.minutes = ''


class Injuries(object):
    def __init__(self):
        self.season = ''
        self.name = ''
        self.since = ''
        self.until = ''
        self.days = 0
        self.games_missed = 0