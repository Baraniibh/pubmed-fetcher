from Bio import Entrez

Entrez.email = "your_email@example.com"  # Replace this with your email

def fetch_pubmed_ids(query: str, max_results: int = 10) -> list[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def fetch_details(paper_ids: list[str]) -> list:
    handle = Entrez.efetch(db="pubmed", id=",".join(paper_ids), retmode="xml")
    records = Entrez.read(handle)
    return records["PubmedArticle"]
 
