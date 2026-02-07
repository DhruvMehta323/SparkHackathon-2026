"""Seed database with demo data."""
from datetime import datetime, timedelta
import random
from app.repositories.projects import ProjectRepository
from app.repositories.creators import CreatorRepository
from app.repositories.users import UserRepository
from app.repositories.engagements import EngagementRepository
from app.core.database import get_connection
from app.repositories.collab import CollabRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


def seed_database():
    """Seed database with realistic demo data"""

    # Check if already seeded
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count > 0:
        logger.info("Database already seeded, skipping...")
        return {"message": "Already seeded"}
    
    logger.info("Starting database seeding...")
    
    try:
        # Sample creator data
        creators_data = [
            {"name": "Alice Chen", "role": "Director", "skills": "Directing,Cinematography,Editing", "location": "Chicago", "availability": "Weekends"},
            {"name": "Bob Martinez", "role": "Editor", "skills": "Final Cut Pro,Premiere Pro,Color Grading", "location": "Los Angeles", "availability": "Flexible"},
            {"name": "Carol Kim", "role": "Cinematographer", "skills": "RED Camera,Lighting,Camera Operation", "location": "New York", "availability": "Weekdays"},
            {"name": "David Park", "role": "Sound Designer", "skills": "Pro Tools,Sound Mixing,Foley", "location": "Chicago", "availability": "Weekends"},
            {"name": "Emma Wilson", "role": "Writer", "skills": "Screenwriting,Story Development,Dialogue", "location": "Austin", "availability": "Flexible"},
            {"name": "Frank Garcia", "role": "Producer", "skills": "Project Management,Budgeting,Scheduling", "location": "Los Angeles", "availability": "Full-time"},
            {"name": "Grace Lee", "role": "Actor", "skills": "Method Acting,Improv,Voice Acting", "location": "New York", "availability": "Weekends"},
            {"name": "Henry Thompson", "role": "Composer", "skills": "Film Scoring,Logic Pro,Sound Design", "location": "Nashville", "availability": "Flexible"},
            {"name": "Iris Patel", "role": "Production Designer", "skills": "Set Design,Art Direction,Props", "location": "Chicago", "availability": "Weekdays"},
            {"name": "Jack Robinson", "role": "VFX Artist", "skills": "After Effects,Nuke,3D Modeling", "location": "San Francisco", "availability": "Flexible"}
        ]
        
        # Create users and creators
        creator_ids = []
        for i, creator in enumerate(creators_data):
            # Create user first
            user_id = i + 1  # Manual IDs for demo
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, name, user_type, verified, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, creator["name"], "creator", 1, datetime.utcnow().isoformat())
            )
            conn.commit()
            conn.close()
            
            # Create creator profile
            CreatorRepository.create_creator_profile(
                user_id=user_id,
                role=creator["role"],
                skills=creator["skills"],
                availability=creator.get("availability", "Flexible"),
                location=creator.get("location", ""),
                bio=f"Experienced {creator['role'].lower()} passionate about collaborative filmmaking."
            )
            creator_ids.append(user_id)
        
        logger.info(f"Created {len(creator_ids)} creators")
        
        # Sample project data
        projects_data = [
            {"title": "Urban Dreams", "abstract": "A short film exploring life in the modern city through the eyes of diverse characters.", "stage": "active"},
            {"title": "The Last Frame", "abstract": "Documentary about film restoration and the people who preserve cinema history.", "stage": "idea"},
            {"title": "Neon Nights", "abstract": "Cyberpunk thriller set in a dystopian future where memories can be bought and sold.", "stage": "active"},
            {"title": "Whispers in the Wind", "abstract": "Poetic meditation on nature and human connection through stunning landscape cinematography.", "stage": "completed"},
            {"title": "Breaking Bread", "abstract": "Food documentary celebrating immigrant communities and their culinary traditions.", "stage": "active"},
            {"title": "Silent Echo", "abstract": "Psychological horror about a sound designer who hears voices in her recordings.", "stage": "idea"},
            {"title": "The Space Between", "abstract": "Intimate drama about two strangers who meet on a delayed train journey.", "stage": "active"},
            {"title": "Concrete Jungle", "abstract": "Parkour documentary showcasing urban athletes transforming cityscapes into playgrounds.", "stage": "completed"},
            {"title": "Digital Ghosts", "abstract": "Sci-fi short about AI consciousness and what it means to be human.", "stage": "active"},
            {"title": "Home Cooking", "abstract": "Web series featuring home cooks sharing family recipes and stories.", "stage": "active"},
            {"title": "Midnight Run", "abstract": "Action comedy about a rideshare driver who accidentally picks up a spy.", "stage": "idea"},
            {"title": "Canvas Dreams", "abstract": "Artist biopic exploring the life and work of an emerging painter.", "stage": "active"},
            {"title": "The Garden", "abstract": "Time-lapse documentary about an urban community garden over one year.", "stage": "completed"},
            {"title": "Frequency", "abstract": "Music video series pairing emerging musicians with visual artists.", "stage": "active"},
            {"title": "Lost & Found", "abstract": "Anthology series about objects and the people who lose and find them.", "stage": "idea"},
            {"title": "City Lights Revisited", "abstract": "Modern reimagining of the Chaplin classic set in contemporary Chicago.", "stage": "active"},
            {"title": "The Interview", "abstract": "Single-take dramatic short about a job interview that goes unexpectedly.", "stage": "active"},
            {"title": "Soundscapes", "abstract": "ASMR-inspired film capturing the sonic textures of different environments.", "stage": "idea"},
            {"title": "Fast Forward", "abstract": "Coming-of-age story about a teenager who discovers old camcorder tapes.", "stage": "active"},
            {"title": "The Collaborators", "abstract": "Meta-documentary about the process of making a film with strangers online.", "stage": "active"}
        ]
        
        # Create projects with varied timestamps
        project_ids = []
        for i, proj in enumerate(projects_data):
            # Vary creation times over the past 30 days
            days_ago = random.randint(0, 30)
            created_at = (datetime.utcnow() - timedelta(days=days_ago)).isoformat()
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO projects 
                (creator_id, title, abstract, stage, created_at, impressions) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    random.choice(creator_ids),
                    proj["title"],
                    proj["abstract"],
                    proj["stage"],
                    created_at,
                    random.randint(10, 500)  # Random impressions
                )
            )
            conn.commit()
            project_id = cursor.lastrowid
            conn.close()
            
            project_ids.append(project_id)
        
        logger.info(f"Created {len(project_ids)} projects")
        
        # Create engagements
        reaction_types = ["like", "insightful", "inspiring"]
        engagement_count = 0
        
        for project_id in project_ids:
            # Random number of engagements per project (0-15)
            num_engagements = random.randint(0, 15)
            engaged_users = random.sample(creator_ids, min(num_engagements, len(creator_ids)))
            
            for user_id in engaged_users:
                reaction = random.choice(reaction_types)
                EngagementRepository.create_engagement(
                    project_id=project_id,
                    user_id=user_id,
                    reaction=reaction,
                    weight=1.0
                )
                engagement_count += 1
        
        logger.info(f"Created {engagement_count} engagements")
        
        # Create collaboration requests
        collab_count = 0
        for _ in range(5):
            CollabRepository.create_request(
                requester_id=random.choice(creator_ids),
                project_id=random.choice(project_ids),
                role_needed=random.choice(["Editor", "Cinematographer", "Sound Designer", "Actor"]),
                skills_needed=random.choice([
                    "Final Cut Pro,Color Grading",
                    "RED Camera,Lighting",
                    "Pro Tools,Sound Mixing",
                    "Method Acting,Improv"
                ]),
                location_pref=random.choice(["Chicago", "Los Angeles", "Remote"])
            )
            collab_count += 1
        
        logger.info(f"Created {collab_count} collaboration requests")
        
        result = {
            "creators": len(creator_ids),
            "projects": len(project_ids),
            "engagements": engagement_count,
            "collab_requests": collab_count
        }
        
        logger.info(f"Database seeding completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to seed database: {e}")
        raise


if __name__ == "__main__":
    seed_database()