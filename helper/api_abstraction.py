import requests

def get_course_by_id(id):
    url = 'https://bestande.ch/api/institution/uzh/module/' + str(id)
    r = requests.get(url)
    return r

def get_course_rating_by_id(id):
    url = 'https://bestande.ch/api/institution/uzh/module/' + str(id) + '/ratings'
    r = requests.get(url)
    return r

def get_course_grades_by_id(id):
    url = 'https://bestande.ch/api/grades/UZH/' + str(id)
    r = requests.get(url)
    return r

