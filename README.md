# Creator DNA

Creator DNA is a fair-discovery and collaboration platform for emerging creators who are tired of algorithmic bias.  
Instead of rewarding virality and popularity, Creator DNA helps unfinished ideas get the visibility and collaboration they deserve.

---

##  Inspiration

Creator DNA was inspired by a simple question:

> **“What if unfinished work wasn’t a weakness, but a signal for collaboration?”**

Existing platforms reward virality and algorithmic popularity, leaving early-stage creators invisible — especially those with raw ideas, rough cuts, and half-written scripts.  
We wanted to build a fair-discovery space where potential matters more than popularity, and creators grow through visibility, transparency, and collaboration — not just likes.

---

##  What It Does

Creator DNA helps emerging creators:

1. Upload unfinished creative work (scripts, videos, audio, ideas)  
2. Get discovered through a **FairRank** system instead of popularity bias  
3. Receive AI-assisted suggestions for collaborators and micro-tasks (UI-driven)  
4. Find collaborators through intelligent matching  
5. Earn points, levels, and rewards through meaningful engagement  

---

##  How We Built It

**Frontend**
- React 18 + React Router  
- Custom CSS with variables for consistent creative theme  
- Modular pages for:
  - Uploading unfinished work  
  - Fair discovery feed  
  - Creator profiles & leaderboards  

**Backend**
- Python 3 + SQLite  
- Clean architecture:
  - `repositories/` → database access  
  - `services/` → business logic  
- Core engines:
  - **FairRankEngine** – fair discovery scoring  
  - **SimilarityEngine** – project similarity  
  - **MatchingEngine** – collaborator matching  
- Gamification:
  - Points, levels, rewards  
- Designed to expose FastAPI endpoints for frontend integration and scaling  

---

##  Challenges We Ran Into

1. FairRank + similarity computations were heavy, so full frontend-backend integration couldn’t be completed within hackathon time  
2. Frontend and backend work properly as **independent modules**, and API integration is the next step  

---

##  Accomplishments

- Built a fair, non-viral discovery system  
- Delivered a polished, product-grade UI  
- Designed an accessible, no-cost platform for early-stage creators  

---

##  What We Learned

- Fair discovery requires intentional design, not just “better algorithms”  
- Collaboration is a UX + product problem, not only a technical one  
- Clean backend architecture (engines + services + repos) made debugging and iteration faster  

---

##  What’s Next

- Full FastAPI integration between frontend and backend  
- Creator analytics dashboard  
- Public launch for student and indie creator communities  

---

##  Tech Stack

- React  
- Node.js  
- CSS3  
- Python 3  
- SQLite  
- FastAPI (planned integration)  

---

##  Running the Project Locally

### 1️ Clone the Repository

```bash
cd "YOUR_DIRECTORY"
gh repo clone DhruvMehta323/SparkHackathon-2026
cd SparkHackathon-2026
```
##  Running the Project Locally

### 2️ Run Frontend

```bash
cd frontend
npm install
npm run dev
```
### 3️ Run Backend (Engines & CLI)

```bash
cd backend
PYTHONPATH=. python3 app/scripts/init_db.py
PYTHONPATH=. python3 -m unittest discover -v tests
```
## Optional Engine Runs

```bash
PYTHONPATH=. python3 main.py --run-fairrank
PYTHONPATH=. python3 main.py --compute-similarity
PYTHONPATH=. python3 main.py --run-matching --request-id 1
```
##  Features

- Fair discovery feed (no popularity bias)  
- Unfinished work showcase  
- Style-based collaborator matching  
- Gamified rewards for engagement  
- Clean UI focused on creators, not algorithms  

---

##  Credits / Acknowledgments

- Jaaswand Kutre  
- Moulshree Guleria  
- Dhruv Mehta  
- Michelle Azie  

