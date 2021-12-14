
def query_to_table(query_results, dynamic_link_path: str = None) -> str:
    result_string = ''
    for result in query_results:
        result_string += "<tr>"
        for entry in result:
            result_string += "<td>"
            if dynamic_link_path is not None and entry == result[0]:
                result_string += "<a href=" + dynamic_link_path + str(entry) + ".html > " + str(entry) + "</a>"
            else:
                result_string += str(entry)
            result_string += "</td>"
        result_string += "</tr>"
    return result_string
