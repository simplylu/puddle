from datetime import datetime, timezone
from collections import Counter
import pandas as pd
import re


def blur_data(s: str, blur: bool = False) -> str:
    if blur:
        return re.sub('[aeiou]', '*', s, flags=re.IGNORECASE)
    return s


def print_stats(fname: str, top_n_keywords: int = 50, models_per_download: int = 20, blur: bool = True) -> None:
    if fname.endswith(".json"):
        df = pd.read_json(fname)
    elif fname.endswith(".xlsx"):
        df = pd.read_excel(fname)
    elif fname.endswith(".csv"):
        df = pd.read_csv(fname)
    else:
        print(f"Unsupported file format: {fname}")
        return
    
    now = datetime.now(timezone.utc)

    # Convert createdAt column to datetime with UTC timezone
    df['createdAt'] = pd.to_datetime(df['createdAt'], format='mixed', utc=True)

    # Calculate hours since each model was created
    df['hours_since_creation'] = (now - df['createdAt']).dt.total_seconds() / 3600  # type: ignore

    # Calculate download rate (downloads per hour) for each model
    # Only calculate if model has existed for some time and has downloads
    df['downloads_per_hour'] = df.apply(
        lambda row: row['downloadCount'] / row['hours_since_creation']
        if row['hours_since_creation'] > 0 and pd.notna(row['downloadCount']) and row['downloadCount'] > 0
        else 0,
        axis=1
    )

    # Extract all model names for keyword analysis
    names = df['name'].dropna().tolist()

    # Tokenize model names to extract keywords
    tokens = []
    for name in names:
        name_lower = name.lower()
        # Split on common delimiters (space, underscore, hyphen, brackets, etc.)
        words = re.split(r'[\s_\-\(\)\[\]/|]+', name_lower)
        # Define common words to exclude from analysis
        stop_words = {'a', 'an', 'the', 'and', 'or', 'for', 'of', 'in', 'on', 'at', 'to', 'by', 'with'}
        # Remove punctuation and filter out stop words
        words = [w.strip('.,!?":;') for w in words if w and w not in stop_words]
        tokens.extend(words)

    # Count frequency of each keyword across all model names
    word_counts = Counter(tokens)
    
    downloads_from_huggingface = df[df['source'] == 'huggingface']['downloadCount'].sum()
    bookmarks_from_huggingface = df[df['source'] == 'huggingface']['collectedCount'].sum()

    downloads_from_civitai = df[df['source'] == 'civitai']['downloadCount'].sum()
    bookmarks_from_civitai = df[df['source'] == 'civitai']['collectedCount'].sum()
    thumbs_up_from_civitai = df[df['source'] == 'civitai']['thumbsUpCount'].sum()
    thumbs_down_from_civitai = df[df['source'] == 'civitai']['thumbsDownCount'].sum()
    tips_from_civitai = df[df['source'] == 'civitai']['tippedAmountCount'].sum()

    downloads_from_shakker = df[df['source'] == 'shakker']['downloadCount'].sum()
    comments_from_shakker = df[df['source'] == 'shakker']['commentCount'].sum()
    runs_from_shakker = df[df['source'] == 'shakker']['runCount'].sum()

    print("=" * 50)
    print("Statistics Summary")
    print(f"Keywords: {blur_data(', '.join(df['tag'].unique()), blur)}")
    print(f"Total Models: {len(df):,}")
    print("=" * 50)
    print("\nHuggingface:")
    print(f"  Total Models: {len(df[df['source'] == 'huggingface']):,}")
    print(f"  Downloads: {downloads_from_huggingface:,}")
    print(f"  Bookmarks: {bookmarks_from_huggingface:,}")

    print("\nCivitai:")
    print(f"  Total Models: {len(df[df['source'] == 'civitai']):,}")
    print(f"  Downloads: {downloads_from_civitai:,}")
    print(f"  Bookmarks: {bookmarks_from_civitai:,}")
    print(f"  Thumbs Up: {thumbs_up_from_civitai:,}")
    print(f"  Thumbs Down: {thumbs_down_from_civitai:,}")
    print(f"  Tips: {tips_from_civitai:,}")

    print("\nShakker:")
    print(f"  Total Models: {len(df[df['source'] == 'shakker']):,}")
    print(f"  Downloads: {downloads_from_shakker:,}")
    print(f"  Comments: {comments_from_shakker:,}")
    print(f"  Runs: {runs_from_shakker:,}")
    print("=" * 50)

    print(f"\nTop {models_per_download} Models by Downloads Per Hour")
    print("=" * 50)
    top_by_rate = df.nlargest(models_per_download, 'downloads_per_hour')[['name', 'source', 'downloadCount', 'hours_since_creation', 'downloads_per_hour', "tag"]]
    print(top_by_rate.to_string(index=False))
    print("=" * 50)
    print("Total Downloads per Hour Across All Models: {:,.2f}".format(df['downloads_per_hour'].sum()))

    print(f"\nTop {top_n_keywords} Most Used Keywords in Model Names")
    print("=" * 50)
    for word, count in word_counts.most_common(top_n_keywords):
        print(f"{blur_data(word, blur):30} {count:>6}")
    print("=" * 50)
    print(f"\nTotal unique keywords: {len(word_counts)}")
    print(f"Total tokens analyzed: {len(tokens)}")
