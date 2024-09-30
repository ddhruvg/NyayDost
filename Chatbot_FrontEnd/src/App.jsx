import React, { useState } from 'react';
import './Chatbot.css'; // Ensure you import the CSS

function Chatbot() {
  const [currentSession, setCurrentSession] = useState(0);
  const [sessions, setSessions] = useState([
    [{ sender: 'bot', text: 'Hello! How can I assist you today?' }],
  ]);
  const [input, setInput] = useState('');
  const [showHelp, setShowHelp] = useState(false);
  const [showSettings, setShowSettings] = useState(false); // State for settings popup
  const [isMenuOpen, setIsMenuOpen] = useState(false); // State for Hamburger menu

  const handleSend = () => {
    if (input.trim() === '') return;

    const newMessages = [...sessions];
    const userMessage = { sender: 'user', text: input };
    newMessages[currentSession].push(userMessage);
    
    const botResponse = { sender: 'bot', text: "I'm still learning!" };
    setTimeout(() => {
      const updatedMessages = [...newMessages];
      updatedMessages[currentSession].push(botResponse);
      setSessions(updatedMessages);
    }, 1000);

    setSessions(newMessages);
    setInput('');
  };

  const startNewSession = () => {
    setSessions([...sessions, [{ sender: 'bot', text: 'New conversation started!' }]]);
    setCurrentSession(sessions.length);
  };

  const switchSession = (index) => {
    setCurrentSession(index);
  };

  const toggleHelp = () => {
    setShowHelp(!showHelp); // Toggle help popup visibility
  };

  const toggleSettings = () => {
    setShowSettings(!showSettings); // Toggle settings popup visibility
  };

  const handleSaveSettings = () => {
    // Add save logic here if needed
    setShowSettings(false); // Close settings popup
  };

  const handleCancelSettings = () => {
    setShowSettings(false); // Close settings popup without saving
  };

  return (
    <div className="chatbot-fullscreen">
      {/* Header Bar */}
      <div className="header-bar">
        <button className="hamburger-menu" onClick={() => setIsMenuOpen(!isMenuOpen)}>
          ☰
        </button>
        <div className="header-title">Nyaydost</div>
        <button className="settings-button" onClick={toggleSettings}>⚙️</button>
      </div>

      {/* Sidebar for chat history */}
      <div className={`history-sidebar ${isMenuOpen ? 'open' : ''}`}>
        <button onClick={startNewSession} className="new-session-button">New Chat</button>
        {sessions.map((session, index) => (
          <div
            key={index}
            className={`history-item ${index === currentSession ? 'active' : ''}`}
            onClick={() => switchSession(index)}
          >
            Chat {index + 1}
          </div>
        ))}
        <button onClick={toggleHelp} className="help-button">Help</button>
      </div>

      <div className="chat-content">
        <div className="chat-window">
          {sessions[currentSession].map((msg, index) => (
            <div key={index} className={`chat-message ${msg.sender}`}>
              {msg.sender === 'bot' && <img src="/path/to/bot-icon.png" alt="Bot Icon" className="message-icon bot-icon" />}
              <div className="message-text">{msg.text}</div>
              {msg.sender === 'user' && <img src="/path/to/user-icon.png" alt="User Icon" className="message-icon user-icon" />}
            </div>
          ))}
        </div>
        <div className="chat-input-container">
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="chat-input"
          />
          <button onClick={handleSend} className="send-button">
            Send
          </button>
        </div>
      </div>

      {/* Help Popup */}
      {showHelp && (
        <div className="help-popup">
          <div className="help-popup-content">
            <h2>Help Section</h2>
            <div className="help-section">
              <h3>Generic Title 1</h3>
              <p>This is the body text for Generic Title 1.</p>
            </div>
            <button onClick={toggleHelp} className="close-help-button">Close</button>
          </div>
        </div>
      )}

      {/* Settings Popup */}
      {showSettings && (
        <div className="settings-popup">
          <div className="settings-popup-content">
            <h2>Settings</h2>
            <div className="setting-item">
              <label>
                <input type="checkbox" /> Enable Dark Mode
              </label>
            </div>
            <div className="setting-item">
              <label>
                <input type="checkbox" /> Enable Notifications
              </label>
            </div>
            <div className="setting-item">
              <label>
                <input type="checkbox" /> Auto-Save Chat History
              </label>
            </div>
            <div className="popup-buttons">
              <button onClick={handleSaveSettings} className="save-button">Save Changes</button>
              <button onClick={handleCancelSettings} className="cancel-button">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
