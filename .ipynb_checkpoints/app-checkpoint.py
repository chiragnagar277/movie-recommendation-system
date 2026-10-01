import streamlit as st
import joblib
import html

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CineMatch - Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e1b4b 50%,
            #312e81 100%
        );
        color: white;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        background: linear-gradient(
            90deg,
            #f97316,
            #ec4899,
            #8b5cf6,
            #06b6d4
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 19px;
        margin-bottom: 35px;
    }

    /* Search area */
    .search-box {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }

    /* Section headings */
    .section-title {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    /* Movie cards */
    .movie-card {
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.12),
            rgba(255,255,255,0.05)
        );

        border: 1px solid rgba(255,255,255,0.15);

        border-radius: 20px;

        padding: 22px;

        min-height: 390px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.25);

        transition: transform 0.25s ease,
                    box-shadow 0.25s ease;

        margin-bottom: 20px;
    }

    .movie-card:hover {
        transform: translateY(-8px);

        box-shadow:
            0 20px 40px rgba(0,0,0,0.4);
    }

    .movie-number {
        display: inline-block;

        background: linear-gradient(
            90deg,
            #f97316,
            #ec4899
        );

        color: white;

        border-radius: 50px;

        padding: 5px 12px;

        font-size: 13px;

        font-weight: 700;

        margin-bottom: 12px;
    }

    .movie-title {
        color: #ffffff;

        font-size: 22px;

        font-weight: 800;

        margin-bottom: 15px;

        min-height: 55px;
    }

    .movie-info {
        color: #cbd5e1;

        font-size: 14px;

        line-height: 1.8;
    }

    .rating {
        color: #fbbf24;

        font-size: 18px;

        font-weight: 700;
    }

    .similarity {
        color: #22d3ee;

        font-weight: 700;

        font-size: 15px;
    }

    .genre-tag {
        display: inline-block;

        background: rgba(139,92,246,0.25);

        color: #c4b5fd;

        border: 1px solid rgba(139,92,246,0.4);

        padding: 5px 10px;

        border-radius: 20px;

        font-size: 12px;

        margin-bottom: 12px;
    }

    /* Recommendation button */
    .stButton > button {
        width: 100%;

        border: none;

        border-radius: 12px;

        padding: 12px;

        font-size: 17px;

        font-weight: 700;

        color: white;

        background: linear-gradient(
            90deg,
            #f97316,
            #ec4899,
            #8b5cf6
        );

        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: scale(1.02);

        box-shadow:
            0 8px 25px rgba(236,72,153,0.4);
    }

    /* Slider */
    .stSlider {
        padding-top: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;

        color: #94a3b8;

        margin-top: 45px;

        padding: 20px;

        border-top: 1px solid
        rgba(255,255,255,0.1);
    }

    /* Hide Streamlit menu */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    return joblib.load(
        "model/recommender.pkl"
    )


model = load_model()

movie_ds = model["movie_ds"]

cosine_sim = model["cosine_sim"]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎬 CineMatch</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover your next favorite movie with '
    'AI-powered recommendations'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SEARCH SECTION
# =========================================================

st.markdown(
    '<div class="search-box">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">🔎 Find a Movie</div>',
    unsafe_allow_html=True
)

# Get all movie names
movie_list = (
    movie_ds["Movie_Title"]
    .dropna()
    .astype(str)
    .tolist()
)

# Search input
search_text = st.text_input(
    "Type movie name",
    placeholder="Example: Shadow Hunter...",
    label_visibility="collapsed"
)


# =========================================================
# FILTER MOVIES
# =========================================================

if search_text.strip():

    filtered_movies = [
        movie
        for movie in movie_list
        if search_text.lower() in movie.lower()
    ]

else:

    filtered_movies = movie_list


# If no movie found
if not filtered_movies:

    st.warning(
        "❌ No movie found. Try another movie name."
    )

    st.stop()


# Dropdown
selected_movie = st.selectbox(
    "Select a movie from the list",
    filtered_movies
)


