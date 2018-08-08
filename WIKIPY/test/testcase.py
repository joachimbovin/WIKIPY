#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from lxml import etree
from WIKIPY.WIKIPY import Wikipython



class WIKIPYTests(TestCase):
    def setUp(self):
        self.Wikipython = Wikipython()


    def test_get_metadata(self):
        self.Wikipython.get_metadata("Q3417753")

    def test_create_xml(self):
        self.Wikipython.get_metadata("Q3417753")
        self.Wikipython.create_viaa_xml()
        self.Wikipython.write_wikidata_general_to_update_tree()
        self.Wikipython.write_wikidata_functions_to_update_tree()
        self.Wikipython.write_tree_to_xml()
        print(etree.tostring(self.Wikipython.update_tree, pretty_print=True))





    
    