import re, os, sys, math, yaml
import json

from scrapy.spider import Spider
from scrapy.selector import Selector
from url_constructor_file import url_constructor

if __name__ == '__main__':

    '''
        Running the google search
    '''
    # User options
    NUM_SEARCH_RESULTS = 50    # number of search results returned

    print 'Start search'

    ## Parameters setting
    search_subject= 'car'
    search_label = 'price'
    #search_words = ['best area to stay in tokyo','cheap place to stay in tokyo']
    GS_LINK_JSON_FILE = "output.json" #must be same as the get_google_link_results.py

    # spider store location, depend on user input
    spider_file_path = os.getcwd()
    spider_filename = '__init__.py'

    ## Google site link scrape
    print 'Get the google search results links'
    crawler = url_constructor(search_subject, search_label)
    crawler.num_of_search_results(NUM_SEARCH_RESULTS)
    crawler.data_format = 1
    crawler.set_pages_url()

    ## Set the setting for json
    temp_data_for_store = crawler.prepare_data_for_json_store()
    crawler.set_setting_to_json_file(temp_data_for_store)
    new_project_cmd = 'scrapy settings -s DEPTH_LIMIT=1 & cd "%s" & scrapy runspider %s' %(spider_file_path,spider_filename)
    os.system(new_project_cmd)

    # print 'Start scrape individual results'
    # data  = crawler.retrieved_setting_fr_json_file(GS_LINK_JSON_FILE)
    #
    # ##check if proper url --> must at least start with http
    # url_links_general_search = [n for n in data['output_url'] if n.startswith('http')]
    #
    # ## Switch to the second seach
    # crawler.data_format_switch = 2
    #
    # crawler.url_array = url_links_general_search
    #
    # ## Set the setting for json
    # temp_data_for_store = crawler.prepare_data_for_json_store()
    # crawler.set_setting_to_json_file(temp_data_for_store)
    #
    # ## Run the crawler -- and remove the pause if do not wish to see contents of the command prompt
    # new_project_cmd = 'scrapy settings -s DEPTH_LIMIT=1 & cd "%s" & scrapy runspider %s' %(spider_file_path,spider_filename)
    # os.system(new_project_cmd)
