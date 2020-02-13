import json

from django.test import TestCase

from risk_profile.risk import Risk


class RiskTest(TestCase):
    def setUp(self):
        self.user_data = {
            'age': 20, 'dependents': 1,
            'house': {'ownership_status': 'mortgaged'}, 'income': 100000,
            'marital_status': 'married', 'risk_questions': [0, 0, 0],
            'vehicle': {'year': 2005}
        }

    def test_risk_profile_scenario_1(self):
        """Scenario 1:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_2(self):
        """Scenario 2:
            30 <= age < 40
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['age'] = 35

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'regular'
        }, json.loads(result))

    def test_risk_profile_scenario_3(self):
        """Scenario 3:
            40 <= age <= 60
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['age'] = 50

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'regular', 'home': 'regular',
            'life': 'regular'
        }, json.loads(result))

    def test_risk_profile_scenario_4(self):
        """Scenario 4:
            age > 60
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['age'] = 61

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'ineligible', 'home': 'regular',
            'life': 'ineligible'
        }, json.loads(result))

    def test_risk_profile_scenario_5(self):
        """Scenario 5:
            0 <= age < 30
            dependents = 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['dependents'] = 0

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_6(self):
        """Scenario 6:
            0 <= age < 30
            dependents > 0
            house = owned
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['house']['ownership_status'] = 'owned'

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_7(self):
        """Scenario 7:
            0 <= age < 30
            dependents > 0
            house = 0
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['house'] = {}

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'ineligible',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_8(self):
        """Scenario 8:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income > 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['income'] = 300000

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_9(self):
        """Scenario 9:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income = 0
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['income'] = 0

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'ineligible', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_10(self):
        """Scenario 10:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = single
            risk_questions = [0, 0, 0]
            current year - vehicle year > 5
        """
        self.user_data['marital_status'] = 'single'

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_11(self):
        """Scenario 11:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 1]
            current year - vehicle year > 5
        """
        self.user_data['risk_questions'] = [0, 0, 1]

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'regular'
        }, json.loads(result))

    def test_risk_profile_scenario_12(self):
        """Scenario 12:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 1, 1]
            current year - vehicle year > 5
        """
        self.user_data['risk_questions'] = [0, 1, 1]

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'regular', 'home': 'regular',
            'life': 'regular'
        }, json.loads(result))

    def test_risk_profile_scenario_13(self):
        """Scenario 13:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [1, 1, 1]
            current year - vehicle year > 5
        """
        self.user_data['risk_questions'] = [1, 1, 1]

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'regular', 'disability': 'regular', 'home': 'regular',
            'life': 'responsible'
        }, json.loads(result))

    def test_risk_profile_scenario_14(self):
        """Scenario 14:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            current year - vehicle year <= 5
        """
        self.user_data['vehicle']['year'] = 2018

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'economic', 'disability': 'economic', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))

    def test_risk_profile_scenario_15(self):
        """Scenario 15:
            0 <= age < 30
            dependents > 0
            house = mortgaged
            income <= 200000
            marital_status = married
            risk_questions = [0, 0, 0]
            vehicle = 0
        """
        self.user_data['vehicle'] = {}

        risk = Risk(self.user_data)
        result = risk.evaluate()

        self.assertEqual({
            'auto': 'ineligible', 'disability': 'economic', 'home': 'economic',
            'life': 'economic'
        }, json.loads(result))
