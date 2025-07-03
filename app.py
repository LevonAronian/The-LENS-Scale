import streamlit as st
import requests
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from datetime import datetime

# ==============================================================================
# 0. DATA DEFINITIONS (PASTE YOUR FULL LIST HERE)
# ==============================================================================

CATEGORY_DEFINITIONS = [
    {
        "name": "Story/Plot",
        "max_score": 10,
        "weight": 0.14,
        "weight_multipliers": { 10: 1.25, 9: 1.2, 8: 1.15, 7: 1.1, 6: 1.0, 5: 1.0, 4: 1.1, 3: 1.15, 2: 1.2,  1: 1.25 },
        "descriptors": [
            "1: Incoherent. A complete mess with no discernible structure or purpose.",
            "2: Barely Functional. The plot is technically present but is illogical, confusing, and almost impossible to follow.",
            "3: Deeply Flawed. Riddled with clichés and nonsensical events that make it a chore to watch.",
            "4: Predictable. A 'paint-by-numbers' plot that is completely transparent and holds no surprises.",
            "5: Functional but Bland. The story makes sense but is uninspired, unoriginal, and fails to be engaging.",
            "6: Competent. A standard, well-structured plot that serves its purpose without major issues.",
            "7: Solid and Engaging. The plot is coherent, holds your attention effectively, and has some rewarding moments.",
            "8: Very Well-Crafted. A compelling and skillfully told story with strong pacing and meaningful development.",
            "9: Excellent. An inventive, emotionally resonant, and memorable story that feels fresh and impactful.",
            "10: A Masterpiece. A profound, original, and flawlessly executed story that redefines its genre or sets a new standard."
        ]
    },
    {
        "name": "Acting (Leading roles)",
        "max_score": 10,
        "weight": 0.08,
        "weight_multipliers": { 10: 1.2, 9: 1.17, 8: 1.13, 7: 1.05, 6: 1.0, 5: 1.0, 4: 1.05, 3: 1.13, 2: 1.17, 1: 1.2 },
        "descriptors": [
            "1: Unwatchable. The performance is so bad it's embarrassing and ruins every scene.",
            "2: Amateurish. The actor is clearly out of their depth, breaking the illusion of the film.",
            "3: Consistently Weak. An unbelievable or wooden performance that undermines the character's credibility.",
            "4: Flat / One-Note. The actor shows little to no emotional range, making the character feel lifeless.",
            "5: Inconsistent. A mix of good and bad moments, where the actor fails to maintain a believable character throughout.",
            "6: Competent. The actor is believable in the role and delivers their lines effectively. A professional job.",
            "7: Good. A solid performance with clear emotional depth that makes the character feel real.",
            "8: Excellent. A charismatic, nuanced, and memorable performance that elevates the material.",
            "9: Powerful. A truly commanding and deeply moving performance that is a highlight of the film.",
            "10: Flawless / Iconic. A transcendent performance that becomes the definitive portrayal of that character."
        ]
    },
    {
        "name": "Acting (Supporting roles)",
        "max_score": 10,
        "weight": 0.05,
        "weight_multipliers": { 10: 1.2, 9: 1.17, 8: 1.13, 7: 1.05, 6: 1.0, 5: 1.0, 4: 1.05, 3: 1.13, 2: 1.17, 1: 1.2 },
        "descriptors": [
            "1: Unwatchable. The performance is so bad it's embarrassing and ruins every scene.",
            "2: Amateurish. The actor is clearly out of their depth, breaking the illusion of the film.",
            "3: Consistently Weak. An unbelievable or wooden performance that undermines the character's credibility.",
            "4: Flat / One-Note. The actor shows little to no emotional range, making the character feel lifeless.",
            "5: Inconsistent. A mix of good and bad moments, where the actor fails to maintain a believable character throughout.",
            "6: Competent. The actor is believable in the role and delivers their lines effectively. A professional job.",
            "7: Good. A solid performance with clear emotional depth that makes the character feel real.",
            "8: Excellent. A charismatic, nuanced, and memorable performance that elevates the material.",
            "9: Powerful. A truly commanding and deeply moving performance that is a highlight of the film.",
            "10: Flawless / Iconic. A transcendent performance that becomes the definitive portrayal of that character."
        ]
    },
    {
        "name": "Soundtrack (Quality and Fit)",
        "max_score": 10,
        "weight": 0.06,
        "weight_multipliers": { 10: 1.2, 9: 1.17, 8: 1.13, 7: 1.05, 6: 1.0, 5: 1.0, 4: 1.05, 3: 1.13, 2: 1.17, 1: 1.2 },
        "descriptors": [
            "1: Detrimental. The music is actively annoying or so inappropriate it sabotages the film's mood.",
            "2: Poor. A distracting or badly implemented soundtrack that consistently takes you out of the movie.",
            "3: Generic & Forgettable. The music is bland 'elevator music' that adds absolutely nothing.",
            "4: Misplaced. The music technically works but is often ill-suited for the tone or emotion of a scene.",
            "5: Adequate. The soundtrack is present and doesn't cause any problems, but is entirely unmemorable.",
            "6: Fitting. The music appropriately matches the film's tone and supports the on-screen action.",
            "7: Good. An effective soundtrack that noticeably enhances the emotion and atmosphere of key scenes.",
            "8: Excellent. A very strong, memorable score that is a core part of the film's identity.",
            "9: Powerful & Integral. The music is perfectly woven into the film, elevating the entire experience in a profound way.",
            "10: Iconic. An unforgettable, masterful soundtrack that defines the film and becomes a classic in its own right."
        ]
    },
    {
        "name": "Plotholes",
        "max_score": 10,
        "weight": 0.07,
        "weight_multipliers": { 10: 1.25, 9: 1.2, 8: 1.15, 7: 1.1, 6: 1.0, 5: 1.0, 4: 1.1, 3: 1.15, 2: 1.2,  1: 1.25 },
        "descriptors": [
            "1: Completely Broken. The film's logic is so flawed it is fundamentally nonsensical.",
            "2: Riddled with Story-Breaking Holes. Massive contradictions that make the entire plot fall apart.",
            "3: Numerous Major Holes. The plot relies on events or motivations that make no sense upon reflection.",
            "4: Several Noticeable Holes. Logical gaps that are obvious during viewing and undermine key moments.",
            "5: A Few Nagging Holes. Some inconsistencies that create distracting questions but don't derail the whole story.",
            "6: Mostly Consistent. There might be one or two minor head-scratchers that can be overlooked.",
            "7: Largely Cohesive. Any potential issues are small enough to be considered nitpicks, not true plotholes.",
            "8: Very Tight. The plot is logical and well-constructed with strong cause-and-effect.",
            "9: Almost Airtight. The internal logic is exceptionally consistent and rewards close attention.",
            "10: Flawless. Every action, motivation, and event is perfectly consistent with the film's established rules."
        ]
    },
    {
        "name": "Tonality (Fit and Consistency)",
        "max_score": 10,
        "weight": 0.07,
        "weight_multipliers": {  10: 1.2, 9: 1.17, 8: 1.13, 7: 1.05, 6: 1.0, 5: 1.0, 4: 1.05, 3: 1.13, 2: 1.17, 1: 1.2 },
        "descriptors": [
            "1: Incoherent Whiplash. Jarring, chaotic shifts between incompatible tones.",
            "2: Frequently Confused. Significant tonal shifts that feel amateurishly handled.",
            "3: Consistently Wrong. The tone is consistent, but fundamentally wrong for the story.",
            "4: Ill-Fitting Tone. Creates a consistent 'off' feeling, preventing full impact.",
            "5: Inconsistent Execution. Aims for the right tone but falters distractingly.",
            "6: Skillful but Blended Tones. Juggles multiple tones well, but lacks singular focus.",
            "7: Competent & Consistent. Establishes and maintains a clear, appropriate tone.",
            "8: Strong & Effective Tone. The tone is a powerful tool that enhances the story.",
            "9: Masterful & Immersive Tone. The tone creates a rich, all-encompassing atmosphere.",
            "10: A Tonal Masterclass. A perfect, unwavering tone that defines the experience."
        ]
    },
    {
        "name": "Core Concept",
        "max_score": 10,
        "weight": 0.03,
        "weight_multipliers": {  10: 1.2, 9: 1.17, 8: 1.13, 7: 1.05, 6: 1.0, 5: 1.0, 4: 1.05, 3: 1.13, 2: 1.17, 1: 1.2 },
        "descriptors": [
            "1: Fundamentally Bad Idea. A premise with no discernible merit.",
            "2: Deeply Unoriginal. A blatant copy of a better idea.",
            "3: Tired Premise. Done to death with nothing new to add.",
            "4: Generic Concept. A 'by-the-numbers' idea that is safe but unexciting.",
            "5: Standard Premise. An acceptable, familiar concept.",
            "6: Solid Concept. A good, sturdy idea that offers a good platform.",
            "7: Interesting Concept. A genuinely intriguing premise that sparks curiosity.",
            "8: Great Concept. A clever, original, or thought-provoking idea.",
            "9: Brilliant Concept. A truly unique and fascinating premise.",
            "10: Game-Changing Idea. A revolutionary concept."
        ]
    },
    {
        "name": "Expectation (Personal + What the Movie sets for itself)",
        "max_score": 10,
        "weight": 0.04,
        "weight_multipliers": {  10: 1.2, 9: 1.17, 8: 1.13, 7: 1.05, 6: 1.0, 5: 1.0, 4: 1.05, 3: 1.13, 2: 1.17, 1: 1.2 },
        "descriptors": [
            "1: Colossal Disappointment. Failed on all fronts.",
            "2: A Bait-and-Switch. Fundamentally misrepresented itself.",
            "3: Significant Letdown. A pale, poorly executed shadow of what it should be.",
            "4: Underwhelming. Delivered the premise in a dull, uninspired way.",
            "5: Mixed Bag. Succeeded on some promises while failing on others.",
            "6: Delivered on its Promise. Exactly what it advertised.",
            "7: Satisfying Fulfillment. Delivered on its promise in an enjoyable way.",
            "8: Exceeded Expectations. Delivered everything promised and then some.",
            "9: Impressive Over-delivery. Elevated its premise to a surprising level.",
            "10: A Transcendent Experience. Redefined what you thought the movie could be."
        ]
    },
    {
        "name": "Audio (Sound effects and Quality)",
        "max_score": 5,
        "weight": 0.06,
        "weight_multipliers": {5: 1.18, 4: 1.1, 3: 1.0, 2: 1.1, 1: 1.18},
        "descriptors": [
            "1: Unusable. Ruins the viewing experience.",
            "2: Poor. Persistent issues that pull you out of the movie.",
            "3: Acceptable. Functional but not perfect (e.g., too quiet/loud).",
            "4: Good. Clean, clear, and well-balanced. Does its job.",
            "5: Excellent. Immersive, dynamic, and enhances the film."
        ]
    },
    {
        "name": "Visuals (Realism and Interest/Intrigue)",
        "max_score": 5,
        "weight": 0.06,
        "weight_multipliers": {5: 1.18, 4: 1.1, 3: 1.0, 2: 1.1, 1: 1.18},
        "descriptors": [
            "1: Unwatchable. Visually incoherent or ugly.",
            "2: Poor. Amateurish, clumsy, or cheap-looking.",
            "3: Competent. Standard and functional, but not memorable.",
            "4: Strong. A distinct and well-executed visual style.",
            "5: Stunning. Breathtaking, innovative; every frame a painting."
        ]
    },
    {
        "name": "Effects (Visual and Special)",
        "max_score": 5,
        "weight": 0.05,
        "weight_multipliers": {5: 1.15, 4: 1.1, 3: 1.0, 2: 1.1, 1: 1.15},
        "descriptors": [
            "1: Abysmal. Laughably bad, shatters immersion.",
            "2: Poor. Unconvincing, cheap, or out of place.",
            "3: Serviceable. Gets the job done but lacks polish.",
            "4: Very Good. Convincing and well-integrated.",
            "5: Seamless. Flawless, completely believable."
        ]
    },
    {
        "name": "Length",
        "max_score": 5,
        "weight": 0.07,
        "weight_multipliers": {5: 1.18, 4: 1.12, 3: 1.0, 2: 1.12, 1: 1.18},
        "descriptors": [
            "1: Terribly Judged. Grotesquely bloated or brutally short.",
            "2: Poorly Judged. Noticeably too long or too short.",
            "3: Serviceable. Okay, but could be trimmed or use an extra scene.",
            "4: Good. Well-judged runtime, feels appropriate.",
            "5: Perfect. The absolute ideal length for the story."
        ]
    },
    {
        "name": "Pacing",
        "max_score": 5,
        "weight": 0.07,
        "weight_multipliers": {5: 1.18, 4: 1.12, 3: 1.0, 2: 1.12, 1: 1.18},
        "descriptors": [
            "1: Excruciating. The flow is completely broken; a chore to watch.",
            "2: Uneven. Inconsistent, with noticeable lulls or frantic sections.",
            "3: Acceptable. Generally fine, but with some sections that drag or feel rushed.",
            "4: Well-Paced. Good, steady rhythm that keeps you engaged.",
            "5: Masterful. Expertly controlled rhythm and flow."
        ]
    },
    {
        "name": "Potential (Subplot quality/interest as well as amount to explore)",
        "max_score": 5,
        "weight": 0.03,
        "weight_multipliers": {5: 1.15, 4: 1.1, 3: 1.0, 2: 1.1, 1: 1.15},
        "descriptors": [
            "1: Shallow & Uninspired. Feels like a cardboard cutout.",
            "2: Hollow Lore. Gestures at depth, but threads are dull.",
            "3: Sufficiently Built. Adequate for the plot, but not fascinating.",
            "4: Genuinely Intriguing. Raises compelling questions, makes you want more.",
            "5: Rich & Compelling Universe. Feels layered and real, sparks the imagination."
        ]
    },
    {
        "name": "Cast (Casting & Role Fit(look and personality))",
        "max_score": 6,
        "weight": 0.05,
        "weight_multipliers": {6: 1.2, 5: 1.14, 4: 1.0, 3: 1.0, 2: 1.14, 1: 1.18},
        "descriptors": [
            "1: Completely Miscast. Distractingly wrong for the role in every way.",
            "2: Persistent Mismatch. Generally feels out of place; hard to believe.",
            "3: Right Look, Wrong Fit. Looks the part but fails to act it.",
            "4: Performance Transcends Look. Overcomes a visual mismatch with a great performance.",
            "5: Strong Fit. A great choice where everything works.",
            "6: Perfect / Iconic Casting. Impossible to imagine anyone else in the role."
        ]
    },
    {
        "name": "Action",
        "max_score": 5,
        "weight": 0.05,
        "weight_multipliers": {5: 1.15, 4: 1.1, 3: 1.0, 2: 1.1, 1: 1.15},
        "descriptors": [
            "1: Terrible. Confusing, uninteresting, or fake-looking.",
            "2: Lackluster. Generic, clumsy, or lacks impact.",
            "3: Competent. Functional and easy to follow, but not memorable.",
            "4: Well-Executed. Exciting, creative, and a clear highlight.",
            "5: Masterful. Unique, breathtaking sequences that elevate the movie."
        ]
    },
    {
        "name": "Personal Enjoyment (Individuals Overall Score)",
        "max_score": 10,
        "weight": 0.02,
        "weight_multipliers": { 10: 1.25, 9: 1.2, 8: 1.15, 7: 1.1, 6: 1.0, 5: 1.0, 4: 1.1, 3: 1.15, 2: 1.2, 1: 1.25 },
        "descriptors": [
            "This is your personal gut-check score from 1-10.",
            "1: Hated it.",
            "10: Loved it."
        ]
    }
]


