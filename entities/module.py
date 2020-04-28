import requests

class Module:

    map_semester_period = [
        ('FS20', 20201),
        ('FS19', 20191),
        ('FS18', 20181),
        ('FS17', 20171),
        ('FS16', 20161),
        ('FS15', 20151),
        ('FS14', 20141),
        ('FS13', 20131),
        ('FS12', 20121),
        ('FS11', 20111),
        ('FS10', 20101),
        ('HS20', 20202),
        ('HS19', 20192),
        ('HS18', 20182),
        ('HS17', 20172),
        ('HS16', 20162),
        ('HS15', 20152),
        ('HS14', 20142),
        ('HS13', 20132),
        ('HS12', 20122),
        ('HS11', 20112),
        ('HS10', 20102),
    ]

    def __init__(self, module_id):
        self.__module_id = module_id
        self.__data = self.fetch_module_data(module_id)
        self.__ratings = self.fetch_ratings_data(module_id)
        self.__grades = self.fetch_grades_data(module_id)

    @staticmethod
    def fetch_module_data(module_id):
        try:
            url = 'https://bestande.ch/api/institution/uzh/module/' + str(module_id)
            r = requests.get(url).json()
            if not r['success']:
                raise RuntimeError('ERROR: Fetching module data via API failed.')
        except RuntimeError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            return r['data']

    @staticmethod
    def fetch_ratings_data(module_id):
        try:
            url = 'https://bestande.ch/api/institution/uzh/module/' + str(module_id) + '/ratings'
            r = requests.get(url).json()
            if not r['success']:
                raise RuntimeError('ERROR: Fetching ratings via API failed.')
        except RuntimeError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            return r['data']

    @staticmethod
    def fetch_grades_data(module_id):
        try:
            url = 'https://bestande.ch/api/grades/UZH/' + str(module_id)
            r = requests.get(url).json()
            if not r['success']:
                raise RuntimeError('ERROR: Fetching grades via API failed.')
        except RuntimeError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            return r

    def get_data(self):
        # whole data set
        return self.__data

    def get_departments(self):
        # departement (usually null)
        return self.__data['departments']

    def get_faculty(self):
        # f.ex. "Recht" or "Wirtschaft"
        return self.__data['faculty']

    def get_gradeStatistics(self):
        return self.__data['gradeStatistics']

    def get_gradeStatistics_average(self):
        # all grades averaged
        return self.__data['gradeStatistics']['average']

    def get_gradeStatistics_count(self):
        # number of grades available
        return self.__data['gradeStatistics']['count']

    def get_gradeStatistics_failed(self):
        # number of failed grades (grade < 4.0)
        return self.__data['gradeStatistics']['failed']

    def get_gradeStatistics_passed(self):
        # number of passed grades (grade >= 4.0)
        return self.__data['gradeStatistics']['passed']

    def get_messages(self):
        # amount of messages sent in chat
        return self.__data['messages']

    def get_name(self):
        # name of the module (f.ex. "Labor and Employment Law")
        return self.__data['name']

    def get_ratingSummary(self):
        return self.__data['ratingSummary']

    def get_ratingSummary_average(self):
        # average of all ratings
        return self.__data['ratingSummary']['average']

    def get_ratingSummary_total(self):
        # amount of ratings
        return self.__data['ratingSummary']['total']

    def get_shortName(self):
        # f.ex. "Labor and Employment Law"
        return self.__data['short_name']

    def get_type(self):
        # f.ex. "COURSE"
        return self.__data['type']

    def get_module_id(self):
        # unique id of the module
        return self.__module_id

    def get_userCount(self):
        return self.__data['userCount']

    def get_userCount_all(self):
        # amount of bestande users who booked this module
        return self.__data['userCount']['all']

    def get_(self):
        return self.__data['']

    def get_aggregated_semester_information(self):
        """
        aggregates all information which are specific to a semester and combines them in a
        dictionary with the semester name as key.

        aggregation = {
            "FS19": {
                "semesterDetail": { ... },
                "gradesDetail": { ... },
                "userCount": Integer
            },
            ...
        }
        """
        aggregation = {}

        for semesterDetail in self.__data['semesters']:
            period = semesterDetail['period_human']
            aggregation.setdefault(period, {}).__setitem__('semesterDetail', semesterDetail)

        for userCount in self.get_userCount()['semester']:
            period_code = userCount['period']
            period = None
            for tuple in self.map_semester_period:
                if tuple[1] == period_code:
                    period = tuple[0]
                    break
            if period:
                aggregation.setdefault(period, {}).__setitem__('userCount', userCount['count'])

        for gradesInformation in self.__grades['detailed']:
            period = gradesInformation['semester']
            aggregation.setdefault(period, {}).__setitem__('gradesDetail', gradesInformation)

        return aggregation


