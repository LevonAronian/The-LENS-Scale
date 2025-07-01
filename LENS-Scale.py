class Category:
    """
    An object representing a single rating category.
    It holds its own data and knows how to ask for its rating.
    """
    def __init__(self, name, max_score, weight, descriptors):
        self.name = name
        self.max_score = max_score
        self.weight = weight
        self.descriptors = descriptors
        self.user_rating = None # This will be filled in by the user

    def ask_for_rating(self):
        """Displays the category info and prompts the user for a valid rating."""
        print("-" * 50)
        print(f"RATING FOR: {self.name.upper()}")
        print("-" * 50)

        for desc in self.descriptors:
            print(desc)

        # Special handling for the Action category
        is_action_category = (self.name == "Action")
        if is_action_category:
            print("OR type 'N' if the movie has no action.")

        while True:
            prompt = f"Your rating (1-{self.max_score}{' or N' if is_action_category else ''}): "
            user_input = input(prompt).strip()

            if is_action_category and user_input.lower() == 'n':
                self.user_rating = None
                return

            try:
                rating = int(user_input)
                if 1 <= rating <= self.max_score:
                    self.user_rating = rating
                    return
                else:
                    print(f"Error: Please enter a number between 1 and {self.max_score}.")
            except ValueError:
                print("Error: Invalid input. Please enter a number.")


class MovieRater:
    """
    The main controller object that manages the entire rating process.
    """
    def __init__(self, category_data):
        self.categories = [Category(**data) for data in category_data]
        self.final_score = 0.0

    def collect_all_ratings(self):
        """Goes through each category and asks the user for a rating."""
        print("Welcome to your custom movie rater!")
        print("Please answer the following questions to generate a score.\n")
        for category in self.categories:
            category.ask_for_rating()

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

    def display_summary(self):
        """Prints a final summary of all ratings and the calculated score."""
        print("\n" + "=" * 50)
        print("        MOVIE RATING SUMMARY")
        print("=" * 50)

        for category in self.categories:
            # Display the rating or 'N/A' if skipped
            rating_display = str(category.user_rating) if category.user_rating is not None else "N/A (No Action)"
            
            # The :<25 formats the string to be left-aligned in a 25-character space
            print(f"{category.name:<25}: {rating_display}")
        
        print("-" * 50)
        print(f"FINAL CALCULATED SCORE: {self.final_score:.1f} / 10.0")
        print("=" * 50)


# --- ALL YOUR CATEGORY DATA IS STORED HERE ---
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
    {
        "name": "Soundtrack",
        "max_score": 10,
        "weight": 0.08,
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
        "weight": 0.05,
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
        "name": "Tonality",
        "max_score": 10,
        "weight": 0.08,
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
        "name": "Expectation",
        "max_score": 10,
        "weight": 0.05,
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
        "name": "Audio",
        "max_score": 5,
        "weight": 0.05,
        "descriptors": [
            "1: Unusable. Ruins the viewing experience.",
            "2: Poor. Persistent issues that pull you out of the movie.",
            "3: Acceptable. Functional but not perfect (e.g., too quiet/loud).",
            "4: Good. Clean, clear, and well-balanced. Does its job.",
            "5: Excellent. Immersive, dynamic, and enhances the film."
        ]
    },
    {
        "name": "Visuals",
        "max_score": 5,
        "weight": 0.05,
        "descriptors": [
            "1: Unwatchable. Visually incoherent or ugly.",
            "2: Poor. Amateurish, clumsy, or cheap-looking.",
            "3: Competent. Standard and functional, but not memorable.",
            "4: Strong. A distinct and well-executed visual style.",
            "5: Stunning. Breathtaking, innovative; every frame a painting."
        ]
    },
    {
        "name": "Effects",
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
        "weight": 0.08,
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
        "weight": 0.08,
        "descriptors": [
            "1: Excruciating. The flow is completely broken; a chore to watch.",
            "2: Uneven. Inconsistent, with noticeable lulls or frantic sections.",
            "3: Acceptable. Generally fine, but with some sections that drag or feel rushed.",
            "4: Well-Paced. Good, steady rhythm that keeps you engaged.",
            "5: Masterful. Expertly controlled rhythm and flow."
        ]
    },
    {
        "name": "Potential (World/Lore)",
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
        "name": "Cast (Casting & Role Fit)",
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



# --- MAIN EXECUTION BLOCK ---
# This is where the program runs.
if __name__ == "__main__":
    # 1. Create a rater object with all your defined categories
    movie_rater = MovieRater(CATEGORY_DEFINITIONS)
    
    # 2. Start the rating process
    movie_rater.collect_all_ratings()
    
    # 3. Calculate the final score
    movie_rater.calculate_score()
    
    # 4. Show the results
    movie_rater.display_summary()
