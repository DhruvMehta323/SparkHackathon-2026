import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, User, Bell, Camera, Film, Mic, Pencil,
  FileText, Video, Music, X, Check, ChevronDown, AlertCircle
} from 'lucide-react';
import './UploadPage.css';

const UploadPage = () => {
  const navigate = useNavigate();
  const videoInputRef = useRef(null);
  const audioInputRef = useRef(null);

  const [uploadType, setUploadType] = useState('');
  const [showScriptEditor, setShowScriptEditor] = useState(false);
  const [acceptingCollabs, setAcceptingCollabs] = useState(true);
  
  const [projectData, setProjectData] = useState({
    title: '',
    description: '',
    genre: '',
    tags: [],
    scriptContent: '',
    videoFile: null,
    audioFile: null,
    collaborationNeeds: []
  });

  const [aiSuggestions, setAiSuggestions] = useState({
    microTasks: [
      'Actor for dramatic monologue',
      'Editor for rough cut',
      'Sound Designer for atmospheric score'
    ],
    recommendedRoles: ['Actor', 'Director']
  });

  const genres = [
    'Drama', 'Comedy', 'Sci-Fi', 'Fantasy', 'Horror', 
    'Romance', 'Thriller', 'Documentary', 'Experimental'
  ];

  const predefinedTags = [
    '#shortFilm', '#studentFilm', '#indieFilm', '#experimental',
    '#drama', '#comedy', '#scifi', '#fantasy', '#horror',
    '#character', '#miniseries', '#musicVideo', '#documentary'
  ];

  const collaborationOptions = [
    'Actor', 'Director', 'Writer', 'Editor', 'Sound Designer',
    'Cinematographer', 'Producer', 'Composer', 'VFX Artist'
  ];

  const handleUploadTypeSelect = (type) => {
    setUploadType(type);
    if (type === 'script') {
      setShowScriptEditor(true);
    } else if (type === 'video') {
      videoInputRef.current?.click();
    } else if (type === 'audio') {
      audioInputRef.current?.click();
    }
  };

  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProjectData({ ...projectData, videoFile: file });
      // In real app, you'd upload to server here
      alert(`Video "${file.name}" selected successfully!`);
    }
  };

  const handleAudioUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProjectData({ ...projectData, audioFile: file });
      alert(`Audio "${file.name}" selected successfully!`);
    }
  };

  const toggleTag = (tag) => {
    if (projectData.tags.includes(tag)) {
      setProjectData({
        ...projectData,
        tags: projectData.tags.filter(t => t !== tag)
      });
    } else {
      setProjectData({
        ...projectData,
        tags: [...projectData.tags, tag]
      });
    }
  };

  const toggleCollabNeed = (need) => {
    if (projectData.collaborationNeeds.includes(need)) {
      setProjectData({
        ...projectData,
        collaborationNeeds: projectData.collaborationNeeds.filter(n => n !== need)
      });
    } else {
      setProjectData({
        ...projectData,
        collaborationNeeds: [...projectData.collaborationNeeds, need]
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validation
    if (!projectData.title) {
      alert('Please add a project title');
      return;
    }

    if (!uploadType) {
      alert('Please select an upload type');
      return;
    }

    if (uploadType === 'script' && !projectData.scriptContent) {
      alert('Please write your script content');
      return;
    }

    if (uploadType === 'video' && !projectData.videoFile) {
      alert('Please upload a video file');
      return;
    }

    if (uploadType === 'audio' && !projectData.audioFile) {
      alert('Please upload an audio file');
      return;
    }

    // In real app, submit to backend
    console.log('Project data:', projectData);
    alert('Project submitted successfully!');
    navigate('/home');
  };

  return (
    <div className="upload-page">
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
            <div className="profile-menu" onClick={() => navigate('/profile')}>
              <div className="profile-avatar">
                <User size={20} />
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Upload Header */}
      <div className="upload-header">
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
          <h1>Upload Your Unfinished Work</h1>
          <p>Share your ideas, scripts, and rough cuts. Find collaborators to finish your story.</p>
        </div>
      </div>

      {/* Upload Form */}
      <div className="upload-content container">
        <form onSubmit={handleSubmit} className="upload-form-container">
          {/* Left Column - Project Details */}
          <div className="form-column">
            <div className="upload-section">
              <h2>Project Details</h2>

              <div className="collab-toggle">
                <label className="toggle-label">
                  <input
                    type="checkbox"
                    checked={acceptingCollabs}
                    onChange={(e) => setAcceptingCollabs(e.target.checked)}
                  />
                  <span className="toggle-slider"></span>
                  <span className="toggle-text">Accepting Collaborators for this Project</span>
                </label>
              </div>

              <div className="upload-types">
                <button
                  type="button"
                  className={`upload-type-btn ${uploadType === 'script' ? 'active' : ''}`}
                  onClick={() => handleUploadTypeSelect('script')}
                >
                  <FileText size={32} />
                  <span>Script (PDF)</span>
                </button>

                <button
                  type="button"
                  className={`upload-type-btn ${uploadType === 'video' ? 'active' : ''}`}
                  onClick={() => handleUploadTypeSelect('video')}
                >
                  <Video size={32} />
                  <span>Video Clip (MP4)</span>
                </button>

                <button
                  type="button"
                  className={`upload-type-btn ${uploadType === 'audio' ? 'active' : ''}`}
                  onClick={() => handleUploadTypeSelect('audio')}
                >
                  <Music size={32} />
                  <span>Audio/Monologue</span>
                </button>
              </div>

              {/* Hidden file inputs */}
              <input
                type="file"
                ref={videoInputRef}
                onChange={handleVideoUpload}
                accept="video/*"
                style={{ display: 'none' }}
              />
              <input
                type="file"
                ref={audioInputRef}
                onChange={handleAudioUpload}
                accept="audio/*"
                style={{ display: 'none' }}
              />

              {/* Script Editor */}
              {showScriptEditor && uploadType === 'script' && (
                <div className="script-editor">
                  <div className="editor-header">
                    <h3>Write Your Script</h3>
                    <button
                      type="button"
                      className="close-editor-btn"
                      onClick={() => setShowScriptEditor(false)}
                    >
                      <X size={20} />
                    </button>
                  </div>
                  <textarea
                    className="script-textarea"
                    placeholder="INT. COFFEE SHOP - DAY&#10;&#10;A young woman sits alone, staring at her laptop...&#10;&#10;Or paste your script here, or upload a PDF file below."
                    value={projectData.scriptContent}
                    onChange={(e) => setProjectData({ ...projectData, scriptContent: e.target.value })}
                    rows={15}
                  />
                  <div className="editor-footer">
                    <span className="char-count">{projectData.scriptContent.length} characters</span>
                    <button type="button" className="btn btn-outline btn-sm">
                      <Upload size={16} /> Upload PDF Instead
                    </button>
                  </div>
                </div>
              )}

              {/* File Upload Status */}
              {projectData.videoFile && (
                <div className="file-status">
                  <Video size={20} />
                  <span>{projectData.videoFile.name}</span>
                  <button
                    type="button"
                    onClick={() => setProjectData({ ...projectData, videoFile: null })}
                    className="remove-file-btn"
                  >
                    <X size={16} />
                  </button>
                </div>
              )}

              {projectData.audioFile && (
                <div className="file-status">
                  <Music size={20} />
                  <span>{projectData.audioFile.name}</span>
                  <button
                    type="button"
                    onClick={() => setProjectData({ ...projectData, audioFile: null })}
                    className="remove-file-btn"
                  >
                    <X size={16} />
                  </button>
                </div>
              )}

              <div className="form-group">
                <label>Project Title *</label>
                <input
                  type="text"
                  className="input"
                  placeholder="Enter your project title"
                  value={projectData.title}
                  onChange={(e) => setProjectData({ ...projectData, title: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  className="input"
                  rows={4}
                  placeholder="Describe your project, its themes, and what makes it unique..."
                  value={projectData.description}
                  onChange={(e) => setProjectData({ ...projectData, description: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Genre</label>
                <div className="genre-select">
                  <select
                    className="input"
                    value={projectData.genre}
                    onChange={(e) => setProjectData({ ...projectData, genre: e.target.value })}
                  >
                    <option value="">Select genre</option>
                    {genres.map(genre => (
                      <option key={genre} value={genre}>{genre}</option>
                    ))}
                  </select>
                  <ChevronDown className="select-icon" size={20} />
                </div>
              </div>

              <div className="form-group">
                <label>Tags</label>
                <div className="tags-grid">
                  {predefinedTags.map(tag => (
                    <button
                      key={tag}
                      type="button"
                      className={`tag-btn ${projectData.tags.includes(tag) ? 'active' : ''}`}
                      onClick={() => toggleTag(tag)}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label>What Collaborators Do You Need?</label>
                <div className="collab-needs-grid">
                  {collaborationOptions.map(option => (
                    <button
                      key={option}
                      type="button"
                      className={`collab-need-btn ${projectData.collaborationNeeds.includes(option) ? 'active' : ''}`}
                      onClick={() => toggleCollabNeed(option)}
                    >
                      {projectData.collaborationNeeds.includes(option) && <Check size={16} />}
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - AI Assistant */}
          <div className="form-column">
            <div className="upload-section ai-section">
              <h2>AI Smart Assistant</h2>
              <p className="ai-subtitle">Based on your content, AI suggests:</p>

              <div className="ai-card">
                <h3>Micro-Tasks Needed</h3>
                <div className="micro-tasks-list">
                  {aiSuggestions.microTasks.map((task, index) => (
                    <div key={index} className="micro-task-item">
                      <span className="task-number">{index + 1}</span>
                      <span>{task}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="ai-card">
                <h3>Recommended Collaborator Types</h3>
                <div className="recommended-roles">
                  {aiSuggestions.recommendedRoles.map(role => (
                    <button
                      key={role}
                      type="button"
                      className="recommended-role-btn"
                      onClick={() => toggleCollabNeed(role)}
                    >
                      {role}
                    </button>
                  ))}
                </div>
              </div>

              <div className="ai-card">
                <h3>Recommended Improvement Feedback</h3>
                <div className="feedback-suggestions">
                  <div className="feedback-item">
                    <AlertCircle size={18} className="feedback-icon" />
                    <div>
                      <strong>Pacing:</strong> Consider tightening Act 2 for better flow
                    </div>
                  </div>
                  <div className="feedback-item">
                    <AlertCircle size={18} className="feedback-icon" />
                    <div>
                      <strong>Character:</strong> Main character's motivation could be clearer
                    </div>
                  </div>
                </div>
              </div>

              <div className="ai-card">
                <h3>Tone/Style Improvement Feedback</h3>
                <p className="ai-feedback-text">
                  Your script has a strong visual style with deliberate pacing. 
                  The tone leans towards introspective drama. Consider adding 
                  moments of levity to balance the emotional weight.
                </p>
              </div>
            </div>

            <button type="submit" className="btn btn-primary btn-large submit-btn">
              <Upload size={20} />
              Submit for Collaboration
            </button>

            <div className="submit-note">
              <AlertCircle size={16} />
              <span>Your work will be visible in the Fair Discovery Feed. All creators get equal visibility!</span>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UploadPage;
