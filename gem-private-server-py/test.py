import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.downloader import download
# Load spaCy model
nlp = spacy.load("en_core_web_sm")
download('vader_lexicon')

# Initialize VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

def analyze_trip(review):
    # Process the review using spaCy
    doc = nlp(review)

    # Initialize parameters
    trip_type_score = 0

    # Define keywords for trip type analysis with weights
    adventurous_keywords = {"tracking": 1, "journey": 1, "steep": 1, "route": 1, "thrilling": 0.8, "exciting": 0.8, "adventure": 1, "exploration": 1, "challenge": 1, "excursion": 0.8, "exhilarating": 0.8, "bold": 0.8, "daring": 0.8, "intrepid": 0.8, "spirited": 0.8}
    relaxed_keywords = {"bench": 1, "rest": 1, "shaded": 1, "calm": 1, "tranquil": 1, "relaxing": 1, "serene": 1, "soothing": 1, "unwind": 1, "refreshing": 1, "easygoing": 1, "leisurely": 1}

    # Check for keywords related to trip type with weights
    for keyword, weight in adventurous_keywords.items():
        if keyword in review.lower():
            trip_type_score += weight

    for keyword, weight in relaxed_keywords.items():
        if keyword in review.lower():
            trip_type_score -= weight  # Subtract weight for relaxation

    # Normalize scores to a scale of 0 to 1
    trip_type = max(0, min(1, trip_type_score / sum(adventurous_keywords.values())))

    return trip_type

def analyze_budget(review):
    # Initialize parameters
    budget_score = 0

    # Define keywords for budget analysis with weights
    affordable_keywords = {"fare": 1, "limited": 1, "pocket-friendly": 1, "cheap": 1, "afforded": 1, "budget": 1, "economical": 1, "reasonable": 1, "cost-effective": 1, "inexpensive": 1, "affordable": 1, "wallet-friendly": 1, "practical": 1, "thrifty": 1, "moderate": 1, "economical": 1}
    luxurious_keywords = {"CCD": 1, "McDonalds": 1, "luxury": 1, "expensive": 1, "premium": 1, "lavish": 1, "sumptuous": 1, "opulent": 1, "extravagant": 1, "high-end": 1, "luxurious": 1, "plush": 1, "swanky": 1, "posh": 1, "sophisticated": 1}

    # Check for keywords related to budget with weights
    for keyword, weight in affordable_keywords.items():
        if keyword in review.lower():
            budget_score += weight

    for keyword, weight in luxurious_keywords.items():
        if keyword in review.lower():
            budget_score -= weight  # Subtract weight for affordability

    # Normalize scores to a scale of 0 to 1
    budget = max(0, min(1, budget_score / sum(affordable_keywords.values())))

    return budget

def predict(user_preferences, reviews):
    # Initialize overall parameters
    total_trip_type = 0
    total_budget = 0
    total_sentiment = 0
    sid = SentimentIntensityAnalyzer()

    # Analyze each review
    for i, review in enumerate(reviews, start=1):
        trip_type = analyze_trip(review)
        budget = analyze_budget(review)
        sentiment_score = sid.polarity_scores(review)['compound']

        total_trip_type += trip_type
        total_budget += budget
        total_sentiment += sentiment_score

        print(f"Review {i} - Trip Type: {trip_type}, Budget: {budget}, Sentiment: {sentiment_score}")

    # Calculate average values
    average_trip_type = total_trip_type / len(reviews)
    average_budget = total_budget / len(reviews)
    average_sentiment = total_sentiment / len(reviews)

    # Compare with user preferences
    user_distance = ((average_trip_type - user_preferences[0]) ** 2 + (average_budget - user_preferences[1]) ** 2) ** 0.5

    print(f"\nOverall Summary - Average Trip Type: {average_trip_type}, Average Budget: {average_budget}, Average Sentiment: {average_sentiment}")
    print(f"User Preferences - Trip Type: {user_preferences[0]}, Budget: {user_preferences[1]}")
    print(f"User Distance from Average - {user_distance}")

    # Decide whether the user would like the trip or not based on distance
    threshold = 0.2  # Adjust as needed
    if user_distance < threshold:
        print("The trip aligns with the user's preferences. They would likely enjoy it!")
    else:
        print("The trip may not align with the user's preferences. They might not enjoy it as much.")

def analyze_trip(review):
    # Your code to analyze trip type from the review goes here
    return 0  # Replace 0 with the analyzed trip type value

def analyze_budget(review):
    # Your code to analyze budget from the review goes here
    return 0  # Replace 0 with the analyzed budget value