# ==============================================================================
# 1. API, DATABASE, & CORE FUNCTIONS
# ==============================================================================

# --- OMDb API Functions ---
def search_omdb(api_key, query):
    if not api_key or not query: return []
    url = f"http://www.omdbapi.com/?s={query.strip()}&type=movie&apikey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True": return data.get("Search", [])
    except requests.exceptions.RequestException as e: st.error(f"API request failed: {e}")
    return []

def get_movie_details(api_key, imdb_id):
    if not api_key or not imdb_id: return None
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True": return data
    except requests.exceptions.RequestException as e: st.error(f"API request failed: {e}")
    return None

# --- Google Sheets Functions ---
@st.cache_resource
def connect_to_gsheet():
    creds = st.secrets["gcp_service_account"]
    gc = gspread.service_account_from_dict(creds)
    spreadsheet = gc.open("MovieRatingsDB")
    return spreadsheet.worksheet("Sheet1")

def save_rating_to_gsheet(worksheet, imdb_id, movie_title, rating):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [imdb_id, movie_title, float(rating), timestamp]
    worksheet.append_row(new_row, value_input_option='USER_ENTERED')

@st.cache_data(ttl=600)
def get_leaderboard_stats(_worksheet, imdb_id):
    all_data = pd.DataFrame(_worksheet.get_all_records())
    if all_data.empty: return {"count": 0, "mean": 0, "top": [], "bottom": []}
    
    movie_ratings = all_data[all_data["imdbID"] == imdb_id].copy()
    if movie_ratings.empty: return {"count": 0, "mean": 0, "top": [], "bottom": []}
    
    movie_ratings["rating"] = pd.to_numeric(movie_ratings["rating"])
    count = len(movie_ratings)
    mean_score = movie_ratings["rating"].mean()
    top_10 = movie_ratings.nlargest(10, "rating")["rating"].tolist()
    bottom_10 = movie_ratings.nsmallest(10, "rating")["rating"].tolist()
    
    return {"count": count, "mean": mean_score, "top": top_10, "bottom": bottom_10}

