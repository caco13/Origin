import json
from datetime import datetime


class Risk(object):
    INELEGIBLE = 'inelegible'
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
        self.init_risk_scores()
        self.base_score()
        self.final_score()
        self.evaluate_risk()

        return json.dumps(self.risk)

    def init_risk_scores(self):
        for key in [self.AUTO, self.DISABILITY, self.HOME, self.LIFE]:
            self.scores[key] = 0
            self.risk[key] = ''

    def base_score(self):
        initial_score = sum(self.user_data['risk_questions'])
        for key in [self.AUTO, self.DISABILITY, self.HOME, self.LIFE]:
            self.scores[key] = initial_score

    def final_score(self):
        if self.disability_eligible():
            self.evaluate_disability_score()
        if self.auto_insurance_eligible():
            self.evaluate_auto_score()
        if self.home_insurance_eligible():
            self.evaluate_home_score()
        if self.life_insurance_eligible():
            self.evaluate_life_score()

    def evaluate_risk(self):
        for key in [self.AUTO, self.DISABILITY, self.HOME, self.LIFE]:
            if self.risk[key] != self.INELEGIBLE:
                if self.scores[key] <= 0:
                    self.risk[key] = self.ECONOMIC
                elif 1 <= self.scores[key] <= 2:
                    self.risk[key] = self.REGULAR
                else:
                    self.risk[key] = self.RESPONSIBLE

    def disability_eligible(self):
        if self.user_data['income'] < 1 or self.user_data['age'] > 60:
            self.risk[self.DISABILITY] = self.INELEGIBLE
            return False

        return True

    def evaluate_disability_score(self):
        if self.user_data['age'] < 30:
            self.scores[self.DISABILITY] -= 2
        if 30 <= self.user_data['age'] < 40:
            self.scores[self.DISABILITY] -= 1
        if self.user_data['income'] > 200000:
            self.scores[self.DISABILITY] -= 1
        if self.user_data['house']['ownership_status'] and \
                self.user_data['house']['ownership_status'] == self.MORTGAGED:
            self.scores[self.DISABILITY] += 1
        if self.user_data['marital_status'] == self.MARRIED:
            self.scores[self.DISABILITY] -= 1

    def auto_insurance_eligible(self):
        if not self.user_data['vehicle']:
            self.risk[self.AUTO] = self.INELEGIBLE
            return False

        return True

    def evaluate_auto_score(self):
        if self.user_data['age'] < 30:
            self.scores[self.AUTO] -= 2
        if 30 <= self.user_data['age'] < 40:
            self.scores[self.AUTO] -= 1
        if self.user_data['income'] > 200000:
            self.scores[self.AUTO] -= 1
        if self.user_data['vehicle'] and \
                datetime.now().year - self.user_data['vehicle']['year'] <= 5:
            self.scores[self.AUTO] += 1

    def home_insurance_eligible(self):
        if not self.user_data['house']:
            self.risk[self.HOME] = self.INELEGIBLE
            return False

        return True

    def evaluate_home_score(self):
        if self.user_data['age'] < 30:
            self.scores[self.HOME] -= 2
        if 30 <= self.user_data['age'] < 40:
            self.scores[self.HOME] -= 1
        if self.user_data['income'] > 200000:
            self.scores[self.HOME] -= 1
        if self.user_data['house']['ownership_status'] and \
                self.user_data['house']['ownership_status'] == self.MORTGAGED:
            self.scores[self.HOME] += 1

    def life_insurance_eligible(self):
        if self.user_data['age'] > 60:
            self.risk[self.LIFE] = self.INELEGIBLE
            return False

        return True

    def evaluate_life_score(self):
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

