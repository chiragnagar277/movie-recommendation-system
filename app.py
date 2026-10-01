import streamlit as st
import streamlit.components.v1 as components
import joblib
import numpy as np
import html


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("model/recommender.pkl")


model = load_model()

movie_ds = model["movie_ds"]
cosine_sim = model["cosine_sim"]

movie_ds["Movie_Title"] = movie_ds["Movie_Title"].astype(str)

movie_list = sorted(
    movie_ds["Movie_Title"].dropna().unique().tolist()
)


# ============================================================
# MAIN THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(124, 58, 237, 0.22),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 5%,
            rgba(236, 72, 153, 0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(6, 182, 212, 0.08),
            transparent 35%
        ),
        #080b16;

    color: #f8fafc;
}

.block-container {
    max-width: 1200px;
    padding-top: 30px;
    padding-bottom: 40px;
}


/* ==========================================================
   BRAND
   ========================================================== */

.brand {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

.brand span {
    color: #a78bfa;
}

.tagline {
    color: #8f9bb3;
    font-size: 14px;
    margin-bottom: 30px;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    background:
        linear-gradient(
            135deg,
            #1e1b4b,
            #312e81
        );

    border: 1px solid
        rgba(139, 92, 246, 0.25);

    border-radius: 24px;

    padding: 35px;

    margin-bottom: 30px;

    box-shadow:
        0 20px 60px
        rgba(0, 0, 0, 0.30);
}

.hero-title {
    font-size: 32px;
    font-weight: 800;
    color: white;
}

.hero-text {
    color: #c4cbe0;
    font-size: 15px;
    margin-top: 8px;
    line-height: 1.6;
}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 20px;
    margin-bottom: 8px;
}


/* ==========================================================
   SEARCH BOX
   ========================================================== */

div[data-baseweb="select"] > div {
    background-color: #151b2d;
    border: 1px solid #303952;
    border-radius: 12px;
}


/* ==========================================================
   BUTTON
   ========================================================== */

.stButton > button {
    width: 100%;
    height: 52px;

    border: none;
    border-radius: 13px;

    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #ec4899
        );

    color: white;

    font-size: 16px;
    font-weight: 700;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 30px
        rgba(168, 85, 247, 0.35);
}


/* ==========================================================
   RECOMMENDATION HEADING
   ========================================================== */

.recommend-heading {
    font-size: 27px;
    font-weight: 800;

    color: white;

    margin-top: 38px;
    margin-bottom: 22px;
}


