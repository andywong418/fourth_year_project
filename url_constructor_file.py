import re, os, sys, math, yaml
import json

from scrapy.spider import Spider
from scrapy.selector import Selector

class url_constructor(object):
    # subject refers to the info you want, labels are the types of paramters that you want to label your data with. E.g. Car prices - subject is car, label is prices.
    def __init__(self, subject, label):
        #initialise the first level google search to get a list of relevant urls.
        self.prefix_search_text = "https://www.google.com/search?q="
        self.postfix_search_text = '&num=100'# non changable text
        self.spider_name = 'first_level_search'
        self.allowed_domains = ['www.google.com']
        self.search_url_list = []#place to put the search results
        self.subject = subject
        self.label = label
        self.json_file = 'google_search.json'
         ## Type of crawler.
        self.data_format = 1 # 1 - google site crawler, 2 - individual site crawler

    def join_keywords(self):
        # Join subject and label to create one
        print "LABEL"
        print self.label
        s = "+"
        seq = (self.subject, self.label)
        if self.image_detection:
            self.search_key = self.subject
        else:
            self.search_key = s.join(seq)
            self.search_key = self.search_key.rstrip().replace(' ', '+')
    def num_of_search_results(self, number):
        self.search_results_number = number
    def set_scan_number_of_pages(self):
        self.pages_to_scan = int(math.ceil(self.search_results_number/100.0))
    def target_page(self, page_number):
        return "&start=%i" %(page_number*100)
    def image_detector(self):
        self.image_query = "&tbm=isch"
    def set_pages_url(self):
        ## scan the number of results needed
        self.set_scan_number_of_pages()

        ## convert the input search result
        self.join_keywords();
        print "SEARCH KEY"
        print self.search_key
        self.url_array = []
        for n in range(0, self.pages_to_scan, 1):
            if self.image_detection:
                self.image_detector()
                self.output_url = self.prefix_search_text + self.search_key + \
                                self.postfix_search_text + \
                                self.target_page(n) + \
                                self.image_query
            else:
                self.output_url = self.prefix_search_text + self.search_key + \
                                self.postfix_search_text + \
                                self.target_page(n)
            print "HELLO"
            print self.output_url
            self.url_array.append(self.output_url)
        print self.url_array
        return self.url_array
    def set_setting_to_json_file(self, data_dict):
        ## set settings for json file
        with open(self.json_file, "w") as outfile:
            json.dump(data_dict, outfile, indent=4)
    def prepare_data_for_json_store(self, additonal_parm_dict = {}):
        if self.data_format == 1:
            temp_data = {'Name': self.spider_name, 'Domain': self.allowed_domains,
                        'SearchUrl':self.url_array, 'type_of_parse':'google_search'}

        elif self.data_format == 2:
            temp_data = {'Name':'random target website', 'Domain':[],
                        'SearchUrl':self.url_array,'type_of_parse':'general'}
        else:
            raise

        temp_data.update(additonal_parm_dict)
        return temp_data
    def retrieved_setting_fr_json_file(self, filename = ''):
        '''
            Function to retrieve the various setting from the json file specified by the self.setting_json_file
            None --> json object  setting_data
            set the various parameters
        '''
        if filename =='':
            filename = self.json_file

        with open(filename, "r") as infile:
            setting_data = yaml.load(infile)

        return setting_data
