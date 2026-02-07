import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, User, Bell, Search, Send, Paperclip, 
  MoreVertical, Check, X, Clock, Film, MessageCircle,
  AlertCircle, UserPlus, CheckCircle, XCircle
} from 'lucide-react';
import './MessagesPage.css';

const MessagesPage = () => {
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  const [selectedConversation, setSelectedConversation] = useState(1);
  const [newMessage, setNewMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('all');

  const [conversations, setConversations] = useState([
    {
      id: 1,
      type: 'collaboration',
      name: 'Marcus Chen',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=60&h=60&fit=crop',
      role: 'Cinematographer',
      project: 'Echoes of the Silent City',
      lastMessage: 'I can definitely help with the cinematography! When can we discuss the vision?',
      timestamp: '2024-02-07T10:30:00',
      unread: 2,
      online: true
    },
    {
      id: 2,
      type: 'request',
      name: 'Sarah Martinez',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop',
      role: 'Actor',
      project: 'Urban Dreams',
      lastMessage: 'Applied to collaborate on Urban Dreams',
      timestamp: '2024-02-07T09:15:00',
      unread: 0,
      online: false,
      isPending: true
    },
    {
      id: 3,
      type: 'collaboration',
      name: 'Project Team: Echoes',
      avatar: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=60&h=60&fit=crop',
      role: 'Group Chat',
      project: 'Echoes of the Silent City',
      lastMessage: 'Elena: The sound design draft is ready for review',
      timestamp: '2024-02-06T18:45:00',
      unread: 5,
      online: false,
      isGroup: true
    },
    {
      id: 4,
      type: 'feedback',
      name: 'David Kim',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop',
      role: 'Director',
      project: 'Midnight Café Chronicles',
      lastMessage: 'Thanks for the collaboration! Left you some feedback.',
      timestamp: '2024-02-06T14:20:00',
      unread: 1,
      online: true
    },
    {
      id: 5,
      type: 'request',
      name: 'Emma Wilson',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=60&h=60&fit=crop',
      role: 'Sound Designer',
      project: 'Urban Dreams',
      lastMessage: 'Applied to collaborate on Urban Dreams',
      timestamp: '2024-02-05T16:30:00',
      unread: 0,
      online: false,
      isPending: true
    }
  ]);

  const [messages, setMessages] = useState({
    1: [
      {
        id: 1,
        sender: 'Marcus Chen',
        senderId: 2,
        text: 'Hi! I saw your project "Echoes of the Silent City" and I\'m really interested in collaborating!',
        timestamp: '2024-02-07T09:00:00',
        isOwn: false
      },
      {
        id: 2,
        sender: 'You',
        senderId: 1,
        text: 'Thank you for your interest! I checked out your portfolio and your cinematography work is incredible.',
        timestamp: '2024-02-07T09:15:00',
        isOwn: true
      },
      {
        id: 3,
        sender: 'Marcus Chen',
        senderId: 2,
        text: 'Thanks! I love the mysterious atmosphere in your script. What\'s your vision for the visual style?',
        timestamp: '2024-02-07T09:30:00',
        isOwn: false
      },
      {
        id: 4,
        sender: 'You',
        senderId: 1,
        text: 'I\'m thinking moody, desaturated colors with dramatic lighting. Kind of like Blade Runner 2049 meets Her.',
        timestamp: '2024-02-07T09:45:00',
        isOwn: true
      },
      {
        id: 5,
        sender: 'Marcus Chen',
        senderId: 2,
        text: 'I can definitely help with that! When can we discuss the vision in more detail?',
        timestamp: '2024-02-07T10:30:00',
        isOwn: false
      }
    ],
    3: [
      {
        id: 1,
        sender: 'You',
        senderId: 1,
        text: 'Hey team! Thanks everyone for joining this project.',
        timestamp: '2024-02-05T10:00:00',
        isOwn: true
      },
      {
        id: 2,
        sender: 'Marcus Chen',
        senderId: 2,
        text: 'Excited to be part of this! The script is amazing.',
        timestamp: '2024-02-05T10:15:00',
        isOwn: false
      },
      {
        id: 3,
        sender: 'Elena Rodriguez',
        senderId: 3,
        text: 'I\'ve started working on some sound concepts. Will share soon!',
        timestamp: '2024-02-05T11:30:00',
        isOwn: false
      },
      {
        id: 4,
        sender: 'Elena Rodriguez',
        senderId: 3,
        text: 'The sound design draft is ready for review',
        timestamp: '2024-02-06T18:45:00',
        isOwn: false,
        hasAttachment: true,
        attachmentName: 'sound_design_v1.mp3'
      }
    ],
    4: [
      {
        id: 1,
        sender: 'David Kim',
        senderId: 4,
        text: 'Just wanted to say it was a pleasure working with you on Midnight Café Chronicles!',
        timestamp: '2024-02-06T14:00:00',
        isOwn: false
      },
      {
        id: 2,
        sender: 'David Kim',
        senderId: 4,
        text: 'Thanks for the collaboration! Left you some feedback.',
        timestamp: '2024-02-06T14:20:00',
        isOwn: false
      }
    ]
  });

  const [notifications] = useState([
    {
      id: 1,
      type: 'application',
      text: 'Sarah Martinez applied to collaborate on "Urban Dreams"',
      timestamp: '2024-02-07T09:15:00',
      read: false
    },
    {
      id: 2,
      type: 'comment',
      text: 'Marcus Chen commented on "Echoes of the Silent City"',
      timestamp: '2024-02-07T08:30:00',
      read: false
    },
    {
      id: 3,
      type: 'message',
      text: 'New message in Project Team: Echoes',
      timestamp: '2024-02-06T18:45:00',
      read: true
    }
  ]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, selectedConversation]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const newMsg = {
      id: (messages[selectedConversation]?.length || 0) + 1,
      sender: 'You',
      senderId: 1,
      text: newMessage,
      timestamp: new Date().toISOString(),
      isOwn: true
    };

    setMessages({
      ...messages,
      [selectedConversation]: [...(messages[selectedConversation] || []), newMsg]
    });

    // Update conversation last message
    setConversations(conversations.map(conv => 
      conv.id === selectedConversation 
        ? { ...conv, lastMessage: newMessage, timestamp: new Date().toISOString() }
        : conv
    ));

    setNewMessage('');
  };

  const handleAcceptRequest = (convId) => {
    setConversations(conversations.map(conv =>
      conv.id === convId
        ? { ...conv, type: 'collaboration', isPending: false }
        : conv
    ));
    alert('Collaboration request accepted!');
  };

  const handleDeclineRequest = (convId) => {
    setConversations(conversations.filter(conv => conv.id !== convId));
    alert('Collaboration request declined.');
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  const formatMessageTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const selectedConv = conversations.find(c => c.id === selectedConversation);
  const conversationMessages = messages[selectedConversation] || [];

  const filteredConversations = conversations.filter(conv => {
    const matchesSearch = conv.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         conv.project?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesTab = activeTab === 'all' || 
                      (activeTab === 'requests' && conv.isPending) ||
                      (activeTab === 'active' && !conv.isPending);
    return matchesSearch && matchesTab;
  });

  return (
    <div className="messages-page">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container container">
          <div className="nav-logo" onClick={() => navigate('/home')}>
            <div className="logo-icon">
              <span className="logo-gradient">C</span>
            </div>
            <span className="logo-text">Creator DNA</span>
          </div>

          <div className="nav-menu">
            <a href="#" onClick={() => navigate('/home')} className="nav-link">Explore Feed</a>
            <a href="#" onClick={() => navigate('/my-projects')} className="nav-link">My Projects</a>
            <a href="#" className="nav-link active">Messages</a>
          </div>

          <div className="nav-actions">
            <button className="icon-btn">
              <Bell size={20} />
              {notifications.filter(n => !n.read).length > 0 && (
                <span className="notification-badge">{notifications.filter(n => !n.read).length}</span>
              )}
            </button>
            <button className="btn btn-primary btn-upload" onClick={() => navigate('/upload')}>
              <Upload size={18} />
              Upload Work
            </button>
            <div className="profile-menu" onClick={() => navigate('/profile')} style={{ cursor: 'pointer' }}>
              <div className="profile-avatar">
                <User size={20} />
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Messages Layout */}
      <div className="messages-layout">
        {/* Sidebar */}
        <div className="messages-sidebar">
          <div className="sidebar-header">
            <h2>Messages</h2>
            <button className="icon-btn">
              <MoreVertical size={20} />
            </button>
          </div>

          <div className="search-box">
            <Search size={18} />
            <input
              type="text"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="message-tabs">
            <button 
              className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
              onClick={() => setActiveTab('all')}
            >
              All ({conversations.length})
            </button>
            <button 
              className={`tab-btn ${activeTab === 'requests' ? 'active' : ''}`}
              onClick={() => setActiveTab('requests')}
            >
              Requests ({conversations.filter(c => c.isPending).length})
            </button>
            <button 
              className={`tab-btn ${activeTab === 'active' ? 'active' : ''}`}
              onClick={() => setActiveTab('active')}
            >
              Active ({conversations.filter(c => !c.isPending).length})
            </button>
          </div>

          <div className="conversations-list">
            {filteredConversations.map(conv => (
              <div
                key={conv.id}
                className={`conversation-item ${selectedConversation === conv.id ? 'active' : ''} ${conv.unread > 0 ? 'unread' : ''}`}
                onClick={() => setSelectedConversation(conv.id)}
              >
                <div className="conv-avatar">
                  <img src={conv.avatar} alt={conv.name} />
                  {conv.online && <span className="online-indicator"></span>}
                </div>
                <div className="conv-info">
                  <div className="conv-header">
                    <h4>{conv.name}</h4>
                    <span className="conv-time">{formatTime(conv.timestamp)}</span>
                  </div>
                  <div className="conv-preview">
                    <p>{conv.lastMessage}</p>
                    {conv.unread > 0 && <span className="unread-badge">{conv.unread}</span>}
                  </div>
                  {conv.project && <span className="conv-project"><Film size={12} /> {conv.project}</span>}
                  {conv.isPending && (
                    <span className="pending-badge">
                      <Clock size={12} /> Pending Request
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chat Area */}
        <div className="chat-area">
          {selectedConv ? (
            <>
              {/* Chat Header */}
              <div className="chat-header">
                <div className="chat-header-info">
                  <div className="chat-avatar">
                    <img src={selectedConv.avatar} alt={selectedConv.name} />
                    {selectedConv.online && <span className="online-indicator"></span>}
                  </div>
                  <div>
                    <h3>{selectedConv.name}</h3>
                    <p>{selectedConv.role} • {selectedConv.project}</p>
                  </div>
                </div>

                {selectedConv.isPending && (
                  <div className="request-actions">
                    <button 
                      className="btn btn-outline btn-sm"
                      onClick={() => handleDeclineRequest(selectedConv.id)}
                    >
                      <X size={16} /> Decline
                    </button>
                    <button 
                      className="btn btn-primary btn-sm"
                      onClick={() => handleAcceptRequest(selectedConv.id)}
                    >
                      <Check size={16} /> Accept
                    </button>
                  </div>
                )}

                <button className="icon-btn">
                  <MoreVertical size={20} />
                </button>
              </div>

              {/* Messages */}
              <div className="messages-container">
                {selectedConv.isPending && (
                  <div className="collaboration-request-banner">
                    <UserPlus size={24} />
                    <div>
                      <h4>Collaboration Request</h4>
                      <p>{selectedConv.name} wants to collaborate on "{selectedConv.project}"</p>
                    </div>
                  </div>
                )}

                {conversationMessages.map((msg) => (
                  <div key={msg.id} className={`message ${msg.isOwn ? 'own' : 'other'}`}>
                    {!msg.isOwn && (
                      <img 
                        src={selectedConv.avatar} 
                        alt={msg.sender} 
                        className="message-avatar"
                      />
                    )}
                    <div className="message-content">
                      {!msg.isOwn && <span className="message-sender">{msg.sender}</span>}
                      <div className="message-bubble">
                        <p>{msg.text}</p>
                        {msg.hasAttachment && (
                          <div className="message-attachment">
                            <Paperclip size={16} />
                            <span>{msg.attachmentName}</span>
                          </div>
                        )}
                      </div>
                      <span className="message-time">{formatMessageTime(msg.timestamp)}</span>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>

              {/* Message Input */}
              <form onSubmit={handleSendMessage} className="message-input-form">
                <button type="button" className="icon-btn">
                  <Paperclip size={20} />
                </button>
                <input
                  type="text"
                  placeholder={selectedConv.isPending ? "Accept request to send messages" : "Type a message..."}
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  disabled={selectedConv.isPending}
                />
                <button 
                  type="submit" 
                  className="send-btn"
                  disabled={!newMessage.trim() || selectedConv.isPending}
                >
                  <Send size={20} />
                </button>
              </form>
            </>
          ) : (
            <div className="no-conversation-selected">
              <MessageCircle size={64} color="#D1D5DB" />
              <h3>Select a conversation</h3>
              <p>Choose a conversation from the sidebar to start messaging</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessagesPage;
