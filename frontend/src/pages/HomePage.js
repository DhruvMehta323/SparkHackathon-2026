import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Camera, Film, Mic, Pencil, User, Upload, 
  MapPin, Clock, Heart, MessageCircle, Share2,
  Filter, Search, Bell, LogOut
} from 'lucide-react';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const [selectedGenre, setSelectedGenre] = useState('all');
  const [selectedRole, setSelectedRole] = useState('all');

  
  const projects = [
    {
      id: 1,
      title: "Echoes of the Silent City",
      type: "Script",
      author: "Sarah Martinez",
      need: "Needs actor for monologue",
      genre: "Fantasy",
      tags: ["#fantasy", "#studentFilm", "#short"],
      timeAgo: "2 hours ago",
      image: "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=300&fit=crop",
      excerpt: "A mysterious city where sounds have disappeared...",
      likes: 24,
      comments: 8
    },
    {
      id: 2,
      title: "Urban Rhythms",
      type: "Rough Cut",
      author: "Marcus Chen",
      need: "Looking for sound designer",
      genre: "Documentary",
      tags: ["#documentary", "#experimental"],
      timeAgo: "5 hours ago",
      image: "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=400&h=300&fit=crop",
      excerpt: "Exploring the heartbeat of city life through movement...",
      likes: 42,
      comments: 15
    },
    {
      id: 3,
      title: "Midnight Café Chronicles",
      type: "Script",
      author: "Elena Rodriguez",
      need: "Seeking director collaboration",
      genre: "Drama",
      tags: ["#drama", "#indieFilm", "#character"],
      timeAgo: "1 day ago",
      image: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop",
      excerpt: "Stories that unfold in a 24-hour café...",
      likes: 67,
      comments: 23
    },
    {
      id: 4,
      title: "The Last Transmission",
      type: "Idea",
      author: "David Kim",
      need: "Writers & concept artists wanted",
      genre: "Sci-Fi",
      tags: ["#scifi", "#thriller", "#miniseries"],
      timeAgo: "3 days ago",
      image: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=300&fit=crop",
      excerpt: "A lone astronaut receives a message from Earth...",
      likes: 89,
      comments: 34
    },
    {
      id: 5,
      title: "Brushstrokes",
      type: "Rough Cut",
      author: "Aisha Patel",
      need: "Composer needed",
      genre: "Drama",
      tags: ["#artFilm", "#experimental"],
      timeAgo: "1 week ago",
      image: "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400&h=300&fit=crop",
      excerpt: "An artist's journey through color and emotion...",
      likes: 56,
      comments: 19
    },
    {
      id: 6,
      title: "Comedy of Errors 2.0",
      type: "Script",
      author: "Jake Williams",
      need: "Actors for ensemble cast",
      genre: "Comedy",
      tags: ["#comedy", "#modernAdaptation"],
      timeAgo: "1 week ago",
      image: "https://images.unsplash.com/photo-1503095396549-807759245b35?w=400&h=300&fit=crop",
      excerpt: "Shakespeare meets social media chaos...",
      likes: 112,
      comments: 45
    }
  ];

  const genres = ['All', 'Fantasy', 'Documentary', 'Drama', 'Sci-Fi', 'Comedy', 'Horror', 'Romance'];
  const roles = ['All', 'Actor', 'Writer', 'Director', 'Editor', 'Composer'];

  const filteredProjects = projects.filter(project => {
    const genreMatch = selectedGenre === 'all' || project.genre.toLowerCase() === selectedGenre.toLowerCase();
    return genreMatch;
  });

  return (
    <div className="home-page">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container container">
          <div className="nav-logo">
            <div className="logo-icon">
              <span className="logo-gradient">C</span>
            </div>
            <span className="logo-text">Creator DNA</span>
          </div>

          <div className="nav-menu">
            <a href="#" className="nav-link active">Explore Feed</a>
            <a href="#" onClick={(e) => { e.preventDefault(); navigate('/my-projects'); }} className="nav-link">My Projects</a>
            <a href="#" onClick={(e) => { e.preventDefault(); navigate('/messages'); }} className="nav-link">Messages</a>
          </div>

          <div className="nav-actions">
            <button className="icon-btn">
              <Bell size={20} />
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

      {/* Hero Banner */}
      <div className="hero-banner">
        <div className="banner-content container">
          <div className="banner-icons">
            <div className="banner-icon" style={{ top: '30%', left: '15%' }}>
              <Camera size={40} strokeWidth={1.5} />
            </div>
            <div className="banner-icon" style={{ top: '20%', right: '20%' }}>
              <Film size={45} strokeWidth={1.5} />
            </div>
            <div className="banner-icon" style={{ bottom: '30%', left: '25%' }}>
              <Mic size={35} strokeWidth={1.5} />
            </div>
            <div className="banner-icon" style={{ bottom: '25%', right: '15%' }}>
              <Pencil size={38} strokeWidth={1.5} />
            </div>
          </div>

          <h1 className="banner-title">
            Discover talent, collaborate freely,<br />
            finish your story.
          </h1>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions container">
        <div className="action-card">
          <div className="action-icon gradient-blue">
            <MapPin size={24} color="white" />
          </div>
          <div className="action-text">
            <h3>Task Type</h3>
            <p>Storyboard & Complete</p>
          </div>
        </div>

        <div className="action-card">
          <div className="action-icon gradient-purple">
            <Film size={24} color="white" />
          </div>
          <div className="action-text">
            <h3>Get Matched</h3>
            <p>Scriptwriters for Creatives</p>
          </div>
        </div>
      </div>

      {/* Discovery Feed */}
      <div className="feed-section container">
        <div className="feed-header">
          <h2 className="feed-title">Fair Discovery Feed</h2>
          
          <div className="feed-filters">
            <div className="filter-group">
              <Filter size={18} />
              <select 
                className="filter-select"
                value={selectedGenre}
                onChange={(e) => setSelectedGenre(e.target.value)}
              >
                {genres.map(genre => (
                  <option key={genre} value={genre.toLowerCase()}>
                    {genre}
                  </option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <User size={18} />
              <select 
                className="filter-select"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
              >
                {roles.map(role => (
                  <option key={role} value={role.toLowerCase()}>
                    {role}
                  </option>
                ))}
              </select>
            </div>

            <button className="icon-btn">
              <Search size={20} />
            </button>
          </div>
        </div>

        {/* Project Grid */}
        <div className="projects-grid">
          {filteredProjects.map(project => (
            <div key={project.id} className="project-card">
              <div className="project-image">
                <img src={project.image} alt={project.title} />
                <div className="project-type-badge">{project.type}</div>
              </div>

              <div className="project-content">
                <h3 className="project-title">{project.title}</h3>
                <p className="project-author">by {project.author}</p>
                
                <p className="project-excerpt">{project.excerpt}</p>

                <div className="project-need">
                  <span className="need-icon">🎬</span>
                  {project.need}
                </div>

                <div className="project-tags">
                  {project.tags.map(tag => (
                    <span key={tag} className="tag">{tag}</span>
                  ))}
                </div>

                <div className="project-footer">
                  <div className="project-stats">
                    <span className="stat">
                      <Heart size={16} />
                      {project.likes}
                    </span>
                    <span className="stat">
                      <MessageCircle size={16} />
                      {project.comments}
                    </span>
                  </div>

                  <div className="project-actions">
                    <button className="action-btn">
                      <Share2 size={16} />
                    </button>
                    <button className="btn btn-sm btn-primary">Apply</button>
                  </div>
                </div>

                <div className="project-time">
                  <Clock size={14} />
                  {project.timeAgo}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;