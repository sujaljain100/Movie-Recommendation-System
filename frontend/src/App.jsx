import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [movie, setMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchedMovie, setSearchedMovie] = useState("");
  const [error, setError] = useState("");

  const recommendMovie = async () => {
    if (!movie.trim()) {
      setError("Please enter a movie name.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await axios.post("http://127.0.0.1:5000/recommend", {
        movie: movie,
      });

      setRecommendations(res.data.recommendations);
      setSearchedMovie(movie);
    } catch (err) {
      console.error(err);
      setError("Backend is not running.");
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <div className="background-circle one"></div>
      <div className="background-circle two"></div>

      <header>

        <div className="logo">
          🎬 MovieMatch AI
        </div>

      </header>

      <main>

        <section className="hero">

          <span className="tag">
            AI Powered Recommendation System
          </span>

          <h1>
            Discover Your Next
            <br />
            Favourite Movie
          </h1>

          <p>
            Search any movie and instantly get similar recommendations
            using Machine Learning.
          </p>

          <div className="search-box">

            <input
              type="text"
              placeholder="Search movie..."
              value={movie}
              onChange={(e) => setMovie(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && recommendMovie()
              }
            />

            <button onClick={recommendMovie}>
              {loading ? "Searching..." : "Search"}
            </button>

          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>

        {loading && (

          <section className="results">

            <div className="section-title">
              Searching...
            </div>

            {[1,2,3,4,5].map((item)=>(
              <div className="skeleton-card" key={item}></div>
            ))}

          </section>

        )}

        {!loading &&
          recommendations.length > 0 && (

          <section className="results">

            <div className="section-title">

              Results for

              <span>
                {" "}
                "{searchedMovie}"
              </span>

            </div>

            {recommendations.map((movie,index)=>(
              <div
                className="movie-card"
                key={index}
              >

                <div className="movie-left">

                  <div className="movie-number">
                    {String(index+1).padStart(2,"0")}
                  </div>

                  <div>

                    <h2>
                      {movie}
                    </h2>

                    <p>
                      Recommended based on storyline,
                      genre and content similarity.
                    </p>

                  </div>

                </div>

                <button className="recommend-btn">
                  Recommended ⭐
                </button>

              </div>
            ))}

          </section>

        )}

        {!loading &&
          recommendations.length===0 &&
          searchedMovie!=="" && (

          <div className="empty">

            No recommendations found.

          </div>

        )}

      </main>

    </div>
  );
}

export default App;