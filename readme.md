# 🏋️ IronForge 3.0 — Advanced Gym Tracker

A fully-featured gym tracking web app built with Python + Streamlit + SQLite.

## What's New in v3.0

### 🗄️ SQLite Database (Persistent Storage)
- All data stored in SQLite — survives restarts and redeployments
- Multi-user support with username-based login
- Full schema: users, workouts, exercises, PRs, bodyweight, badges, challenges, XP log
- Render `render.yaml` mounts a persistent disk at `/data` for the database

### 💪 123 Exercises (vs 60 in v2)
- Chest: 14 exercises (Bench Press, Incline, Decline, Cable Flye, Pec Deck, Pullover…)
- Back: 14 exercises (Deadlift, Pull-Up, Bent-Over Row, T-Bar Row, Face Pull…)
- Shoulders: 11 (OHP, Arnold Press, Lateral Raise, Rear Delt Flye, Landmine Press…)
- Biceps: 9 (Barbell Curl, Incline DB, Preacher, 21s, Spider Curl…)
- Triceps: 8 (Skull Crusher, Close-Grip Bench, JM Press…)
- Legs: 16 (Back Squat, Front Squat, RDL, Bulgarian Split, Nordic Curl…)
- Core: 13 (Dragon Flag, L-Sit, Ab Wheel, Pallof Press, Hollow Hold…)
- Glutes: 9 (Hip Thrust, Sumo Deadlift, Cable Kickback…)
- Calves: 5
- Full Body: 8 (Power Clean, Turkish Get-Up, Thruster…)
- Cardio: 8 (Rowing Machine, Assault Bike, HIIT Sprints…)
- Recovery: 8 (World's Greatest Stretch, 90/90 Hip, Pigeon Pose…)

### 🎯 Daily Challenges System
- 3 fresh challenges every day (deterministically seeded per user)
- Bonus XP on completion
- Auto-checked against your workout log
- 15 challenge types

### ✨ Enhanced Gamification
- **XP Multipliers** — streak bonus (up to +50%), volume bonus, early bird/night owl bonus (up to 3×)
- **10 levels**: Novice → Beginner → Iron → Bronze → Silver → Gold → Platinum → Diamond → Master → Grandmaster → IronForge Legend
- **36 Badges** across 9 categories: Milestone, Streak, Workouts, Volume, XP, Level, Balance, Special, Challenge
- **1RM estimator** — auto-calculates estimated 1 rep max from weight × reps
- **Muscle balance score** — shows how balanced your training is across muscle groups
- **Longest streak tracking**

### 📐 Muscle Diagrams
- Front and back SVG body diagram for every exercise
- Primary muscles highlighted in orange
- Secondary muscles highlighted in blue
- Auto-rendered in Exercise Library filter view

### 🎬 YouTube Tutorials
- Every exercise has a YouTube search link
- Opens best form tutorials directly
- Works for all 123 exercises

---

## 🚀 Deploy on Render

```bash
# 1. Push to GitHub
git init && git add . && git commit -m "IronForge 3.0"
git remote add origin https://github.com/YOUR_USERNAME/ironforge.git
git push -u origin main

# 2. Create Web Service on render.com
# Connect GitHub repo → render.yaml auto-configures everything
# Includes a 1GB persistent disk for SQLite
```

## 🏃 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
# Opens at http://localhost:8501
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `IRONFORGE_DB` | `ironforge.db` | Path to SQLite database file |

For production on Render, the `render.yaml` sets this to `/data/ironforge.db` on a persistent disk.