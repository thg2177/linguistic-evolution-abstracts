"""
readability_metrics.py

Compute and append linguistic and readability metrics (K–X) to a CSV containing abstracts.
Designed for flexible execution in any Python environment.

Columns A–J must already exist:
  A: Year
  B: Source Title
  C: Page Count
  D: Cited by
  E: DOI
  F: Abstract
  G: Publisher
  H: Document Status
  I: Document Type
  J: Open Access

Columns to generate:
  K: Word Count (int)
  L: Sentence Count (int)
  M: Average Sentence Length (2 dp)
  N: Flesch Reading Ease (2 dp)
  O: Flesch-Kincaid Grade Level (2 dp)
  P: Syllable Count (int)
  Q: Gunning Fog Index (2 dp)
  R: Complex Word Count (int)
  S: SMOG Index (2 dp)
  T: Hedging Frequency (int)
  U: Hedging % (2 dp)
  V: Passive Voice Ratio (2 dp)
  W: Nominalisation Rate (4 dp)
  X: Lexical Density (4 dp)

Usage:
  python readability_metrics.py input.csv output.csv

Requirements:
  pandas, nltk, textstat, spacy
  (also download NLTK punkt, averaged_perceptron_tagger, stopwords;
   and spaCy model en_core_web_sm)
"""

import argparse
import pandas as pd
import nltk
import textstat
import spacy
from nltk import word_tokenize, sent_tokenize
# -- HEDGING WORD LIST (from Sonnet_4_linguistic_analysis.py) --
HEDGING_WORDS = {'may', 'might', 'could', 'would', 'should', 'possibly', 'probably', 'perhaps', 'maybe', 'likely', 'unlikely', 'potential', 'potentially', 'seem', 'seems', 'appear', 'appears', 'suggest', 'suggests', 'indicate', 'indicates', 'imply', 'implies', 'assume', 'assumes', 'presumably', 'conceivably', 'arguably', 'relatively', 'somewhat', 'rather', 'quite', 'fairly', 'mainly', 'largely', 'generally', 'typically', 'usually', 'often', 'frequently', 'sometimes', 'occasionally', 'tend', 'tends', 'incline', 'inclines'}

# -- NOMINALISATION WORD LIST (from Sonnet_4_linguistic_analysis.py) --
NOMINALISATION_WORDS = {}


# -- CONFIGURATION -----------------------------------------------------------
# Decimal places for each metric
DECIMAL_PLACES = {
    'Average Sentence Length': 2,
    'Flesch Reading Ease': 2,
    'Flesch-Kincaid Grade Level': 2,
    'Gunning Fog Index': 2,
    'SMOG Index': 2,
    'Hedging %': 2,
    'Passive Voice Ratio': 2,
    'Nominalisation Rate': 4,
    'Lexical Density': 4
}

# Hedging cue list (expand as needed)
HEDGE_WORDS = set([
    'may','might','could','seems','appears','suggest','likely','possible',
    'possibly','probable','probably','assume','indicative','tends','often',
    'sometimes','somewhat'
])

# Nominalisation suffixes
NOMINAL_SUFFIXES = ('ion','ment','ity','ness','ance','ence','ship')

# -----------------------------------------------------------------------------

def ensure_nltk_resources():
    """Download required NLTK data if missing."""
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('stopwords', quiet=True)


def load_spacy_model():
    """Load spaCy English model."""
    try:
        return spacy.load('en_core_web_sm')
    except OSError:
        raise RuntimeError("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")


def compute_metrics(text: str, nlp) -> dict:
    """
    Compute all metrics for a single abstract.
    """
    # Normalize text and tokenize
    text = text or ''
    sentences = sent_tokenize(text)
    sent_count = len(sentences)
    tokens = word_tokenize(text)
    words = [w for w in tokens if w.isalpha()]
    word_count = len(words)

    # Basic counts
    syllable_count = textstat.syllable_count(text)
    complex_words = textstat.difficult_words(text)

    # Readability indices
    flesch_reading = textstat.flesch_reading_ease(text)
    flesch_kincaid = textstat.flesch_kincaid_grade(text)
    gunning_fog = textstat.gunning_fog(text)
    smog = textstat.smog_index(text)

    # Hedging metrics
    hedge_count = sum(1 for w in words if w.lower() in HEDGE_WORDS)
    hedge_pct = (hedge_count / word_count * 100) if word_count else 0

    # Passive voice detection
    passive_sentences = 0
    for sent in sentences:
        doc = nlp(sent)
        if any(tok.dep_ == 'nsubjpass' for tok in doc):
            passive_sentences += 1
    passive_ratio = (passive_sentences / sent_count) if sent_count else 0

    # Nominalisation rate
    nominal_count = sum(1 for w in words if w.lower().endswith(NOMINAL_SUFFIXES))
    nominal_rate = (nominal_count / word_count * 100) if word_count else 0

    # Lexical density: proportion of content words
    doc_full = nlp(text)
    lexical_count = sum(1 for tok in doc_full if tok.pos_ in {'NOUN','VERB','ADJ','ADV'})
    lexical_density = (lexical_count / word_count * 100) if word_count else 0

    # Average sentence length
    avg_sent_len = (word_count / sent_count) if sent_count else 0

    # Assemble raw metrics
    raw = {
        'Word Count': word_count,
        'Sentence Count': sent_count,
        'Average Sentence Length': avg_sent_len,
        'Flesch Reading Ease': flesch_reading,
        'Flesch-Kincaid Grade Level': flesch_kincaid,
        'Syllable Count': syllable_count,
        'Gunning Fog Index': gunning_fog,
        'Complex Word Count': complex_words,
        'SMOG Index': smog,
        'Hedging Frequency': hedge_count,
        'Hedging %': hedge_pct,
        'Passive Voice Ratio': passive_ratio,
        'Nominalisation Rate': nominal_rate,
        'Lexical Density': lexical_density
    }

    # Round to specified decimals
    for key, val in raw.items():
        if key in DECIMAL_PLACES:
            raw[key] = round(val, DECIMAL_PLACES[key])
        elif isinstance(val, float):
            raw[key] = round(val, 0)
    return raw


def process_dataframe(df: pd.DataFrame, nlp) -> pd.DataFrame:
    """
    Compute metrics for each row's abstract.
    """
    # Fill missing abstracts
    df['Abstract'] = df['Abstract'].fillna('')

    # Compute metrics
    metrics = df['Abstract'].apply(lambda txt: compute_metrics(txt, nlp))
    metrics_df = pd.DataFrame(metrics.tolist(), index=df.index)

    # Merge and reorder columns A–X
    combined = pd.concat([df, metrics_df], axis=1)
    desired_order = list(df.columns) + list(metrics_df.columns)
    return combined[desired_order]


def main(input_csv: str, output_csv: str):
    ensure_nltk_resources()
    nlp = load_spacy_model()

    df = pd.read_csv(input_csv)
    result = process_dataframe(df, nlp)
    result.to_csv(output_csv, index=False)
    print(f"Metrics added and saved to: {output_csv}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add readability & linguistic metrics to abstracts CSV.')
    parser.add_argument('input_csv', help='Path to source CSV')
    parser.add_argument('output_csv', help='Path for output CSV')
    args = parser.parse_args()
    main(args.input_csv, args.output_csv)

