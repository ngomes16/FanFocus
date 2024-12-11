import React, { useState, useEffect } from 'react';
import { IoHomeOutline, IoPersonOutline } from "react-icons/io5";
import './Profile.css';

function Profile() {
  const [interests, setInterests] = useState(() => {
    // Retrieve saved interests from localStorage when the component mounts
    const savedInterests = localStorage.getItem('interests');
    return savedInterests ? JSON.parse(savedInterests) : [];
  });
  const [inputValue, setInputValue] = useState('');

  useEffect(() => {
    // Save interests to localStorage whenever the `interests` state changes
    localStorage.setItem('interests', JSON.stringify(interests));
  }, [interests]);

  const handleAddInterest = () => {
    if (inputValue.trim() !== '') {
      setInterests([...interests, inputValue.trim()]);
      setInputValue('');
    }
  };

  const handleRemoveInterest = (indexToRemove) => {
    const filteredInterests = interests.filter((_, index) => index !== indexToRemove);
    setInterests(filteredInterests);
  };

  return (
    <div className="App">
      {/* Home Icon */}
      <IoHomeOutline
        size={50}
        color="white"
        className="home-icon"
        onClick={() => window.location = '/'}
      />
      
      <IoPersonOutline
        size={50}
        color="white"
        className="profile-icon"
        onClick={() => window.location = '/profile'}
      />
      
      <div className="FanFocus">FanFocus</div>
      <div className="PageName">Profile</div>
      
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
              onClick={() => handleRemoveInterest(index)} // Remove interest on click
              title="Click to remove"
            >
              {interest}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Profile;
