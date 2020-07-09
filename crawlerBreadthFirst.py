import urllib.request # Python's handy web request library
import re             # Python's handy regular expression library
import json           # Python's handy JSON library

TERMS = ["Awesome", "Corona", "Email", "Fulford", "School", "Steve", "Welcome", "Xenon"]
BASE_URL="https://www.bbc.co.uk/"
DEPTH = 1 # How many pages/links deep we will crawl

def make_url_list(url, depth): # breadth first iteration through child links
    url_list = []
    urls = [url]
    for d in range(depth+1):
        next_depth_urls = []
        for i in range(len(urls)):
            print("(depth " + str(d) + ": " + str(i+1) + "/" + str(len(urls)) + " URLs. Scrapable URLs: " + str(len(url_list)) + ")", end="\r")
            scrapable = False
            children = []
            if d < depth: scrapable, children = url_scrapable(url, True)
            else: scrapable, children = url_scrapable(url, False)
            if scrapable and (urls[i] not in url_list) and suitable_url(urls[i]):
                url_list.append(urls[i]) #build up the url list
            next_depth_urls.extend(children)
        print("(depth " + str(d) + ": " + str(i+1) + "/" + str(len(urls)) + " URLs. Scrapable URLs: " + str(len(url_list)) + ")")
        urls = list(next_depth_urls)
    return url_list

def url_scrapable(url,withChildren):
    try: 
        context = urllib.request.urlopen(url) # context manager activated
        html = context.read().decode("utf-8").lower() # page into a string
        context.close()
        if withChildren: #note, ths regex does let a few poor urls through which will not be openable
            regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            url_children_obj = re.findall(regex,html) # for regex magic ask the www genie
            url_children = [ url_children_obj[i][0] for i in range(len(url_children_obj)) ]
            return True, url_children
        else:
            return True, []
    except:
        return False, []

def suitable_url(url):
    unsuitable_ends = [".png", ".jpg", ".jpeg", ".css", ".js", ".xml", ".pdf", ".mod", ".dtd", ".svg"]
    unsuitable_mids = ["js?", "css?", "//schema.org", "//api.w.org", "//yoast.com", "//t.co", "//www.w3.org"]
    for end in unsuitable_ends:
        if url[-len(end):] == end: return False
    for mid in unsuitable_mids:
        if mid in url: return False
    return True

def index_pages(urls, index_dic): 
    for i in range(len(urls)):
        debug = str(i+1) + "/" + str(len(urls)) + ": " + urls[i] + ". Index terms: "
        print(debug + "none.", end="\r")
        try:
            context = urllib.request.urlopen(urls[i]) # context manager activated
            html = context.read().decode("utf-8").lower() # page into a string
            context.close()
            for term in index_dic:
                if html.find(term) > -1:
                    index_dic[term].append(urls[i])
                    debug += term + ", "
                    print(debug, end="\r")
            print("")
        except: print("URL error: " + urls[i])
    
# CREATE INDEX
index = {} # index is a key,value Dictionary
for term in TERMS:
    index.update({term.lower():[]}) # values are lists of URLs

#SCRAPE PAGES RECURSIVELY
print("Compiling list of URLs to scrape from " + BASE_URL + "...")
urls_to_index = make_url_list(BASE_URL, DEPTH) # the crawling
print("Indexing " + str(len(urls_to_index)) + " URLs")
index_pages(urls_to_index, index)              # the scraping. index passed by ref

# SAVE INDEX TO FILE
FILE_NAME = "index.json"
print("Saving index to file: " + FILE_NAME + "...")
with open(FILE_NAME, 'w') as file_handler:
    json.dump(index, file_handler, sort_keys=True, indent=4)

#SHOW OFF THE RESULTING INDEX        
print(index)
for key, value in index.items():
    print(key + ": " + str(len(value)))