import requests, sys
import json
import pandas as pd
import scispacy
import spacy


from bs4 import BeautifulSoup

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

myqueryterm = (
    '"ibuprofen" AND "adverse effects"' 'AND (PMID:* OR PMCID:*)' 'AND ABSTRACT:*'
)
requestURL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="+myqueryterm+"&format=json&pageSize=50&resultType=core"

#print(requestURL)


#select the type of data format, XML or json

r= requests.get(requestURL, headers={"Accept" : "application/json"})

#verify connection with the API
if not r.ok:
	r.raise_for_status()	
	sys.exit()

#save data
data = r.json()


# create a list for the type of information you want to collect example are below:
PubMed_Id = [] # PMID id
Title = [] # Title of the publication
publication_date = [] # Year of publication
abstract = [] #abstract

# now parse the json file and collect information for ALL references in the data:
for each_publication in data['resultList']['result']:
   
    PubMed_Id.append(each_publication.get('id', 'N/A'))
    Title.append(each_publication['title'])
    publication_date.append(each_publication['pubYear'])
    abstract.append(html_to_text(each_publication['abstractText']))

    
    
    data_ibuprofen_EPMC = pd.DataFrame(

	{ 'PMID' : PubMed_Id,
	  'Title' : Title,
	 'Pub_Year' : publication_date,
         'abstract' : abstract
} )

print("Data retrieved on ibuprofen and its adverse effects from Europe PMC:")

print("Check CSV file in the folder for more detailed information")

data_ibuprofen_EPMC.to_csv("...\DataIbuprofen_EuropePMC.csv", index = False)

#---------------------------------------------------
#Retrieving drug name and adverse event (disease)
#----------------------------------------------------

nlp = spacy.load("en_ner_bc5cdr_md")

df = pd.read_csv("...\DataIbuprofen_EuropePMC.csv")

required_cols = {"PMID", "Title", "Pub_Year", "abstract"}
if not required_cols.issubset(df.columns):
    raise ValueError("CSV must contain PMID, title, Pub_Year and abstract columns")



def extract_drug_ae(text):
    if pd.isna(text):
        return [], []

    doc = nlp(text)

    drugs = []
    aes = []

    for ent in doc.ents:
        if ent.label_ == "CHEMICAL":
            drugs.append(ent.text)
        elif ent.label_ == "DISEASE":
            aes.append(ent.text)

# Deduplicate
    drugs = list(set(drugs))
    aes = list(set(aes))

    return drugs, aes
# ---------------------------------------------------------
# 4. APPLY EXTRACTION TO EACH ROW
# ---------------------------------------------------------
drug_list = []
ae_list = []

for abstract in df["abstract"]:
    drugs, aes = extract_drug_ae(abstract)
    drug_list.append(drugs)
    ae_list.append(aes)

df["drug_names"] = drug_list
df["adverse_events"] = ae_list

# ---------------------------------------------------------
# 5. SAVE RESULTS
# ---------------------------------------------------------
df.to_csv("drug_ae_extracted.csv", index=False)

print("Extraction complete! Saved to drug_ae_extracted.csv")








