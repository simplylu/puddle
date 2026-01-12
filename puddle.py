from argparse import ArgumentParser, Action
from sites.huggingface import HuggingFace
from sites.shakker_ai import ShakkerAI
from sites.civitai import CivitAI
from stats import print_stats
from colorama import Fore
from glob import glob
import pandas as pd

KEYWORDS = open("keywords.txt").read().splitlines()


SITE_MAP = {
    "shakkerai": [ShakkerAI],
    "civitai": [CivitAI],
    "huggingface": [HuggingFace],
    "all": [ShakkerAI, CivitAI, HuggingFace],
}

EXPORT_MAP = {
    "xlsx": "to_excel",
    "csv": "to_csv",
    "json": "to_json",
}


class ValidateAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ext = str(values).split(".")[-1]
        if ext not in EXPORT_MAP:
            print(f"{Fore.RED}Unsupported file extension: {ext}. Supported extensions are: {list(EXPORT_MAP.keys())}{Fore.RESET}")
            exit(1)
        setattr(namespace, self.dest, values)


def hello():
    hello = Fore.MAGENTA + "            __" + Fore.RESET + "\n"
    hello += Fore.MAGENTA + "           /(`o   " + Fore.RESET + "\n"
    hello += Fore.MAGENTA + "     ,-,  //  \\\\ " + Fore.CYAN + "                 (c) 2026 Luna-Marika Dahl\n" + Fore.RESET
    hello += Fore.MAGENTA + "    (,,,) ||   V  " + Fore.RESET + "\n"
    hello += Fore.MAGENTA + "   (,,,,)\\//      " + Fore.RESET + "\n"
    hello += Fore.MAGENTA + "   (,,,/w)-' " + Fore.RESET + "     $$$$$$$\\                  $$\\       $$\\ $$\\           " + "\n"
    hello += Fore.MAGENTA + "   \\,,/w) " + Fore.RESET + "        $$  __$$\\                 $$ |      $$ |$$ |          " + "\n"
    hello += Fore.MAGENTA + "   `V/uu " + Fore.RESET + "         $$ |  $$ |$$\\   $$\\  $$$$$$$ | $$$$$$$ |$$ | $$$$$$\\  " + "\n"
    hello += Fore.MAGENTA + "     / | " + Fore.RESET + "         $$$$$$$  |$$ |  $$ |$$  __$$ |$$  __$$ |$$ |$$  __$$\\ " + "\n"
    hello += Fore.MAGENTA + "     | | " + Fore.RESET + "         $$  ____/ $$ |  $$ |$$ /  $$ |$$ /  $$ |$$ |$$$$$$$$ |" + "\n"
    hello += Fore.MAGENTA + "     o o  " + Fore.RESET + "        $$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$   ____|" + "\n"
    hello += Fore.MAGENTA + "     \\ | " + Fore.RESET + "         $$ |      \\$$$$$$  |\\$$$$$$$ |\\$$$$$$$ |$$ |\\$$$$$$$\\ " + "\n"
    hello += Fore.GREEN + "\\,/  ," + Fore.MAGENTA + "\\|" + Fore.GREEN + ",.  \\,/ " + Fore.RESET + "  \\__|       \\______/  \\_______| \\_______|\\__| \\_______|" + "\n"
    hello += "\n"
    print(hello)


def merge_data(output_file="statistics.csv"):
    stat_files = [f for f in glob("data/*.json") if "_" not in f]
    dataframes = [pd.read_json(f) for f in stat_files]
    # Concatenate all dataframes, filling missing columns with -1
    df = pd.concat(dataframes, ignore_index=True, sort=False).fillna(-1)
    
    # Remove duplicate entries based on 'name', keeping the first occurrence
    df = df.drop_duplicates(subset=['name'], keep='first')
    
    # Add source and tag columns based on the source_file name
    df["source"] = df["source_file"].apply(lambda x: x.split("/")[1].split("_")[0])
    df["tag"] = df["source_file"].apply(lambda x: x.split("_")[1].split(".")[0])

    # Save to the specified output file
    export_func = EXPORT_MAP.get(output_file.split(".")[-1], "to_excel")
    getattr(df, export_func)(output_file, index=False)
    

