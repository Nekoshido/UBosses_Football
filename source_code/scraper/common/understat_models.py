# -*- coding: utf-8 -*-


class Performance(object):
    def __init__(self):
        """Player model class

        :rtype: object
        """
        self.name = ''
        self.ID = 0
        self.season = ''
        self.team = ''
        self.apps = 0
        self.min = 0
        self.goals = 0
        self.assist = 0
        self.shots = None
        self.KP = None
        self.sh90 = None
        self.kp90 = None
        self.xG = None
        self.xA = None
        self.xG90 = None
        self.xA90 = None
        self.xAKP = None
        self.ShxG = None


class Player(object):
    def __init__(self):
        self.name = ''
        self.ID = 0
        self.general = None
        self.performance_by_position = []
        self.performance_by_situation = []
        self.performance_by_shot_zones = []
        self.performance_by_shot_types = []
