# NLP Pipeline for Drug and Adverse Event Extraction from biomedical abstracts in EuropePMC 
## 📌 Project Overview

This project implements an end-to-end Natural Language Processing (NLP) pipeline to:

Retrieve biomedical article abstracts from Europe PMC using its public API.

Store the retrieved metadata and abstracts in a structured CSV file.

Apply SciSpacy models to extract drug and adverse event (AE) entities from the abstracts.

Save the extracted entities into a second CSV file for downstream analysis.

The pipeline is designed to support pharmacovigilance, literature mining, and biomedical text analytics.
## 🔍 Data Retrieval from Europe PMC
### Source

Europe PMC REST API

#### Extracted Fields

The following fields are retrieved and stored in a CSV file:

Column Name	Description

PMID	- PubMed Identifier

Title	- Article title

Pub_year	- Year of publication

Abstract	- Article abstract text

## 🧪 Named Entity Recognition with SciSpacy
### Objective

#### Identify and extract:

Drugs

Adverse Events (AEs)

from the abstract text.

#### NLP Tools Used

SciSpacy

Pretrained biomedical NER models (e.g. en_ner_bc5cdr_md)

##### Extracted Fields
Column Name	Description

PMID	- PubMed Identifier

Drug	- Identified drug entity

Adverse_Event	- Identified adverse event

Sentence	- Source sentence containing the entities