def main():
    parser = ArgumentParser(description="Analyze AI model providers' open source model data.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    search_parser = subparsers.add_parser("search", help="Search for models on specified site.")
    search_parser.add_argument("--site", choices=list(SITE_MAP.keys()), required=True, help="Site to search")
    search_parser.add_argument("--keyword", type=str, help="Specific keyword to search. If 'all', searches all predefined keywords.")
    search_parser.add_argument("--update", action="store_true", help="Update and overwrite existing saved results.")
    search_parser.add_argument("--save", action="store_true", default=True, help="Save the search results to a file.")
    
    stats_parser = subparsers.add_parser("stats", help="Generate statistics from saved data.")
    stats_parser.add_argument("--site", choices=list(SITE_MAP.keys()), required=True, help="Site to generate stats for.")
    stats_parser.add_argument("--save", action="store_true", default=True, help="Save the statistics to a file.")
    
    merge_parser = subparsers.add_parser("merge", help="Merge statistics from all sites into a single Excel, JSON or CSV file.")
    merge_parser.add_argument("--output", type=str, default="statistics.csv", help="Output file name.", action=ValidateAction)
    
    full_parser = subparsers.add_parser("full", help="Perform full workflow: search, stats, and merge.")
    full_parser.add_argument("--output", type=str, default="statistics.csv", help="Output file name.", action=ValidateAction)
    full_parser.add_argument("--update", action="store_true", help="Update and overwrite existing saved results.")
    
    show_parser = subparsers.add_parser("show", help="Show statistics from the merged statistics file.")
    show_parser.add_argument("--input", type=str, default="statistics.csv", help="Input file name.", action=ValidateAction)
    show_parser.add_argument("--models-per-download", type=int, default=20, help="Number of top models to show per download count.")
    show_parser.add_argument("--top-keywords", type=int, default=50, help="Number of top keywords to display.")
    show_parser.add_argument("--blur", action="store_true", default=False, help="Blur sensitive data in the output.")
    
    hello()
    args = parser.parse_args()
    
    # Determine clients based on site argument
    if args.command in {"search", "stats"}:
        clients = SITE_MAP[args.site]
    else:
        clients = []
    
    if args.command == "search":
        for client in clients:
            client = client()
            if args.keyword == "all":
                for keyword in KEYWORDS:
                    keyword = keyword.strip()
                    if not keyword:
                        continue
                    print(f"Searching '{keyword}' on {client.__class__.__name__}...")
                    client.search(keyword, save=True, update=args.update)
            else:
                print(f"Searching '{args.keyword}' on {client.__class__.__name__}...")
                client.search(args.keyword, save=True, update=args.update)
                if args.keyword not in KEYWORDS:
                    KEYWORDS.append(args.keyword)
                    with open("keywords.txt", "a") as f:
                        f.write(args.keyword + "\n")

    elif args.command == "stats":
        for client in clients:
            print("Generating statistics for", client.__class__.__name__)
            client = client()
            client.parse(save=args.save)

    elif args.command == "merge":
        merge_data(args.output)

    elif args.command == "full":
        clients = SITE_MAP["all"]
        for client in clients:
            print(f"Searching and generating statistics for {client.__name__}...")
            client = client()
            for keyword in KEYWORDS:
                print(f"Searching '{keyword}' on {client.__class__.__name__}...")
                client.search(keyword, save=True, update=args.update)
            print("Generating statistics for", client.__class__.__name__)
            client.parse(save=True)
        print(f"Merging all statistics to {args.output}...")
        merge_data(args.output)

    elif args.command == "show":
        print_stats(fname=args.input, top_n_keywords=args.top_keywords, models_per_download=args.models_per_download, blur=args.blur)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
