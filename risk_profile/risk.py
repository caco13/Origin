import json
from datetime import datetime


class Risk(object):
    INELIGIBLE = 'ineligible'
    MORTGAGED = 'mortgaged'
    MARRIED = 'married'
    ECONOMIC = 'economic'
    REGULAR = 'regular'
    RESPONSIBLE = 'responsible'
    AUTO = 'auto'
    DISABILITY = 'disability'
    HOME = 'home'
    LIFE = 'life'

    def __init__(self, user_data):
        self.user_data = user_data
        self.scores = {}
        self.risk = {}

    def evaluate(self):
        self._init_risk_scores()
        self._base_score()
        self._final_score()
        self._evaluate_risk()

        return self.risk

    def _init_risk_scores(self):
        for key in [self.AUTO, self.DISABILITY, self.HOME, self.LIFE]:
            self.scores[key] = 0
            self.risk[key] = ''

    def _base_score(self):
        initial_score = sum(self.user_data['risk_questions'])
        for key in [self.AUTO, self.DISABILITY, self.HOME, self.LIFE]:
            self.scores[key] = initial_score

    def _final_score(self):
        if self._disability_eligible():
            self._evaluate_disability_score()
        if self._auto_insurance_eligible():
            self._evaluate_auto_score()
        if self._home_insurance_eligible():
            self._evaluate_home_score()
        if self._life_insurance_eligible():
            self._evaluate_life_score()

    def _evaluate_risk(self):
        for key in [self.AUTO, self.DISABILITY, self.HOME, self.LIFE]:
            if self.risk[key] != self.INELIGIBLE:
                if self.scores[key] <= 0:
                    self.risk[key] = self.ECONOMIC
                elif 1 <= self.scores[key] <= 2:
                    self.risk[key] = self.REGULAR
                else:
                    self.risk[key] = self.RESPONSIBLE

    def _disability_eligible(self):
        if self.user_data['income'] < 1 or self.user_data['age'] > 60:
            self.risk[self.DISABILITY] = self.INELIGIBLE
            return False

        return True

    def _evaluate_disability_score(self):
        if self.user_data['age'] < 30:
            self.scores[self.DISABILITY] -= 2
        if 30 <= self.user_data['age'] < 40:
            self.scores[self.DISABILITY] -= 1
        if self.user_data['income'] > 200000:
            self.scores[self.DISABILITY] -= 1
        if self.user_data['house'] and \
                self.user_data['house']['ownership_status'] == self.MORTGAGED:
            self.scores[self.DISABILITY] += 1
        if self.user_data['dependents'] > 0:
            self.scores[self.DISABILITY] += 1
        if self.user_data['marital_status'] == self.MARRIED:
            self.scores[self.DISABILITY] -= 1

    def _auto_insurance_eligible(self):
        if not self.user_data['vehicle']:
            self.risk[self.AUTO] = self.INELIGIBLE
            return False

        return True

    def _evaluate_auto_score(self):
        if self.user_data['age'] < 30:
            self.scores[self.AUTO] -= 2
        if 30 <= self.user_data['age'] < 40:
            self.scores[self.AUTO] -= 1
        if self.user_data['income'] > 200000:
            self.scores[self.AUTO] -= 1
        if self.user_data['vehicle'] and \
                datetime.now().year - self.user_data['vehicle']['year'] <= 5:
            self.scores[self.AUTO] += 1

    def _home_insurance_eligible(self):
        if not self.user_data['house']:
            self.risk[self.HOME] = self.INELIGIBLE
            return False

        return True

    def _evaluate_home_score(self):
        if self.user_data['age'] < 30:
            self.scores[self.HOME] -= 2
        if 30 <= self.user_data['age'] < 40:
            self.scores[self.HOME] -= 1
        if self.user_data['income'] > 200000:
            self.scores[self.HOME] -= 1
        if self.user_data['house'] and \
                self.user_data['house']['ownership_status'] == self.MORTGAGED:
            self.scores[self.HOME] += 1

    def _life_insurance_eligible(self):
        if self.user_data['age'] > 60:
            self.risk[self.LIFE] = self.INELIGIBLE
            return False

        return True

    def _evaluate_life_score(self):
        if self.user_data['age'] < 30:
            self.scores[self.LIFE] -= 2
        if 30 <= self.user_data['age'] < 40:
            self.scores[self.LIFE] -= 1
        if self.user_data['income'] > 200000:
            self.scores[self.LIFE] -= 1
        if self.user_data['dependents'] > 0:
            self.scores[self.LIFE] += 1
        if self.user_data['marital_status'] == self.MARRIED:
            self.scores[self.LIFE] += 1

