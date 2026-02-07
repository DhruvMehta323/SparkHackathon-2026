import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Camera, Edit2, Instagram, Music2, Link as LinkIcon, Award,
  Briefcase, Star, MessageCircle, Upload, User, Bell, LogOut,
  Film, Pencil, Mic, Plus, X, Check
} from 'lucide-react';
import './ProfilePage.css';

const ProfilePage = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [isEditing, setIsEditing] = useState({
    basic: false,
    bio: false,
    skills: false,
    portfolio: false,
    awards: false
  });

  const [profile, setProfile] = useState({
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop',
    name: 'Alice Chen',
    profession: 'Filmmaker | Writer',
    pronouns: 'She/Her',
    bio: 'Passionate storyteller crafting narratives that bridge cultures and challenge perspectives. Specializing in character-driven dramas with a touch of magical realism.',
    hashtags: ['#IndieFilmmaker', '#CharacterDriven', '#VisualStoryteller'],
    instagram: '@alicechen.films',
    tiktok: '@alicecinema',
    skills: {
      directing: true,
      screenwriting: true,
      cinematography: false,
      editing: true,
      producing: false
    },
    portfolioLink: 'https://alicechen.portfolio.com',
    awards: [
      'Best Short Film - Sundance 2024',
      'Emerging Filmmaker Award - Toronto FF 2023',
      'Audience Choice - SXSW 2023'
    ]
  });

  const [myProjects] = useState([
    {
      id: 1,
      title: 'Echoes of the Silent City',
      type: 'Short Film',
      year: '2024',
      role: 'Writer/Director',
      image: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=200&fit=crop',
      status: 'Completed'
    },
    {
      id: 2,
      title: 'Midnight Café Chronicles',
      type: 'Web Series',
      year: '2023',
      role: 'Creator/Writer',
      image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop',
      status: 'In Production'
    },
    {
      id: 3,
      title: 'Urban Dreams',
      type: 'Documentary',
      year: '2023',
      role: 'Director',
      image: 'https://images.unsplash.com/photo-1514565131-fce0801e5785?w=300&h=200&fit=crop',
      status: 'Completed'
    }
  ]);

  const [collaborations] = useState([
    {
      id: 1,
      name: 'Marcus Chen',
      role: 'Director of Photography',
      project: 'Echoes of the Silent City',
      image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop'
    },
    {
      id: 2,
      name: 'Sarah Martinez',
      role: 'Lead Actor',
      project: 'Midnight Café Chronicles',
      image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop'
    },
    {
      id: 3,
      name: 'Indie Films Production',
      role: 'Production Company',
      project: 'Urban Dreams',
      image: 'https://images.unsplash.com/photo-1551836022-4c4c79ecde51?w=100&h=100&fit=crop'
    },
    {
      id: 4,
      name: 'Elena Rodriguez',
      role: 'Sound Designer',
      project: 'Echoes of the Silent City',
      image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop'
    }
  ]);

  const [feedback] = useState([
    {
      id: 1,
      name: 'Marcus Chen',
      role: 'Director of Photography',
      text: 'Alice has an incredible vision for storytelling. Working with her on "Echoes" was a masterclass in visual narrative. She knows exactly what she wants and communicates it beautifully.',
      rating: 5,
      project: 'Echoes of the Silent City',
      image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=60&h=60&fit=crop'
    },
    {
      id: 2,
      name: 'Sarah Martinez',
      role: 'Actor',
      text: 'One of the most collaborative directors I\'ve worked with. Alice creates a safe space for creativity and really listens to her actors. Her scripts are powerful and nuanced.',
      rating: 5,
      project: 'Midnight Café Chronicles',
      image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop'
    },
    {
      id: 3,
      name: 'David Kim',
      role: 'Producer',
      text: 'Professional, organized, and incredibly talented. Alice delivered beyond expectations and on schedule. Would definitely work with her again!',
      rating: 5,
      project: 'Urban Dreams',
      image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop'
    }
  ]);

  const handleImageClick = () => {
    fileInputRef.current.click();
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfile({ ...profile, image: reader.result });
      };
      reader.readAsDataURL(file);
    }
  };

  const toggleEdit = (section) => {
    setIsEditing({ ...isEditing, [section]: !isEditing[section] });
  };

  const updateProfile = (field, value) => {
    setProfile({ ...profile, [field]: value });
  };

  const updateHashtag = (index, value) => {
    const newHashtags = [...profile.hashtags];
    newHashtags[index] = value;
    setProfile({ ...profile, hashtags: newHashtags });
  };

  const addAward = () => {
    setProfile({ ...profile, awards: [...profile.awards, ''] });
  };

  const updateAward = (index, value) => {
    const newAwards = [...profile.awards];
    newAwards[index] = value;
    setProfile({ ...profile, awards: newAwards });
  };

  const removeAward = (index) => {
    const newAwards = profile.awards.filter((_, i) => i !== index);
    setProfile({ ...profile, awards: newAwards });
  };

  return (
    <div className="profile-page">
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
            <a href="#" className="nav-link">My Projects</a>
            <a href="#" className="nav-link">Messages</a>
          </div>

          <div className="nav-actions">
            <button className="icon-btn">
              <Bell size={20} />
            </button>
            <button className="btn btn-primary btn-upload" onClick={() => navigate('/upload')}>
              <Upload size={18} />
              Upload Work
            </button>
            <div className="profile-menu">
              <div className="profile-avatar active">
                <User size={20} />
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Profile Header */}
      <div className="profile-header">
        <div className="header-background">
          <div className="floating-icon" style={{ top: '20%', left: '15%' }}>
            <Camera size={40} strokeWidth={1.5} />
          </div>
          <div className="floating-icon" style={{ top: '30%', right: '20%' }}>
            <Film size={45} strokeWidth={1.5} />
          </div>
          <div className="floating-icon" style={{ bottom: '25%', left: '25%' }}>
            <Mic size={35} strokeWidth={1.5} />
          </div>
          <div className="floating-icon" style={{ bottom: '20%', right: '15%' }}>
            <Pencil size={38} strokeWidth={1.5} />
          </div>
        </div>

        <div className="header-content container">
          <div className="profile-main">
            <div className="profile-image-container">
              <img src={profile.image} alt={profile.name} className="profile-image-large" />
              <button className="change-photo-btn" onClick={handleImageClick}>
                <Camera size={20} />
              </button>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleImageChange}
                accept="image/*"
                style={{ display: 'none' }}
              />
            </div>

            <div className="profile-info">
              {!isEditing.basic ? (
                <>
                  <div className="info-header">
                    <div>
                      <h1 className="profile-name">{profile.name}</h1>
                      <p className="profile-profession">{profile.profession}</p>
                      <p className="profile-pronouns">{profile.pronouns}</p>
                    </div>
                    <button className="edit-btn" onClick={() => toggleEdit('basic')}>
                      <Edit2 size={18} />
                    </button>
                  </div>
                </>
              ) : (
                <div className="edit-form">
                  <input
                    type="text"
                    className="input"
                    value={profile.name}
                    onChange={(e) => updateProfile('name', e.target.value)}
                    placeholder="Name"
                  />
                  <input
                    type="text"
                    className="input"
                    value={profile.profession}
                    onChange={(e) => updateProfile('profession', e.target.value)}
                    placeholder="Profession"
                  />
                  <input
                    type="text"
                    className="input"
                    value={profile.pronouns}
                    onChange={(e) => updateProfile('pronouns', e.target.value)}
                    placeholder="Pronouns"
                  />
                  <button className="btn btn-primary btn-sm" onClick={() => toggleEdit('basic')}>
                    <Check size={16} /> Save
                  </button>
                </div>
              )}

              <div className="social-links">
                <a href={`https://instagram.com/${profile.instagram.replace('@', '')}`} target="_blank" rel="noopener noreferrer" className="social-btn">
                  <Instagram size={20} />
                  {profile.instagram}
                </a>
                <a href={`https://tiktok.com/${profile.tiktok.replace('@', '')}`} target="_blank" rel="noopener noreferrer" className="social-btn">
                  <Music2 size={20} />
                  {profile.tiktok}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Profile Content */}
      <div className="profile-content container">
        {/* Bio Section */}
        <div className="profile-section">
          <div className="section-header">
            <h2>About</h2>
            <button className="edit-btn" onClick={() => toggleEdit('bio')}>
              <Edit2 size={18} />
            </button>
          </div>
          {!isEditing.bio ? (
            <>
              <p className="bio-text">{profile.bio}</p>
              <div className="hashtags">
                {profile.hashtags.map((tag, index) => (
                  <span key={index} className="hashtag">{tag}</span>
                ))}
              </div>
            </>
          ) : (
            <div className="edit-form">
              <textarea
                className="input"
                rows="4"
                value={profile.bio}
                onChange={(e) => updateProfile('bio', e.target.value)}
                placeholder="Tell us about yourself..."
              />
              <div className="hashtag-edit">
                {profile.hashtags.map((tag, index) => (
                  <input
                    key={index}
                    type="text"
                    className="input"
                    value={tag}
                    onChange={(e) => updateHashtag(index, e.target.value)}
                    placeholder={`Hashtag ${index + 1}`}
                  />
                ))}
              </div>
              <button className="btn btn-primary btn-sm" onClick={() => toggleEdit('bio')}>
                <Check size={16} /> Save
              </button>
            </div>
          )}
        </div>

        {/* Skills & Portfolio Section */}
        <div className="two-column-section">
          <div className="profile-section">
            <div className="section-header">
              <h2>Skills</h2>
              <button className="edit-btn" onClick={() => toggleEdit('skills')}>
                <Edit2 size={18} />
              </button>
            </div>
            <div className="skills-list">
              {Object.entries(profile.skills).map(([skill, enabled]) => (
                <div key={skill} className="skill-item">
                  <input
                    type="checkbox"
                    id={skill}
                    checked={enabled}
                    onChange={(e) => setProfile({
                      ...profile,
                      skills: { ...profile.skills, [skill]: e.target.checked }
                    })}
                    disabled={!isEditing.skills}
                  />
                  <label htmlFor={skill}>{skill.charAt(0).toUpperCase() + skill.slice(1)}</label>
                </div>
              ))}
            </div>
          </div>

          <div className="profile-section">
            <div className="section-header">
              <h2>Portfolio Link</h2>
              <button className="edit-btn" onClick={() => toggleEdit('portfolio')}>
                <Edit2 size={18} />
              </button>
            </div>
            {!isEditing.portfolio ? (
              <a href={profile.portfolioLink} target="_blank" rel="noopener noreferrer" className="portfolio-link">
                <LinkIcon size={18} />
                {profile.portfolioLink}
              </a>
            ) : (
              <div className="edit-form">
                <input
                  type="url"
                  className="input"
                  value={profile.portfolioLink}
                  onChange={(e) => updateProfile('portfolioLink', e.target.value)}
                  placeholder="Portfolio URL"
                />
                <button className="btn btn-primary btn-sm" onClick={() => toggleEdit('portfolio')}>
                  <Check size={16} /> Save
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Awards & Recognition */}
        <div className="profile-section">
          <div className="section-header">
            <h2><Award size={24} /> Awards & Recognition</h2>
            <button className="edit-btn" onClick={() => toggleEdit('awards')}>
              <Edit2 size={18} />
            </button>
          </div>
          <div className="awards-list">
            {profile.awards.map((award, index) => (
              <div key={index} className="award-item">
                {!isEditing.awards ? (
                  <>
                    <Star size={18} className="award-icon" />
                    <span>{award}</span>
                  </>
                ) : (
                  <>
                    <input
                      type="text"
                      className="input"
                      value={award}
                      onChange={(e) => updateAward(index, e.target.value)}
                      placeholder="Award name"
                    />
                    <button className="icon-btn-small" onClick={() => removeAward(index)}>
                      <X size={16} />
                    </button>
                  </>
                )}
              </div>
            ))}
            {isEditing.awards && (
              <button className="btn btn-outline btn-sm" onClick={addAward}>
                <Plus size={16} /> Add Award
              </button>
            )}
          </div>
        </div>

        {/* My Projects */}
        <div className="profile-section">
          <div className="section-header">
            <h2><Film size={24} /> My Projects</h2>
          </div>
          <div className="projects-grid-profile">
            {myProjects.map(project => (
              <div key={project.id} className="project-card-profile">
                <img src={project.image} alt={project.title} />
                <div className="project-info-profile">
                  <span className="project-status">{project.status}</span>
                  <h3>{project.title}</h3>
                  <p>{project.type} • {project.year}</p>
                  <p className="project-role">{project.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Collaborations */}
        <div className="profile-section">
          <div className="section-header">
            <h2><Briefcase size={24} /> Collaborations</h2>
          </div>
          <div className="collaborations-grid">
            {collaborations.map(collab => (
              <div key={collab.id} className="collab-card">
                <img src={collab.image} alt={collab.name} className="collab-image" />
                <div className="collab-info">
                  <h4>{collab.name}</h4>
                  <p className="collab-role">{collab.role}</p>
                  <p className="collab-project">{collab.project}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Feedback */}
        <div className="profile-section">
          <div className="section-header">
            <h2><MessageCircle size={24} /> Feedback from Collaborators</h2>
          </div>
          <div className="feedback-list">
            {feedback.map(item => (
              <div key={item.id} className="feedback-card">
                <div className="feedback-header">
                  <img src={item.image} alt={item.name} className="feedback-avatar" />
                  <div className="feedback-author">
                    <h4>{item.name}</h4>
                    <p>{item.role}</p>
                  </div>
                  <div className="feedback-rating">
                    {[...Array(item.rating)].map((_, i) => (
                      <Star key={i} size={16} fill="#FFC107" color="#FFC107" />
                    ))}
                  </div>
                </div>
                <p className="feedback-text">"{item.text}"</p>
                <p className="feedback-project">Project: {item.project}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
