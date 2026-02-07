import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Smartphone, Camera, Film, Mic, Pencil, Users, ChevronDown } from 'lucide-react';
import './CreateAccountPage.css';

const CreateAccountPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    role: '',
    skills: []
  });

  const roleOptions = [
    { value: 'actor', label: 'Actor', icon: Mic },
    { value: 'writer', label: 'Writer', icon: Pencil },
    { value: 'director', label: 'Director', icon: Film },
    { value: 'multi-role', label: 'Multi-role', icon: Users }
  ];

  const skillOptions = [
    'Acting - Drama',
    'Acting - Comedy',
    'Acting - Improv',
    'Screenwriting',
    'Documentary',
    'Sound Design',
    'Cinematography',
    'Editing',
    'Producing',
    'Animation',
    'VFX',
    'Music Composition'
  ];

  const handleSkillToggle = (skill) => {
    if (formData.skills.includes(skill)) {
      setFormData({
        ...formData,
        skills: formData.skills.filter(s => s !== skill)
      });
    } else {
      setFormData({
        ...formData,
        skills: [...formData.skills, skill]
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send data to backend
    console.log('Form submitted:', formData);
    navigate('/home');
  };

  const handleSocialSignIn = (provider) => {
    console.log(`Sign in with ${provider}`);
    // Implement social sign-in logic
    navigate('/home');
  };

  return (
    <div className="create-account-page">
      <div className="account-container">
        {/* Left Side - Branding */}
        <div className="branding-side">
          <div className="branding-content">
            <div className="logo">
              <div className="logo-icon">
                <span className="logo-gradient">C</span>
              </div>
              <span className="logo-text">Creator DNA</span>
            </div>

            <div className="creative-icons">
              <div className="creative-icon" style={{ top: '20%', left: '15%' }}>
                <Camera size={40} strokeWidth={1.5} />
              </div>
              <div className="creative-icon" style={{ top: '35%', right: '20%' }}>
                <Film size={45} strokeWidth={1.5} />
              </div>
              <div className="creative-icon" style={{ bottom: '30%', left: '25%' }}>
                <Mic size={35} strokeWidth={1.5} />
              </div>
              <div className="creative-icon" style={{ bottom: '20%', right: '15%' }}>
                <Pencil size={38} strokeWidth={1.5} />
              </div>
            </div>

            <h2 className="branding-tagline">
              Discover talent, collaborate freely, finish your story.
            </h2>
          </div>
        </div>

        {/* Right Side - Form */}
        <div className="form-side">
          <div className="form-content">
            <h1 className="form-title">Join the Creative Network</h1>
            <p className="form-subtitle">Tell us a bit about yourself</p>

            {/* Social Sign In Buttons */}
            <div className="social-buttons">
              <button 
                className="btn btn-social btn-email"
                onClick={() => handleSocialSignIn('email')}
              >
                <Mail size={20} />
                Continue with Email
              </button>
              
              <button 
                className="btn btn-social btn-google"
                onClick={() => handleSocialSignIn('google')}
              >
                <svg width="20" height="20" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
              </button>

              <button 
                className="btn btn-social btn-phone"
                onClick={() => handleSocialSignIn('phone')}
              >
                <Smartphone size={20} />
                Continue with Phone
              </button>
            </div>

            <div className="divider">
              <span>OR</span>
            </div>

            {/* Sign Up Form */}
            <form onSubmit={handleSubmit} className="signup-form">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="fullName">Full Name</label>
                  <input
                    type="text"
                    id="fullName"
                    className="input"
                    placeholder="Enter your name"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    className="input"
                    placeholder="your.email@example.com"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="role">Role</label>
                <div className="role-select">
                  <select
                    id="role"
                    className="input"
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                    required
                  >
                    <option value="">Select your role</option>
                    {roleOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="select-icon" size={20} />
                </div>
              </div>

              <div className="form-group">
                <label>Skills</label>
                <div className="skills-grid">
                  {skillOptions.map(skill => (
                    <button
                      key={skill}
                      type="button"
                      className={`skill-tag ${formData.skills.includes(skill) ? 'active' : ''}`}
                      onClick={() => handleSkillToggle(skill)}
                    >
                      {skill}
                    </button>
                  ))}
                </div>
              </div>

              <button type="submit" className="btn btn-primary btn-full">
                Create My Creator DNA Profile
              </button>

              <div className="terms-checkbox">
                <input type="checkbox" id="terms" required />
                <label htmlFor="terms">I agree to the terms and conditions</label>
              </div>
            </form>

            <div className="login-link">
              Already have an account? <span onClick={() => navigate('/home')}>Login</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateAccountPage;
