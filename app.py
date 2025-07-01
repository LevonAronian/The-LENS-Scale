
# app.py
import streamlit as st

# --- ALL YOUR CATEGORY DATA IS STORED HERE ---
# No changes needed here. This data structure is perfect.
CATEGORY_DEFINITIONS = [
    {
        "name": "Story/Plot",
        "max_score": 10,
        "weight": 0.16,
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
        "name": "Acting",
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
    # ... (all your other categories from the original script go here) ...
    # I've omitted them for brevity, but you should copy the entire list.
    {
        "name": "Soundtrack", "max_score": 10, "weight": 0.08, "descriptors": ["..."]
    },
    {
        "name": "Plotholes", "max_score": 10, "weight": 0.05, "descriptors": ["..."]
    },
    {
        "name": "Tonality", "max_score": 10, "weight": 0.08, "descriptors": ["..."]
    },
    {
        "name": "Core Concept", "max_score": 10, "weight": 0.03, "descriptors": ["..."]
    },
    {
        "name": "Expectation", "max_score": 10, "weight": 0.05, "descriptors": ["..."]
    },
    {
        "name": "Audio", "max_score": 5, "weight": 0.05, "descriptors": ["..."]
    },
    {
        "name": "Visuals", "max_score": 5, "weight": 0.05, "descriptors": ["..."]
    },
    {
        "name": "Effects", "max_score": 5, "weight": 0.05, "descriptors": ["..."]
    },
    {
        "name": "Length", "max_score": 5, "weight": 0.08, "descriptors": ["..."]
    },
    {
        "name": "Pacing", "max_score": 5, "weight": 0.08, "descriptors": ["..."]
    },
    {
        "name": "Potential (World/Lore)", "max_score": 5, "weight": 0.03, "descriptors": ["..."]
    },
    {
        "name": "Cast (Casting & Role Fit)", "max_score": 6, "weight": 0.05, "descriptors": ["..."]
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
        "name": "Personal Enjoyment",
        "max_score": 10,
        "weight": 0.03,
        "descriptors": [
            "This is your personal gut-check score from 1-10.",
            "1: Hated it.",
            "10: Loved it."
        ]
    }
]

# --- HELPER FUNCTIONS (Adapted from your classes) ---

def calculate_score(ratings):
    """
    Calculates the final movie score based on collected ratings.
    'ratings' is a dictionary like: {'Story/Plot': 7, 'Action': None, ...}
    """
    total_weighted_score = 0.0
    total_weight_used = 0.0

    for category_data in CATEGORY_DEFINITIONS:
        name = category_data['name']
        user_rating = ratings.get(name) # Safely get the rating

        if user_rating is not None:
            max_score = category_data['max_score']
            weight = category_data['weight']

            # Normalize the score to a 0-1 scale
            normalized_score = (user_rating - 1) / (max_score - 1) if max_score > 1 else 0

            total_weighted_score += normalized_score * weight
            total_weight_used += weight

    if total_weight_used > 0:
        final_score = (total_weighted_score / total_weight_used) * 10
    else:
        final_score = 0.0

    return final_score


# --- STREAMLIT APP LAYOUT ---

# Replaces `print("Welcome...")`
st.set_page_config(page_title="Custom Movie Rater", layout="wide")
st.title("🎬 Custom Movie Rater")
st.write("Rate a movie across multiple categories to generate a precise, weighted final score.")

# Use st.session_state to store ratings across reruns
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# This replaces the `collect_all_ratings` method loop
for category in CATEGORY_DEFINITIONS:
    name = category['name']
    max_score = category['max_score']
    
    st.subheader(name)

    # Use an expander to hide the long descriptor list, making the UI cleaner
    # This replaces `print(desc)`
    with st.expander("Show/Hide Scoring Guide"):
        for desc in category['descriptors']:
            st.write(desc)
    
    # This is the replacement for `input()` and the special 'N' logic
    if name == "Action":
        # For the 'Action' category, we first ask if there is any action
        has_action = st.checkbox("Does this movie have action sequences?", key=f"has_{name}")
        if has_action:
            # If yes, show a slider to rate it
            # The 'key' is crucial for Streamlit to uniquely identify each widget
            st.session_state.ratings[name] = st.slider(
                f"Your rating (1-{max_score})", 1, max_score, key=name
            )
        else:
            # If no, we store None, just like typing 'N' in the original script
            st.session_state.ratings[name] = None
            st.info("Action category will be excluded from the final score.")
    else:
        # For all other categories, just show the slider
        st.session_state.ratings[name] = st.slider(
            f"Your rating (1-{max_score})", 1, max_score, key=name
        )
    
    st.markdown("---") # Adds a visual separator

# --- CALCULATION AND DISPLAY ---

# A button to trigger the calculation and display the summary
if st.button("✨ Calculate Final Score", use_container_width=True):
    # Retrieve all the ratings the user has entered from the session state
    user_ratings = st.session_state.ratings

    # Calculate the score using our helper function
    final_score = calculate_score(user_ratings)

    # This section replaces the `display_summary` method
    st.header("🏆 Movie Rating Summary")
    
    # Using columns for a nicer layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Ratings")
        for category in CATEGORY_DEFINITIONS:
            name = category['name']
            rating = user_ratings.get(name)
            rating_display = str(rating) if rating is not None else "N/A (No Action)"
            st.markdown(f"**{name}:** {rating_display}")

    with col2:
        st.subheader("Final Score")
        # st.metric is a great way to display a key number
        st.metric(
            label="Calculated Movie Score",
            value=f"{final_score:.1f} / 10.0",
            help="Score is calculated based on your weighted ratings."
        )
        # A progress bar provides a nice visual
        st.progress(final_score / 10.0)
        st.success("Calculation complete! See the breakdown on the left.")
