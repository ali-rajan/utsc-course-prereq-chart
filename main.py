from pyvis.network import Network
import prerequisite_scraper

URL_CS_COURSES = 'https://utsc.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug?course_keyword=&field_program_area_value=Computer%20Science&field_prerequisite_value=&breadth=All&field_enrolment_limits_value=All&field_course_experience_value=All&page=1'
course_lvl_to_node_colour = {'A': 'green', 'B': 'yellow', 'C': 'orange', 'D': 'red'}


def append_dict_graph_to_network(graph_dict: dict[str, list[str]], network: Network) -> None:
    for course_code in graph_dict:
        course_lvl = prerequisite_scraper.get_course_level(course_code)
        network.add_node(course_code, label=course_code, color=course_lvl_to_node_colour[course_lvl])

    for course_code in graph_dict:
        for other_course_code in graph_dict[course_code]:
            network.add_node(other_course_code, label=other_course_code)
            network.add_edge(other_course_code, course_code)


if __name__ == '__main__':
    url = URL_CS_COURSES
    graph_dict = prerequisite_scraper.create_graph(url)
    network = Network(directed=True, height="720px", width="100%", bgcolor="#282424", font_color="white")
    append_dict_graph_to_network(graph_dict, network)
    network.show("graph.html", notebook=False)
