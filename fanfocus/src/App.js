import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { IoHomeOutline, IoPersonOutline } from "react-icons/io5";
import { BiUpvote, BiDownvote } from "react-icons/bi";
import './App.css';

function App() {
  const navigate = useNavigate();

  // State to hold articles and the current article index
  const [articles, setArticles] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);


  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('articles.json');
        const data = await response.json();

        // Randomize the order of articles
        const randomizedArticles = data.sort(() => Math.random() - 0.5);
        setArticles(randomizedArticles);
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    };

    fetchArticles();
  }, []);

  const handleVote = () => {
  
    if (currentIndex < articles.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      alert("No more articles to display."); 
    }
  };

  return (
    <div className="App">

      <IoHomeOutline size={50} color="white" className="home-icon" onClick={() => navigate('/')} />
      <div className="FanFocus">FanFocus</div>
      <div className="PageName">Home</div>
      <IoPersonOutline size={50} color="white" className="profile-icon" onClick={() => navigate('/profile')} />


      <div className="ArticleContent">
        {articles.length > 0 ? (
          <>
            <p>{articles[currentIndex][1]}</p> {/* Display article content */}
            <a href={articles[currentIndex][0]} target="_blank" rel="noopener noreferrer">
              {articles[currentIndex][0]}
            </a> 
          </>
        ) : (
          <p>Loading articles...</p>
        )}
      </div>

      <div className="VoteButtons">
        <BiUpvote
          size={50}
          color="white"
          className="upvote-icon"
          onClick={handleVote}
        />
        <BiDownvote
          size={50}
          color="white"
          className="downvote-icon"
          onClick={handleVote}
        />
      </div>
    </div>
  );
}

export default App;