# --- Core App Functions ---
def reset_app():
    keys_to_delete = ["movie_selected", "search_query", "last_searched_query", "search_results", "selected_movie_details"]
    for key in keys_to_delete:
        if key in st.session_state: del st.session_state[key]
    
    for category in CATEGORY_DEFINITIONS:
        st.session_state[f"rating_{category['name']}"] = category['max_score'] // 2 + 1
        if category["name"] == "Action": st.session_state[f"no_action_{category['name']}"] = False
    
    st.session_state.scroll_to_top = True

if "scroll_to_top" in st.session_state:
    st.components.v1.html('<script>window.parent.scrollTo(0, 0);</script>', height=0)
    del st.session_state.scroll_to_top


# ==============================================================================
# 2. CORE LOGIC CLASSES
# ==============================================================================
class Category:
    def __init__(self, name, max_score, weight, user_rating, multipliers):
        self.name, self.max_score, self.base_weight, self.user_rating, self.weight_multipliers = name, max_score, weight, user_rating, multipliers
        self.dynamic_weight = weight
class MovieRater:
    def __init__(self, categories):
        self.categories, self.final_score = categories, 0.0
    def calculate_score(self):
        total_weighted_score, total_weight_used = 0.0, 0.0
        for cat in self.categories:
            if cat.user_rating is not None and cat.max_score > 1:
                norm_score = (cat.user_rating - 1) / (cat.max_score - 1)
                multiplier = cat.weight_multipliers.get(cat.user_rating, 1.0)
                cat.dynamic_weight = cat.base_weight * multiplier
                total_weighted_score += norm_score * cat.dynamic_weight
                total_weight_used += cat.dynamic_weight
        self.final_score = (total_weighted_score / total_weight_used) * 10 if total_weight_used > 0 else 0.0
        return self.final_score, self.categories


