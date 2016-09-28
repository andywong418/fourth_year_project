# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re
import os
import sys
import json
import pickle
import yaml
from scrapy.selector import Selector
from url_constructor_file import url_constructor
GS_LINK_JSON_FILE       =  "output.json"
RESULT_FILE             = "htmlread_1.txt"

ENABLE_TEXT_SUMMARIZE   = 0 # For NLTK to look into the text for details.
ENABLE_PARAGRAPH_STORED = 1 # Store website content to file.

class GoogleSpider(scrapy.Spider):
    with open(RESULT_FILE,'w') as f:
        f.write('')
        print 'Restart the log file'
    with open(GS_LINK_JSON_FILE,'w') as f:
        f.write('')
        print 'Restart the GS_LINK_JSON_FILE file'
    search_class = url_constructor("car", "price")
    setting_data = search_class.retrieved_setting_fr_json_file()
    print setting_data
    name = setting_data['Name']
    allowed_domains = setting_data['Domain']
    start_urls = setting_data['SearchUrl']
    def combine_all_url_link_for_multiple_search(self,more_url_list):
        '''
            Combine all the url link list in the event of mutliple search.
            list more_url_list --> none
            get from Json file and eventually dump all back
        '''

        with open(GS_LINK_JSON_FILE, "r") as outfile:
            setting_data = yaml.load(outfile)

        if setting_data is None or not setting_data.has_key('output_url'):
            setting_data = dict()
            setting_data['output_url'] = []

        with open(GS_LINK_JSON_FILE, "w") as outfile:
            json.dump({'output_url': setting_data['output_url']+more_url_list}, outfile, indent=4)
    def remove_escape_characters(self, raw_input):
        for n in ['\n','\t','\r']:
            raw_input = raw_input.replace(n,'')
        return raw_input
    def join_list_of_str(self,list_of_str, joined_chars= '...'):
        return joined_chars.join([n for n in list_of_str])
    def parse(self, response):
        if self.setting_data['type_of_parse'] == 'google_search':
            print 'For google search parsing'

            ## Get the selector for xpath parsing
            sel = Selector(response)
            print("SELECTOR")
            print sel
            google_search_links_list =  sel.xpath('//img/@src').extract()
            print 'one'
            # print google_search_links_list
            # google_search_links_list = [re.search('q=(.*)&sa',n).group(1) for n in google_search_links_list if re.search('q=(.*)&sa',n)]
            # print 'two'
            print google_search_links_list
            print len(google_search_links_list)
            ## Display a list of the result link
            for n in google_search_links_list:
                print n

            self.combine_all_url_link_for_multiple_search(google_search_links_list)
        if self.setting_data['type_of_parse'] == 'general':
            # Need to separate out one subject - i.e. need to find price for Toyota SUV 1000 or whatever, Chevrolet 3000, etc. Give some example car brands.
            # Need to specify purpose - image detection, label (e.g. price prediction) and datatype. Find label and
            # Also need to include false data.
            print
            print "General link scraping"
            sel = Selector(response)
            print sel
            title = sel.xpath('//title/text()').extract()
            if len(title)>0:
                title = title[0].encode(errors='replace') #replace any unknown character with ?
            contents = sel.xpath('/html/head/meta[@name="description"]/@content').extract()
            if len(contents)>0:
                contents = contents[0].encode(errors='replace') #replace any unknown character with ?
            paragraph_list = sel.xpath('//p/text()').extract()
            para_str = self.join_list_of_str(paragraph_list, joined_chars= '..')
            para_str = para_str.encode(errors='replace')
            para_str = self.remove_escape_characters(para_str)
            print
            print title
            print
            print contents
            ## Dump results to text file
            with open(RESULT_FILE,'a') as f:
                f.write('\n')
                f.write('#'*20)
                f.write('\n')
                f.write(title + '\n')
                f.write(response.url)
                for n in range(2): f.write('\n')
                f.write(str(contents))
                for n in range(2): f.write('\n')
                f.write(para_str)
                f.write('\n')
                f.write('#'*20)
                for n in range(2): f.write('\n')

            print
            print 'Completed'
