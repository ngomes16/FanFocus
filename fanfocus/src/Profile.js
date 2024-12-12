import React, { useState, useEffect } from 'react';
import { IoHomeOutline, IoPersonOutline } from "react-icons/io5";
import './Profile.css';

const nbaTeams = [
  "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", 
  "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", 
  "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", 
  "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", 
  "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", 
  "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", 
  "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", 
  "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", 
  "Utah Jazz", "Washington Wizards"
];

const nflTeams = [
  "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", 
  "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", 
  "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers", 
  "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", 
  "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", 
  "Los Angeles Rams", "Miami Dolphins", "Minnesota Vikings", 
  "New England Patriots", "New Orleans Saints", "New York Giants", 
  "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", 
  "San Francisco 49ers", "Seattle Seahawks", "Tampa Bay Buccaneers", 
  "Tennessee Titans", "Washington Commanders"
];

function Profile() {
  const [interests, setInterests] = useState(() => {
    const savedInterests = localStorage.getItem('interests');
    return savedInterests ? JSON.parse(savedInterests) : [];
  });
  const [inputValue, setInputValue] = useState('');
  const [selectedTeams, setSelectedTeams] = useState([]);

  useEffect(() => {
    localStorage.setItem('interests', JSON.stringify(interests));
  }, [interests]);

  // Add a new interest (team name)
  const handleAddInterest = () => {
    if (inputValue.trim() !== '') {
      setInterests([...interests, inputValue.trim()]);
      setInputValue('');
    }
  };

  // Remove an interest
  const handleRemoveInterest = (indexToRemove) => {
    const filteredInterests = interests.filter((_, index) => index !== indexToRemove);
    setInterests(filteredInterests);
  };

  // Toggle team selection
  const toggleTeamSelection = (team) => {
    if (selectedTeams.includes(team)) {
      setSelectedTeams(selectedTeams.filter((t) => t !== team));
    } else {
      setSelectedTeams([...selectedTeams, team]);
      if (!interests.includes(team)) {
        setInterests([...interests, team]);
      }
    }
  };

  const fetchArticles = async () => {
    try {
      const validTeams = interests.filter(team => nbaTeams.includes(team) || nflTeams.includes(team));
      console.log('Valid Teams to scrape:', validTeams);
      
      const response = await fetch('/scrape_articles', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ teamNames: validTeams })
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Server error:', errorData);
        throw new Error(errorData.error || 'Failed to fetch articles');
      }
  
      const data = await response.json();
      console.log('Response from backend:', data);
    } catch (error) {
      console.error('Detailed Error:', error);
      alert(`Error fetching articles: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <IoHomeOutline
        size={50}
        color="white"
        className="home-icon"
        onClick={() => (window.location = '/')}
      />
      <IoPersonOutline
        size={50}
        color="white"
        className="profile-icon"
        onClick={() => (window.location = '/profile')}
      />
      <div className="FanFocus">FanFocus</div>
      <div className="PageName">Profile</div>

      <div className="main-container">
        {/* Teams List Section */}
        <div className="teams-section">
          <h3>NBA Teams</h3>
          <div className="teams-list">
            {nbaTeams.map((team, index) => (
              <button
                key={index}
                className={`team-button ${selectedTeams.includes(team) ? 'selected' : ''}`}
                onClick={() => toggleTeamSelection(team)}
              >
                {team}
              </button>
            ))}
          </div>
          <h3>NFL Teams</h3>
          <div className="teams-list">
            {nflTeams.map((team, index) => (
              <button
                key={index}
                className={`team-button ${selectedTeams.includes(team) ? 'selected' : ''}`}
                onClick={() => toggleTeamSelection(team)}
              >
                {team}
              </button>
            ))}
          </div>
        </div>

        {/* Interests Section */}
        <div className="interests-section">
          <h2>Your Interests</h2>
          <div className="input-container">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter an interest"
              className="interest-input"
            />
            <button onClick={handleAddInterest} className="add-button">Add</button>
          </div>
          <ul className="interests-list">
            {interests.map((interest, index) => (
              <li
                key={index}
                className="interest-item"
                onClick={() => handleRemoveInterest(index)}
                title="Click to remove"
              >
                {interest}
              </li>
            ))}
          </ul>
        </div>

        {/* Action Button */}
        <div className="fetch-articles-section">
          <button onClick={fetchArticles}>Fetch Articles</button>
        </div>
      </div>
    </div>
  );
}

export default Profile;
