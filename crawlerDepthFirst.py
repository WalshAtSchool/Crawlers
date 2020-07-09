import urllib.request # Python's handy web request library
import re             # Python's handy regular expression library

TERMS = ["Awesome", "Corona", "Email", "Fulford", "School", "Steve", "Welcome", "Xenon"]
BASE_URL="https://www.bbc.co.uk/"
DEPTH = 1 # How many pages/links deep we will crawl

def scrape_page(url,more_pages_deeper):
    print("Depth " + str(DEPTH - more_pages_deeper) + ", scraping: " + url)
    pages_visited.append(url)
    try:
        context = urllib.request.urlopen(url) # context manager activated
        html = context.read().decode("utf-8").lower() # page into a string
        context.close()
        terms_found = "" # console success message
        for key in index: # hunt for the terms in the page
            if html.find(key) != -1: # term successfully found
                terms_found += key + ", " # console success message
                index[key].append(url) # url appended to list for that term
        if terms_found != "":
            print ("Found: " + terms_found)
        
        if more_pages_deeper > 0: # recursive depth-first until at the bottom of the DEPTH    
            regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            url_children = re.findall(regex,html) # for regex magic ask the www genie
            for url_child in url_children:
                if (url_child[0] not in pages_visited) and suitable_url(url_child[0]):
                    scrape_page(url_child[0],more_pages_deeper-1) 
    except:
        print("Unsuccessful with this URL")

def suitable_url(url):
    unsuitable_ends = [".png", ".jpg", ".jpeg", ".css", ".js", ".xml", ".pdf", ".mod", ".dtd", ".svg"]
    unsuitable_mids = ["js?", "css?", "//schema.org", "//api.w.org", "//yoast.com", "//t.co", "//www.w3.org"]
    for end in unsuitable_ends:
        if url[-len(end):] == end: return False
    for mid in unsuitable_mids:
        if mid in url: return False
    return True


# CREATE INDEX
index = {} # index is a key,value Dictionary
for term in TERMS:
    index.update({term.lower():[]}) # values are lists of URLs

#SCRAPE PAGES RECURSIVELY
pages_visited = []
scrape_page(BASE_URL,DEPTH)

#SHOW OFF THE RESULTING INDEX        
print(index)
for key, value in index.items():
    print(key + ": " + str(len(value)))