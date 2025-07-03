import streamlit as st

# ==============================================================================
# 1. CORE FUNCTIONS & STATE MANAGEMENT (REVISED)
# ==============================================================================

def reset_ratings():
    """
    Surgically removes all rating-related keys from the session state
    and sets a flag to trigger a scroll to the top on the next rerun.
    This is more reliable than st.session_state.clear().
    """
    # List all keys that need to be reset
    keys_to_delete = ['ratings']
    for category in CATEGORY_DEFINITIONS:
        keys_to_delete.append(f'rating_{category["name"]}')
        # Also handle the special 'no_action' checkbox key
        if category["name"] == "Action":
            keys_to_delete.append(f'no_action_{category["name"]}')

    # Delete only the specific keys, leaving others (like the scroll flag) intact
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

    # Now, set the scroll flag, which will persist
    st.session_state.scroll_to_top = True

# This block handles the scroll-to-top functionality.
# It runs on every script rerun and checks for the flag.
if "scroll_to_top" in st.session_state:
    st.components.v1.html(
        """
        <script>
            // This script targets the parent window (the main browser window)
            // and scrolls it to the top.
            window.parent.scrollTo(0, 0);
        </script>
        """,
        height=0
    )
    # After scrolling, delete the flag to prevent it from running again.
    del st.session_state.scroll_to_top


# ==============================================================================
# 2. DATA DEFINITIONS (WITH DYNAMIC WEIGHT PLACEHOLDERS)
# ==============================================================================

CATEGORY_DEFINITIONS = [
    {
        "name": "Story/Plot",
        "max_score": 10,
        "weight": 0.14,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.25, 9: 1.2, 8: 1.15, 7: 1.1, 6: 1.0,
            5: 1.0, 4: 1.1, 3: 1.15, 2: 1.2, 1: 1.25
        },
        "descriptors": [
            "1: Incoherent. A complete mess with no discernible structure or purpose.",
            "10: A Masterpiece. A profound, original, and flawlessly executed story."
        ]
    },
    {
        "name": "Acting (Leading roles)",
        "max_score": 10,
        "weight": 0.08,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.2, 9: 1.17, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Unwatchable.", "10: Flawless / Iconic."]
    },
    {
        "name": "Acting (Supporting roles)",
        "max_score": 10,
        "weight": 0.05,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Unwatchable.", "10: Flawless / Iconic."]
    },
    {
        "name": "Soundtrack (Quality and Fit)",
        "max_score": 10,
        "weight": 0.06,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Detrimental.", "10: Iconic."]
    },
    {
        "name": "Plotholes",
        "max_score": 10,
        "weight": 0.07,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Completely Broken.", "10: Flawless."]
    },
    {
        "name": "Tonality (Fit and Consistency)",
        "max_score": 10,
        "weight": 0.07,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Incoherent Whiplash.", "10: A Tonal Masterclass."]
    },
    {
        "name": "Core Concept",
        "max_score": 10,
        "weight": 0.03,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Fundamentally Bad Idea.", "10: Game-Changing Idea."]
    },
    {
        "name": "Expectation (Personal + What the Movie sets for itself)",
        "max_score": 10,
        "weight": 0.04,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Colossal Disappointment.", "10: A Transcendent Experience."]
    },
    {
        "name": "Audio (Sound effects and Quality)",
        "max_score": 5,
        "weight": 0.06,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Unusable.", "5: Excellent."]
    },
    {
        "name": "Visuals (Realism and Interest/Intrigue)",
        "max_score": 5,
        "weight": 0.06,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Unwatchable.", "5: Stunning."]
    },
    {
        "name": "Effects (Visual and Special)",
        "max_score": 5,
        "weight": 0.05,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Abysmal.", "5: Seamless."]
    },
    {
        "name": "Length",
        "max_score": 5,
        "weight": 0.07,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Terribly Judged.", "5: Perfect."]
    },
    {
        "name": "Pacing",
        "max_score": 5,
        "weight": 0.07,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Excruciating.", "5: Masterful."]
    },
    {
        "name": "Potential (Subplot quality/interest as well as amount to explore)",
        "max_score": 5,
        "weight": 0.03,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Shallow & Uninspired.", "5: Rich & Compelling Universe."]
    },
    {
        "name": "Cast (Casting & Role Fit(look and personality))",
        "max_score": 6,
        "weight": 0.05,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {6: 1.0, 5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Completely Miscast.", "6: Perfect / Iconic Casting."]
    },
    {
        "name": "Action",
        "max_score": 5,
        "weight": 0.05,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0},
        "descriptors": ["1: Terrible.", "5: Masterful."]
    },
    {
        "name": "Personal Enjoyment (Individuals Overall Score)",
        "max_score": 10,
        "weight": 0.02,
        # <<< EDIT YOUR 'U-CURVE' MULTIPLIERS HERE >>>
        "weight_multipliers": {
            10: 1.0, 9: 1.0, 8: 1.0, 7: 1.0, 6: 1.0,
            5: 1.0, 4: 1.0, 3: 1.0, 2: 1.0, 1: 1.0
        },
        "descriptors": ["1: Hated it.", "10: Loved it."]
    }
]


