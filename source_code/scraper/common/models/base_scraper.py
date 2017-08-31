# -*- coding: utf-8 -*-
import abc


class BaseScraper(object):

    @abc.abstractmethod
    def load(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abc.abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abc.abstractmethod
    def save(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")


class StatsScraper(object):

    @abc.abstractmethod
    def get_all_seasons(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abc.abstractmethod
    def get_teams_for_seasons(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abc.abstractmethod
    def get_players_for_team(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abc.abstractmethod
    def create_team(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abc.abstractmethod
    def create_player(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")
