import streamlit as st
import requests

# ==============================================================================
# 0. DATA DEFINITIONS (PASTE YOUR FULL LIST HERE)
# ==============================================================================

# <<< PASTE YOUR COMPLETE, UNABRIDGED CATEGORY_DEFINITIONS LIST HERE >>>
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
# 1. API & CORE FUNCTIONS
# ==============================================================================

def search_omdb(api_key, query):
    """Searches OMDb for movies matching the query."""
    if not api_key or not query:
        return []
    url = f"http://www.omdbapi.com/?s={query.strip()}&type=movie&apikey={api_key}"
    try:
        response = requests.get(url)
        # Raises an exception for bad responses (4xx or 5xx)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Search", [])
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    return []

def get_movie_details(api_key, imdb_id):
    """Gets detailed information for a single movie using its IMDb ID."""
    if not api_key or not imdb_id:
        return None
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return data
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    return None

def reset_app():
    """Resets the entire app state to go back to the search screen."""
    # List of all state keys to reset or delete
    keys_to_reset = [
        "movie_selected", "search_query", "last_searched_query",
        "search_results", "selected_movie_details"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    
    # Also explicitly reset the rating widgets to their default values
    for category in CATEGORY_DEFINITIONS:
        name = category["name"]
        max_score = category["max_score"]
        st.session_state[f"rating_{name}"] = max_score // 2 + 1
        if name == "Action":
            st.session_state[f"no_action_{name}"] = False
    
    # Set the scroll flag to trigger on the next rerun
    st.session_state.scroll_to_top = True


# This block handles the scroll-to-top functionality.
if "scroll_to_top" in st.session_state:
    st.components.v1.html('<script>window.parent.scrollTo(0, 0);</script>', height=0)
    del st.session_state.scroll_to_top


# ==============================================================================
# 2. CORE LOGIC CLASSES (No changes needed)
# ==============================================================================

class Category:
    """An object representing a single rating category with its data."""
    def __init__(self, name, max_score, weight, user_rating, multipliers):
        self.name = name
        self.max_score = max_score
        self.base_weight = weight
        self.user_rating = user_rating
        self.weight_multipliers = multipliers
        self.dynamic_weight = weight

class MovieRater:
    """The main controller that calculates the final score."""
    def __init__(self, categories):
        self.categories = categories
        self.final_score = 0.0

    def calculate_score(self):
        total_weighted_score = 0.0
        total_weight_used = 0.0
        for category in self.categories:
            if category.user_rating is not None and category.max_score > 1:
                normalized_score = (category.user_rating - 1) / (category.max_score - 1)
                multiplier = category.weight_multipliers.get(category.user_rating, 1.0)
                category.dynamic_weight = category.base_weight * multiplier
                total_weighted_score += normalized_score * category.dynamic_weight
                total_weight_used += category.dynamic_weight

        if total_weight_used > 0:
            self.final_score = (total_weighted_score / total_weight_used) * 10
        else:
            self.final_score = 0.0
        return self.final_score, self.categories


# ==============================================================================
# 3. STREAMLIT APP LAYOUT (Main control flow)
# ==============================================================================

st.set_page_config(page_title="LENS Movie Rater", page_icon="🎥", layout="centered")

# Securely load the API key from Streamlit's secrets management
OMDB_API_KEY = st.secrets.get("OMDB_API_KEY", "")


# --- VIEW 1: MOVIE SEARCH SCREEN ---
if "movie_selected" not in st.session_state or not st.session_state.movie_selected:
    st.title("Search for a Movie to Rate 🔎")
    
    if not OMDB_API_KEY:
        st.error("OMDb API key not found. Please add it to your Streamlit secrets.")
        st.stop() # Halt execution if no key is present

    # Dynamic text input. The script reruns on every character typed.
    search_query = st.text_input("Movie Title", key="search_query", help="Start typing to see results...")

    # --- Dynamic Search Logic ---
    # Only trigger a search if the query is long enough AND has changed.
    if len(search_query) >= 3 and search_query != st.session_state.get('last_searched_query'):
        with st.spinner("Searching..."):
            st.session_state.search_results = search_omdb(OMDB_API_KEY, search_query)
            st.session_state.last_searched_query = search_query
    
    # If the user clears the search bar, also clear the results for a clean UI.
    if not search_query:
        st.session_state.search_results = []

    # --- Display Search Results ---
    if st.session_state.get('search_results'):
        st.subheader("Search Results")
        for movie in st.session_state.search_results:
            col1, col2 = st.columns([1, 4])
            with col1:
                poster_url = movie.get("Poster") if movie.get("Poster") != "N/A" else "https://i.imgur.com/u1T0t5f.png"
                st.image(poster_url, width=100)
            with col2:
                st.write(f"**{movie['Title']}** ({movie['Year']})")
                if st.button("Select to Rate", key=movie['imdbID']):
                    with st.spinner("Loading movie details..."):
                         details = get_movie_details(OMDB_API_KEY, movie['imdbID'])
                         if details:
                            # Store details and switch view
                            st.session_state.selected_movie_details = details
                            st.session_state.movie_selected = True
                            st.experimental_rerun()
                         else:
                            st.error("Could not fetch details for this movie.")


# --- VIEW 2: MOVIE RATING SCREEN ---
else:
    movie = st.session_state.selected_movie_details
    
    # Display selected movie header
    col1, col2 = st.columns([1, 3])
    with col1:
        poster_url = movie.get("Poster") if movie.get("Poster") != "N/A" else "https://i.imgur.com/u1T0t5f.png"
        st.image(poster_url)
    with col2:
        st.title(movie.get("Title", "N/A"))
        st.subheader(f"({movie.get('Year', 'N/A')})")
        st.write(f"**Director:** {movie.get('Director', 'N/A')}")
        st.caption(f"_{movie.get('Plot', '')}_")

    st.button("Rate a Different Movie", on_click=reset_app)
    st.divider()

    # --- RATING WIDGETS ---
    st.header("The LENS Movie Rating System 🎥")
    for category_data in CATEGORY_DEFINITIONS:
        name = category_data["name"]
        max_score = category_data["max_score"]
        widget_key = f"rating_{name}"

        # Initialize widget state if it doesn't exist
        if widget_key not in st.session_state:
            st.session_state[widget_key] = max_score // 2 + 1
        if name == "Action" and f"no_action_{name}" not in st.session_state:
            st.session_state[f"no_action_{name}"] = False

        st.subheader(name)
        with st.expander("Show Rating Descriptors"):
            for desc in category_data["descriptors"]:
                st.write(f" - {desc}")

        if name == "Action":
            no_action = st.checkbox("This movie has no action.", key=f"no_action_{name}")
            if not no_action:
                st.slider(f"Rate {name}", 1, max_score, key=widget_key)
        else:
            st.slider(f"Rate {name}", 1, max_score, key=widget_key)
        st.divider()

    # --- CALCULATION & DISPLAY ---
    if st.button("Calculate Final Score", type="primary", use_container_width=True):
        rated_categories = []
        for cat_def in CATEGORY_DEFINITIONS:
            cat_name = cat_def["name"]
            user_rating = None
            if cat_name == "Action" and st.session_state.get(f"no_action_{cat_name}"):
                user_rating = None
            else:
                user_rating = st.session_state.get(f"rating_{cat_name}")
            rated_categories.append(
                Category(
                    name=cat_name, max_score=cat_def["max_score"], weight=cat_def["weight"],
                    user_rating=user_rating, multipliers=cat_def.get("weight_multipliers", {})
                )
            )

        rater = MovieRater(rated_categories)
        final_score, summary_categories = rater.calculate_score()

        st.header("🏆 Final Movie Score")
        st.metric(label="LENS Score", value=f"{final_score:.1f} / 10.0")
        st.info("Weights are dynamically adjusted based on your scores.", icon="⚖️")
        st.header("📊 Rating Summary")
        st.markdown("`Category: Your Score (Actual Weight Used)`")
        
        col1, col2 = st.columns(2)
        mid_point = (len(summary_categories) + 1) // 2
        with col1:
            for category in summary_categories[:mid_point]:
                rating_display = str(category.user_rating) if category.user_rating is not None else "N/A"
                weight_display = f"({category.dynamic_weight:.3f})" if category.user_rating is not None else ""
                st.markdown(f"**{category.name}:** {rating_display} {weight_display}")
        with col2:
            for category in summary_categories[mid_point:]:
                rating_display = str(category.user_rating) if category.user_rating is not None else "N/A"
                weight_display = f"({category.dynamic_weight:.3f})" if category.user_rating is not None else ""
                st.markdown(f"**{category.name}:** {rating_display} {weight_display}")