# ==============================================================================
# 3. CORE LOGIC CLASSES (UPDATED FOR DYNAMIC WEIGHTS)
# ==============================================================================

class Category:
    """An object representing a single rating category with its data."""
    def __init__(self, name, max_score, weight, user_rating, multipliers):
        self.name = name
        self.max_score = max_score
        self.base_weight = weight
        self.user_rating = user_rating
        self.weight_multipliers = multipliers
        self.dynamic_weight = weight # Initial value, will be updated during calculation

class MovieRater:
    """The main controller that calculates the final score."""
    def __init__(self, categories):
        self.categories = categories
        self.final_score = 0.0

    def calculate_score(self):
        """Calculates the final movie score based on all collected ratings."""
        total_weighted_score = 0.0
        total_weight_used = 0.0

        for category in self.categories:
            if category.user_rating is not None and category.max_score > 1:
                # Normalize the user's score to a 0-1 scale
                normalized_score = (category.user_rating - 1) / (category.max_score - 1)

                # Look up the multiplier from the dictionary using the user's score.
                # If for some reason a score is not in the dict, default to 1.0 (no change).
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
# 4. STREAMLIT APP LAYOUT
# ==============================================================================

st.set_page_config(page_title="LENS Movie Rater", page_icon="🎥", layout="centered")

st.title("The LENS Movie Rating System 🎥")
st.markdown("> *The Logical & Editorial Narrative Scrutiny (LENS) Scale*")
st.markdown("A comprehensive framework for cinematic evaluation that brings focus to film criticism.")
st.divider()

# This check re-initializes the ratings dictionary if it's been cleared.
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- Dynamically create sliders for each category ---
for category_data in CATEGORY_DEFINITIONS:
    name = category_data["name"]
    max_score = category_data["max_score"]
    st.subheader(name)

    # Simplified the expander for brevity, you can add all descriptors back if you wish
    with st.expander("Show Rating Descriptors"):
        for desc in category_data["descriptors"]:
            st.write(f" - {desc}")

    widget_key = f"rating_{name}"

    if name == "Action":
        # The key for the checkbox must be unique and persistent
        no_action = st.checkbox("This movie has no action.", key=f"no_action_{name}")
        if no_action:
            st.session_state.ratings[name] = None # Explicitly set to None
        else:
            # When the checkbox is unchecked, we get the slider's value
            st.session_state.ratings[name] = st.slider(
                f"Rate {name}", 1, max_score, value=(max_score // 2 + 1), key=widget_key
            )
    else:
        st.session_state.ratings[name] = st.slider(
            f"Rate {name}", 1, max_score, value=(max_score // 2 + 1), key=widget_key
        )

    st.divider()

# --- Calculation and Display Section ---
if st.button("Calculate Final Score", type="primary", use_container_width=True):
    rated_categories = []
    for cat_def in CATEGORY_DEFINITIONS:
        cat_name = cat_def["name"]
        user_rating = st.session_state.ratings.get(cat_name)
        # Safely get the multipliers dictionary, defaulting to empty if not found
        multipliers = cat_def.get("weight_multipliers", {})

        rated_categories.append(
            Category(
                name=cat_name,
                max_score=cat_def["max_score"],
                weight=cat_def["weight"],
                user_rating=user_rating,
                multipliers=multipliers # Pass the new dictionary to the Category object
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

# --- Final Reset Button (with corrected logic) ---
st.button("Reset Ratings", use_container_width=True, on_click=reset_ratings)
