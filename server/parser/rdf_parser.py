from rdflib import Graph


class RDF_Parser(object):
    """docstring for RDF_Parser"""
    def __init__(self):
        super(RDF_Parser, self).__init__()

    def parse(self, filename):
        graph = Graph()
        graph.parse(filename)

        separator = '_judet_'
        separator_length = len(separator)

        counties_locality_graph = {}

        for subj, _, _  in graph:
            subj = subj.lower()
            separator_index = subj.find(separator)
            locality_index = subj.rfind('/')
            locality = subj[locality_index+1:separator_index]
            county = subj[separator_index+separator_length:]

            locality = ''.join([i if i not in ['-', ' '] else '_'  for i in locality.strip()])

            if (separator_index > 0 and locality_index > 0 and county
                    and locality):
                if county in counties_locality_graph:
                    counties_locality_graph[county][locality] = []
                else:
                    counties_locality_graph[county] = {locality: []}

        return counties_locality_graph

if __name__ == '__main__':
    rdf_parser = RDF_Parser()
    rdf_parser.parse('toponym-export-20170221-135802.rdf')