# ==============================================================================
# 3. STREAMLIT APP LAYOUT
# ==============================================================================
st.set_page_config(page_title="LENS Movie Rater", page_icon="🎥", layout="centered")

OMDB_API_KEY = st.secrets.get("OMDB_API_KEY", "")

# --- VIEW 1: MOVIE SEARCH SCREEN ---
if not st.session_state.get("movie_selected"):
    st.title("The LENS Movie Rating System 🎥")
    
    # --- NEW: Project Description ---
    st.markdown("> *The Logical & Editorial Narrative Scrutiny (LENS) Scale*")
    st.markdown("A comprehensive framework for cinematic evaluation that brings focus to film criticism.")
    st.markdown("🖋️ In the modern discourse of film, meaningful critique is too often lost in a sea of reductive scores and unchecked personal bias. The LENS scale was conceived as a corrective, comprehensive and all-encompassing standard for cinematic evaluation.")
    st.markdown("https://github.com/LevonAronian/The-LENS-Scale/tree/main")
    st.divider()

    st.header("Search for a Movie to Rate 🔎")
    if not OMDB_API_KEY:
        st.error("OMDb API key not found. Please add it to your Streamlit secrets.")
        st.stop()
    
    search_query = st.text_input("Movie Title", key="search_query", help="Start typing to see results...")

    if len(search_query) >= 3 and search_query != st.session_state.get('last_searched_query'):
        with st.spinner("Searching..."):
            st.session_state.search_results = search_omdb(OMDB_API_KEY, search_query)
            st.session_state.last_searched_query = search_query
    if not search_query: st.session_state.search_results = []

    if st.session_state.get('search_results'):
        st.subheader("Search Results")
        for movie in st.session_state.search_results:
            col1, col2 = st.columns([1, 4])
            with col1: st.image(movie.get("Poster") if movie.get("Poster") != "N/A" else "https://i.imgur.com/u1T0t5f.png", width=100)
            with col2:
                st.write(f"**{movie['Title']}** ({movie['Year']})")
                if st.button("Select to Rate", key=movie['imdbID']):
                    with st.spinner("Loading movie details..."):
                         details = get_movie_details(OMDB_API_KEY, movie['imdbID'])
                         if details:
                            st.session_state.selected_movie_details = details
                            st.session_state.movie_selected = True
                            st.rerun()
                         else: st.error("Could not fetch details for this movie.")

