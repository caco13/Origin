import json
from datetime import datetime


class Risk(object):
    INELEGIBLE = 'inelegible'
    MORTGAGED = 'mortgaged'
    MARRIED = 'married'
    ECONOMIC = 'economic'
    REGULAR = 'regular'
    RESPONSIBLE = 'responsible'

    def __init__(self, user_data):
        self.user_data = user_data
        self.auto_score = self.disability_score = self.home_score = self.life_score = 0

    def evaluate(self):
        self.final_score()

        risk = {'auto': self.auto_score, 'disability': self.disability_score, 'home': self.home_score, 'life': self.life_score}
        risk = self.evaluate_risk(risk)

        print(risk)  # DB

        return json.dumps(risk)

    def final_score(self):
        if self.user_data['income'] < 1 or not self.user_data['vehicle'] or not self.user_data['house']:
            self.auto_score = self.disability_score = self.home_score = self.INELEGIBLE
        if self.user_data['age'] > 60:
            self.disability_score = self.life_score = self.INELEGIBLE
        if self.user_data['age'] < 30:
            self.auto_score -= 2
            self.disability_score -= 2
            self.home_score -= 2
            self.life_score -= 2
        if 30 <= self.user_data['age'] < 40:
            self.auto_score -= 1
            self.disability_score -= 1
            self.home_score -= 1
            self.life_score -= 1
        if self.user_data['income'] > 200000:
            self.auto_score -= 1
            self.disability_score -= 1
            self.home_score -= 1
            self.life_score -= 1
        if self.user_data['house']['ownership_status'] and self.user_data['house']['ownership_status'] == self.MORTGAGED:
            self.home_score += 1
            self.disability_score += 1
        if self.user_data['dependents'] > 0:
            self.disability_score += 1
            self.life_score += 1
        if self.user_data['marital_status'] == self.MARRIED:
            self.life_score += 1
            self.disability_score -= 1
        if self.user_data['vehicle'] and self.user_data['vehicle']['year'] - datetime.now().year <= 5:
            self.auto_score += 1

    def evaluate_risk(self, risk):
        for key, value in risk.items():
            print(key, value)  # DB
            if value <= 0:
                risk[key] = self.ECONOMIC
            elif 1 <= value <= 2:
                risk[key] = self.REGULAR
            else:
                risk[key] = self.RESPONSIBLE

        return risk

