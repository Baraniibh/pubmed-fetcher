def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ["university", "college", "institute", "school", "hospital", "department"]
    return not any(keyword in affiliation.lower() for keyword in academic_keywords)

def extract_relevant_data(records, debug=False) -> list[dict]:
    output = []
    for article in records:
        try:
            medline = article["MedlineCitation"]
            article_data = medline["Article"]
            pmid = medline["PMID"]
            title = article_data["ArticleTitle"]
            pub_date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
            pub_year = pub_date.get("Year", "Unknown")

            non_academic_authors = []
            company_affiliations = []
            email = ""

            for author in article_data.get("AuthorList", []):
                affils = author.get("AffiliationInfo", [])
                for aff in affils:
                    affil_text = aff.get("Affiliation", "")
                    if "@" in affil_text:
                        email = affil_text
                    if is_non_academic(affil_text):
                        non_academic_authors.append(author.get("LastName", "") + " " + author.get("ForeName", ""))
                        company_affiliations.append(affil_text)

            if non_academic_authors:
                output.append({
                    "PubmedID": str(pmid),
                    "Title": title,
                    "Publication Date": pub_year,
                    "Non-academic Author(s)": "; ".join(non_academic_authors),
                    "Company Affiliation(s)": "; ".join(company_affiliations),
                    "Corresponding Author Email": email,
                })

        except Exception as e:
            if debug:
                print("Error parsing article:", e)

    return output
 
