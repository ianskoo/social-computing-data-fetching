import requests
from datetime import datetime

class Module:

    map_semester_period = [
        ('FS20', 20201, datetime.timestamp(datetime.strptime('15-02-2020', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2020', '%d-%m-%Y'))),
        ('FS19', 20191, datetime.timestamp(datetime.strptime('15-02-2019', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2019', '%d-%m-%Y'))),
        ('FS18', 20181, datetime.timestamp(datetime.strptime('15-02-2018', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2018', '%d-%m-%Y'))),
        ('FS17', 20171, datetime.timestamp(datetime.strptime('15-02-2017', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2017', '%d-%m-%Y'))),
        ('FS16', 20161, datetime.timestamp(datetime.strptime('15-02-2016', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2016', '%d-%m-%Y'))),
        ('FS15', 20151, datetime.timestamp(datetime.strptime('15-02-2015', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2015', '%d-%m-%Y'))),
        ('FS14', 20141, datetime.timestamp(datetime.strptime('15-02-2014', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2014', '%d-%m-%Y'))),
        ('FS13', 20131, datetime.timestamp(datetime.strptime('15-02-2013', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2013', '%d-%m-%Y'))),
        ('FS12', 20121, datetime.timestamp(datetime.strptime('15-02-2012', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2012', '%d-%m-%Y'))),
        ('FS11', 20111, datetime.timestamp(datetime.strptime('15-02-2011', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2011', '%d-%m-%Y'))),
        ('FS10', 20101, datetime.timestamp(datetime.strptime('15-02-2010', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-09-2010', '%d-%m-%Y'))),
        ('HS20', 20202, datetime.timestamp(datetime.strptime('15-09-2020', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2021', '%d-%m-%Y'))),
        ('HS19', 20192, datetime.timestamp(datetime.strptime('15-09-2019', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2020', '%d-%m-%Y'))),
        ('HS18', 20182, datetime.timestamp(datetime.strptime('15-09-2018', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2019', '%d-%m-%Y'))),
        ('HS17', 20172, datetime.timestamp(datetime.strptime('15-09-2017', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2018', '%d-%m-%Y'))),
        ('HS16', 20162, datetime.timestamp(datetime.strptime('15-09-2016', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2017', '%d-%m-%Y'))),
        ('HS15', 20152, datetime.timestamp(datetime.strptime('15-09-2015', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2016', '%d-%m-%Y'))),
        ('HS14', 20142, datetime.timestamp(datetime.strptime('15-09-2014', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2015', '%d-%m-%Y'))),
        ('HS13', 20132, datetime.timestamp(datetime.strptime('15-09-2013', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2014', '%d-%m-%Y'))),
        ('HS12', 20122, datetime.timestamp(datetime.strptime('15-09-2012', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2013', '%d-%m-%Y'))),
        ('HS11', 20112, datetime.timestamp(datetime.strptime('15-09-2011', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2012', '%d-%m-%Y'))),
        ('HS10', 20102, datetime.timestamp(datetime.strptime('15-09-2010', '%d-%m-%Y')), datetime.timestamp(datetime.strptime('15-02-2011', '%d-%m-%Y')))
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


        for rating in self.get_ratings():
            rating_date = rating['date'] / 1000 # my timestamps are without milliseconds
            period = None
            for tuple in self.map_semester_period:
                if tuple[2] <= rating_date <= tuple[3]:
                    period = tuple[0]
            if period:
                aggregation.setdefault(period, {}).setdefault('ratings', []).append(rating)

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
                if not r['success'] or r['data']['ratings'] == [] or offset >= 45:
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


