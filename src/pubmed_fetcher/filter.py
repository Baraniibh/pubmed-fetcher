def is_pharma_or_biotech_affiliation(affiliation: str) -> bool:
    affiliation = affiliation.lower()

    academic_keywords = [
        "university", "college", "institute", "school", "hospital", "department", "faculty",
        "nih", "cdc", "government", "ministry"
    ]
    industry_keywords = [
        "inc", "ltd", "llc", "pharma", "biotech", "therapeutics", "genomics", "biosciences", "technologies", 
        "gmbh", "corp", "corporation", "solutions", "labs"
    ]

    return (
        any(keyword in affiliation for keyword in industry_keywords) and
        not any(keyword in affiliation for keyword in academic_keywords)
    )

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

            industry_authors = []
            company_affiliations = []
            email = ""

            for author in article_data.get("AuthorList", []):
                affils = author.get("AffiliationInfo", [])
                for aff in affils:
                    affil_text = aff.get("Affiliation", "")
                    if "@" in affil_text and not email:
                        email = affil_text
                    if is_pharma_or_biotech_affiliation(affil_text):
                        full_name = f"{author.get('LastName', '')} {author.get('ForeName', '')}".strip()
                        industry_authors.append(full_name)
                        company_affiliations.append(affil_text)

            if industry_authors:
                output.append({
                    "PubmedID": str(pmid),
                    "Title": title,
                    "Publication Date": pub_year,
                    "Non-academic Author(s)": "; ".join(industry_authors),
                    "Company Affiliation(s)": "; ".join(company_affiliations),
                    "Corresponding Author Email": email,
                })

        except Exception as e:
            if debug:
                print("Error parsing article:", e)

    return output