/* ==========================================================
   HIDE STREAMLIT DEFAULT BRANDING
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="brand">🎬 Cine<span>Match</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">'
    'Your personal movie discovery assistant'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    "## 🍿 Find your next favorite movie"
)

st.write(
    "Choose a movie you already enjoy and discover "
    "movies with similar characteristics."
)

# ============================================================
# MOVIE SEARCH
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔎 Search for a movie'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Click the box and start typing to search for a movie."
)

selected_movie = st.selectbox(
    "Movie",
    movie_list,
    label_visibility="collapsed"
)


# ============================================================
# NUMBER OF RECOMMENDATIONS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🎯 Number of recommendations'
    '</div>',
    unsafe_allow_html=True
)

number_of_movies = st.slider(
    "Number of movies",
    min_value=3,
    max_value=10,
    value=6,
    step=1,
    label_visibility="collapsed"
)

st.caption(
    "CineMatch will show "
    + str(number_of_movies)
    + " similar movies."
)


# ============================================================
# RECOMMENDATION ALGORITHM
# ============================================================

def recommend_movies(movie_name, number):

    titles = (
        movie_ds["Movie_Title"]
        .str.lower()
        .values
    )

    matches = np.where(
        titles == movie_name.lower()
    )[0]

    if len(matches) == 0:
        return []

    movie_position = int(matches[0])

    scores = list(
        enumerate(
            cosine_sim[movie_position]
        )
    )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for position, similarity in scores:

        if position == movie_position:
            continue

        recommendations.append(
            (
                int(position),
                float(similarity)
            )
        )

        if len(recommendations) >= number:
            break

    return recommendations


# ============================================================
# MOVIE CARD TEMPLATE
#
# IMPORTANT:
# This is a NORMAL string, NOT an f-string.
# Therefore the previous triple-quote syntax error cannot occur.
# ============================================================

CARD_TEMPLATE = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, Helvetica, sans-serif;
}

.movie-card {

    width: 100%;

    min-height: 330px;

    padding: 24px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            #171d35,
            #0f1425
        );

    border:
        1px solid
        rgba(139, 92, 246, 0.18);

    box-shadow:
        0 10px 30px
        rgba(0, 0, 0, 0.30);

    color: white;

    cursor: pointer;

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease,
        border-color 0.30s ease,
        background 0.30s ease;

    overflow: hidden;

    font-family: Arial, Helvetica, sans-serif;
}

.movie-card:hover {

    transform:
        translateY(-9px)
        scale(1.015);

    background:
        linear-gradient(
            145deg,
            #28204d,
            #171a36
        );

    border-color:
        rgba(168, 85, 247, 0.80);

    box-shadow:
        0 22px 45px
        rgba(124, 58, 237, 0.38),
        0 0 28px
        rgba(236, 72, 153, 0.14);
}

.number {

    display: inline-block;

    padding:
        5px 11px;

    border-radius: 20px;

    background:
        rgba(139, 92, 246, 0.15);

    color: #c4b5fd;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 0.5px;

    margin-bottom: 14px;
}

.title {

    font-size: 21px;

    font-weight: 800;

    line-height: 1.3;

    color: #ffffff;

    margin-bottom: 13px;
}

.genre {

    display: inline-block;

    padding:
        5px 10px;

    border-radius: 15px;

    background:
        rgba(236, 72, 153, 0.12);

    color: #f9a8d4;

    font-size: 12px;

    margin-bottom: 15px;
}

.info {

    color: #aeb9cf;

    font-size: 13px;

    line-height: 2;
}

.rating {

    color: #fbbf24;

    font-weight: 700;
}

.match {

    color: #67e8f9;

    font-weight: 700;

    margin-top: 7px;
}

.bar {

    height: 6px;

    width: 100%;

    background: #252c45;

    border-radius: 20px;

    margin-top: 6px;

    overflow: hidden;
}

.bar-fill {

    height: 100%;

    width: __SIMILARITY_PERCENT__%;

    border-radius: 20px;

    background:
        linear-gradient(
            90deg,
            #06b6d4,
            #8b5cf6,
            #ec4899
        );
}

</style>

</head>

<body>

<div class="movie-card">

    <div class="number">
        RECOMMENDATION #__NUMBER__
    </div>

    <div class="title">
        🎬 __TITLE__
    </div>

    <div class="genre">
        🎭 __GENRE__
    </div>

    <div class="info">

        <div class="rating">
            ⭐ __RATING__/10
        </div>

        <div>
            📅 __YEAR__
        </div>

        <div>
            ⏱️ __RUNTIME__ minutes
        </div>

        <div>
            🌐 __LANGUAGE__
        </div>

        <div class="match">
            🎯 Match: __SIMILARITY__%
        </div>

        <div class="bar">
            <div class="bar-fill"></div>
        </div>

    </div>

</div>

</body>

</html>
"""


# ============================================================
# FIND RECOMMENDATIONS
# ============================================================

if st.button(
    "✨ Find My Recommendations"
):

    recommendations = recommend_movies(
        selected_movie,
        number_of_movies
    )


    # ========================================================
    # NO RESULTS
    # ========================================================

    if not recommendations:

        st.error(
            "Sorry, no recommendations were found."
        )


    # ========================================================
    # SHOW RESULTS
    # ========================================================

    else:

        safe_selected_movie = html.escape(
            selected_movie
        )

        st.markdown(
            '<div class="recommend-heading">'
            '🍿 Movies similar to '
            '<span style="color:#a78bfa;">'
            + safe_selected_movie
            + '</span>'
            '</div>',
            unsafe_allow_html=True
        )


        # ====================================================
        # THREE CARDS PER ROW
        # ====================================================

        for start in range(
            0,
            len(recommendations),
            3
        ):

            row = recommendations[
                start:start + 3
            ]

            columns = st.columns(
                3,
                gap="large"
            )


            # =================================================
            # EACH CARD
            # =================================================

            for card_number, (
                position,
                similarity
            ) in enumerate(row):

                movie = movie_ds.iloc[position]


                # ---------------------------------------------
                # GET MOVIE INFORMATION
                # ---------------------------------------------

                title = html.escape(
                    str(movie["Movie_Title"])
                )

                genre = html.escape(
                    str(movie["Genre"])
                )

                language = html.escape(
                    str(movie["Language"])
                )

                rating = float(
                    movie["Rating"]
                )

                year = int(
                    round(
                        float(
                            movie["Release_Year"]
                        )
                    )
                )

                runtime = int(
                    round(
                        float(
                            movie["Runtime_Minutes"]
                        )
                    )
                )

                similarity = max(
                    0.0,
                    min(
                        float(similarity),
                        1.0
                    )
                )

                similarity_percent = round(
                    similarity * 100,
                    1
                )


                # ---------------------------------------------
                # BUILD CARD WITHOUT F-STRING
                # ---------------------------------------------

                card = CARD_TEMPLATE

                card = card.replace(
                    "__NUMBER__",
                    str(
                        start
                        + card_number
                        + 1
                    )
                )

                card = card.replace(
                    "__TITLE__",
                    title
                )

                card = card.replace(
                    "__GENRE__",
                    genre
                )

                card = card.replace(
                    "__RATING__",
                    f"{rating:.1f}"
                )

                card = card.replace(
                    "__YEAR__",
                    str(year)
                )

                card = card.replace(
                    "__RUNTIME__",
                    str(runtime)
                )

                card = card.replace(
                    "__LANGUAGE__",
                    language
                )

                card = card.replace(
                    "__SIMILARITY__",
                    f"{similarity_percent:.1f}"
                )

                card = card.replace(
                    "__SIMILARITY_PERCENT__",
                    f"{similarity_percent:.1f}"
                )


                # ---------------------------------------------
                # DISPLAY CARD
                # ---------------------------------------------

                with columns[card_number]:

                    components.html(
                        card,
                        height=360,
                        scrolling=False
                    )


# ============================================================
# FOOTER
#
# NO HTML HERE.
# ============================================================

st.divider()

st.caption(
    "🎬 CineMatch • AI-Powered Movie Recommendation System"
)

st.caption(
    "Built with Python • Pandas • Scikit-learn • Streamlit"
)