# Recommendation count slider

recommendation_count = st.slider(
    "🎚️ Number of recommendations",
    min_value=1,
    max_value=10,
    value=5,
    step=1
)

st.markdown(
    f"**{recommendation_count} movie(s)** will be recommended."
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# RECOMMENDATION FUNCTION
# =========================================================

def recommend_movies(
    movie_name,
    n=5
):

    matches = movie_ds[
        movie_ds["Movie_Title"]
        .astype(str)
        .str.lower()
        == movie_name.lower()
    ]

    if matches.empty:
        return []

    # Get actual position
    index = movie_ds.index.get_loc(
        matches.index[0]
    )

    # Similarity scores
    scores = list(
        enumerate(
            cosine_sim[index]
        )
    )

    # Sort highest similarity first
    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for i, score in scores[1:n+1]:

        movie = movie_ds.iloc[i]

        recommendations.append({

            "title":
                movie["Movie_Title"],

            "genre":
                movie["Genre"],

            "rating":
                movie["Rating"],

            "ratings":
                movie["Number_of_Ratings"],

            "year":
                movie["Release_Year"],

            "runtime":
                movie["Runtime_Minutes"],

            "language":
                movie["Language"],

            "age":
                movie["Age_Group"],

            "similarity":
                score
        })

    return recommendations


# =========================================================
# RECOMMEND BUTTON
# =========================================================

if st.button(
    "🚀 Get My Recommendations"
):

    recommendations = recommend_movies(
        selected_movie,
        recommendation_count
    )

    if recommendations:

        st.markdown(
            f'<div class="section-title">'
            f'✨ Movies Similar to '
            f'{html.escape(selected_movie)}'
            f'</div>',
            unsafe_allow_html=True
        )

        # Create columns
        columns = st.columns(
            min(recommendation_count, 5)
        )

        for number, movie in enumerate(
            recommendations,
            start=1
        ):

            column = columns[
                (number - 1) % len(columns)
            ]

            with column:

                # Safe values
                title = html.escape(
                    str(movie["title"])
                )

                genre = html.escape(
                    str(movie["genre"])
                )

                language = html.escape(
                    str(movie["language"])
                )

                age = html.escape(
                    str(movie["age"])
                )

                rating = float(
                    movie["rating"]
                )

                similarity = float(
                    movie["similarity"]
                )

                # Keep similarity between 0 and 1
                similarity_progress = max(
                    0,
                    min(
                        similarity,
                        1
                    )
                )

                similarity_percent = (
                    similarity_progress * 100
                )

                year = float(
                    movie["year"]
                )

                runtime = float(
                    movie["runtime"]
                )

                ratings_count = float(
                    movie["ratings"]
                )

                # Card
                st.markdown(
                    f"""
                    <div class="movie-card">

                        <div class="movie-number">
                            #{number}
                        </div>

                        <div class="movie-title">
                            🎬 {title}
                        </div>

                        <div class="genre-tag">
                            {genre}
                        </div>

                        <div class="movie-info">

                            <div class="rating">
                                ⭐ {rating:.2f}/10
                            </div>

                            <div>
                                👥
                                {ratings_count:,.0f}
                                ratings
                            </div>

                            <div>
                                📅 {year:.0f}
                            </div>

                            <div>
                                ⏱️ {runtime:.0f} minutes
                            </div>

                            <div>
                                🌐 {language}
                            </div>

                            <div>
                                👤 Age: {age}
                            </div>

                            <br>

                            <div class="similarity">
                                🎯 Similarity:
                                {similarity_percent:.1f}%
                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Progress bar
                st.progress(
                    similarity_progress
                )

    else:

        st.warning(
            "No recommendations found."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🎬 <b>CineMatch</b>

        <br>

        AI / Machine Learning Movie
        Recommendation System

        <br><br>

        Built using Python • Pandas • Scikit-learn • Streamlit

    </div>
    """,
    unsafe_allow_html=True
)