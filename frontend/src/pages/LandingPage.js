import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Film, Mic, Pencil, Users, Sparkles } from 'lucide-react';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-background">
          <div className="floating-icon" style={{ top: '15%', left: '10%' }}>
            <Camera size={40} strokeWidth={1.5} />
          </div>
          <div className="floating-icon" style={{ top: '25%', right: '15%' }}>
            <Film size={45} strokeWidth={1.5} />
          </div>
          <div className="floating-icon" style={{ bottom: '20%', left: '20%' }}>
            <Mic size={35} strokeWidth={1.5} />
          </div>
          <div className="floating-icon" style={{ bottom: '15%', right: '10%' }}>
            <Pencil size={38} strokeWidth={1.5} />
          </div>
          <div className="floating-icon" style={{ top: '50%', left: '50%' }}>
            <Sparkles size={42} strokeWidth={1.5} />
          </div>
        </div>

        <div className="hero-content container">
          <div className="logo-section">
            <div className="logo">
              <div className="logo-icon">
                <span className="logo-gradient">C</span>
              </div>
              <span className="logo-text">Creator DNA</span>
            </div>
          </div>

          <h1 className="hero-title fade-in">
            Discover talent, collaborate freely,<br />
            finish your story.
          </h1>

          <p className="hero-subtitle fade-in">
            Fair discovery. Novel approach. No popularity bias.<br />
            Celebrate unfinished work, find the right help, and grow together.
          </p>

          <div className="hero-buttons fade-in">
            <button 
              className="btn btn-primary btn-large"
              onClick={() => navigate('/home')}
            >
              <Users size={20} />
              Login
            </button>
            <button 
              className="btn btn-outline btn-large"
              onClick={() => navigate('/create-account')}
            >
              Create Account
            </button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section container">
        <h2 className="section-title">Why Creator DNA?</h2>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon gradient-blue">
              <Users size={32} color="white" />
            </div>
            <h3>Fair Discovery</h3>
            <p>No popularity bias. Every creator gets equal visibility regardless of followers or reputation.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon gradient-purple">
              <Sparkles size={32} color="white" />
            </div>
            <h3>Celebrate Unfinished Work</h3>
            <p>Upload scripts, rough cuts, and ideas. Get matched with collaborators who fit your creative style.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon gradient-blue">
              <Film size={32} color="white" />
            </div>
            <h3>Style-Based Matching</h3>
            <p>AI-powered recommendations based on genre, narrative style, and collaboration preferences.</p>
          </div>
        </div>
      </div>

      {/* Target Users Section */}
      <div className="users-section">
        <div className="container">
          <h2 className="section-title">Built for Creators</h2>
          
          <div className="users-grid">
            <div className="user-card">
              <Pencil size={48} className="user-icon" />
              <h3>Writers</h3>
              <p>Upload scripts, seek actors and directors, get feedback on your work.</p>
            </div>

            <div className="user-card">
              <Film size={48} className="user-icon" />
              <h3>Directors</h3>
              <p>Share rough cuts, find writers or actors, collaborate on projects.</p>
            </div>

            <div className="user-card">
              <Mic size={48} className="user-icon" />
              <h3>Actors</h3>
              <p>Showcase skills, audition for projects, contribute micro-tasks.</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="cta-section">
        <div className="container">
          <h2>Ready to finish your story?</h2>
          <p>Join creators who collaborate without boundaries</p>
          <button 
            className="btn btn-primary btn-large"
            onClick={() => navigate('/create-account')}
          >
            Get Started Free
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-logo">
              <div className="logo-icon small">
                <span className="logo-gradient">C</span>
              </div>
              <span>Creator DNA</span>
            </div>
            <p className="footer-text">© 2026 Creator DNA. Discover talent, collaborate freely, finish your story.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