# --- VIEW 2: MOVIE RATING SCREEN ---
else:
    movie = st.session_state.selected_movie_details
    try:
        worksheet = connect_to_gsheet()
    except Exception as e:
        st.error(f"Could not connect to the database. Leaderboard features are disabled. Error: {e}")
        worksheet = None

    col1, col2 = st.columns([1, 3])
    with col1: st.image(movie.get("Poster", "https://i.imgur.com/u1T0t5f.png"))
    with col2:
        st.title(movie.get("Title", "N/A"))
        st.subheader(f"({movie.get('Year', 'N/A')})")
        st.write(f"**Director:** {movie.get('Director', 'N/A')}")
        st.caption(f"_{movie.get('Plot', '')}_")

    if worksheet:
        with st.expander("⭐ See Community Ratings for this Movie"):
            with st.spinner("Fetching leaderboard..."):
                stats = get_leaderboard_stats(worksheet, movie["imdbID"])
            if stats["count"] == 0:
                st.write("Be the first to rate this movie!")
            else:
                # --- CONFIRMED: Leaderboard style with mean and top/bottom lists ---
                st.metric(label=f"Average Score (from {stats['count']} ratings)", value=f"{stats['mean']:.1f} / 10.0")
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("Top Ratings"); [st.markdown(f"- **{r:.1f}**") for r in stats["top"]]
                with c2:
                    st.subheader("Lowest Ratings"); [st.markdown(f"- **{r:.1f}**") for r in stats["bottom"]]
    
    st.divider()

    st.header("Rate this Movie using The LENS Scale")
    for cat_data in CATEGORY_DEFINITIONS:
        name, max_score, key = cat_data["name"], cat_data["max_score"], f"rating_{cat_data['name']}"
        if key not in st.session_state: st.session_state[key] = max_score // 2 + 1
        if name == "Action" and f"no_action_{name}" not in st.session_state: st.session_state[f"no_action_{name}"] = False
        st.subheader(name)
        with st.expander("Show Rating Descriptors"):
            for desc in cat_data["descriptors"]: st.write(f" - {desc}")
        if name == "Action":
            if not st.checkbox("This movie has no action.", key=f"no_action_{name}"):
                st.slider(f"Rate {name}", 1, max_score, key=key)
        else: st.slider(f"Rate {name}", 1, max_score, key=key)
        st.divider()

    if st.button("Calculate Final Score & Submit", type="primary", use_container_width=True):
        rated_cats = []
        for cat_def in CATEGORY_DEFINITIONS:
            cat_name = cat_def["name"]
            rating = None if cat_name == "Action" and st.session_state.get(f"no_action_{cat_name}") else st.session_state.get(f"rating_{cat_name}")
            rated_cats.append(Category(name=cat_name, max_score=cat_def["max_score"], weight=cat_def["weight"], user_rating=rating, multipliers=cat_def.get("weight_multipliers", {})))
        
        rater = MovieRater(rated_cats)
        final_score, summary_cats = rater.calculate_score()

        if worksheet:
            try:
                with st.spinner("Saving your rating to the leaderboard..."):
                    save_rating_to_gsheet(worksheet, movie["imdbID"], movie["Title"], final_score)
                st.success("Your rating has been saved!")
            except Exception as e: st.error(f"Could not save your rating. Error: {e}")

        st.header("🏆 Your Final Score"); st.metric(label="LENS Score", value=f"{final_score:.1f} / 10.0")
        st.info("Weights are dynamically adjusted based on your scores.", icon="⚖️")
        st.header("📊 Your Rating Summary"); st.markdown("`Category: Your Score (Actual Weight Used)`")
        
        c1, c2 = st.columns(2)
        mid = (len(summary_cats) + 1) // 2
        with c1:
            for cat in summary_cats[:mid]:
                r_disp = str(cat.user_rating) if cat.user_rating is not None else "N/A"
                w_disp = f"({cat.dynamic_weight:.3f})" if cat.user_rating is not None else ""
                st.markdown(f"**{cat.name}:** {r_disp} {w_disp}")
        with c2:
            for cat in summary_cats[mid:]:
                r_disp = str(cat.user_rating) if cat.user_rating is not None else "N/A"
                w_disp = f"({cat.dynamic_weight:.3f})" if cat.user_rating is not None else ""
                st.markdown(f"**{cat.name}:** {r_disp} {w_disp}")

        st.divider()
        # --- MOVED: Reset button is now at the end ---
        st.button("Rate a Different Movie", on_click=reset_app, use_container_width=True)
