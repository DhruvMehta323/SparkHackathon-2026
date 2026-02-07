import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, User, Bell, Camera, Film, Mic, Pencil,
  Eye, Heart, MessageCircle, Edit2, Trash2, CheckCircle,
  Clock, Users, TrendingUp, MoreVertical, X, Check,
  AlertCircle, Archive, RefreshCw
} from 'lucide-react';
import './MyProjectsPage.css';

const MyProjectsPage = () => {
  const navigate = useNavigate();
  
  const [activeTab, setActiveTab] = useState('active');
  const [selectedProject, setSelectedProject] = useState(null);
  const [showApplications, setShowApplications] = useState(false);

  const [projects, setProjects] = useState([
    {
      id: 1,
      title: 'Echoes of the Silent City',
      type: 'Script',
      status: 'looking',
      progress: 0,
      uploadDate: '2024-02-01',
      image: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=300&fit=crop',
      description: 'A mysterious city where sounds have disappeared...',
      genre: 'Fantasy',
      tags: ['#fantasy', '#studentFilm', '#short'],
      stats: {
        views: 234,
        likes: 45,
        comments: 12,
        applications: 8
      },
      collaborators: [],
      needsHelp: ['Actor for monologue', 'Sound Designer']
    },
    {
      id: 2,
      title: 'Urban Dreams',
      type: 'Rough Cut',
      status: 'in-progress',
      progress: 75,
      uploadDate: '2024-01-15',
      image: 'https://images.unsplash.com/photo-1514565131-fce0801e5785?w=400&h=300&fit=crop',
      description: 'Exploring the heartbeat of city life through movement...',
      genre: 'Documentary',
      tags: ['#documentary', '#experimental'],
      stats: {
        views: 456,
        likes: 89,
        comments: 23,
        applications: 5
      },
      collaborators: [
        { name: 'Marcus Chen', role: 'Cinematographer', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=60&h=60&fit=crop' },
        { name: 'Elena Rodriguez', role: 'Sound Designer', avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=60&h=60&fit=crop' }
      ],
      needsHelp: ['Composer for final score']
    },
    {
      id: 3,
      title: 'Midnight Café Chronicles',
      type: 'Script',
      status: 'completed',
      progress: 100,
      uploadDate: '2023-12-20',
      image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop',
      description: 'Stories that unfold in a 24-hour café...',
      genre: 'Drama',
      tags: ['#drama', '#indieFilm'],
      stats: {
        views: 678,
        likes: 123,
        comments: 45,
        applications: 15
      },
      collaborators: [
        { name: 'Sarah Martinez', role: 'Lead Actor', avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=60&h=60&fit=crop' },
        { name: 'David Kim', role: 'Director', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&h=60&fit=crop' },
        { name: 'Lisa Wong', role: 'Editor', avatar: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=60&h=60&fit=crop' }
      ],
      needsHelp: []
    }
  ]);

  const [applications] = useState([
    {
      id: 1,
      projectId: 1,
      applicant: {
        name: 'Jake Williams',
        role: 'Actor',
        image: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=80&h=80&fit=crop',
        bio: 'Professional actor with 5 years of theater experience',
        portfolio: 'https://jakewilliams.com'
      },
      message: 'I\'d love to bring this character to life! I have experience with dramatic monologues and really connect with the mysterious atmosphere of your script.',
      appliedDate: '2024-02-05',
      status: 'pending'
    },
    {
      id: 2,
      projectId: 1,
      applicant: {
        name: 'Emma Chen',
        role: 'Sound Designer',
        image: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=80&h=80&fit=crop',
        bio: 'Award-winning sound designer specializing in atmospheric scores',
        portfolio: 'https://emmachen.audio'
      },
      message: 'The concept of a silent city is fascinating! I\'d love to create an atmospheric soundscape that enhances the mystery.',
      appliedDate: '2024-02-04',
      status: 'pending'
    },
    {
      id: 3,
      projectId: 1,
      applicant: {
        name: 'Tom Rodriguez',
        role: 'Actor',
        image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop',
        bio: 'Character actor with indie film background',
        portfolio: 'https://tomrodriguez.com'
      },
      message: 'This script speaks to me. I\'ve been looking for exactly this kind of project!',
      appliedDate: '2024-02-03',
      status: 'pending'
    }
  ]);

  const getStatusBadge = (status) => {
    switch(status) {
      case 'looking':
        return <span className="status-badge looking"><Clock size={14} /> Looking for Collaborators</span>;
      case 'in-progress':
        return <span className="status-badge in-progress"><Users size={14} /> In Progress</span>;
      case 'completed':
        return <span className="status-badge completed"><CheckCircle size={14} /> Completed</span>;
      default:
        return null;
    }
  };

  const filteredProjects = projects.filter(project => {
    if (activeTab === 'active') return project.status !== 'completed';
    if (activeTab === 'completed') return project.status === 'completed';
    return true;
  });

  const handleViewApplications = (project) => {
    setSelectedProject(project);
    setShowApplications(true);
  };

  const handleAcceptApplication = (appId) => {
    alert('Collaborator accepted! They will be notified.');
    // In real app, update backend and add to collaborators
  };

  const handleRejectApplication = (appId) => {
    alert('Application declined.');
    // In real app, update backend
  };

  const handleDeleteProject = (projectId) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      setProjects(projects.filter(p => p.id !== projectId));
      alert('Project deleted successfully!');
    }
  };

  const handleArchiveProject = (projectId) => {
    alert('Project archived!');
  };

  return (
    <div className="my-projects-page">
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
            <a href="#" className="nav-link active">My Projects</a>
            <a href="#" onClick={() => navigate('/messages')} className="nav-link">Messages</a>
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

      {/* Page Header */}
      <div className="page-header">
        <div className="header-content container">
          <h1>My Projects</h1>
          <p>Manage your uploads, track collaborations, and grow your creative network</p>
        </div>
      </div>

      {/* Content */}
      <div className="projects-content container">
        {/* Stats Overview */}
        <div className="stats-overview">
          <div className="stat-card">
            <div className="stat-icon gradient-blue">
              <Film size={24} />
            </div>
            <div className="stat-info">
              <h3>{projects.length}</h3>
              <p>Total Projects</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon gradient-purple">
              <Users size={24} />
            </div>
            <div className="stat-info">
              <h3>{projects.reduce((sum, p) => sum + p.stats.applications, 0)}</h3>
              <p>Total Applications</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon gradient-blue">
              <TrendingUp size={24} />
            </div>
            <div className="stat-info">
              <h3>{projects.reduce((sum, p) => sum + p.stats.views, 0)}</h3>
              <p>Total Views</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon gradient-purple">
              <Heart size={24} />
            </div>
            <div className="stat-info">
              <h3>{projects.reduce((sum, p) => sum + p.stats.likes, 0)}</h3>
              <p>Total Likes</p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="projects-tabs">
          <button 
            className={`tab-btn ${activeTab === 'active' ? 'active' : ''}`}
            onClick={() => setActiveTab('active')}
          >
            Active Projects ({projects.filter(p => p.status !== 'completed').length})
          </button>
          <button 
            className={`tab-btn ${activeTab === 'completed' ? 'active' : ''}`}
            onClick={() => setActiveTab('completed')}
          >
            Completed ({projects.filter(p => p.status === 'completed').length})
          </button>
          <button 
            className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            All Projects ({projects.length})
          </button>
        </div>

        {/* Projects List */}
        <div className="projects-list">
          {filteredProjects.map(project => (
            <div key={project.id} className="project-item">
              <div className="project-item-image">
                <img src={project.image} alt={project.title} />
                <span className="project-type-badge">{project.type}</span>
              </div>

              <div className="project-item-content">
                <div className="project-item-header">
                  <div>
                    <h3>{project.title}</h3>
                    {getStatusBadge(project.status)}
                  </div>
                  <div className="project-actions">
                    <button className="icon-btn" onClick={() => navigate('/upload')}>
                      <Edit2 size={18} />
                    </button>
                    <button className="icon-btn" onClick={() => handleArchiveProject(project.id)}>
                      <Archive size={18} />
                    </button>
                    <button className="icon-btn danger" onClick={() => handleDeleteProject(project.id)}>
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>

                <p className="project-description">{project.description}</p>

                <div className="project-tags">
                  {project.tags.map(tag => (
                    <span key={tag} className="tag">{tag}</span>
                  ))}
                </div>

                {/* Progress Bar */}
                {project.status === 'in-progress' && (
                  <div className="progress-section">
                    <div className="progress-header">
                      <span>Progress</span>
                      <span>{project.progress}%</span>
                    </div>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${project.progress}%` }}></div>
                    </div>
                  </div>
                )}

                {/* Collaborators */}
                {project.collaborators.length > 0 && (
                  <div className="collaborators-section">
                    <span className="section-label">Working with:</span>
                    <div className="collaborators-list">
                      {project.collaborators.map((collab, index) => (
                        <div key={index} className="collaborator-mini" title={`${collab.name} - ${collab.role}`}>
                          <img src={collab.avatar} alt={collab.name} />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Needs Help */}
                {project.needsHelp.length > 0 && (
                  <div className="needs-help-section">
                    <AlertCircle size={16} />
                    <span>Still needs: {project.needsHelp.join(', ')}</span>
                  </div>
                )}

                {/* Stats */}
                <div className="project-item-stats">
                  <div className="stat-item">
                    <Eye size={16} />
                    <span>{project.stats.views}</span>
                  </div>
                  <div className="stat-item">
                    <Heart size={16} />
                    <span>{project.stats.likes}</span>
                  </div>
                  <div className="stat-item">
                    <MessageCircle size={16} />
                    <span>{project.stats.comments}</span>
                  </div>
                  <div className="stat-item applications" onClick={() => handleViewApplications(project)}>
                    <Users size={16} />
                    <span>{project.stats.applications} Applications</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredProjects.length === 0 && (
          <div className="empty-state">
            <Film size={64} color="#D1D5DB" />
            <h3>No projects found</h3>
            <p>Start by uploading your first project!</p>
            <button className="btn btn-primary" onClick={() => navigate('/upload')}>
              <Upload size={18} />
              Upload Work
            </button>
          </div>
        )}
      </div>

      {/* Applications Modal */}
      {showApplications && selectedProject && (
        <div className="modal-overlay" onClick={() => setShowApplications(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Applications for "{selectedProject.title}"</h2>
              <button className="close-modal-btn" onClick={() => setShowApplications(false)}>
                <X size={24} />
              </button>
            </div>

            <div className="applications-list">
              {applications.filter(app => app.projectId === selectedProject.id).map(app => (
                <div key={app.id} className="application-card">
                  <div className="application-header">
                    <img src={app.applicant.image} alt={app.applicant.name} className="applicant-avatar" />
                    <div className="applicant-info">
                      <h4>{app.applicant.name}</h4>
                      <p>{app.applicant.role}</p>
                      <a href={app.applicant.portfolio} target="_blank" rel="noopener noreferrer" className="portfolio-link">
                        View Portfolio →
                      </a>
                    </div>
                    <span className="applied-date">{new Date(app.appliedDate).toLocaleDateString()}</span>
                  </div>

                  <p className="applicant-bio">{app.applicant.bio}</p>
                  <p className="application-message">"{app.message}"</p>

                  <div className="application-actions">
                    <button className="btn btn-outline" onClick={() => handleRejectApplication(app.id)}>
                      <X size={16} />
                      Decline
                    </button>
                    <button className="btn btn-primary" onClick={() => handleAcceptApplication(app.id)}>
                      <Check size={16} />
                      Accept & Collaborate
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyProjectsPage;
