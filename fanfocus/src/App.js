import React from 'react';
import { useNavigate } from 'react-router-dom';
import { IoHomeOutline, IoPersonOutline } from "react-icons/io5"
import { BiUpvote, BiDownvote } from "react-icons/bi";
import './App.css';


function App() {
  const navigate = useNavigate();

  return (
    <div className="App">
      <IoHomeOutline size={50} color = "white" className = "home-icon" onClick={() => navigate('/')} />
      <div className="FanFocus">FanFocus</div>
      <div className="PageName">Home</div>
      <IoPersonOutline size={50} color="white" className="profile-icon" onClick={() => navigate('/profile')}  />
      <BiDownvote size={50} color="white" className="downvote-icon" />
      <BiUpvote size={50} color="white" className="upvote-icon" />
      <div className="NextButton">Next Article</div>
    </div>
  );
}

export default App;
