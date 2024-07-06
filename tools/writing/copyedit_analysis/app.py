import os

import altair as alt
import streamlit as st
import polars as pl
import spacy


@st.cache_resource
def load_spacy_sm() -> "spacy.language.Language":
    return spacy.load("en_core_web_sm")


@st.cache_data
def load_all_writing(user_writing: str = "") -> list[tuple[str, str]]:
    """Load all files in `text_samples`."""

    @st.cache_data
    def _load_writing(file: str) -> str:
        """Load a single file in `text_samples`."""
        with open(file, "r", encoding="utf-8") as text:
            return text.read().replace("\n", " ").replace("\r", "")

    writing: list[tuple[str, str]] = []
    for text_file in os.listdir("text_samples"):
        file_loc = os.path.join("text_samples", text_file)
        author_book = text_file.split(".")[0]
        writing.append((author_book, _load_writing(file_loc)))

    # Write the user's writing.
    writing.append(("_User Input", user_writing))
    return list(writing)


@st.cache_data
def tokenize_sentences(text: str) -> list[list[str]]:
    """Parse sentences with Spacy."""
    nlp = load_spacy_sm()
    sents_tokenized: list[str] = [str(sent) for sent in nlp(text).sents]

    sents_word_tokenized: list[list[str]] = [
        [str(word) for word in nlp(sent) if not (word.is_punct or word.is_space)]
        for sent in sents_tokenized
    ]
    return sents_word_tokenized


@st.cache_data
def create_text_metadata(
    author: str, sentences_tokenized: list[list[str]]
) -> pl.DataFrame:
    sent_word_count: list[int] = [
        len(sent_tokens) for sent_tokens in sentences_tokenized
    ]
    df_word_count = pl.DataFrame(
        {
            "author": author,
            "sent_number": range(len(sent_word_count)),
            "sent_len": sent_word_count,
        }
    )
    return df_word_count


@st.cache_data
def create_long_df_all_writing(user_writing: str, num_sents: int = 50) -> pl.DataFrame:
    """Create long dataframe with `author, sent_number, sent_length`."""

    text_mappings = load_all_writing(user_writing=user_writing)
    dfs: list[pl.DataFrame] = []

    for work in text_mappings:
        author = work[0]
        text = work[1]
        sentences_tokenized: list[list[str]] = tokenize_sentences(text=text)[:num_sents]
        _df = create_text_metadata(
            author=author, sentences_tokenized=sentences_tokenized
        )
        dfs.append(_df)

    df: pl.DataFrame = pl.concat(dfs)
    return df


def plot_words_per_sentence(df_long_all_writing: pl.DataFrame) -> alt.Chart:
    selection = alt.selection_point(
        fields=["author"], bind="legend", value="_User Input"
    )
    chart = (
        alt.Chart(
            df_long_all_writing,
            title=alt.Title(
                "Words per Sentence of Texts",
            ),
        )
        .mark_line()
        .encode(
            alt.X("sent_number:O"),
            alt.Y("sent_len:Q", scale=alt.Scale(domain=[-1, 100])),
            color=alt.Color("author"),
            opacity=alt.condition(selection, alt.value(1.0), alt.value(0.0)),
        )
        .add_selection(selection)
        .properties(width=1000)
        .interactive()
    )

    return chart


def create_all_writing_statistics(df_long_all_writing: pl.DataFrame) -> pl.DataFrame:
    """Create statistics per author."""
    df = df_long_all_writing.group_by("author").agg(
        pl.col("sent_len").mean().alias("mean_len"),
        pl.col("sent_len").std().alias("stdev"),
        pl.col("sent_len").quantile(0.25).alias("q25"),
        pl.col("sent_len").median().alias("median_len"),
        pl.col("sent_len").quantile(0.25).alias("q75"),
    )
    return df.sort(by="author")


#######
# MAIN
#######
user_writing = st.text_area(label="Input Text", height=200, max_chars=100_000)
if len(user_writing) > 2:  # Needs at least 2 words.

    df_long_all_writing = create_long_df_all_writing(
        user_writing=user_writing, num_sents=50
    )

    wps_chart = plot_words_per_sentence(df_long_all_writing=df_long_all_writing)
    st.altair_chart(wps_chart)

    df_writing_stats = create_all_writing_statistics(
        df_long_all_writing=df_long_all_writing
    )
    st.dataframe(df_writing_stats)
