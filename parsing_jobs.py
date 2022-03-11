import datetime
import os

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


LANGUAGES = [
    'JavaScript',
    'Java',
    'Python',
    'Ruby',
    'PHP',
    'C++',
    'CSS',
    'C#',
    'C',
    'Go',
]


def get_hh_vacancies_by_language(language, page=1):
    current_date = datetime.date.today()
    month = datetime.timedelta(31)
    date_from = current_date - month
    params = {
        'specialization': 1,
        'area': 1,
        'date_from': date_from,
        'text': language,
        'only_with_dalary': 'true',
        'page': page,
    }
    vacancies_url = 'https://api.hh.ru/vacancies'
    response = requests.get(
        url=vacancies_url,
        params=params,
    )
    response.raise_for_status()
    return response.json()


def predict_rub_salary(currency, salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def parse_language_statistics_hh(language):
    language_stat = {language: {}}
    language_vacancies = get_hh_vacancies_by_language(language=language)
    language_stat[language]['vacancies_found'] = language_vacancies['found']
    total_pages = language_vacancies['pages']
    salaries = []
    for vacancy_page in range(total_pages):
        vacancies_in_page = get_hh_vacancies_by_language(
            language=language,
            page=vacancy_page,
        )
        if not vacancies_in_page['found']:
            language_stat[language]['vacancies_processed'] = 0
            language_stat[language]['average_salary'] = 0
            return language_stat
        for vacancy in vacancies_in_page['items']:
            if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
                continue
            salary_currency = vacancy['salary'].get('currency')
            salary_from = vacancy['salary'].get('from')
            salary_to = vacancy['salary'].get('to')
            avg_salary = predict_rub_salary(
                currency=salary_currency,
                salary_from=salary_from,
                salary_to=salary_to,
            )
            if not avg_salary:
                continue
            salaries.append(avg_salary)
    avg_language_salary = sum(salaries) / len(salaries)
    language_stat[language]['vacancies_processed'] = len(salaries)
    language_stat[language]['average_salary'] = int(avg_language_salary)
    return language_stat


def get_superjob_vacancies_by_language(language, superjob_token, page=0):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': superjob_token,
    }
    params = {
        'town': 4,
        'catalogues': 48,
        'keyword': language,
        'page': page
    }
    response = requests.get(
        url=vacancies_url,
        headers=headers,
        params=params,
    )
    response.raise_for_status()
    return response.json()


def parse_language_staistics_superjob(language, superjob_token):
    language_stat = {}
    language_stat[language] = {}
    salaries = []
    more = True
    page = 0
    while more:
        vacancies = get_superjob_vacancies_by_language(
            language=language,
            superjob_token=superjob_token,
            page=page,
        )
        more = vacancies['more']
        page += 1
        language_stat[language]['vacancies_found'] = vacancies['total']
        if not vacancies['total']:
            language_stat[language]['vacancies_processed'] = 0
            language_stat[language]['average_salary'] = 0
            return language_stat
        for vacancy in vacancies['objects']:
            salary_currency = vacancy.get('currency', None)
            if not salary_currency or salary_currency != 'rub':
                continue
            salary_from = vacancy.get('payment_from', None)
            salary_to = vacancy.get('payment_to', None)
            avg_salary = predict_rub_salary(
                currency=salary_currency,
                salary_from=salary_from,
                salary_to=salary_to,
            )
            if not avg_salary:
                continue
            salaries.append(avg_salary)
    language_stat[language]['vacancies_processed'] = len(salaries)
    avg_salary = sum(salaries) / len(salaries)
    language_stat[language]['average_salary'] = int(avg_salary)
    return language_stat


def create_table_with_languages(languages_stat, service_name):
    languages_info = [
        [service_name],
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ],
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


def main():
    load_dotenv()
    superjob_token = os.environ.get('SUPERJOB_TOKEN')
    hh_languages_statistics = {}
    superjob_languages_statistics = {}
    for language in LANGUAGES[:2]:
        language_stat_hh = parse_language_statistics_hh(language=language)
        language_stat_superjob = parse_language_staistics_superjob(
            language=language,
            superjob_token=superjob_token,
        )
        superjob_languages_statistics.update(language_stat_superjob)
        hh_languages_statistics.update(language_stat_hh)
    hh_vacancies_table = create_table_with_languages(
        languages_stat=hh_languages_statistics,
        service_name='hh',
    )
    superjob_vacancies_table = create_table_with_languages(
        languages_stat=superjob_languages_statistics,
        service_name='Superjob',
    )
    print(superjob_vacancies_table)
    print(hh_vacancies_table)


if __name__ == '__main__':
    main()
