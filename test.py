from terminaltables import AsciiTable

vacancies_stat_hh = {
    'Python': {
        'vacancies_found': 56,
        'vacancies_processed': 55,
        'average_salary': 165443,
    },
    'Java': {
        'vacancies_found': 50,
        'vacancies_processed': 39,
        'average_salary': 193625,
    },
}

vacancies_table = [
    ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ['Python', 56, 55, 165443],
    ['Java', 50, 39, 193625],
]

def creating_table_with_languages(service_with_vacancies, languages_stat):
    languages_info = [
        [service_with_vacancies],
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for language, language_stat in languages_stat.items():
        language_stat = [
            language,
            language_stat['vacancies_found'],
            language_stat['vacancies_processed'],
            language_stat['average_salary'],
        ]
        languages_info.append(language_stat)
    vacancies_table = AsciiTable(languages_info)
    return vacancies_table.table



print(creating_table_with_languages('hh',vacancies_stat_hh))