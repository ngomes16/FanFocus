import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { IoHomeOutline, IoPersonOutline } from "react-icons/io5";
import { BiUpvote, BiDownvote } from "react-icons/bi";
import './App.css';

function App() {
  const navigate = useNavigate();


  const [articlesQueue, setArticlesQueue] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('/articles/one?k=5'); 
        const data = await response.json();

        if (data.length > 0) {
          
          setArticlesQueue((prevQueue) => [...prevQueue, ...data]);
        } else {
          console.error('No articles found or relevant articles available.');
        }
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    };

    // Fetch articles if queue is empty
    if (articlesQueue.length === 0) {
      fetchArticles();
    }
  }, [articlesQueue]); 

  const handleVote = async (feedback) => {
    const articleId = articlesQueue[currentIndex].id; 

    try {
      const response = await fetch(`/article/one/${articleId}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ vote: feedback }), 
      });

      if (response.ok) {
        console.log(`Feedback recorded: ${feedback === 1 ? 'Upvote' : 'Downvote'}`);
      } else {
        console.error('Failed to record feedback');
      }
    } catch (error) {
      console.error('Error sending feedback:', error);
    }

    if (currentIndex < articlesQueue.length - 1) {

      await trackArticleAsSeen(articleId);
    
      setCurrentIndex(currentIndex + 1);
    } else if (articlesQueue.length === 1) {

      console.log('Fetching more articles');
      fetchArticles();
    } 
  };

  const trackArticleAsSeen = async (articleId) => {
    try {
      const response = await fetch(`/article/one/${articleId}/seen`, {
        method: 'POST',
      });

      if (response.ok) {
        console.log(`Article ${articleId} marked as seen.`);
      } else {
        console.error('Failed to mark article as seen');
      }
    } catch (error) {
      console.error('Error marking article as seen:', error);
    }
  };

  const fetchArticles = async () => {
    try {
      const response = await fetch('/articles/one?k=5'); 
      const data = await response.json();

      if (data.length > 0) {
        
        setArticlesQueue((prevQueue) => [...prevQueue, ...data]);
        setCurrentIndex(0); 
      } else {
        console.error('No articles found or relevant articles available.');
      }
    } catch (error) {
      console.error('Error fetching articles:', error);
    }
  };

  
  const removeArticleFromQueue = () => {
    setArticlesQueue((prevQueue) => prevQueue.slice(1)); 
    setCurrentIndex(0); 
  };

  
  useEffect(() => {
    if (articlesQueue.length > 0) {
      console.log('Current queue state:', articlesQueue);
    }
  }, [currentIndex, articlesQueue]); 

  const resetSeenArticles = async () => {
    try {
      const response = await fetch('/user/one/reset-seen', {
        method: 'POST',
      });

      if (response.ok) {
        console.log('Seen articles reset successfully');
        
        setArticlesQueue([]);
        setCurrentIndex(0); 
        
        navigate('/profile');
      } else {
        console.error('Failed to reset seen articles');
      }
    } catch (error) {
      console.error('Error resetting seen articles:', error);
    }
  };

  return (
    <div className="App">
      <IoHomeOutline size={50} color="white" className="home-icon" onClick={() => navigate('/')} />
      <div className="FanFocus">FanFocus</div>
      <div className="PageName">Home</div>
      <IoPersonOutline 
        size={50} 
        color="white" 
        className="profile-icon" 
        onClick={resetSeenArticles} 
      />


      <div className="ArticleContent">
        {articlesQueue.length > 0 && articlesQueue[currentIndex] ? (
          <>
            <p>{articlesQueue[currentIndex]?.excerpt || "No excerpt available"}</p> 
            <a href={articlesQueue[currentIndex]?.url || "#"} target="_blank" rel="noopener noreferrer">
              {articlesQueue[currentIndex]?.url || "No URL available"}
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
          onClick={() => handleVote(1)} 
        />
        <BiDownvote
          size={50}
          color="white"
          className="downvote-icon"
          onClick={() => handleVote(0)} 
        />
      </div>
    </div>
  );
}

export default App;
