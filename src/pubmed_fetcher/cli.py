import argparse
from pubmed_fetcher.fetch import fetch_pubmed_ids, fetch_details
from pubmed_fetcher.filter import extract_relevant_data
from pubmed_fetcher.csv_writer import save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors")
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-f", "--file", help="CSV filename to save results")

    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    ids = fetch_pubmed_ids(args.query)
    records = fetch_details(ids)
    data = extract_relevant_data(records, debug=args.debug)

    if args.file:
        save_to_csv(data, args.file)
        print(f"Results saved to {args.file}")
    else:
        for row in data:
            print(row)
 
