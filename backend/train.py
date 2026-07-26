import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================
# Load Datasets
# ==========================

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

# Keep only useful columns
movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew",
    ]
]

# Remove missing values
movies.dropna(inplace=True)


# ==========================
# Helper Functions
# ==========================

def convert(text):
    data = ast.literal_eval(text)
    result = []

    for item in data:
        result.append(item["name"])

    return result


def convert_cast(text):
    data = ast.literal_eval(text)
    result = []

    for item in data[:3]:
        result.append(item["name"])

    return result


def fetch_director(text):
    data = ast.literal_eval(text)

    for item in data:
        if item["job"] == "Director":
            return [item["name"]]

    return []


# ==========================
# Feature Extraction
# ==========================

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert_cast)
movies["crew"] = movies["crew"].apply(fetch_director)

movies["overview"] = movies["overview"].apply(lambda x: x.split())

# Remove spaces
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["keywords"] = movies["keywords"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["cast"] = movies["cast"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["crew"] = movies["crew"].apply(lambda x: [i.replace(" ", "") for i in x])

# Create Tags
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

# Final DataFrame
new_df = movies[["movie_id", "title", "tags"]]

new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))
new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

# ==========================
# Vectorization
# ==========================

cv = CountVectorizer(max_features=5000, stop_words="english")

vectors = cv.fit_transform(new_df["tags"]).toarray()

similarity = cosine_similarity(vectors)

# ==========================
# Save Files
# ==========================

pickle.dump(new_df, open("movies.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("✅ Training Completed Successfully!")