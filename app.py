import streamlit as st

# --- ALL YOUR CATEGORY DATA IS STORED HERE ---
# (This data is unchanged from your original script)
CATEGORY_DEFINITIONS = [
    {
        "name": "Story/Plot",
        "max_score": 10,
        "weight": 0.14,
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
        "descriptors": [
            "1: Shallow & Uninspired. Feels like a cardboard cutout.",
            "2: Hollow Lore. Gestures at depth, but threads are dull.",
            "3: Sufficiently Built. Adequate for the plot, but not fascinating.",
            "4: Genuinely Intriguing. Raises compelling questions, makes you want more.",
            "5: Rich & Compelling Universe. Feels layered and real, sparks the imagination."
        ]
    },
    {
        "name": "Cast (Casting & Role Fit(look and personality)",
        "max_score": 6,
        "weight": 0.05,
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
        "descriptors": [
            "This is your personal gut-check score from 1-10.",
            "1: Hated it.",
            "10: Loved it."
        ]
    }
]


# --- CORE LOGIC CLASSES ---
# These classes handle the data and calculations, separated from the UI.

class Category:
    """An object representing a single rating category with its data."""
    def __init__(self, name, max_score, weight, user_rating):
        self.name = name
        self.max_score = max_score
        self.weight = weight
        self.user_rating = user_rating

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
            if category.user_rating is not None:
                # Normalize the score to a 0-1 scale
                normalized_score = (category.user_rating - 1) / (category.max_score - 1)

                # Add the weighted score and weight to their respective totals
                total_weighted_score += normalized_score * category.weight
                total_weight_used += category.weight

        if total_weight_used > 0:
            # Calculate the final score and scale it to 10
            self.final_score = (total_weighted_score / total_weight_used) * 10
        else:
            self.final_score = 0.0

        return self.final_score, self.categories


# --- STREAMLIT APP LAYOUT AND LOGIC ---

st.set_page_config(page_title="LENS Movie Rater", page_icon="🎥", layout="centered")

# --- Title and Introduction ---
st.title("The LENS Movie Rating System 🎥")
st.markdown("> *The Logical & Editorial Narrative Scrutiny (LENS) Scale*")
st.markdown("A comprehensive framework for cinematic evaluation that brings focus to film criticism.")
st.divider()

# --- Initialize session_state to hold ratings ---
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- Dynamically create sliders for each category ---
for category_data in CATEGORY_DEFINITIONS:
    name = category_data["name"]
    max_score = category_data["max_score"]

    st.subheader(name)

    # Use an expander to hide the detailed descriptions, keeping the UI clean
    with st.expander("Show/Hide Rating Descriptions"):
        for desc in category_data["descriptors"]:
            st.write(f" - {desc}")

    # Special handling for the "Action" category
    if name == "Action":
        no_action = st.checkbox("This movie has no action.", key=f"no_action_{name}")
        if no_action:
            # If checkbox is ticked, store None for this rating
            st.session_state.ratings[name] = None
        else:
            # Otherwise, show the slider and store its value
            st.session_state.ratings[name] = st.slider(
                f"Rate {name}", 1, max_score, value=(max_score // 2 + 1), key=f"rating_{name}"
            )
    else:
        # Standard slider for all other categories
        st.session_state.ratings[name] = st.slider(
            f"Rate {name}", 1, max_score, value=(max_score // 2 + 1), key=f"rating_{name}"
        )

    st.divider()


# --- Calculation and Display ---
if st.button("Calculate Final Score", type="primary", use_container_width=True):
    # Create Category objects from the ratings stored in session_state
    rated_categories = []
    for cat_def in CATEGORY_DEFINITIONS:
        cat_name = cat_def["name"]
        user_rating = st.session_state.ratings.get(cat_name)
        rated_categories.append(
            Category(
                name=cat_name,
                max_score=cat_def["max_score"],
                weight=cat_def["weight"],
                user_rating=user_rating
            )
        )

    # Use the MovieRater class to perform the calculation
    rater = MovieRater(rated_categories)
    final_score, summary_categories = rater.calculate_score()

    # Display the final score prominently
    st.header("🏆 Final Movie Score")
    # --- MODIFICATION 1: Changed the format string from .2f to .1f ---
    st.metric(label="LENS Score", value=f"{final_score:.1f} / 10.0")

    st.header("📊 Rating Summary")

    # Display a clean, two-column summary of the user's ratings
    col1, col2 = st.columns(2)

    # Split categories for two-column layout
    mid_point = len(summary_categories) // 2 + 1

    with col1:
        for category in summary_categories[:mid_point]:
            rating_display = str(category.user_rating) if category.user_rating is not None else "N/A"
            st.markdown(f"**{category.name}:** {rating_display}")

    with col2:
        for category in summary_categories[mid_point:]:
            rating_display = str(category.user_rating) if category.user_rating is not None else "N/A"
            st.markdown(f"**{category.name}:** {rating_display}")

# --- ADDITION 2: Added a Reset button at the bottom of the app ---
st.divider() # Add a small divider for visual separation

if st.button("Reset Ratings", use_container_width=True):
    # A simple way to reset is to clear the entire session state.
    # This will remove all stored slider values and checkbox states.
    st.session_state.clear()
    # Rerun the app from the top.
    # This ensures the page reloads with all widgets in their default state.
    st.rerun()
