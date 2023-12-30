import requests
from bs4 import BeautifulSoup

COURSE_CODE_LEN = 8
COURSE_LEVEL_INDEX = 3


def get_course_name(course_list_item):
    if course_list_item == None:
        return None

    name_div = course_list_item.find('div', attrs={'class': 'views-field views-field-field-course-title'})
    if name_div == None:
        return None

    name_header = name_div.find('h3')
    if name_header == None:
        return None

    return name_header.text


def get_course_prereqs(course_list_item):
    if course_list_item == None:
        return []

    prereq_span = course_list_item.find('span', attrs={'class': 'views-field views-field-field-prerequisite'})
    if prereq_span == None:
        return []

    prereq_link_container = prereq_span.find('span', attrs={'class': 'field-content'})
    if prereq_link_container == None:
        return []

    prereq_links = prereq_link_container.find_all('a')
    if prereq_links == None:
        return []

    prereqs = []
    for link in prereq_links:
        prereqs.append(link.text)
    return prereqs


def get_course_code(course_name_str):
    if len(course_name_str) < COURSE_CODE_LEN:
        return None

    return course_name_str[:COURSE_CODE_LEN]


def get_course_level(course_code):
    if len(course_code) != COURSE_CODE_LEN:
        return None

    return course_code[COURSE_LEVEL_INDEX]


# url must be a printer-friendly version of some course search page from
# https://utsc.calendar.utoronto.ca/search-courses (click "Printer-Friendly Version" at the bottom of the search page)
def create_graph(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    course_list_items = soup.find_all('div', attrs={'class': 'no-break w3-row views-row'})
    graph = dict()

    for item in course_list_items:
        course_name = get_course_name(item)
        course_code = get_course_code(course_name)
        course_prereqs = get_course_prereqs(item)
        graph[course_code] = course_prereqs

    return graph
