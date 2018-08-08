#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from lxml import etree



class Wikipython(object):
    def __init__(self):
        self.update_tree = None
        self.metadata = None



    def get_metadata(self, Q_Value):
        my_dict = {"Production": [], "Composer" : [], "Choreographer" : []}
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = """SELECT ?choreograafLabel ?composerLabel ?productionLabel WHERE {{
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
          {0} wdt:P1809 ?choreograaf.
          {0} wdt:P86 ?composer.
          {0} rdfs:label? ?production
        }}
        LIMIT 100""".format("wd:" + Q_Value)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) == 0:
            pass
        else:
            my_dict["Choreographer"] = results["results"]["bindings"][0]["choreograafLabel"]["value"]
            my_dict["Composer"] = results["results"]["bindings"][0]["composerLabel"]["value"]
            my_dict["Production"] = results["results"]["bindings"][0]["productionLabel"]["value"]
        self.metadata = my_dict


    def create_viaa_xml(self):
        self.update_tree = etree.Element("MediaHAVEN_external_metadata")
        self.update_tree.append(etree.Element("MDProperties"))


    def ensure_element_exists(self, element_name):
        elements = self.update_tree.xpath('//' + element_name)
        if len(elements) == 0:
            element = list(self.update_tree.iter("MDProperties"))[0]
            child = etree.Element(element_name)
            element.insert(0, child)

    def map_kp_general_to_dc_titles(self, name_tag_viaa, tag_wikidata):
        element = list(self.update_tree.iter('dc_titles'))[0]
        child = etree.Element(name_tag_viaa)
        element.insert(0, child)
        child.text = self.metadata[tag_wikidata]

    def write_wikidata_general_to_update_tree(self):
        self.ensure_element_exists('dc_titles')
        self.map_kp_general_to_dc_titles("title", "Production")

    def map_wikidata_general_to_dc_creators(self, name_tag_viaa, tag_wikidata):
        element = list(self.update_tree.iter('dc_creators'))[0]
        child = etree.Element(name_tag_viaa)
        element.insert(0, child)
        child.text = self.metadata[tag_wikidata]

    def write_wikidata_functions_to_update_tree(self):
        self.ensure_element_exists('dc_creators')
        self.map_wikidata_general_to_dc_creators("Choreograaf", "Choreographer")

    def map_kp_general_to_dc_contributors(self, name_tag_viaa, tag_wikidata):
        element = list(self.update_tree.iter('dc_creators'))[0]
        child = etree.Element(name_tag_viaa)
        element.insert(0, child)
        child.text = self.metadata[tag_wikidata]

    def write_wikidata_functions_to_update_tree_contributors(self):
        self.ensure_element_exists('dc_creators')
        self.map_wikidata_general_to_dc_creators("Soundtrack", "Composer")


    def write_tree_to_xml(self):
        with open("../resources/xml_viaa.xml", "wb") as f:
            f.write(etree.tostring(self.update_tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))


#if __name__ == '__main__':

