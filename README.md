# Creator DNA - Creative Collaboration Platform

A fair discovery platform for creators to collaborate freely and finish their stories.

## 🎨 Features

- **Fair Discovery Feed**: No popularity bias - every creator gets equal visibility
- **Style-Based Matching**: AI-powered recommendations based on genre and creative style
- **Unfinished Work Showcase**: Upload scripts, rough cuts, and ideas to find collaborators
- **Multi-Role Support**: Built for Writers, Directors, Actors, and all creative roles

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js** (version 14.0 or higher)
  - Download from: https://nodejs.org/
  - Verify installation: `node --version`

- **npm** (usually comes with Node.js)
  - Verify installation: `npm --version`

## 🚀 Installation Guide

### Step 1: Navigate to the Project Directory

Open your terminal/command prompt and navigate to the project folder:

```bash
cd path/to/creator-dna-app
```

### Step 2: Install Dependencies

Run the following command to install all required packages:

```bash
npm install
```

This will install:
- React
- React Router DOM
- Lucide React (for icons)
- All other necessary dependencies

### Step 3: Start the Development Server

Once installation is complete, start the application:

```bash
npm start
```

The application will automatically open in your default browser at:
```
http://localhost:3000
```

If it doesn't open automatically, manually navigate to the above URL.

## 📱 Application Flow

### 1. Landing Page (`/`)
- Welcome screen with project overview
- Two options:
  - **Login** → Goes directly to Home Page
  - **Create Account** → Goes to Create Account Page

### 2. Create Account Page (`/create-account`)
- Three sign-in options:
  - Continue with Email
  - Continue with Google
  - Continue with Phone
- Registration form with:
  - Full Name
  - Email Address
  - Role (Actor, Writer, Director, Multi-role)
  - Skills (multiple selection)
- After account creation → Redirects to Home Page

### 3. Home Page (`/home`)
- Top Navigation Bar with:
  - Logo
  - Menu items (Explore Feed, My Projects, Messages)
  - Upload Work button
  - Notifications
  - Profile menu
- Hero banner with tagline
- Quick action cards for Task Type and Get Matched
- Fair Discovery Feed with:
  - Genre filters
  - Role filters
  - Search functionality
  - Project cards displaying:
    - Project images
    - Title and author
    - Collaboration needs
    - Tags and categories
    - Like/comment counts
    - Apply button

## 🎯 Available Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Landing Page | Welcome screen with login/signup options |
| `/create-account` | Create Account | Registration form with social sign-in |
| `/home` | Home Page | Main feed with discovery and projects |

## 🛠️ Project Structure

```
creator-dna-app/
├── public/
│   └── index.html
├── src/
│   ├── pages/
│   │   ├── LandingPage.js
│   │   ├── LandingPage.css
│   │   ├── CreateAccountPage.js
│   │   ├── CreateAccountPage.css
│   │   ├── HomePage.js
│   │   └── HomePage.css
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🎨 Key Technologies

- **React 18** - UI Framework
- **React Router DOM** - Navigation/Routing
- **Lucide React** - Icon Library
- **CSS3** - Custom Styling
- **Modern JavaScript (ES6+)**

## ⚙️ Development Commands

| Command | Description |
|---------|-------------|
| `npm start` | Start development server |
| `npm run build` | Create production build |
| `npm test` | Run tests |

## 🌐 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 📝 Notes

- The application uses React Router for navigation between pages
- All images in the project are placeholder URLs from Unsplash
- The current version is a frontend-only implementation
- Backend integration and API calls are ready to be implemented

## 🔧 Troubleshooting

### Issue: `npm install` fails
**Solution**: Try clearing npm cache and reinstalling
```bash
npm cache clean --force
npm install
```

### Issue: Port 3000 is already in use
**Solution**: Either:
- Stop the process using port 3000
- Or run on a different port:
```bash
PORT=3001 npm start
```

### Issue: Module not found errors
**Solution**: Delete node_modules and reinstall
```bash
rm -rf node_modules
npm install
```

## 🚀 Next Steps for Development

To make this a fully functional platform, you would need to:

1. **Backend Development**
   - Set up Node.js/Express server
   - Create MongoDB database
   - Implement authentication (JWT, OAuth)
   - Build REST API endpoints

2. **AI Integration**
   - Implement style analysis
   - Build matching algorithm
   - Add recommendation engine

3. **Additional Features**
   - User profiles
   - Project upload functionality
   - Messaging system
   - Collaboration workspace
   - File storage (AWS S3)

4. **Deployment**
   - Deploy frontend (Vercel, Netlify)
   - Deploy backend (Heroku, AWS)
   - Configure domain and SSL

## 📧 Support

For issues or questions, please check the troubleshooting section above.

---

**Built with ❤️ for creators who want to collaborate freely and finish their stories.**
