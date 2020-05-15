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
        self.module_id = module_id
        self.__data = self.fetch_module_data(module_id)
        self.__ratings = self.fetch_ratings_data(module_id)
        self.__grades = self.fetch_grades_data(module_id)
        self.departments = self.__data['departments']
        self.faculty = self.__data['faculty']
        self.gradeStatistics = self.__data['gradeStatistics']
        self.gradeStatistics_average = self.__data['gradeStatistics']["average"]
        self.gradeStatistics_count = self.__data['gradeStatistics']["count"]
        self.gradeStatistics_failed = self.__data['gradeStatistics']["failed"]
        self.gradeStatistics_passed = self.__data['gradeStatistics']["passed"]
        self.messages = self.__data['messages']
        self.name = self.__data['name']
        self.ratingSummary = self.__data['ratingSummary']
        self.ratingSummary_average = self.__data['ratingSummary']['average']
        self.ratingSummary_total = self.__data['ratingSummary']['total']
        self.shortName = self.__data['short_name']
        self.type = self.__data['type']
        self.userCount = self.__data['userCount']
        self.userCount_all = self.__data['userCount']['all']
        self.aggregatedSemesterInformation = self.get_aggregated_semester_information()

    def get_data(self):
        # whole data set
        return self.__data

    def get_ratings(self):
        return self.__ratings

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

        for userCount in self.userCount['semester']:
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
        all_ratings = []
        offset = 0

        while True:
            try:
                url = 'https://bestande.ch/api/institution/uzh/module/' + str(module_id) + '/ratings?offset=' + str(offset) + '&sort=newest'
                r = requests.get(url).json()
                if not r['success'] or r['data']['ratings'] == []: # or offset >= 45:
                    break
                    # raise RuntimeError('ERROR: Fetching ratings via API failed.')
            except RuntimeError as e:
                print(e)
            except Exception as e:
                print(e)
            else:
                all_ratings += r['data']['ratings']
                offset += 15
        return all_ratings

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


