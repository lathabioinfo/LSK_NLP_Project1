import requests, sys
import json
import pprint
import pandas as pd
from bs4 import BeautifulSoup

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

myqueryterm = (
    '"nurofen" AND "adverse effects"' 'AND (PMID:* OR PMCID:*)' 'AND ABSTRACT:*'
)
requestURL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="+myqueryterm+"&format=json&pageSize=100&resultType=core"

print(requestURL)


#select the type of data format, XML or json

r= requests.get(requestURL, headers={"Accept" : "application/json"})

#verify connection with the API
if not r.ok:
	r.raise_for_status()	
	sys.exit()

#save data
data = r.json()

#print result
pp = pprint.PrettyPrinter(indent=0, width=80, compact=False)
#print("Pretty printing JSON data using pprint module")
#pp.pprint(data)

# create a list for the type of information you want to collect example are below:
PubMed_Id = [] # PMID id
Title = [] # Title of the publication
publication_date = [] # Year of publication
abstract = [] #abstract

# now parse the json file and collect information for ALL references in the data:
for each_publication in data['resultList']['result']:
    # to verify if you are collecting the right information, use the print command below.
    #Remove the simbol # and run the script.
    #It will print on the screen the information for that line

    PubMed_Id.append(each_publication.get('id', 'N/A'))
    #print(each_publication['id'])
    Title.append(each_publication['title'])
    publication_date.append(each_publication['pubYear'])
    abstract.append(html_to_text(each_publication['abstractText']))

    
    
    data_nurofen_EPMC = pd.DataFrame(

	{ 'PMID' : PubMed_Id,
	  'Title' : Title,
	 'Pub_Year' : publication_date,
         'abstract' : abstract
} )

print("Data retrieved on Nurofen and its adverse effects from Europe PMC:")
print(data_nurofen_EPMC)
print("Check CSV file in the folder for more detailed information")

data_nurofen_EPMC.to_csv("D:\Latha\project\Jan2026\DataNurofen_EuropePMC.csv", index = False)
    


