"""
IronForge 3.0 — Advanced Gym Tracker
PostgreSQL (Supabase) · 120+ Exercises · Muscle Diagrams · YouTube Links · Enhanced Gamification
"""

import streamlit as st
import psycopg2
import psycopg2.extras
import json
import os
import datetime
import time
import random
import math
import hashlib
from contextlib import contextmanager
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IronForge 3.0",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif !important;
    background-color: #0a0a0d !important;
    color: #f0f0f5 !important;
}
section[data-testid="stSidebar"] {
    background: #0f0f13 !important;
    border-right: 1px solid #1e1e28 !important;
}
section[data-testid="stSidebar"] * { color: #f0f0f5 !important; }
.main .block-container { background: #0a0a0d !important; padding-top: 1.5rem !important; }

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #16161d, #1a1a22) !important;
    border: 1px solid #252530 !important;
    border-radius: 14px !important;
    padding: 18px 22px !important;
}
[data-testid="stMetricValue"] {
    color: #f97316 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 2.4rem !important;
    font-weight: 900 !important;
}
[data-testid="stMetricLabel"] { color: #7878a0 !important; font-size: 13px !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    letter-spacing: 1.5px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #fb923c, #f97316) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px #f9731640 !important;
}
.btn-secondary .stButton > button {
    background: #16161d !important;
    color: #9898ba !important;
    border: 1px solid #252530 !important;
}
.btn-danger .stButton > button { background: linear-gradient(135deg, #ef4444, #dc2626) !important; color: #fff !important; }
.btn-green .stButton > button { background: linear-gradient(135deg, #22c55e, #16a34a) !important; color: #000 !important; }
.btn-blue .stButton > button { background: linear-gradient(135deg, #3b82f6, #2563eb) !important; color: #fff !important; }
.btn-purple .stButton > button { background: linear-gradient(135deg, #a855f7, #7c3aed) !important; color: #fff !important; }

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #14141a !important;
    color: #f0f0f5 !important;
    border: 1px solid #252530 !important;
    border-radius: 10px !important;
}
.streamlit-expanderHeader {
    background: #16161d !important;
    border: 1px solid #252530 !important;
    border-radius: 12px !important;
    color: #f0f0f5 !important;
}
.streamlit-expanderContent { background: #13131a !important; border: 1px solid #252530 !important; }
.stTabs [data-baseweb="tab-list"] { background: #0f0f13 !important; border-bottom: 1px solid #1e1e28 !important; }
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #5a5a7a !important;
    font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important;
    letter-spacing: 1px !important; border-radius: 6px 6px 0 0 !important; padding: 10px 18px !important;
}
.stTabs [aria-selected="true"] { background: #16161d !important; color: #f97316 !important; border-bottom: 2px solid #f97316 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #0a0a0d !important; padding-top: 20px !important; }
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #f97316, #fbbf24) !important;
    border-radius: 4px !important;
}
.stProgress > div > div > div { background: #1a1a22 !important; border-radius: 4px !important; }
.stAlert { background: #16161d !important; border: 1px solid #252530 !important; border-radius: 12px !important; }
hr { border-color: #1e1e28 !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0a0a0d; }
::-webkit-scrollbar-thumb { background: #252530; border-radius: 3px; }

/* Custom cards */
.if-card {
    background: linear-gradient(135deg, #16161d, #1a1a22);
    border: 1px solid #252530;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.if-card:hover { border-color: #f9731640; }
.if-card-highlight { border-color: #f97316 !important; background: linear-gradient(135deg, #f9731610, #1a1a22) !important; }
.if-card-blue { border-color: #3b82f640 !important; background: linear-gradient(135deg, #3b82f610, #1a1a22) !important; }
.if-card-green { border-color: #22c55e40 !important; background: linear-gradient(135deg, #22c55e10, #1a1a22) !important; }
.if-card-purple { border-color: #a855f740 !important; background: linear-gradient(135deg, #a855f710, #1a1a22) !important; }

.if-tag { display:inline-block; padding:3px 10px; border-radius:20px; font-size:12px; font-family:'Barlow Condensed',sans-serif; font-weight:700; letter-spacing:0.5px; margin-right:6px; }
.tag-gym     { background:#3b82f615; color:#3b82f6; border:1px solid #3b82f630; }
.tag-body    { background:#22c55e15; color:#22c55e; border:1px solid #22c55e30; }
.tag-orange  { background:#f9731615; color:#f97316; border:1px solid #f9731630; }
.tag-blue    { background:#3b82f615; color:#3b82f6; border:1px solid #3b82f630; }
.tag-green   { background:#22c55e15; color:#22c55e; border:1px solid #22c55e30; }
.tag-purple  { background:#a855f715; color:#a855f7; border:1px solid #a855f730; }
.tag-red     { background:#ef444415; color:#ef4444; border:1px solid #ef444430; }
.tag-yellow  { background:#fbbf2415; color:#fbbf24; border:1px solid #fbbf2430; }

.if-title  { font-family:'Barlow Condensed',sans-serif; font-size:32px; font-weight:900; letter-spacing:3px; color:#f0f0f5; }
.if-muted  { color:#6868888; font-size:13px; }
.if-orange { color:#f97316; }

/* XP popup animation */
@keyframes xp-pop { 0%{transform:scale(0.5);opacity:0} 50%{transform:scale(1.2)} 100%{transform:scale(1);opacity:1} }
.xp-pop { animation: xp-pop 0.4s ease-out; }

/* Badges */
.badge-earned {
    background: linear-gradient(135deg, #1a1a22, #16161d);
    border: 1px solid #f97316;
    border-radius: 14px; padding: 18px; text-align: center;
    box-shadow: 0 0 20px #f9731620;
}
.badge-locked {
    background: #111117;
    border: 1px solid #1e1e28;
    border-radius: 14px; padding: 18px; text-align: center; opacity: 0.4;
}

/* Level bar gradient */
.level-bar { height:8px; border-radius:4px; background: linear-gradient(90deg, #f97316, #fbbf24); }

/* Challenge card */
.challenge-active { border-color: #3b82f6 !important; background: linear-gradient(135deg, #3b82f608, #1a1a22) !important; }
.challenge-done   { border-color: #22c55e !important; background: linear-gradient(135deg, #22c55e08, #1a1a22) !important; }

/* Difficulty tags */
.diff-beginner     { background:#22c55e15; color:#22c55e; border:1px solid #22c55e30; }
.diff-intermediate { background:#f9731615; color:#f97316; border:1px solid #f9731630; }
.diff-advanced     { background:#ef444415; color:#ef4444; border:1px solid #ef444430; }

/* Multiplier badge */
.multiplier-badge {
    background: linear-gradient(135deg, #fbbf24, #f97316);
    color: #000; font-family: 'Barlow Condensed', sans-serif; font-weight: 900;
    font-size: 13px; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATABASE LAYER  — PostgreSQL via psycopg2 (Supabase / Neon)
# Set DATABASE_URL env var to your Supabase connection string
# ─────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if not DATABASE_URL:
    st.error("⚠️ DATABASE_URL environment variable is not set. Please add your Supabase connection string in Render → Environment.")
    st.stop()

@contextmanager
def get_db():
    """Open a psycopg2 connection using RealDictCursor so rows behave like dicts."""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def _exec(conn, sql, params=()):
    """Execute a single statement and return the cursor."""
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur

def init_db():
    """Create all tables if they don't exist. Safe to run on every startup."""
    tables = [
        """CREATE TABLE IF NOT EXISTS users (
            id                SERIAL PRIMARY KEY,
            username          TEXT    UNIQUE NOT NULL,
            created_at        TEXT    DEFAULT CURRENT_DATE,
            total_xp          INTEGER DEFAULT 0,
            level             INTEGER DEFAULT 0,
            streak            INTEGER DEFAULT 0,
            longest_streak    INTEGER DEFAULT 0,
            last_workout_date TEXT,
            bodyweight_unit   TEXT    DEFAULT 'kg'
        )""",
        """CREATE TABLE IF NOT EXISTS workouts (
            id              SERIAL PRIMARY KEY,
            user_id         INTEGER NOT NULL REFERENCES users(id),
            date            TEXT    NOT NULL,
            total_sets      INTEGER DEFAULT 0,
            total_xp        INTEGER DEFAULT 0,
            base_xp         INTEGER DEFAULT 0,
            bonus_xp        INTEGER DEFAULT 0,
            xp_multiplier   REAL    DEFAULT 1.0,
            note            TEXT,
            duration_min    INTEGER DEFAULT 0,
            muscles_trained TEXT,
            exercise_count  INTEGER DEFAULT 0
        )""",
        """CREATE TABLE IF NOT EXISTS workout_exercises (
            id              SERIAL PRIMARY KEY,
            workout_id      INTEGER NOT NULL REFERENCES workouts(id),
            exercise_id     INTEGER NOT NULL,
            exercise_name   TEXT    NOT NULL,
            muscle_group    TEXT,
            sets_completed  INTEGER DEFAULT 0,
            weight_used     REAL,
            reps_completed  TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS personal_records (
            id            SERIAL PRIMARY KEY,
            user_id       INTEGER NOT NULL REFERENCES users(id),
            exercise_id   INTEGER NOT NULL,
            exercise_name TEXT    NOT NULL,
            weight        REAL,
            reps          INTEGER,
            one_rep_max   REAL,
            date          TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS bodyweight_log (
            id      SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            date    TEXT    NOT NULL,
            weight  REAL    NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS badges_earned (
            id        SERIAL PRIMARY KEY,
            user_id   INTEGER NOT NULL REFERENCES users(id),
            badge_id  TEXT    NOT NULL,
            earned_at TEXT    DEFAULT CURRENT_DATE,
            UNIQUE(user_id, badge_id)
        )""",
        """CREATE TABLE IF NOT EXISTS daily_challenges (
            id           SERIAL PRIMARY KEY,
            user_id      INTEGER NOT NULL REFERENCES users(id),
            date         TEXT    NOT NULL,
            challenge_id TEXT    NOT NULL,
            completed    INTEGER DEFAULT 0,
            completed_at TEXT,
            UNIQUE(user_id, date, challenge_id)
        )""",
        """CREATE TABLE IF NOT EXISTS xp_log (
            id      SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            date    TEXT    NOT NULL,
            amount  INTEGER NOT NULL,
            source  TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS muscle_stats (
            id         SERIAL PRIMARY KEY,
            user_id    INTEGER NOT NULL REFERENCES users(id),
            muscle     TEXT    NOT NULL,
            total_sets INTEGER DEFAULT 0,
            UNIQUE(user_id, muscle)
        )""",
        """CREATE TABLE IF NOT EXISTS unique_exercises (
            user_id     INTEGER NOT NULL REFERENCES users(id),
            exercise_id TEXT    NOT NULL,
            PRIMARY KEY(user_id, exercise_id)
        )""",
    ]
    with get_db() as conn:
        for ddl in tables:
            _exec(conn, ddl)

init_db()

# ─── DB helpers ───────────────────────────────────────────────
def db_get_user(username):
    with get_db() as conn:
        cur = _exec(conn, "SELECT * FROM users WHERE username=%s", (username,))
        row = cur.fetchone()
        return dict(row) if row else None

def db_create_user(username):
    with get_db() as conn:
        _exec(conn, "INSERT INTO users(username) VALUES(%s) ON CONFLICT(username) DO NOTHING", (username,))
    return db_get_user(username)

def db_update_user(user_id, **kwargs):
    if not kwargs: return
    sets = ", ".join(f"{k}=%s" for k in kwargs)
    vals = list(kwargs.values()) + [user_id]
    with get_db() as conn:
        _exec(conn, f"UPDATE users SET {sets} WHERE id=%s", vals)

def db_save_workout(user_id, date, total_sets, total_xp, base_xp, bonus_xp, multiplier,
                     note, duration_min, muscles, exercise_count, exercises):
    with get_db() as conn:
        cur = _exec(conn,
            """INSERT INTO workouts
               (user_id,date,total_sets,total_xp,base_xp,bonus_xp,xp_multiplier,
                note,duration_min,muscles_trained,exercise_count)
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
            (user_id, date, total_sets, total_xp, base_xp, bonus_xp, multiplier,
             note, duration_min, json.dumps(muscles), exercise_count)
        )
        wid = cur.fetchone()["id"]
        for ex in exercises:
            _exec(conn,
                """INSERT INTO workout_exercises
                   (workout_id,exercise_id,exercise_name,muscle_group,sets_completed,weight_used,reps_completed)
                   VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                (wid, ex.get("id", 0), ex["name"], ex.get("muscle",""), ex["sets"],
                 ex.get("weight_used", None), ex.get("reps",""))
            )
        return wid

def db_get_workouts(user_id, limit=100):
    with get_db() as conn:
        cur = _exec(conn,
            "SELECT * FROM workouts WHERE user_id=%s ORDER BY date DESC LIMIT %s",
            (user_id, limit)
        )
        return [dict(r) for r in cur.fetchall()]

def db_get_workout_exercises(workout_id):
    with get_db() as conn:
        cur = _exec(conn,
            "SELECT * FROM workout_exercises WHERE workout_id=%s", (workout_id,)
        )
        return [dict(r) for r in cur.fetchall()]

def db_save_pr(user_id, exercise_id, exercise_name, weight, reps):
    orm = weight * (1 + reps / 30.0) if reps and weight else None
    with get_db() as conn:
        cur = _exec(conn,
            "SELECT id FROM personal_records WHERE user_id=%s AND exercise_id=%s",
            (user_id, exercise_id)
        )
        existing = cur.fetchone()
        if existing:
            _exec(conn,
                "UPDATE personal_records SET weight=%s,reps=%s,one_rep_max=%s,date=%s WHERE id=%s",
                (weight, reps, orm, str(datetime.date.today()), existing["id"])
            )
        else:
            _exec(conn,
                """INSERT INTO personal_records
                   (user_id,exercise_id,exercise_name,weight,reps,one_rep_max,date)
                   VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                (user_id, exercise_id, exercise_name, weight, reps, orm, str(datetime.date.today()))
            )

def db_get_prs(user_id):
    with get_db() as conn:
        cur = _exec(conn, "SELECT * FROM personal_records WHERE user_id=%s", (user_id,))
        return {str(r["exercise_id"]): dict(r) for r in cur.fetchall()}

def db_log_bodyweight(user_id, weight, date):
    with get_db() as conn:
        _exec(conn, "INSERT INTO bodyweight_log(user_id,date,weight) VALUES(%s,%s,%s)",
              (user_id, date, weight))

def db_get_bodyweight_log(user_id, limit=60):
    with get_db() as conn:
        cur = _exec(conn,
            "SELECT * FROM bodyweight_log WHERE user_id=%s ORDER BY date DESC LIMIT %s",
            (user_id, limit)
        )
        return [dict(r) for r in cur.fetchall()]

def db_earn_badge(user_id, badge_id):
    with get_db() as conn:
        _exec(conn,
            "INSERT INTO badges_earned(user_id,badge_id) VALUES(%s,%s) ON CONFLICT DO NOTHING",
            (user_id, badge_id)
        )

def db_get_badges(user_id):
    with get_db() as conn:
        cur = _exec(conn, "SELECT badge_id FROM badges_earned WHERE user_id=%s", (user_id,))
        return [r["badge_id"] for r in cur.fetchall()]

def db_log_xp(user_id, amount, source):
    with get_db() as conn:
        _exec(conn, "INSERT INTO xp_log(user_id,date,amount,source) VALUES(%s,%s,%s,%s)",
              (user_id, str(datetime.date.today()), amount, source))

def db_get_xp_log(user_id, limit=30):
    with get_db() as conn:
        cur = _exec(conn,
            "SELECT * FROM xp_log WHERE user_id=%s ORDER BY id DESC LIMIT %s",
            (user_id, limit)
        )
        return [dict(r) for r in cur.fetchall()]

def db_update_muscle_stats(user_id, muscle, sets_delta):
    with get_db() as conn:
        _exec(conn,
            """INSERT INTO muscle_stats(user_id,muscle,total_sets) VALUES(%s,%s,%s)
               ON CONFLICT(user_id,muscle) DO UPDATE SET total_sets=muscle_stats.total_sets+%s""",
            (user_id, muscle, sets_delta, sets_delta)
        )

def db_get_muscle_stats(user_id):
    with get_db() as conn:
        cur = _exec(conn, "SELECT * FROM muscle_stats WHERE user_id=%s", (user_id,))
        return {r["muscle"]: r["total_sets"] for r in cur.fetchall()}

def db_track_unique_exercise(user_id, exercise_id):
    with get_db() as conn:
        _exec(conn,
            "INSERT INTO unique_exercises(user_id,exercise_id) VALUES(%s,%s) ON CONFLICT DO NOTHING",
            (user_id, str(exercise_id))
        )

def db_count_unique_exercises(user_id):
    with get_db() as conn:
        cur = _exec(conn,
            "SELECT COUNT(*) as cnt FROM unique_exercises WHERE user_id=%s", (user_id,)
        )
        return cur.fetchone()["cnt"]

def db_get_challenges(user_id, date):
    with get_db() as conn:
        cur = _exec(conn,
            "SELECT * FROM daily_challenges WHERE user_id=%s AND date=%s", (user_id, date)
        )
        return {r["challenge_id"]: dict(r) for r in cur.fetchall()}

def db_set_challenge(user_id, date, challenge_id, completed=False):
    with get_db() as conn:
        completed_at = str(datetime.datetime.now()) if completed else None
        _exec(conn,
            """INSERT INTO daily_challenges(user_id,date,challenge_id,completed,completed_at)
               VALUES(%s,%s,%s,%s,%s)
               ON CONFLICT(user_id,date,challenge_id)
               DO UPDATE SET completed=%s, completed_at=%s""",
            (user_id, date, challenge_id, int(completed), completed_at,
             int(completed), completed_at)
        )

# ─────────────────────────────────────────────────────────────
# EXERCISE DATA  (120+ exercises)
# ─────────────────────────────────────────────────────────────
def yt(query):
    """Build YouTube search URL for exercise."""
    return "https://www.youtube.com/results?search_query=" + query.replace(" ", "+") + "+proper+form+tutorial"

EXERCISES = [
    # ── CHEST ──────────────────────────────────────────────
    {"id":1,  "name":"Barbell Bench Press",    "muscle":"Chest",    "secondary":["Triceps","Shoulders"], "eq":"gym",        "sets":4,"reps":"6-8",  "rest":120,"xp":25,"diff":"Intermediate",
     "tips":["Retract shoulder blades","Slight arch in lower back","Drive through heels","Touch bar to lower chest","Grip just outside shoulder width"],
     "youtube":yt("barbell bench press")},
    {"id":2,  "name":"Incline Barbell Press",  "muscle":"Chest",    "secondary":["Triceps","Shoulders"], "eq":"gym",        "sets":4,"reps":"8-10", "rest":90, "xp":22,"diff":"Intermediate",
     "tips":["Set bench 30-45°","Upper chest focus","Control descent","Don't flare elbows wide"],
     "youtube":yt("incline barbell bench press")},
    {"id":3,  "name":"Decline Barbell Press",  "muscle":"Chest",    "secondary":["Triceps"],             "eq":"gym",        "sets":3,"reps":"8-10", "rest":90, "xp":20,"diff":"Intermediate",
     "tips":["Feet locked in","Lower chest activation","Spotter recommended","Don't lower bar too fast"],
     "youtube":yt("decline barbell bench press")},
    {"id":4,  "name":"Dumbbell Bench Press",   "muscle":"Chest",    "secondary":["Triceps","Shoulders"], "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":18,"diff":"Beginner",
     "tips":["Greater ROM than barbell","Palms facing feet","Squeeze at top","Lower to chest level"],
     "youtube":yt("dumbbell bench press")},
    {"id":5,  "name":"Incline DB Press",       "muscle":"Chest",    "secondary":["Triceps","Shoulders"], "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":18,"diff":"Beginner",
     "tips":["Bench at 30-45°","Elbows at 45°","Full range of motion","Squeeze at top"],
     "youtube":yt("incline dumbbell press")},
    {"id":6,  "name":"Cable Flye",             "muscle":"Chest",    "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Slight bend in elbows","Feel stretch at bottom","Squeeze hard at top","Control throughout"],
     "youtube":yt("cable chest flye")},
    {"id":7,  "name":"Pec Deck Machine",       "muscle":"Chest",    "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12,"diff":"Beginner",
     "tips":["Keep back flat on pad","Don't let weight pull arms back","Squeeze at peak contraction","Slow negative"],
     "youtube":yt("pec deck fly machine")},
    {"id":8,  "name":"Dumbbell Flye",          "muscle":"Chest",    "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Wide arc motion","Slight elbow bend always","Feel the stretch","Don't go too heavy"],
     "youtube":yt("dumbbell chest flye")},
    {"id":9,  "name":"Push-Up",                "muscle":"Chest",    "secondary":["Triceps","Shoulders"], "eq":"bodyweight", "sets":4,"reps":"15-20","rest":60, "xp":10,"diff":"Beginner",
     "tips":["Core tight throughout","Elbows at 45°","Full range","Don't let hips sag"],
     "youtube":yt("push up perfect form")},
    {"id":10, "name":"Wide Push-Up",           "muscle":"Chest",    "secondary":["Shoulders"],           "eq":"bodyweight", "sets":3,"reps":"12-15","rest":60, "xp":9, "diff":"Beginner",
     "tips":["Hands wider than shoulder","Body straight","Controlled movement","More chest activation"],
     "youtube":yt("wide push up form")},
    {"id":11, "name":"Decline Push-Up",        "muscle":"Chest",    "secondary":["Triceps"],             "eq":"bodyweight", "sets":3,"reps":"12-15","rest":60, "xp":11,"diff":"Intermediate",
     "tips":["Feet elevated on bench","Upper chest focus","Full lockout at top","Keep body straight"],
     "youtube":yt("decline push up form")},
    {"id":12, "name":"Dumbbell Pullover",      "muscle":"Chest",    "secondary":["Back","Triceps"],      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":15,"diff":"Intermediate",
     "tips":["Lying perpendicular on bench","Arms slightly bent","Feel ribcage expand","Control throughout"],
     "youtube":yt("dumbbell pullover chest")},
    {"id":13, "name":"Chest Dips",             "muscle":"Chest",    "secondary":["Triceps","Shoulders"], "eq":"gym",        "sets":3,"reps":"10-15","rest":75, "xp":16,"diff":"Intermediate",
     "tips":["Lean forward for chest emphasis","Go deep for stretch","Control descent","Don't bounce at bottom"],
     "youtube":yt("chest dips form")},
    {"id":14, "name":"Cable Crossover",        "muscle":"Chest",    "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":14,"diff":"Intermediate",
     "tips":["High to low for lower chest","Low to high for upper chest","Hands cross at end","Slow and controlled"],
     "youtube":yt("cable crossover chest")},

    # ── BACK ───────────────────────────────────────────────
    {"id":15, "name":"Conventional Deadlift",  "muscle":"Back",     "secondary":["Legs","Glutes","Core"],"eq":"gym",        "sets":4,"reps":"4-6",  "rest":180,"xp":35,"diff":"Advanced",
     "tips":["Bar over mid-foot","Hinge hips back","Brace entire core","Chest up, shoulders back","Lock hips at top"],
     "youtube":yt("conventional deadlift form")},
    {"id":16, "name":"Pull-Up",                "muscle":"Back",     "secondary":["Biceps"],              "eq":"bodyweight", "sets":4,"reps":"6-10", "rest":90, "xp":22,"diff":"Intermediate",
     "tips":["Full dead hang start","Pull elbows to hips","Avoid swinging","Chest to bar"],
     "youtube":yt("pull up perfect form")},
    {"id":17, "name":"Chin-Up",                "muscle":"Back",     "secondary":["Biceps"],              "eq":"bodyweight", "sets":3,"reps":"6-10", "rest":90, "xp":20,"diff":"Intermediate",
     "tips":["Supinated (underhand) grip","Full dead hang","Pull chin over bar","Biceps heavily involved"],
     "youtube":yt("chin up form technique")},
    {"id":18, "name":"Barbell Bent-Over Row",  "muscle":"Back",     "secondary":["Biceps","Core"],       "eq":"gym",        "sets":4,"reps":"8-10", "rest":90, "xp":24,"diff":"Intermediate",
     "tips":["Keep back flat","Hinge to 45°","Pull elbows behind body","Bar to lower ribs"],
     "youtube":yt("barbell bent over row")},
    {"id":19, "name":"Dumbbell Row",           "muscle":"Back",     "secondary":["Biceps"],              "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":18,"diff":"Beginner",
     "tips":["Support with same-side hand","Pull elbow high and back","Keep back flat","Full stretch at bottom"],
     "youtube":yt("single arm dumbbell row")},
    {"id":20, "name":"Lat Pulldown",           "muscle":"Back",     "secondary":["Biceps"],              "eq":"gym",        "sets":4,"reps":"10-12","rest":75, "xp":18,"diff":"Beginner",
     "tips":["Lean back 10-15°","Pull to upper chest","Full extension at top","Squeeze lats at bottom"],
     "youtube":yt("lat pulldown form")},
    {"id":21, "name":"Seated Cable Row",       "muscle":"Back",     "secondary":["Biceps"],              "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":16,"diff":"Beginner",
     "tips":["Keep torso upright","Squeeze shoulder blades","Full stretch at front","Don't lean back too far"],
     "youtube":yt("seated cable row form")},
    {"id":22, "name":"T-Bar Row",              "muscle":"Back",     "secondary":["Biceps","Core"],       "eq":"gym",        "sets":4,"reps":"8-10", "rest":90, "xp":22,"diff":"Intermediate",
     "tips":["Chest on pad or bent-over","Neutral grip","Pull to lower chest","Full contraction"],
     "youtube":yt("t-bar row form")},
    {"id":23, "name":"Face Pull",              "muscle":"Back",     "secondary":["Shoulders"],           "eq":"gym",        "sets":3,"reps":"15-20","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Rope at eye level","Pull to face, elbows high","External rotation at end","Great for shoulder health"],
     "youtube":yt("face pull cable exercise")},
    {"id":24, "name":"Straight-Arm Pulldown",  "muscle":"Back",     "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Arms straight throughout","Hinge at shoulder","Pull to thighs","Isolates lats well"],
     "youtube":yt("straight arm pulldown lat")},
    {"id":25, "name":"Rack Pull",              "muscle":"Back",     "secondary":["Legs","Glutes"],       "eq":"gym",        "sets":4,"reps":"5-8",  "rest":150,"xp":28,"diff":"Advanced",
     "tips":["Bar at knee height","Similar to deadlift top half","Great for upper back","Heavy overloading"],
     "youtube":yt("rack pull exercise form")},
    {"id":26, "name":"Back Extension",         "muscle":"Back",     "secondary":["Glutes"],              "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12,"diff":"Beginner",
     "tips":["Don't hyperextend","Squeeze glutes at top","Hold 1 second","Can add weight on chest"],
     "youtube":yt("back extension hyperextension form")},
    {"id":27, "name":"Good Morning",           "muscle":"Back",     "secondary":["Glutes","Hamstrings"], "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":18,"diff":"Intermediate",
     "tips":["Slight knee bend","Hinge at hips","Feel hamstring stretch","Keep back neutral"],
     "youtube":yt("good morning exercise form")},
    {"id":28, "name":"Inverted Row",           "muscle":"Back",     "secondary":["Biceps"],              "eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":13,"diff":"Beginner",
     "tips":["Keep body rigid","Pull chest to bar","Lower feet for difficulty","Pause at top"],
     "youtube":yt("inverted row bodyweight")},

    # ── SHOULDERS ──────────────────────────────────────────
    {"id":29, "name":"Barbell Overhead Press", "muscle":"Shoulders","secondary":["Triceps","Core"],      "eq":"gym",        "sets":4,"reps":"6-10", "rest":120,"xp":24,"diff":"Intermediate",
     "tips":["Brace core hard","Press around face not in front","Lock out completely","Bar in line with heels"],
     "youtube":yt("barbell overhead press form")},
    {"id":30, "name":"Dumbbell Shoulder Press","muscle":"Shoulders","secondary":["Triceps"],             "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":18,"diff":"Beginner",
     "tips":["Seated for stability","Full range of motion","Don't lock out elbows hard","Press straight up"],
     "youtube":yt("dumbbell shoulder press seated")},
    {"id":31, "name":"Arnold Press",           "muscle":"Shoulders","secondary":["Triceps"],             "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":17,"diff":"Intermediate",
     "tips":["Start palms facing you","Rotate as you press","Full range","Hits all 3 delt heads"],
     "youtube":yt("arnold press form technique")},
    {"id":32, "name":"Lateral Raise",          "muscle":"Shoulders","secondary":[],                      "eq":"gym",        "sets":4,"reps":"12-15","rest":60, "xp":13,"diff":"Beginner",
     "tips":["Lead with elbows not hands","Stop at shoulder height","Control the negative","Slight forward lean"],
     "youtube":yt("lateral raise form shoulder")},
    {"id":33, "name":"Cable Lateral Raise",    "muscle":"Shoulders","secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12,"diff":"Beginner",
     "tips":["Constant tension","Better than dumbbells for isolation","Unilateral focus","Don't swing"],
     "youtube":yt("cable lateral raise shoulder")},
    {"id":34, "name":"Front Raise",            "muscle":"Shoulders","secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":11,"diff":"Beginner",
     "tips":["Keep arms straight","Don't swing body","Control descent","Don't raise above shoulder height"],
     "youtube":yt("front raise shoulder exercise")},
    {"id":35, "name":"Rear Delt Flye",         "muscle":"Shoulders","secondary":["Back"],                "eq":"gym",        "sets":3,"reps":"15-20","rest":60, "xp":12,"diff":"Beginner",
     "tips":["Bent over or face-down on incline","Arms wide arc","Squeeze rear delts","Don't trap-shrug"],
     "youtube":yt("rear delt flye form")},
    {"id":36, "name":"Upright Row",            "muscle":"Shoulders","secondary":["Traps","Biceps"],      "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":14,"diff":"Intermediate",
     "tips":["Bar close to body","Elbows above hands","Don't go above chin","Use moderate weight"],
     "youtube":yt("upright row form barbell")},
    {"id":37, "name":"Barbell Shrug",          "muscle":"Shoulders","secondary":[],                      "eq":"gym",        "sets":4,"reps":"12-15","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Don't roll shoulders","Straight up and down","Squeeze at top 1-2 seconds","Heavy weight works well"],
     "youtube":yt("barbell shrug trap exercise")},
    {"id":38, "name":"Landmine Press",         "muscle":"Shoulders","secondary":["Chest","Core"],        "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":15,"diff":"Intermediate",
     "tips":["Arc motion great for shoulder health","Unilateral or bilateral","Good for those with shoulder issues","Core braced"],
     "youtube":yt("landmine press shoulder")},
    {"id":39, "name":"Pike Push-Up",           "muscle":"Shoulders","secondary":["Triceps"],             "eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":11,"diff":"Beginner",
     "tips":["Hips high inverted V","Lower head toward floor","Progression toward handstand","Keep core engaged"],
     "youtube":yt("pike push up shoulder")},

    # ── BICEPS ─────────────────────────────────────────────
    {"id":40, "name":"Barbell Curl",           "muscle":"Biceps",   "secondary":["Forearms"],            "eq":"gym",        "sets":4,"reps":"8-12", "rest":75, "xp":16,"diff":"Beginner",
     "tips":["Keep elbows fixed","Full range","Slow negative 3 seconds","Supinate wrist at top"],
     "youtube":yt("barbell curl bicep form")},
    {"id":41, "name":"Incline DB Curl",        "muscle":"Biceps",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"10-12","rest":60, "xp":15,"diff":"Intermediate",
     "tips":["Bench at 45-60°","Full stretch at bottom","Great long head stretch","Don't swing arms"],
     "youtube":yt("incline dumbbell curl form")},
    {"id":42, "name":"Hammer Curl",            "muscle":"Biceps",   "secondary":["Forearms","Brachialis"],"eq":"gym",       "sets":3,"reps":"10-12","rest":60, "xp":13,"diff":"Beginner",
     "tips":["Thumbs pointing up","Elbows at sides","Don't swing","Hits brachialis and brachioradialis"],
     "youtube":yt("hammer curl form technique")},
    {"id":43, "name":"Concentration Curl",     "muscle":"Biceps",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12,"diff":"Beginner",
     "tips":["Elbow braced on inner thigh","Full range","Squeeze peak contraction","Don't move upper arm"],
     "youtube":yt("concentration curl form")},
    {"id":44, "name":"Preacher Curl",          "muscle":"Biceps",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"10-12","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Full stretch at bottom","Don't hyperextend at bottom","Squeeze at top","Chest against pad"],
     "youtube":yt("preacher curl ez bar form")},
    {"id":45, "name":"Cable Curl",             "muscle":"Biceps",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12,"diff":"Beginner",
     "tips":["Constant tension advantage","Keep elbows fixed","Full range","Can use rope, bar, or handle"],
     "youtube":yt("cable curl bicep form")},
    {"id":46, "name":"Reverse Curl",           "muscle":"Biceps",   "secondary":["Forearms","Brachialis"],"eq":"gym",       "sets":3,"reps":"10-12","rest":60, "xp":11,"diff":"Beginner",
     "tips":["Overhand (pronated) grip","Hits brachioradialis heavily","Use lighter weight","Keep elbows still"],
     "youtube":yt("reverse curl forearm bicep")},
    {"id":47, "name":"Spider Curl",            "muscle":"Biceps",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"10-12","rest":60, "xp":13,"diff":"Intermediate",
     "tips":["Chest on incline bench facing down","Arms hanging freely","Full stretch at bottom","Maximum contraction"],
     "youtube":yt("spider curl bicep form")},
    {"id":48, "name":"21s",                    "muscle":"Biceps",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"21",   "rest":90, "xp":15,"diff":"Intermediate",
     "tips":["7 lower half reps","7 upper half reps","7 full reps = 1 set","Use moderate weight","Feel the burn!"],
     "youtube":yt("21s bicep curl technique")},

    # ── TRICEPS ────────────────────────────────────────────
    {"id":49, "name":"Close-Grip Bench Press", "muscle":"Triceps",  "secondary":["Chest","Shoulders"],   "eq":"gym",        "sets":4,"reps":"8-10", "rest":90, "xp":18,"diff":"Intermediate",
     "tips":["Hands shoulder-width","Elbows close to body","Full range of motion","Don't go too narrow"],
     "youtube":yt("close grip bench press triceps")},
    {"id":50, "name":"Skull Crusher",          "muscle":"Triceps",  "secondary":[],                      "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":16,"diff":"Intermediate",
     "tips":["Upper arms vertical","Only elbows move","Lower to forehead or behind head","Full lockout"],
     "youtube":yt("skull crusher EZ bar form")},
    {"id":51, "name":"Tricep Pushdown",        "muscle":"Triceps",  "secondary":[],                      "eq":"gym",        "sets":4,"reps":"12-15","rest":60, "xp":13,"diff":"Beginner",
     "tips":["Elbows fixed at sides","Full lockout at bottom","Control return","Can use rope or bar"],
     "youtube":yt("tricep pushdown cable form")},
    {"id":52, "name":"Overhead Tricep Ext.",   "muscle":"Triceps",  "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Upper arms close to head","Full stretch at bottom","Long head focused","Keep core tight"],
     "youtube":yt("overhead tricep extension dumbbell")},
    {"id":53, "name":"Tricep Dip",             "muscle":"Triceps",  "secondary":["Chest","Shoulders"],   "eq":"bodyweight", "sets":4,"reps":"12-15","rest":75, "xp":16,"diff":"Beginner",
     "tips":["Torso upright for triceps","Elbows close to body","Full extension at top","Don't dip too low"],
     "youtube":yt("tricep dip bench form")},
    {"id":54, "name":"Tricep Kickback",        "muscle":"Triceps",  "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":11,"diff":"Beginner",
     "tips":["Upper arm parallel to floor","Full extension","Control return","Don't swing"],
     "youtube":yt("tricep kickback dumbbell form")},
    {"id":55, "name":"Diamond Push-Up",        "muscle":"Triceps",  "secondary":["Chest"],               "eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":11,"diff":"Intermediate",
     "tips":["Diamond hand shape under chest","Elbows close","Full extension","Harder than regular push-up"],
     "youtube":yt("diamond push up triceps")},
    {"id":56, "name":"JM Press",               "muscle":"Triceps",  "secondary":["Chest"],               "eq":"gym",        "sets":3,"reps":"8-10", "rest":75, "xp":16,"diff":"Advanced",
     "tips":["Hybrid between skull crusher and close-grip bench","Bar path toward chin","Very effective","Use moderate weight"],
     "youtube":yt("JM press tricep exercise")},

    # ── LEGS ───────────────────────────────────────────────
    {"id":57, "name":"Barbell Back Squat",     "muscle":"Legs",     "secondary":["Glutes","Core"],       "eq":"gym",        "sets":5,"reps":"5-8",  "rest":180,"xp":30,"diff":"Advanced",
     "tips":["Break at hips and knees together","Chest up, brace core","Drive through full foot","Don't let knees cave in","Reach depth"],
     "youtube":yt("barbell back squat form")},
    {"id":58, "name":"Front Squat",            "muscle":"Legs",     "secondary":["Core","Shoulders"],    "eq":"gym",        "sets":4,"reps":"6-8",  "rest":150,"xp":28,"diff":"Advanced",
     "tips":["Bar on front rack position","Elbows up high","More quad focused","Core ultra tight","Great mobility needed"],
     "youtube":yt("front squat form technique")},
    {"id":59, "name":"Hack Squat",             "muscle":"Legs",     "secondary":["Glutes"],              "eq":"gym",        "sets":4,"reps":"10-12","rest":90, "xp":20,"diff":"Intermediate",
     "tips":["Feet on platform at various angles","Knees track over toes","Full depth","Don't lock knees at top"],
     "youtube":yt("hack squat machine form")},
    {"id":60, "name":"Leg Press",              "muscle":"Legs",     "secondary":["Glutes","Calves"],     "eq":"gym",        "sets":4,"reps":"10-15","rest":90, "xp":18,"diff":"Beginner",
     "tips":["Feet shoulder-width","Go as deep as comfortable","Don't lock knees","Foot position changes emphasis"],
     "youtube":yt("leg press machine form")},
    {"id":61, "name":"Romanian Deadlift",      "muscle":"Legs",     "secondary":["Back","Glutes"],       "eq":"gym",        "sets":4,"reps":"10-12","rest":90, "xp":22,"diff":"Intermediate",
     "tips":["Push hips back not down","Feel hamstring stretch","Bar close to legs","Hips hinge not spine bend"],
     "youtube":yt("romanian deadlift form hamstring")},
    {"id":62, "name":"Stiff-Leg Deadlift",     "muscle":"Legs",     "secondary":["Back","Glutes"],       "eq":"gym",        "sets":3,"reps":"10-12","rest":90, "xp":20,"diff":"Intermediate",
     "tips":["Legs nearly straight","Maximum hamstring stretch","Controlled movement","Don't round lower back"],
     "youtube":yt("stiff leg deadlift form")},
    {"id":63, "name":"Lying Leg Curl",         "muscle":"Legs",     "secondary":[],                      "eq":"gym",        "sets":4,"reps":"10-12","rest":75, "xp":14,"diff":"Beginner",
     "tips":["Don't let hips rise","Full range of motion","Slow negative","Curl to glutes"],
     "youtube":yt("lying leg curl hamstring form")},
    {"id":64, "name":"Leg Extension",          "muscle":"Legs",     "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":13,"diff":"Beginner",
     "tips":["Full extension with squeeze","Control the negative","Keep hips down","Isolates quads"],
     "youtube":yt("leg extension machine form quads")},
    {"id":65, "name":"Bulgarian Split Squat",  "muscle":"Legs",     "secondary":["Glutes","Core"],       "eq":"gym",        "sets":3,"reps":"10-12","rest":90, "xp":22,"diff":"Intermediate",
     "tips":["Rear foot elevated","Front foot far enough forward","Knee doesn't go too far past toe","Stay upright"],
     "youtube":yt("bulgarian split squat form")},
    {"id":66, "name":"Walking Lunge",          "muscle":"Legs",     "secondary":["Glutes","Core"],       "eq":"bodyweight", "sets":3,"reps":"12-16","rest":75, "xp":15,"diff":"Beginner",
     "tips":["Long steps","Back knee near floor","Torso upright","Can add dumbbells"],
     "youtube":yt("walking lunge form technique")},
    {"id":67, "name":"Reverse Lunge",          "muscle":"Legs",     "secondary":["Glutes"],              "eq":"bodyweight", "sets":3,"reps":"12-16","rest":75, "xp":14,"diff":"Beginner",
     "tips":["Step back not forward","Easier on knee than forward lunge","Keep front knee stable","Upright torso"],
     "youtube":yt("reverse lunge form")},
    {"id":68, "name":"Step-Up",                "muscle":"Legs",     "secondary":["Glutes","Core"],       "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Drive through the stepping foot","Don't push off trailing foot","Full hip extension at top","Add weight for challenge"],
     "youtube":yt("step up exercise form dumbbell")},
    {"id":69, "name":"Box Jump",               "muscle":"Legs",     "secondary":["Glutes","Core"],       "eq":"gym",        "sets":3,"reps":"8-10", "rest":90, "xp":16,"diff":"Intermediate",
     "tips":["Land softly with bent knees","Full extension at top","Step down don't jump down","Explosive hip extension"],
     "youtube":yt("box jump proper technique")},
    {"id":70, "name":"Jump Squat",             "muscle":"Legs",     "secondary":["Glutes","Calves"],     "eq":"bodyweight", "sets":3,"reps":"12-15","rest":60, "xp":13,"diff":"Intermediate",
     "tips":["Land softly","Full squat depth","Arms assist the jump","Explosive movement"],
     "youtube":yt("jump squat plyometric form")},
    {"id":71, "name":"Sissy Squat",            "muscle":"Legs",     "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":15,"diff":"Advanced",
     "tips":["Extreme quad stretch","Hold support for balance","Lean back as knees come forward","Small range initially"],
     "youtube":yt("sissy squat form quad")},
    {"id":72, "name":"Nordic Hamstring Curl",  "muscle":"Legs",     "secondary":[],                      "eq":"gym",        "sets":3,"reps":"5-8",  "rest":90, "xp":20,"diff":"Advanced",
     "tips":["Feet anchored","Lower body as slowly as possible","Push off floor to return","Incredible hamstring builder"],
     "youtube":yt("nordic hamstring curl form")},

    # ── CORE ───────────────────────────────────────────────
    {"id":73, "name":"Plank",                  "muscle":"Core",     "secondary":["Shoulders","Glutes"],  "eq":"bodyweight", "sets":3,"reps":"45-60s","rest":45,"xp":8, "diff":"Beginner",
     "tips":["Straight line head to heels","Squeeze glutes and abs","Don't hold breath","Progress to longer holds"],
     "youtube":yt("plank form perfect technique")},
    {"id":74, "name":"Side Plank",             "muscle":"Core",     "secondary":["Shoulders"],           "eq":"bodyweight", "sets":3,"reps":"30-45s","rest":45,"xp":9, "diff":"Beginner",
     "tips":["Stack feet or stagger","Hip doesn't sag","Progress to raising top leg","Both sides equally"],
     "youtube":yt("side plank form oblique")},
    {"id":75, "name":"Hanging Leg Raise",      "muscle":"Core",     "secondary":[],                      "eq":"gym",        "sets":3,"reps":"10-15","rest":60, "xp":16,"diff":"Intermediate",
     "tips":["Control the movement","Don't swing","Squeeze abs at top","Progress to toes to bar"],
     "youtube":yt("hanging leg raise abs form")},
    {"id":76, "name":"Cable Crunch",           "muscle":"Core",     "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":14,"diff":"Beginner",
     "tips":["Hips stay still, spine flexes","Round back to crunch","Squeeze abs hard","Load progressively"],
     "youtube":yt("cable crunch abs form")},
    {"id":77, "name":"Ab Wheel Rollout",       "muscle":"Core",     "secondary":["Lats","Shoulders"],    "eq":"gym",        "sets":3,"reps":"8-12", "rest":75, "xp":18,"diff":"Advanced",
     "tips":["Start from knees","Brace core extremely hard","Don't let hips drop","Progress to standing"],
     "youtube":yt("ab wheel rollout form")},
    {"id":78, "name":"Bicycle Crunch",         "muscle":"Core",     "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"20-30","rest":45, "xp":9, "diff":"Beginner",
     "tips":["Slow controlled rotation","Lower back pressed down","Hands light behind head","Opposite elbow to knee"],
     "youtube":yt("bicycle crunch form abs")},
    {"id":79, "name":"Russian Twist",          "muscle":"Core",     "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"20-30","rest":45, "xp":9, "diff":"Beginner",
     "tips":["Lean back slightly","Feet can be elevated","Touch ground each side","Add weight for progression"],
     "youtube":yt("russian twist core form")},
    {"id":80, "name":"Dragon Flag",            "muscle":"Core",     "secondary":["Lats","Shoulders"],    "eq":"gym",        "sets":3,"reps":"5-8",  "rest":90, "xp":22,"diff":"Advanced",
     "tips":["Full body lifted","Don't pike at hips","Incredibly hard","Progress from negative-only"],
     "youtube":yt("dragon flag core exercise")},
    {"id":81, "name":"Hollow Hold",            "muscle":"Core",     "secondary":["Lats"],                "eq":"bodyweight", "sets":3,"reps":"20-30s","rest":45,"xp":11,"diff":"Intermediate",
     "tips":["Lower back pressed to floor","Arms and legs extended","Hold the position","Gymnastics staple"],
     "youtube":yt("hollow body hold form gymnastics")},
    {"id":82, "name":"Dead Bug",               "muscle":"Core",     "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"10-12","rest":45, "xp":10,"diff":"Beginner",
     "tips":["Press lower back to floor","Slow and controlled","Breathe out during extension","Opposite arm-leg"],
     "youtube":yt("dead bug exercise core form")},
    {"id":83, "name":"Mountain Climber",       "muscle":"Core",     "secondary":["Shoulders","Legs"],    "eq":"bodyweight", "sets":3,"reps":"30",   "rest":45, "xp":10,"diff":"Beginner",
     "tips":["Keep hips level","Drive knees to chest","Increase speed for cardio","Shoulders over wrists"],
     "youtube":yt("mountain climber exercise form")},
    {"id":84, "name":"Pallof Press",           "muscle":"Core",     "secondary":["Shoulders"],           "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12,"diff":"Intermediate",
     "tips":["Anti-rotation exercise","Press cable straight out","Resist rotation throughout","Excellent core stability"],
     "youtube":yt("pallof press anti rotation core")},
    {"id":85, "name":"L-Sit",                  "muscle":"Core",     "secondary":["Triceps","Shoulders"], "eq":"gym",        "sets":3,"reps":"10-20s","rest":60,"xp":20,"diff":"Advanced",
     "tips":["Straight legs parallel to floor","Press down hard with hands","Compress hip flexors","Progress from tuck"],
     "youtube":yt("L-sit exercise form gymnastics")},

    # ── GLUTES ─────────────────────────────────────────────
    {"id":86, "name":"Barbell Hip Thrust",     "muscle":"Glutes",   "secondary":["Hamstrings","Core"],   "eq":"gym",        "sets":4,"reps":"10-15","rest":75, "xp":20,"diff":"Intermediate",
     "tips":["Chin tucked","Squeeze glutes hard at top 1-2s","Full hip extension","Bar on hip crease"],
     "youtube":yt("barbell hip thrust form glutes")},
    {"id":87, "name":"Glute Bridge",           "muscle":"Glutes",   "secondary":["Hamstrings","Core"],   "eq":"bodyweight", "sets":3,"reps":"20-25","rest":45, "xp":9, "diff":"Beginner",
     "tips":["Drive through heels","Squeeze glutes at top","Add resistance to progress","Single-leg variation"],
     "youtube":yt("glute bridge form")},
    {"id":88, "name":"Cable Kickback",         "muscle":"Glutes",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12,"diff":"Beginner",
     "tips":["Keep torso stationary","Full extension","Control return","Use ankle attachment"],
     "youtube":yt("cable kickback glute exercise")},
    {"id":89, "name":"Donkey Kick",            "muscle":"Glutes",   "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"15-20","rest":45, "xp":8, "diff":"Beginner",
     "tips":["Core engaged","Kick to hip height","Don't rotate hips","Quadruped position"],
     "youtube":yt("donkey kick glute exercise form")},
    {"id":90, "name":"Frog Pump",              "muscle":"Glutes",   "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"20-30","rest":45, "xp":8, "diff":"Beginner",
     "tips":["Feet together, knees out","Press through outer heel","Short range, high reps","Feel the burn"],
     "youtube":yt("frog pump glute exercise")},
    {"id":91, "name":"Sumo Deadlift",          "muscle":"Glutes",   "secondary":["Back","Legs","Core"],  "eq":"gym",        "sets":4,"reps":"5-8",  "rest":150,"xp":28,"diff":"Advanced",
     "tips":["Feet very wide, toes out","Bar between legs","Push knees out","More glute/adductor than conventional"],
     "youtube":yt("sumo deadlift form technique")},
    {"id":92, "name":"Clamshell",              "muscle":"Glutes",   "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"20-25","rest":45, "xp":7, "diff":"Beginner",
     "tips":["On your side, hips stacked","Open and close like clamshell","Don't roll hip back","Add band for progression"],
     "youtube":yt("clamshell exercise glute med")},
    {"id":93, "name":"Fire Hydrant",           "muscle":"Glutes",   "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"15-20","rest":45, "xp":7, "diff":"Beginner",
     "tips":["Quadruped position","Lift leg to side","Don't rotate torso","Great warm-up exercise"],
     "youtube":yt("fire hydrant exercise glutes")},
    {"id":94, "name":"Sumo Squat",             "muscle":"Glutes",   "secondary":["Legs","Adductors"],    "eq":"bodyweight", "sets":3,"reps":"15-20","rest":60, "xp":10,"diff":"Beginner",
     "tips":["Toes out 45°","Push knees over toes","Full depth","Good for inner thighs too"],
     "youtube":yt("sumo squat form glutes")},

    # ── CALVES ─────────────────────────────────────────────
    {"id":95, "name":"Standing Calf Raise",    "muscle":"Calves",   "secondary":[],                      "eq":"gym",        "sets":4,"reps":"15-20","rest":45, "xp":11,"diff":"Beginner",
     "tips":["Full range of motion","Pause at bottom for stretch","Vary foot positions","Slow movement"],
     "youtube":yt("standing calf raise form")},
    {"id":96, "name":"Seated Calf Raise",      "muscle":"Calves",   "secondary":[],                      "eq":"gym",        "sets":3,"reps":"15-20","rest":45, "xp":9, "diff":"Beginner",
     "tips":["Targets soleus more","Full stretch at bottom","Heavy weight works well","Controlled movement"],
     "youtube":yt("seated calf raise machine form")},
    {"id":97, "name":"Donkey Calf Raise",      "muscle":"Calves",   "secondary":[],                      "eq":"gym",        "sets":4,"reps":"15-20","rest":45, "xp":12,"diff":"Intermediate",
     "tips":["Bent over at 90°","Full range","Great stretch due to body angle","Old school favorite"],
     "youtube":yt("donkey calf raise form")},
    {"id":98, "name":"Single-Leg Calf Raise",  "muscle":"Calves",   "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"15-20","rest":45, "xp":10,"diff":"Intermediate",
     "tips":["Use step for greater ROM","Hold for balance","Equal work both legs","Slow descent key"],
     "youtube":yt("single leg calf raise form")},
    {"id":99, "name":"Tibialis Raise",         "muscle":"Calves",   "secondary":[],                      "eq":"bodyweight", "sets":3,"reps":"15-20","rest":45, "xp":8, "diff":"Beginner",
     "tips":["Work front of shin","Heel on ground, toes up","Great for shin splints prevention","Often neglected"],
     "youtube":yt("tibialis raise exercise shin splints")},

    # ── FULL BODY ──────────────────────────────────────────
    {"id":100,"name":"Power Clean",            "muscle":"Full Body","secondary":["Back","Legs","Shoulders"],"eq":"gym",      "sets":4,"reps":"3-5",  "rest":180,"xp":35,"diff":"Advanced",
     "tips":["Triple extension (ankle, knee, hip)","Explosive pull","Catch in quarter-squat","Requires coaching to learn"],
     "youtube":yt("power clean barbell technique")},
    {"id":101,"name":"Kettlebell Swing",       "muscle":"Full Body","secondary":["Back","Glutes","Core"], "eq":"gym",        "sets":3,"reps":"15-20","rest":60, "xp":16,"diff":"Intermediate",
     "tips":["Hinge not squat","Drive with hips","Arms are just a chain","Hike bell back aggressively"],
     "youtube":yt("kettlebell swing hip hinge form")},
    {"id":102,"name":"Thruster",               "muscle":"Full Body","secondary":["Shoulders","Core"],     "eq":"gym",        "sets":3,"reps":"8-10", "rest":90, "xp":22,"diff":"Advanced",
     "tips":["Front squat to overhead press in one movement","Use squat momentum","Core braced throughout","CrossFit staple"],
     "youtube":yt("thruster exercise barbell form")},
    {"id":103,"name":"Burpee",                 "muscle":"Full Body","secondary":["Core","Shoulders"],     "eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":15,"diff":"Intermediate",
     "tips":["Explosive jump at top","Chest to floor","Consistent rhythm","Arms overhead at top"],
     "youtube":yt("burpee proper form technique")},
    {"id":104,"name":"Turkish Get-Up",         "muscle":"Full Body","secondary":["Core","Shoulders","Legs"],"eq":"gym",      "sets":3,"reps":"3-5",  "rest":120,"xp":22,"diff":"Advanced",
     "tips":["One arm overhead throughout","Slow and controlled","Eye contact with weight","6-step sequence"],
     "youtube":yt("turkish get up kettlebell form")},
    {"id":105,"name":"Man Maker",              "muscle":"Full Body","secondary":["Core","Chest","Back"],  "eq":"gym",        "sets":3,"reps":"6-8",  "rest":90, "xp":20,"diff":"Advanced",
     "tips":["DB in each hand in push-up position","Push-up, row each arm, clean, press","Brutal full body move","Use light weight to start"],
     "youtube":yt("man maker dumbbell exercise")},
    {"id":106,"name":"Bear Crawl",             "muscle":"Full Body","secondary":["Core","Shoulders"],     "eq":"bodyweight", "sets":3,"reps":"20m",  "rest":60, "xp":13,"diff":"Intermediate",
     "tips":["Knees just off ground","Opposite arm-leg move together","Core engaged","Controlled movement"],
     "youtube":yt("bear crawl exercise form")},
    {"id":107,"name":"Jump Rope",              "muscle":"Full Body","secondary":["Calves","Core"],        "eq":"bodyweight", "sets":3,"reps":"60s",  "rest":45, "xp":11,"diff":"Beginner",
     "tips":["Stay on balls of feet","Keep elbows close","Build to longer sets","Great warm-up/cardio"],
     "youtube":yt("jump rope technique beginners")},

    # ── CARDIO ─────────────────────────────────────────────
    {"id":108,"name":"Treadmill Run",          "muscle":"Cardio",   "secondary":["Legs","Core"],         "eq":"gym",        "sets":1,"reps":"20-30min","rest":0,"xp":15,"diff":"Beginner",
     "tips":["Land midfoot","Slight forward lean","Arms at 90°","Vary speed and incline"],
     "youtube":yt("proper running form treadmill")},
    {"id":109,"name":"Stationary Bike",        "muscle":"Cardio",   "secondary":["Legs"],                "eq":"gym",        "sets":1,"reps":"20-30min","rest":0,"xp":12,"diff":"Beginner",
     "tips":["Seat height at hip level","Push and pull through pedals","Maintain steady cadence","Low impact option"],
     "youtube":yt("stationary bike proper form")},
    {"id":110,"name":"Rowing Machine",         "muscle":"Cardio",   "secondary":["Back","Legs","Core"],  "eq":"gym",        "sets":1,"reps":"15-20min","rest":0,"xp":16,"diff":"Intermediate",
     "tips":["Drive with legs first","Then hinge back","Then pull arms","Full stroke each rep","Great full-body cardio"],
     "youtube":yt("rowing machine proper technique ergometer")},
    {"id":111,"name":"Stair Master",           "muscle":"Cardio",   "secondary":["Glutes","Legs"],       "eq":"gym",        "sets":1,"reps":"15-20min","rest":0,"xp":14,"diff":"Beginner",
     "tips":["Don't lean too much on rails","Full step each time","Vary speed","Brutal glute workout too"],
     "youtube":yt("stair master technique tips")},
    {"id":112,"name":"Elliptical",             "muscle":"Cardio",   "secondary":["Legs","Core"],         "eq":"gym",        "sets":1,"reps":"20-30min","rest":0,"xp":12,"diff":"Beginner",
     "tips":["Full stride","Use arms for full body","Low impact on joints","Great beginner cardio"],
     "youtube":yt("elliptical proper form technique")},
    {"id":113,"name":"HIIT Sprints",           "muscle":"Cardio",   "secondary":["Legs","Core"],         "eq":"gym",        "sets":8,"reps":"20s on/40s off","rest":40,"xp":18,"diff":"Advanced",
     "tips":["Max effort on work intervals","Full recovery during rest","Keep sprints explosive","8-12 rounds"],
     "youtube":yt("HIIT sprint treadmill workout")},
    {"id":114,"name":"Battle Ropes",           "muscle":"Cardio",   "secondary":["Shoulders","Core"],    "eq":"gym",        "sets":4,"reps":"30s",  "rest":30, "xp":15,"diff":"Intermediate",
     "tips":["Alternate arm waves","Core braced","Don't just use arms, hips too","Short intense intervals"],
     "youtube":yt("battle ropes workout form")},
    {"id":115,"name":"Assault Bike",           "muscle":"Cardio",   "secondary":["Full Body"],           "eq":"gym",        "sets":5,"reps":"20s",  "rest":40, "xp":18,"diff":"Advanced",
     "tips":["Max effort every interval","Push AND pull the handles","One of the hardest cardio tools","Air resistance increases infinitely"],
     "youtube":yt("assault bike airbike hiit")},

    # ── RECOVERY ───────────────────────────────────────────
    {"id":116,"name":"Foam Roll Quads",        "muscle":"Recovery", "secondary":[],                      "eq":"bodyweight", "sets":1,"reps":"60s",  "rest":0,  "xp":3, "diff":"Beginner",
     "tips":["Slow rolling motions","Pause on tight spots","Breathe through discomfort","10-15 passes per area"],
     "youtube":yt("foam rolling quads technique")},
    {"id":117,"name":"Hip Flexor Stretch",     "muscle":"Recovery", "secondary":[],                      "eq":"bodyweight", "sets":2,"reps":"45s",  "rest":0,  "xp":3, "diff":"Beginner",
     "tips":["Posterior pelvic tilt","Feel stretch in front hip","Hold 30-60s each side","Great after sitting"],
     "youtube":yt("hip flexor stretch technique")},
    {"id":118,"name":"Child's Pose",           "muscle":"Recovery", "secondary":[],                      "eq":"bodyweight", "sets":1,"reps":"60s",  "rest":0,  "xp":3, "diff":"Beginner",
     "tips":["Arms extended overhead","Sink hips to heels","Deep belly breathing","Excellent spinal decompression"],
     "youtube":yt("child's pose yoga stretch")},
    {"id":119,"name":"World's Greatest Stretch","muscle":"Recovery","secondary":[],                      "eq":"bodyweight", "sets":2,"reps":"5 each side","rest":0,"xp":4,"diff":"Beginner",
     "tips":["Combines hip flexor, thoracic, and hip stretches","Slow and controlled","Hold each position","Great warm-up too"],
     "youtube":yt("world's greatest stretch form")},
    {"id":120,"name":"Pigeon Pose",            "muscle":"Recovery", "secondary":[],                      "eq":"bodyweight", "sets":2,"reps":"60s",  "rest":0,  "xp":3, "diff":"Beginner",
     "tips":["Front leg bent at 90°","Square hips to ground","Walk hands forward to deepen","Hip opener"],
     "youtube":yt("pigeon pose yoga hip opener")},
    {"id":121,"name":"Cat-Cow Stretch",        "muscle":"Recovery", "secondary":[],                      "eq":"bodyweight", "sets":2,"reps":"10",   "rest":0,  "xp":3, "diff":"Beginner",
     "tips":["Slow with breath","Cat: round spine up","Cow: drop belly down","Spinal mobility essential"],
     "youtube":yt("cat cow stretch spine mobility")},
    {"id":122,"name":"Thoracic Rotation",      "muscle":"Recovery", "secondary":[],                      "eq":"bodyweight", "sets":2,"reps":"10 each","rest":0, "xp":4, "diff":"Beginner",
     "tips":["Open book or quadruped","Rotate through mid-back","Keep lower back stable","Great for posture"],
     "youtube":yt("thoracic spine rotation mobility")},
    {"id":123,"name":"90/90 Hip Stretch",      "muscle":"Recovery", "secondary":[],                      "eq":"bodyweight", "sets":2,"reps":"60s",  "rest":0,  "xp":4, "diff":"Beginner",
     "tips":["Both knees at 90°","Rotate between internal and external rotation","Sit tall","Hip mobility essential"],
     "youtube":yt("90/90 hip stretch mobility")},
]

MUSCLES = ["All","Chest","Back","Shoulders","Biceps","Triceps","Legs","Core","Glutes","Calves","Full Body","Cardio","Recovery"]
EQUIPMENT = ["All","gym","bodyweight"]
DIFFICULTIES = ["All","Beginner","Intermediate","Advanced"]

MUSCLE_ICONS = {
    "Chest":"🏋️","Back":"🦅","Shoulders":"🤸","Biceps":"💪","Triceps":"⬇️",
    "Legs":"🦵","Core":"🔆","Glutes":"🍑","Calves":"🦶","Full Body":"⚡",
    "Cardio":"🏃","Recovery":"🧘","All":"✦",
}

# ─────────────────────────────────────────────────────────────
# GAMIFICATION DATA
# ─────────────────────────────────────────────────────────────
LEVELS = [
    (0,      "NOVICE",        "#6b7280", "🌱"),
    (500,    "BEGINNER",      "#3b82f6", "⚡"),
    (1500,   "IRON",          "#6b7280", "🔩"),
    (3500,   "BRONZE",        "#b45309", "🥉"),
    (7000,   "SILVER",        "#9ca3af", "🥈"),
    (12000,  "GOLD",          "#f59e0b", "🥇"),
    (20000,  "PLATINUM",      "#06b6d4", "💎"),
    (35000,  "DIAMOND",       "#8b5cf6", "💠"),
    (60000,  "MASTER",        "#ef4444", "👑"),
    (100000, "GRANDMASTER",   "#f97316", "🔱"),
    (150000, "IRONFORGE LEGEND","#fbbf24","⚡"),
]

BADGES = [
    # First steps
    {"id":"first",      "icon":"🎯","name":"First Blood",      "desc":"Complete 1 workout",     "category":"Milestone"},
    {"id":"week_warrior","icon":"⚡","name":"Week Warrior",     "desc":"7-day streak",           "category":"Streak"},
    {"id":"streak3",    "icon":"🔥","name":"On Fire",           "desc":"3-day streak",           "category":"Streak"},
    {"id":"streak7",    "icon":"⚡","name":"Week Warrior",      "desc":"7-day streak",           "category":"Streak"},
    {"id":"streak14",   "icon":"🌊","name":"Fortnight Force",   "desc":"14-day streak",          "category":"Streak"},
    {"id":"streak30",   "icon":"💥","name":"Iron Routine",      "desc":"30-day streak",          "category":"Streak"},
    {"id":"streak60",   "icon":"🚀","name":"Machine Mode",      "desc":"60-day streak",          "category":"Streak"},
    {"id":"streak100",  "icon":"👑","name":"Century Streak",    "desc":"100-day streak",         "category":"Streak"},
    # Workout counts
    {"id":"w5",         "icon":"💪","name":"Iron Will",         "desc":"5 workouts",             "category":"Workouts"},
    {"id":"w10",        "icon":"🏋️","name":"Gym Rat",           "desc":"10 workouts",            "category":"Workouts"},
    {"id":"w25",        "icon":"🌟","name":"Quarter Century",   "desc":"25 workouts",            "category":"Workouts"},
    {"id":"w50",        "icon":"👑","name":"Gym King",          "desc":"50 workouts",            "category":"Workouts"},
    {"id":"w100",       "icon":"🏆","name":"Centurion",         "desc":"100 workouts",           "category":"Workouts"},
    {"id":"w200",       "icon":"💎","name":"Elite Athlete",     "desc":"200 workouts",           "category":"Workouts"},
    # Sets milestones
    {"id":"sets50",     "icon":"⚙️","name":"Grinder",           "desc":"50 total sets",          "category":"Volume"},
    {"id":"sets100",    "icon":"🏆","name":"Century Club",      "desc":"100 total sets",         "category":"Volume"},
    {"id":"sets500",    "icon":"💎","name":"Diamond Sets",      "desc":"500 total sets",         "category":"Volume"},
    {"id":"sets1000",   "icon":"🔱","name":"Titan Volume",      "desc":"1000 total sets",        "category":"Volume"},
    # XP milestones
    {"id":"xp500",      "icon":"📈","name":"XP Hunter",         "desc":"500 XP earned",          "category":"XP"},
    {"id":"xp5000",     "icon":"🚀","name":"XP Legend",         "desc":"5000 XP earned",         "category":"XP"},
    {"id":"xp25000",    "icon":"💫","name":"XP Colossus",       "desc":"25,000 XP earned",       "category":"XP"},
    # Level badges
    {"id":"level_iron", "icon":"🔩","name":"Iron Rank",         "desc":"Reach Iron level",       "category":"Level"},
    {"id":"level_gold", "icon":"🥇","name":"Golden Athlete",    "desc":"Reach Gold level",       "category":"Level"},
    {"id":"level_plat", "icon":"💎","name":"Platinum Elite",    "desc":"Reach Platinum level",   "category":"Level"},
    # Muscle coverage
    {"id":"muscles6",   "icon":"🌐","name":"Balanced Trainer",  "desc":"Train 6 muscle groups",  "category":"Balance"},
    {"id":"muscles10",  "icon":"🌟","name":"Complete Package",  "desc":"Train all 10 main muscles","category":"Balance"},
    # Special
    {"id":"variety20",  "icon":"🎨","name":"Variety Pack",      "desc":"Log 20 different exercises","category":"Special"},
    {"id":"variety50",  "icon":"📚","name":"Exercise Scholar",  "desc":"Log 50 different exercises","category":"Special"},
    {"id":"earlybird",  "icon":"🌅","name":"Early Bird",        "desc":"Workout before 8am",     "category":"Special"},
    {"id":"nightowl",   "icon":"🦉","name":"Night Owl",         "desc":"Workout after 9pm",      "category":"Special"},
    {"id":"pr",         "icon":"🥇","name":"PR Setter",         "desc":"Save a personal record", "category":"Special"},
    {"id":"pr10",       "icon":"🏆","name":"Record Breaker",    "desc":"Save 10 personal records","category":"Special"},
    {"id":"planner",    "icon":"📋","name":"The Planner",       "desc":"Load a workout plan",    "category":"Special"},
    {"id":"challenge5", "icon":"✅","name":"Challenge Accepted", "desc":"Complete 5 daily challenges","category":"Challenge"},
    {"id":"challenge20","icon":"🎯","name":"Challenge Master",  "desc":"Complete 20 daily challenges","category":"Challenge"},
    {"id":"big_session","icon":"💪","name":"Big Session",       "desc":"Log 8+ exercises in one workout","category":"Special"},
    {"id":"consistent", "icon":"📅","name":"Consistent",        "desc":"Work out 4 days in one week","category":"Special"},
    {"id":"volume_day", "icon":"💥","name":"Volume King",       "desc":"Complete 30+ sets in one workout","category":"Special"},
]

WORKOUT_PLANS = {
    "💪 Push Day":        ["Barbell Bench Press","Incline DB Press","Cable Flye","Barbell Overhead Press","Lateral Raise","Tricep Pushdown","Skull Crusher"],
    "🦅 Pull Day":        ["Conventional Deadlift","Pull-Up","Barbell Bent-Over Row","Lat Pulldown","Seated Cable Row","Barbell Curl","Hammer Curl"],
    "🦵 Leg Day":         ["Barbell Back Squat","Romanian Deadlift","Leg Press","Bulgarian Split Squat","Lying Leg Curl","Leg Extension","Standing Calf Raise"],
    "🔆 Core Blast":      ["Plank","Ab Wheel Rollout","Hanging Leg Raise","Cable Crunch","Russian Twist","Dragon Flag","Pallof Press"],
    "⚡ Full Body Power": ["Conventional Deadlift","Barbell Bench Press","Pull-Up","Barbell Back Squat","Barbell Overhead Press","Barbell Bent-Over Row"],
    "🤸 Bodyweight Only": ["Push-Up","Pull-Up","Diamond Push-Up","Tricep Dip","Bodyweight Split Squat","Plank","Mountain Climber","Burpee"],
    "🍑 Glute Focus":     ["Barbell Hip Thrust","Sumo Deadlift","Bulgarian Split Squat","Cable Kickback","Frog Pump","Romanian Deadlift"],
    "💪 Arm Annihilator": ["Barbell Curl","Incline DB Curl","Preacher Curl","21s","Skull Crusher","Close-Grip Bench Press","Tricep Pushdown","Overhead Tricep Ext."],
    "🌅 Morning Quickie": ["Push-Up","Glute Bridge","Mountain Climber","Jump Squat","Plank","Burpee"],
    "🧘 Active Recovery": ["Hip Flexor Stretch","World's Greatest Stretch","Cat-Cow Stretch","Child's Pose","90/90 Hip Stretch","Thoracic Rotation","Pigeon Pose"],
    "🏃 Cardio Blast":    ["Treadmill Run","Battle Ropes","HIIT Sprints","Jump Rope","Assault Bike"],
    "🔱 Advanced Strength":["Conventional Deadlift","Barbell Back Squat","Barbell Bench Press","Barbell Overhead Press","Pull-Up","Power Clean"],
}

DAILY_CHALLENGES_POOL = [
    {"id":"chest_day",   "name":"Chest Destroyer",     "desc":"Add 3+ Chest exercises to your workout",         "xp":50,  "check": lambda log,_: sum(1 for e in log if e["muscle"]=="Chest") >= 3},
    {"id":"back_day",    "name":"Back Attack",          "desc":"Add 3+ Back exercises",                          "xp":50,  "check": lambda log,_: sum(1 for e in log if e["muscle"]=="Back") >= 3},
    {"id":"leg_day_ch",  "name":"Leg Day Legend",       "desc":"Complete a leg workout (3+ exercises)",          "xp":60,  "check": lambda log,_: sum(1 for e in log if e["muscle"]=="Legs") >= 3},
    {"id":"core_focus",  "name":"Core Commitment",      "desc":"Log 3+ core exercises",                          "xp":40,  "check": lambda log,_: sum(1 for e in log if e["muscle"]=="Core") >= 3},
    {"id":"fullbody_ch", "name":"Full Body Assault",    "desc":"Train 5+ different muscle groups",               "xp":80,  "check": lambda log,_: len(set(e["muscle"] for e in log)) >= 5},
    {"id":"sets20_ch",   "name":"Set Grinder",          "desc":"Complete 20+ sets in one session",               "xp":60,  "check": lambda log,_: sum(e["sets"] for e in log) >= 20},
    {"id":"sets30_ch",   "name":"Volume Veteran",       "desc":"Complete 30+ sets in one session",               "xp":100, "check": lambda log,_: sum(e["sets"] for e in log) >= 30},
    {"id":"ex6_ch",      "name":"Exercise Explorer",    "desc":"Log 6+ different exercises",                     "xp":50,  "check": lambda log,_: len(log) >= 6},
    {"id":"ex8_ch",      "name":"Workout Machine",      "desc":"Log 8+ different exercises",                     "xp":75,  "check": lambda log,_: len(log) >= 8},
    {"id":"pushpull_ch", "name":"Push & Pull Balance",  "desc":"Train both Chest/Shoulders and Back",            "xp":65,  "check": lambda log,_: any(e["muscle"] in ["Chest","Shoulders"] for e in log) and any(e["muscle"]=="Back" for e in log)},
    {"id":"bodyweight_ch","name":"No Equipment Needed", "desc":"Only bodyweight exercises today",                "xp":55,  "check": lambda log,_: len(log)>0 and all(e["eq"]=="bodyweight" for e in log)},
    {"id":"recovery_ch", "name":"Recovery Day",         "desc":"Do a full recovery session (3+ stretches)",      "xp":30,  "check": lambda log,_: sum(1 for e in log if e["muscle"]=="Recovery") >= 3},
    {"id":"glute_day",   "name":"Glute Gains",          "desc":"Log 3+ Glute exercises",                         "xp":45,  "check": lambda log,_: sum(1 for e in log if e["muscle"]=="Glutes") >= 3},
    {"id":"cardio_ch",   "name":"Cardio Crusher",       "desc":"Include a cardio exercise",                      "xp":40,  "check": lambda log,_: any(e["muscle"]=="Cardio" for e in log)},
    {"id":"compound_ch", "name":"Compound King",        "desc":"Log 3+ compound lifts (Deadlift, Squat, Press)", "xp":70,  "check": lambda log,_: sum(1 for e in log if any(kw in e["name"] for kw in ["Deadlift","Squat","Press","Row","Pull-Up","Chin-Up"])) >= 3},
]

MOTIVATIONS = [
    "Every rep counts. Every drop of sweat matters.",
    "The body achieves what the mind believes.",
    "Push yourself — no one else will do it for you.",
    "Strength comes from overcoming what you thought you couldn't.",
    "You didn't come this far to only come this far.",
    "The pain you feel today is the strength you feel tomorrow.",
    "Your only competition is who you were yesterday.",
    "Fall down seven times. Get up eight.",
    "Discipline is choosing between what you want now and what you want most.",
    "Champions keep playing until they get it right.",
    "The last three or four reps is what makes the muscle grow.",
    "Success is usually found in those who don't believe in failure.",
    "Wake up. Work out. Be a better person today.",
    "No pain, no gain. Shut up and train.",
    "Train insane or remain the same.",
    "Your body can stand almost anything. It's your mind you have to convince.",
    "Results happen over time, not overnight. Work hard, stay consistent.",
    "Don't stop when you're tired. Stop when you're done.",
]

# ─────────────────────────────────────────────────────────────
# MUSCLE SVG DIAGRAM
# ─────────────────────────────────────────────────────────────
def get_muscle_svg(muscle_group):
    """Generate front+back body SVG with highlighted muscle regions."""
    bg   = "#111117"
    base = "#252530"
    hi   = "#f97316"
    sec  = "#3b82f6"
    skin = "#1e1e26"

    # What to highlight for each group
    A = {
        "Chest":    {"chest_f":hi, "front_delt":sec, "tri_f":sec},
        "Back":     {"lats_b":hi, "trap_b":hi, "bi_b":sec, "lower_b":hi},
        "Shoulders":{"front_delt":hi, "side_delt":hi, "rear_delt":hi, "trap_b":sec},
        "Biceps":   {"bi_f":hi, "fore_f":sec, "front_delt":sec},
        "Triceps":  {"tri_b":hi, "fore_b":sec},
        "Legs":     {"quad_f":hi, "ham_b":hi, "calf_f":sec, "calf_b":sec},
        "Core":     {"abs_f":hi, "obl_f":hi},
        "Glutes":   {"glute_b":hi, "ham_b":sec},
        "Calves":   {"calf_f":hi, "calf_b":hi},
        "Full Body":{"chest_f":hi, "lats_b":hi, "quad_f":hi, "shoulder_f":hi, "abs_f":sec},
        "Cardio":   {"quad_f":hi, "calf_f":hi, "calf_b":hi, "ham_b":sec, "abs_f":sec},
        "Recovery": {"abs_f":sec, "lats_b":sec, "lower_b":sec, "hip_f":sec},
    }
    act = A.get(muscle_group, {})
    def c(key): return act.get(key, base)

    front_svg = f"""
<svg viewBox="0 0 130 290" xmlns="http://www.w3.org/2000/svg">
  <rect width="130" height="290" fill="{bg}" rx="10"/>
  <!-- Head -->
  <ellipse cx="65" cy="18" rx="15" ry="18" fill="{skin}" stroke="#3a3a44" stroke-width="0.8"/>
  <!-- Neck -->
  <rect x="59" y="34" width="12" height="12" rx="2" fill="{skin}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Shoulder/Delt -->
  <ellipse cx="38" cy="56" rx="13" ry="9" fill="{c('front_delt') if c('front_delt')!=base else c('side_delt')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Shoulder/Delt -->
  <ellipse cx="92" cy="56" rx="13" ry="9" fill="{c('front_delt') if c('front_delt')!=base else c('side_delt')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Chest upper -->
  <path d="M48,47 Q65,43 82,47 L84,82 Q65,87 46,82 Z" fill="{c('chest_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Abs / Core -->
  <path d="M46,82 Q65,87 84,82 L82,140 Q65,145 48,140 Z" fill="{c('abs_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Obliques -->
  <path d="M36,80 Q46,85 46,140 L42,138 Q34,88 36,80Z" fill="{c('obl_f')}" stroke="#3a3a44" stroke-width="0.5" opacity="0.8"/>
  <path d="M94,80 Q84,85 84,140 L88,138 Q96,88 94,80Z" fill="{c('obl_f')}" stroke="#3a3a44" stroke-width="0.5" opacity="0.8"/>
  <!-- Left Bicep -->
  <path d="M26,54 Q18,74 20,100 L30,98 Q29,75 38,55Z" fill="{c('bi_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Bicep -->
  <path d="M104,54 Q112,74 110,100 L100,98 Q101,75 92,55Z" fill="{c('bi_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Forearm -->
  <path d="M20,100 Q14,122 17,148 L26,146 Q25,123 30,98Z" fill="{c('fore_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Forearm -->
  <path d="M110,100 Q116,122 113,148 L104,146 Q105,123 100,98Z" fill="{c('fore_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Hips -->
  <path d="M48,140 Q65,145 82,140 L83,162 Q65,167 47,162Z" fill="{c('hip_f') if c('hip_f')!=base else skin}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Quad -->
  <path d="M47,162 Q38,192 38,220 L52,220 Q50,193 57,162Z" fill="{c('quad_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Quad -->
  <path d="M83,162 Q92,192 92,220 L78,220 Q80,193 73,162Z" fill="{c('quad_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Calf front -->
  <path d="M38,220 Q32,246 35,268 L50,268 Q52,246 52,220Z" fill="{c('calf_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Calf front -->
  <path d="M92,220 Q98,246 95,268 L80,268 Q78,246 78,220Z" fill="{c('calf_f')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Feet -->
  <ellipse cx="42" cy="271" rx="9" ry="5" fill="{skin}" stroke="#3a3a44" stroke-width="0.5"/>
  <ellipse cx="88" cy="271" rx="9" ry="5" fill="{skin}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Label -->
  <text x="65" y="285" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#6b6b7e" font-weight="bold">FRONT</text>
</svg>"""

    back_svg = f"""
<svg viewBox="0 0 130 290" xmlns="http://www.w3.org/2000/svg">
  <rect width="130" height="290" fill="{bg}" rx="10"/>
  <!-- Head -->
  <ellipse cx="65" cy="18" rx="15" ry="18" fill="{skin}" stroke="#3a3a44" stroke-width="0.8"/>
  <!-- Neck -->
  <rect x="59" y="34" width="12" height="12" rx="2" fill="{skin}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Traps -->
  <path d="M48,47 Q65,43 82,47 L78,68 Q65,63 52,68Z" fill="{c('trap_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Rear Delts -->
  <ellipse cx="38" cy="56" rx="13" ry="9" fill="{c('rear_delt')}" stroke="#3a3a44" stroke-width="0.5"/>
  <ellipse cx="92" cy="56" rx="13" ry="9" fill="{c('rear_delt')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Lats upper back -->
  <path d="M46,65 Q65,62 84,65 L86,108 Q65,115 44,108Z" fill="{c('lats_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Lower back -->
  <path d="M44,108 Q65,115 86,108 L84,148 Q65,153 46,148Z" fill="{c('lower_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Tricep -->
  <path d="M26,54 Q18,74 20,100 L30,98 Q29,75 38,55Z" fill="{c('tri_b') if c('tri_b')!=base else c('tri_f') if c('tri_f')!=base else base}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Tricep -->
  <path d="M104,54 Q112,74 110,100 L100,98 Q101,75 92,55Z" fill="{c('tri_b') if c('tri_b')!=base else c('tri_f') if c('tri_f')!=base else base}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Forearm back -->
  <path d="M20,100 Q14,122 17,148 L26,146 Q25,123 30,98Z" fill="{c('fore_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Forearm back -->
  <path d="M110,100 Q116,122 113,148 L104,146 Q105,123 100,98Z" fill="{c('fore_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Glutes -->
  <path d="M44,148 Q65,153 86,148 L84,182 Q65,188 46,182Z" fill="{c('glute_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Hamstring -->
  <path d="M46,182 Q38,210 38,238 L52,238 Q50,211 58,182Z" fill="{c('ham_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Hamstring -->
  <path d="M84,182 Q92,210 92,238 L78,238 Q80,211 72,182Z" fill="{c('ham_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Left Calf back -->
  <path d="M38,238 Q32,258 35,272 L50,272 Q52,258 52,238Z" fill="{c('calf_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Right Calf back -->
  <path d="M92,238 Q98,258 95,272 L80,272 Q78,258 78,238Z" fill="{c('calf_b')}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Feet -->
  <ellipse cx="42" cy="275" rx="9" ry="5" fill="{skin}" stroke="#3a3a44" stroke-width="0.5"/>
  <ellipse cx="88" cy="275" rx="9" ry="5" fill="{skin}" stroke="#3a3a44" stroke-width="0.5"/>
  <!-- Label -->
  <text x="65" y="285" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#6b6b7e" font-weight="bold">BACK</text>
</svg>"""

    return front_svg, back_svg

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def get_level_info(xp):
    current = LEVELS[0]
    next_lv = LEVELS[1]
    idx = 0
    for i, (req, name, color, icon) in enumerate(LEVELS):
        if xp >= req:
            current = LEVELS[i]
            idx = i
            next_lv = LEVELS[min(i+1, len(LEVELS)-1)]
    cur_req  = current[0]
    next_req = next_lv[0]
    pct = min(1.0, (xp - cur_req) / max(next_req - cur_req, 1))
    return current[1], current[2], current[3], pct, next_req, idx

def calculate_xp_multiplier(streak, exercise_count, hour):
    """Enhanced XP multiplier calculation."""
    mult = 1.0
    # Streak bonus (up to +0.5x)
    mult += min(streak * 0.03, 0.5)
    # Volume bonus
    if exercise_count >= 8: mult += 0.3
    elif exercise_count >= 5: mult += 0.15
    elif exercise_count >= 3: mult += 0.05
    # Time bonus
    if hour < 7:   mult += 0.2   # Very early bird
    elif hour < 8: mult += 0.15  # Early bird
    elif hour >= 22: mult += 0.15  # Very late night
    elif hour >= 21: mult += 0.1   # Night owl
    return round(min(mult, 3.0), 2)  # Cap at 3x

def earn_badge(user_id, badge_id, badges_earned):
    if badge_id not in badges_earned:
        db_earn_badge(user_id, badge_id)
        badge = next((b for b in BADGES if b["id"] == badge_id), None)
        if badge:
            st.toast(f"🏅 Badge: **{badge['name']}** — {badge['desc']}!", icon="🏅")
        badges_earned.append(badge_id)

def check_badges(user_id, data, badges_earned):
    xp    = data["total_xp"]
    streak = data["streak"]
    workouts = data["workouts"]
    sets_total = data["total_sets"]
    level_idx  = data["level"]
    unique_ex  = data["unique_exercises"]
    muscles_count = data["muscles_trained_count"]
    prs_count = data["prs_count"]
    challenges_done = data["challenges_done"]

    checks = [
        ("first",       workouts >= 1),
        ("streak3",     streak >= 3),
        ("streak7",     streak >= 7),
        ("streak14",    streak >= 14),
        ("streak30",    streak >= 30),
        ("streak60",    streak >= 60),
        ("streak100",   streak >= 100),
        ("w5",          workouts >= 5),
        ("w10",         workouts >= 10),
        ("w25",         workouts >= 25),
        ("w50",         workouts >= 50),
        ("w100",        workouts >= 100),
        ("w200",        workouts >= 200),
        ("sets50",      sets_total >= 50),
        ("sets100",     sets_total >= 100),
        ("sets500",     sets_total >= 500),
        ("sets1000",    sets_total >= 1000),
        ("xp500",       xp >= 500),
        ("xp5000",      xp >= 5000),
        ("xp25000",     xp >= 25000),
        ("level_iron",  level_idx >= 2),
        ("level_gold",  level_idx >= 5),
        ("level_plat",  level_idx >= 6),
        ("muscles6",    muscles_count >= 6),
        ("muscles10",   muscles_count >= 10),
        ("variety20",   unique_ex >= 20),
        ("variety50",   unique_ex >= 50),
        ("pr",          prs_count >= 1),
        ("pr10",        prs_count >= 10),
        ("challenge5",  challenges_done >= 5),
        ("challenge20", challenges_done >= 20),
    ]
    for bid, cond in checks:
        if cond:
            earn_badge(user_id, bid, badges_earned)

def get_today_challenges(user_id, today_str):
    """Get or generate 3 daily challenges for today."""
    existing = db_get_challenges(user_id, today_str)
    if len(existing) < 3:
        # Generate challenges based on date seed for consistency
        seed = int(hashlib.md5((today_str + str(user_id)).encode()).hexdigest()[:8], 16)
        rng  = random.Random(seed)
        chosen = rng.sample(DAILY_CHALLENGES_POOL, 3)
        for ch in chosen:
            if ch["id"] not in existing:
                db_set_challenge(user_id, today_str, ch["id"], False)
        existing = db_get_challenges(user_id, today_str)
    return existing

def plotly_dark(fig, height=300):
    fig.update_layout(
        paper_bgcolor="#16161d", plot_bgcolor="#16161d",
        font_color="#9898ba", margin=dict(l=20, r=20, t=36, b=20),
        showlegend=False, height=height,
    )
    fig.update_xaxes(gridcolor="#252530", tickfont_color="#6b6b7e", linecolor="#252530", zeroline=False)
    fig.update_yaxes(gridcolor="#252530", tickfont_color="#6b6b7e", linecolor="#252530", zeroline=False)
    return fig

# ─────────────────────────────────────────────────────────────
# SESSION INIT
# ─────────────────────────────────────────────────────────────
def init_session():
    if "user"       not in st.session_state: st.session_state.user       = None
    if "today_log"  not in st.session_state: st.session_state.today_log  = []
    if "page"       not in st.session_state: st.session_state.page       = "🏠 Dashboard"
    if "timer_end"  not in st.session_state: st.session_state.timer_end  = None
    if "timer_dur"  not in st.session_state: st.session_state.timer_dur  = 60
    if "motivation" not in st.session_state: st.session_state.motivation = random.choice(MOTIVATIONS)
    if "workout_start" not in st.session_state: st.session_state.workout_start = None

init_session()

# ─────────────────────────────────────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────────────────────────────────────
if st.session_state.user is None:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px 30px;">
        <div style="font-family:'Barlow Condensed',sans-serif; font-size:64px; font-weight:900;
                    letter-spacing:8px; color:#f97316; text-shadow: 0 0 40px #f9731650;">
            IRONFORGE
        </div>
        <div style="color:#6b6b7e; font-size:16px; margin-top:8px; letter-spacing:3px;">
            ADVANCED GYM TRACKER 3.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, mc, _ = st.columns([1, 1, 1])
    with mc:
        st.markdown("### Enter your name to continue")
        username = st.text_input("Your name", placeholder="e.g. AthleteJohn")
        if st.button("⚡ ENTER THE FORGE", use_container_width=True):
            if username.strip():
                user = db_get_user(username.strip()) or db_create_user(username.strip())
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Please enter a username.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# LOAD USER DATA FROM DB
# ─────────────────────────────────────────────────────────────
user = st.session_state.user
user_id = user["id"]

# Refresh user from DB each rerun
user = db_get_user(user["username"])
st.session_state.user = user

workouts_list   = db_get_workouts(user_id)
badges_earned   = db_get_badges(user_id)
muscle_stats    = db_get_muscle_stats(user_id)
prs             = db_get_prs(user_id)
bw_log          = db_get_bodyweight_log(user_id)
today_str       = str(datetime.date.today())
challenges_today = get_today_challenges(user_id, today_str)

# Aggregate stats
total_workouts = len(workouts_list)
total_sets     = sum(w["total_sets"] for w in workouts_list)
total_xp       = user["total_xp"]
streak         = user["streak"]
unique_ex_count = db_count_unique_exercises(user_id)
muscles_count   = len(muscle_stats)
challenges_done_count = sum(1 for c in challenges_today.values() if c["completed"])
challenges_done_total = 0
with get_db() as conn:
    cur = _exec(conn, "SELECT COUNT(*) as cnt FROM daily_challenges WHERE user_id=%s AND completed=1", (user_id,))
    challenges_done_total = cur.fetchone()["cnt"]

user_stats = {
    "total_xp": total_xp,
    "streak": streak,
    "workouts": total_workouts,
    "total_sets": total_sets,
    "level": user["level"],
    "unique_exercises": unique_ex_count,
    "muscles_trained_count": muscles_count,
    "prs_count": len(prs),
    "challenges_done": challenges_done_total,
}
check_badges(user_id, user_stats, badges_earned)

# Update level
lv_name, lv_color, lv_icon, lv_pct, lv_next, lv_idx = get_level_info(total_xp)
if user["level"] != lv_idx:
    db_update_user(user_id, level=lv_idx)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="font-family:'Barlow Condensed',sans-serif; font-size:30px; font-weight:900;
                letter-spacing:5px; color:#f97316; margin-bottom:2px;">IRONFORGE</div>
    <div style="color:#6b6b7e; font-size:11px; letter-spacing:3px; margin-bottom:14px;">ADVANCED GYM TRACKER 3.0</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
        <div style="font-size:28px;">{lv_icon}</div>
        <div>
            <div style="color:{lv_color}; font-family:'Barlow Condensed'; font-weight:800; font-size:16px; letter-spacing:2px;">{lv_name}</div>
            <div style="color:#6b6b7e; font-size:12px;">{total_xp:,} XP · next {lv_next:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(lv_pct)
    st.markdown("---")

    pages = [
        "🏠 Dashboard",
        "💪 Exercise Library",
        "📋 Today's Log",
        "🎯 Daily Challenges",
        "📊 Statistics",
        "📅 History",
        "⚖️ Body Weight",
        "🏅 Achievements",
        "⏱️ Rest Timer",
        "🔄 Workout Plans",
        "⚙️ Settings",
    ]
    selected = st.radio("", pages, label_visibility="collapsed",
                        index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
    st.session_state.page = selected

    st.markdown("---")
    st.markdown(f"""
    <div style="padding:4px 0;">
        <div style="color:#f0f0f5; font-size:16px; font-weight:700;">👋 {user['username']}</div>
        <div style="color:#f97316; font-size:14px; margin-top:4px;">🔥 {streak}-day streak</div>
        <div style="color:#6b6b7e; font-size:12px; margin-top:3px;">{total_workouts} workouts · {total_sets} total sets</div>
        <div style="color:#6b6b7e; font-size:12px;">{len(badges_earned)} / {len(BADGES)} badges</div>
    </div>
    """, unsafe_allow_html=True)

    # Today log indicator
    if st.session_state.today_log:
        st.markdown(f"""
        <div style="background:#f9731615; border:1px solid #f97316; border-radius:8px; padding:8px 12px; margin-top:10px; text-align:center;">
            <div style="color:#f97316; font-weight:700; font-size:13px;">🏋️ {len(st.session_state.today_log)} exercises queued</div>
        </div>
        """, unsafe_allow_html=True)

page = selected

# ─────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown(f'<div class="if-title">Welcome back, {user["username"]} 👋</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b6b7e; margin-bottom:24px; font-size:14px;">{datetime.datetime.now().strftime("%A, %B %d %Y")} &nbsp;·&nbsp; <em>{st.session_state.motivation}</em></div>', unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.metric("🔥 Streak",   f"{streak}d")
    with c2: st.metric("💪 Workouts", total_workouts)
    with c3: st.metric("⚙️ Sets",     total_sets)
    with c4: st.metric("⚡ XP",       f"{total_xp:,}")
    with c5: st.metric("🏅 Badges",   len(badges_earned))
    with c6:
        mult = calculate_xp_multiplier(streak, 0, datetime.datetime.now().hour)
        st.metric("✨ Multiplier", f"{mult}×")

    st.markdown("---")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("#### 🚀 Quick Actions")
        qa1, qa2 = st.columns(2)
        with qa1:
            if st.button("💪 Start Training", use_container_width=True):
                st.session_state.page = "💪 Exercise Library"; st.rerun()
            if st.button("🔄 Load a Plan", use_container_width=True):
                st.session_state.page = "🔄 Workout Plans"; st.rerun()
        with qa2:
            if st.button("📋 Today's Log", use_container_width=True):
                st.session_state.page = "📋 Today's Log"; st.rerun()
            if st.button("🎯 Challenges", use_container_width=True):
                st.session_state.page = "🎯 Daily Challenges"; st.rerun()

        st.markdown("#### 🎯 Today's Challenges")
        for ch_id, ch_data in challenges_today.items():
            ch_def = next((c for c in DAILY_CHALLENGES_POOL if c["id"] == ch_id), None)
            if not ch_def: continue
            done = ch_data["completed"]
            card_class = "if-card challenge-done" if done else "if-card challenge-active"
            st.markdown(f"""
            <div class="{card_class}" style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; color:{'#22c55e' if done else '#f0f0f5'};">{'✅ ' if done else '🎯 '}{ch_def['name']}</span>
                    <span style="color:#f97316; font-family:'Barlow Condensed'; font-weight:800; font-size:14px;">+{ch_def['xp']} XP</span>
                </div>
                <div style="color:#6b6b7e; font-size:12px; margin-top:3px;">{ch_def['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 💬 Motivation")
        st.info(f'*"{st.session_state.motivation}"*')
        if st.button("New Quote", key="new_quote"):
            st.session_state.motivation = random.choice(MOTIVATIONS); st.rerun()

    with col_b:
        st.markdown("#### 📅 Recent Workouts")
        if workouts_list:
            for entry in workouts_list[:5]:
                muscles_list = json.loads(entry.get("muscles_trained") or "[]")
                muscles_str  = ", ".join(muscles_list[:3])
                note_html = f'<span style="color:#6b6b7e;"> · 📝 {entry["note"]}</span>' if entry.get("note") else ""
                mult_str  = f'<span style="color:#fbbf24;font-size:11px;"> ×{entry["xp_multiplier"]:.1f}</span>' if entry.get("xp_multiplier", 1.0) > 1.0 else ""
                st.markdown(f"""
                <div class="if-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#f97316; font-weight:700;">{entry['date']}</span>
                        <span style="color:#22c55e; font-weight:700;">+{entry['total_xp']} XP{mult_str}</span>
                    </div>
                    <div style="color:#9898ba; margin-top:4px; font-size:13px;">{entry['total_sets']} sets · {entry['exercise_count']} exercises · {muscles_str}{note_html}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="if-card" style="color:#6b6b7e; text-align:center; padding:32px;">No workouts yet — go train! 💪</div>', unsafe_allow_html=True)

        # Muscle balance
        if muscle_stats:
            st.markdown("#### 🌐 Muscle Balance")
            total_ms = sum(muscle_stats.values())
            top_muscles = sorted(muscle_stats.items(), key=lambda x: x[1], reverse=True)[:6]
            for muscle, sets_count in top_muscles:
                pct = sets_count / total_ms if total_ms else 0
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
                        <span style="font-size:13px;">{MUSCLE_ICONS.get(muscle,'💪')} {muscle}</span>
                        <span style="color:#f97316; font-size:12px; font-weight:700;">{sets_count} sets</span>
                    </div>
                    <div style="background:#1a1a22; border-radius:4px; height:6px;">
                        <div style="background:linear-gradient(90deg,#f97316,#fbbf24); border-radius:4px; height:6px; width:{pct*100:.0f}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Today log preview
    if st.session_state.today_log:
        st.markdown("---")
        col_prev, col_btn = st.columns([3, 1])
        with col_prev:
            ex_names = " · ".join(e["name"] for e in st.session_state.today_log[:7])
            st.markdown(f'<div class="if-card if-card-highlight"><strong style="color:#f97316;">{len(st.session_state.today_log)} exercises queued:</strong> {ex_names}</div>', unsafe_allow_html=True)
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Finish Workout →", use_container_width=True):
                st.session_state.page = "📋 Today's Log"; st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: EXERCISE LIBRARY
# ─────────────────────────────────────────────────────────────
elif page == "💪 Exercise Library":
    st.markdown('<div class="if-title">Exercise Library</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b6b7e; margin-bottom:20px;">{len(EXERCISES)} exercises · 13 categories · YouTube tutorials · Muscle diagrams</div>', unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3, fc4 = st.columns([2, 2, 2, 3])
    with fc1:
        muscle_filter = st.selectbox("Muscle", MUSCLES, label_visibility="collapsed")
    with fc2:
        eq_filter = st.selectbox("Equipment", EQUIPMENT, label_visibility="collapsed")
    with fc3:
        diff_filter = st.selectbox("Difficulty", DIFFICULTIES, label_visibility="collapsed")
    with fc4:
        search = st.text_input("Search", placeholder="Search exercises…", label_visibility="collapsed")

    filtered = [e for e in EXERCISES
                if (muscle_filter == "All" or e["muscle"] == muscle_filter)
                and (eq_filter == "All" or e["eq"] == eq_filter)
                and (diff_filter == "All" or e["diff"] == diff_filter)
                and (search.lower() in e["name"].lower() or not search)]

    st.markdown(f'<div style="color:#6b6b7e; margin-bottom:16px;">{len(filtered)} exercises found</div>', unsafe_allow_html=True)

    if not filtered:
        st.warning("No exercises match your filters.")
    else:
        # Show muscle diagram if single muscle selected
        if muscle_filter != "All":
            front_svg, back_svg = get_muscle_svg(muscle_filter)
            diag_c1, diag_c2, diag_c3 = st.columns([1, 1, 3])
            with diag_c1:
                st.markdown(front_svg, unsafe_allow_html=True)
            with diag_c2:
                st.markdown(back_svg, unsafe_allow_html=True)
            with diag_c3:
                st.markdown(f"""
                <div style="padding:12px 0;">
                    <div style="font-family:'Barlow Condensed';font-size:24px;font-weight:900;color:{next((l[2] for l in LEVELS if l[1]!=''), '#f97316')};">
                        {MUSCLE_ICONS.get(muscle_filter,'💪')} {muscle_filter.upper()}
                    </div>
                    <div style="color:#6b6b7e;margin-top:8px;font-size:13px;max-width:400px;">
                        <span style="background:#f9731615;color:#f97316;padding:2px 8px;border-radius:4px;margin-right:6px;">■ Primary</span>
                        <span style="background:#3b82f615;color:#3b82f6;padding:2px 8px;border-radius:4px;">■ Secondary</span>
                    </div>
                    <div style="color:#9898ba;margin-top:12px;font-size:14px;">
                        {len(filtered)} exercises targeting {muscle_filter} · {sum(1 for e in filtered if e['eq']=='gym')} gym · {sum(1 for e in filtered if e['eq']=='bodyweight')} bodyweight
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")

        for ex in filtered:
            eq_tag   = '<span class="if-tag tag-gym">🔧 Gym</span>' if ex["eq"]=="gym" else '<span class="if-tag tag-body">🤸 Bodyweight</span>'
            diff_col = {"Beginner":"green","Intermediate":"orange","Advanced":"red"}.get(ex["diff"],"orange")
            diff_tag = f'<span class="if-tag tag-{diff_col}">{ex["diff"]}</span>'
            xp_tag   = f'<span class="if-tag tag-yellow">+{ex["xp"]} XP</span>'
            msc_tag  = f'<span class="if-tag tag-orange">{MUSCLE_ICONS.get(ex["muscle"],"💪")} {ex["muscle"]}</span>'
            pr_data  = prs.get(str(ex["id"]), {})

            with st.expander(f'{MUSCLE_ICONS.get(ex["muscle"],"💪")}  **{ex["name"]}**  —  {ex["sets"]}×{ex["reps"]}  ·  {ex["rest"]}s rest'):
                ex_c1, ex_c2 = st.columns([3, 1])
                with ex_c1:
                    st.markdown(f"{msc_tag} {eq_tag} {diff_tag} {xp_tag}", unsafe_allow_html=True)

                    if ex.get("secondary"):
                        sec_str = " · ".join(ex["secondary"])
                        st.markdown(f'<div style="color:#6b6b7e;font-size:12px;margin-top:4px;">Also works: {sec_str}</div>', unsafe_allow_html=True)

                    st.markdown(f"**Sets:** {ex['sets']}  &nbsp;|&nbsp;  **Reps:** {ex['reps']}  &nbsp;|&nbsp;  **Rest:** {ex['rest']}s")

                    st.markdown("**📋 Form Tips:**")
                    for tip in ex["tips"]:
                        st.markdown(f'<div style="color:#9898ba; font-size:13px; margin:3px 0;">→ {tip}</div>', unsafe_allow_html=True)

                    # YouTube link
                    st.markdown(f"""
                    <a href="{ex['youtube']}" target="_blank" style="
                        display:inline-flex; align-items:center; gap:6px;
                        background:#ef444415; color:#ef4444; border:1px solid #ef444430;
                        padding:6px 14px; border-radius:8px; font-size:13px;
                        font-family:'Barlow Condensed'; font-weight:700; letter-spacing:1px;
                        text-decoration:none; margin-top:10px;">
                        ▶ WATCH TUTORIAL ON YOUTUBE
                    </a>
                    """, unsafe_allow_html=True)

                    if pr_data:
                        pr_parts = []
                        if pr_data.get("weight"): pr_parts.append(f"🥇 **{pr_data['weight']} kg**")
                        if pr_data.get("reps"):   pr_parts.append(f"🔢 **{pr_data['reps']} reps**")
                        if pr_data.get("one_rep_max"): pr_parts.append(f"📐 **1RM: {pr_data['one_rep_max']:.1f} kg**")
                        st.markdown(f'<div style="margin-top:8px;padding:8px 12px;background:#f9731610;border:1px solid #f9731640;border-radius:8px;font-size:13px;">PR: {" · ".join(pr_parts)}</div>', unsafe_allow_html=True)

                with ex_c2:
                    # Muscle mini-diagram
                    front_svg, back_svg = get_muscle_svg(ex["muscle"])
                    diag_col1, diag_col2 = st.columns(2)
                    with diag_col1:
                        st.markdown(front_svg, unsafe_allow_html=True)
                    with diag_col2:
                        st.markdown(back_svg, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("➕ Add to Log", key=f"add_{ex['id']}", use_container_width=True):
                        st.session_state.today_log.append(ex.copy())
                        if not st.session_state.workout_start:
                            st.session_state.workout_start = time.time()
                        st.toast(f"✓ {ex['name']} added! (+{ex['xp']} XP)", icon="💪")

                    if st.button("⏱ Start Timer", key=f"timer_{ex['id']}", use_container_width=True):
                        st.session_state.timer_end = time.time() + ex["rest"]
                        st.session_state.timer_dur = ex["rest"]
                        st.session_state.page = "⏱️ Rest Timer"; st.rerun()

                    st.markdown("**💾 Save PR:**")
                    pr_w = st.number_input("Weight kg", min_value=0.0, step=0.5,
                                           value=float(pr_data.get("weight",0) or 0),
                                           key=f"pr_w_{ex['id']}", label_visibility="collapsed")
                    pr_r = st.number_input("Reps", min_value=0, step=1,
                                           value=int(pr_data.get("reps",0) or 0),
                                           key=f"pr_r_{ex['id']}", label_visibility="collapsed")
                    if st.button("🥇 Save PR", key=f"pr_s_{ex['id']}", use_container_width=True):
                        db_save_pr(user_id, ex["id"], ex["name"], pr_w, pr_r)
                        earn_badge(user_id, "pr", badges_earned)
                        new_prs = db_get_prs(user_id)
                        if len(new_prs) >= 10:
                            earn_badge(user_id, "pr10", badges_earned)
                        st.success(f"PR saved! 🥇 (1RM: {pr_w * (1 + pr_r/30):.1f} kg)")
                        st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: TODAY'S LOG
# ─────────────────────────────────────────────────────────────
elif page == "📋 Today's Log":
    st.markdown('<div class="if-title">Today\'s Log</div>', unsafe_allow_html=True)
    today_log = st.session_state.today_log

    if not today_log:
        st.markdown("""
        <div class="if-card" style="text-align:center; padding:60px; color:#6b6b7e; font-size:18px;">
            No exercises queued.<br>
            <span style="font-size:14px;">Go to Exercise Library or Workout Plans to add exercises! 🏋️</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        sets_total = sum(e["sets"] for e in today_log)
        xp_base    = sum(e["xp"]   for e in today_log)
        bonus_xp   = 50
        hour       = datetime.datetime.now().hour
        mult       = calculate_xp_multiplier(streak, len(today_log), hour)
        xp_with_mult = int((xp_base + bonus_xp) * mult)
        duration   = int((time.time() - st.session_state.workout_start) / 60) if st.session_state.workout_start else 0
        muscles    = list(set(e["muscle"] for e in today_log))

        # XP Breakdown
        st.markdown(f"""
        <div class="if-card if-card-highlight" style="margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; align-items:center;">
                <div>
                    <div style="font-family:'Barlow Condensed';font-size:22px;font-weight:900;color:#f97316;">{len(today_log)} exercises · {sets_total} sets</div>
                    <div style="color:#6b6b7e;font-size:13px;">Muscles: {", ".join(muscles)}</div>
                    {f'<div style="color:#6b6b7e;font-size:13px;">Duration: ~{duration} min</div>' if duration > 0 else ''}
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'Barlow Condensed';font-size:32px;font-weight:900;color:#22c55e;">+{xp_with_mult} XP</div>
                    <div style="color:#6b6b7e;font-size:12px;">{xp_base} base + {bonus_xp} session bonus × {mult:.1f}x</div>
                    <span class="multiplier-badge" style="font-size:11px;">×{mult:.1f} MULTIPLIER</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        note = st.text_input("📝 Workout Note", placeholder="e.g. Felt strong today, PR on bench…")

        for i, ex in enumerate(today_log):
            lc1, lc2, lc3 = st.columns([5, 2, 1])
            with lc1:
                eq_tag  = '🔧' if ex["eq"]=="gym" else '🤸'
                diff_tag = {"Beginner":"🟢","Intermediate":"🟠","Advanced":"🔴"}.get(ex["diff"],"🟡")
                st.markdown(f"""
                <div class="if-card" style="margin-bottom:6px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:18px;">{MUSCLE_ICONS.get(ex['muscle'],'💪')}</span>
                        <div>
                            <span style="font-weight:700; font-size:15px;">{ex['name']}</span>
                            <span style="color:#6b6b7e; font-size:12px;"> · {ex['muscle']} · {ex['sets']}×{ex['reps']} {eq_tag}{diff_tag}</span>
                            <span style="color:#f97316; font-size:12px; margin-left:6px;">+{ex['xp']} XP</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with lc2:
                if st.button(f"⏱ {ex['rest']}s", key=f"lt_{i}", use_container_width=True):
                    st.session_state.timer_end = time.time() + ex["rest"]
                    st.session_state.timer_dur = ex["rest"]
                    st.session_state.page = "⏱️ Rest Timer"; st.rerun()
            with lc3:
                if st.button("✕", key=f"del_{i}", use_container_width=True):
                    st.session_state.today_log.pop(i); st.rerun()

        # Challenge auto-check
        st.markdown("---")
        updated_challenges = False
        for ch_id, ch_data in challenges_today.items():
            if not ch_data["completed"]:
                ch_def = next((c for c in DAILY_CHALLENGES_POOL if c["id"] == ch_id), None)
                if ch_def and ch_def["check"](today_log, user_stats):
                    db_set_challenge(user_id, today_str, ch_id, True)
                    st.toast(f"🎯 Challenge complete: **{ch_def['name']}** +{ch_def['xp']} bonus XP!", icon="🎯")
                    updated_challenges = True
        if updated_challenges:
            challenges_today = get_today_challenges(user_id, today_str)

        # Action buttons
        fa, fb, fc = st.columns([3, 2, 2])
        with fa:
            if st.button("✅ Finish & Save Workout", use_container_width=True):
                # Check challenges completed today
                ch_bonus = sum(
                    next((c["xp"] for c in DAILY_CHALLENGES_POOL if c["id"] == ch_id), 0)
                    for ch_id, ch_data in challenges_today.items()
                    if ch_data["completed"]
                )
                final_xp = xp_with_mult + ch_bonus

                # Save workout
                wid = db_save_workout(
                    user_id, today_str, sets_total, final_xp, xp_base, bonus_xp,
                    mult, note, duration, muscles, len(today_log), today_log
                )

                # Update user stats
                new_xp = total_xp + final_xp
                new_streak = streak
                yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                if user["last_workout_date"] == yesterday:
                    new_streak = streak + 1
                elif user["last_workout_date"] != today_str:
                    new_streak = 1
                new_longest = max(user.get("longest_streak", 0), new_streak)

                # Update level
                new_level = 0
                for i, (req, name, color, icon) in enumerate(LEVELS):
                    if new_xp >= req: new_level = i

                db_update_user(user_id,
                    total_xp=new_xp, streak=new_streak, longest_streak=new_longest,
                    level=new_level, last_workout_date=today_str
                )

                # Update muscle stats
                for ex in today_log:
                    db_update_muscle_stats(user_id, ex["muscle"], ex["sets"])
                    db_track_unique_exercise(user_id, ex["id"])

                # XP log
                db_log_xp(user_id, final_xp, f"Workout: {len(today_log)} exercises")

                # Special badges
                hour_now = datetime.datetime.now().hour
                if hour_now < 8:   earn_badge(user_id, "earlybird", badges_earned)
                if hour_now >= 21: earn_badge(user_id, "nightowl",  badges_earned)
                if len(today_log) >= 8: earn_badge(user_id, "big_session", badges_earned)
                if sets_total >= 30: earn_badge(user_id, "volume_day", badges_earned)

                # Week consistency check
                week_ago = str(datetime.date.today() - datetime.timedelta(days=6))
                with get_db() as conn:
                    cur = _exec(conn, "SELECT COUNT(DISTINCT date) as cnt FROM workouts WHERE user_id=%s AND date>=%s", (user_id, week_ago))
                    week_count = cur.fetchone()["cnt"]
                if week_count >= 4:
                    earn_badge(user_id, "consistent", badges_earned)

                st.session_state.today_log = []
                st.session_state.workout_start = None
                st.success(f"🏆 Workout saved! {sets_total} sets · +{final_xp} XP earned!")
                if ch_bonus > 0:
                    st.success(f"🎯 +{ch_bonus} bonus XP from completed challenges!")
                st.balloons()
                st.rerun()

        with fb:
            if st.button("🗑️ Clear Log", use_container_width=True):
                st.session_state.today_log = []; st.session_state.workout_start = None; st.rerun()
        with fc:
            if st.button("➕ Add Exercises", use_container_width=True):
                st.session_state.page = "💪 Exercise Library"; st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: DAILY CHALLENGES
# ─────────────────────────────────────────────────────────────
elif page == "🎯 Daily Challenges":
    st.markdown('<div class="if-title">Daily Challenges</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b6b7e; margin-bottom:24px;">Resets midnight · {today_str} · Bonus XP on completion</div>', unsafe_allow_html=True)

    done_count = sum(1 for c in challenges_today.values() if c["completed"])
    st.progress(done_count / 3)
    st.markdown(f'<div style="color:#f97316;font-weight:700;margin-bottom:20px;">{done_count}/3 completed today</div>', unsafe_allow_html=True)

    for ch_id, ch_data in challenges_today.items():
        ch_def = next((c for c in DAILY_CHALLENGES_POOL if c["id"] == ch_id), None)
        if not ch_def: continue
        done = ch_data["completed"]
        card_class = "if-card challenge-done" if done else "if-card challenge-active"
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <div>
                    <div style="font-size:18px; font-weight:700; color:{'#22c55e' if done else '#f0f0f5'};">
                        {'✅ ' if done else '🎯 '}{ch_def['name']}
                    </div>
                    <div style="color:#6b6b7e; font-size:13px; margin-top:4px;">{ch_def['desc']}</div>
                    {f'<div style="color:#22c55e;font-size:11px;margin-top:4px;">Completed at {ch_data.get("completed_at","")[:16]}</div>' if done and ch_data.get("completed_at") else ''}
                </div>
                <div style="text-align:right;">
                    <div style="font-family:\'Barlow Condensed\';font-size:28px;font-weight:900;color:#f97316;">+{ch_def['xp']} XP</div>
                    {'<span style="color:#22c55e;font-size:12px;">EARNED ✓</span>' if done else '<span style="color:#6b6b7e;font-size:12px;">Add exercises to complete</span>'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📊 Challenge Stats")
    with get_db() as conn:
        cur1 = _exec(conn, "SELECT COUNT(*) as cnt FROM daily_challenges WHERE user_id=%s AND completed=1", (user_id,))
        total_ch = cur1.fetchone()["cnt"]
        cur2 = _exec(conn, "SELECT COUNT(DISTINCT date) as cnt FROM daily_challenges WHERE user_id=%s AND completed=1", (user_id,))
        days_with_ch = cur2.fetchone()["cnt"]
    ch1, ch2, ch3 = st.columns(3)
    with ch1: st.metric("Total Completed", total_ch)
    with ch2: st.metric("Days With Challenges", days_with_ch)
    with ch3: st.metric("Today's Progress", f"{done_count}/3")

# ─────────────────────────────────────────────────────────────
# PAGE: STATISTICS
# ─────────────────────────────────────────────────────────────
elif page == "📊 Statistics":
    st.markdown('<div class="if-title">Statistics</div>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric("Total Workouts", total_workouts)
    with m2: st.metric("Day Streak",     streak)
    with m3: st.metric("Longest Streak", user.get("longest_streak", streak))
    with m4: st.metric("Total Sets",     total_sets)
    with m5: st.metric("Total XP",       f"{total_xp:,}")

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📈 Progress", "💪 Muscles", "🥇 Records"])

    with tab1:
        ch1, ch2 = st.columns(2)
        with ch1:
            st.markdown("#### 📅 Workout Frequency (30 Days)")
            today_dt = datetime.date.today()
            dates_30  = [(today_dt - datetime.timedelta(days=i)) for i in range(29, -1, -1)]
            hist_dates = set(w["date"] for w in workouts_list)
            freq = [1 if str(dd) in hist_dates else 0 for dd in dates_30]
            labels_30 = [str(dd)[5:] for dd in dates_30]
            fig = go.Figure(go.Bar(
                x=labels_30, y=freq,
                marker_color=["#f97316" if v else "#1a1a22" for v in freq],
            ))
            plotly_dark(fig, height=220)
            fig.update_layout(yaxis_visible=False, bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)

        with ch2:
            st.markdown("#### ⚡ XP Per Workout (Last 20)")
            recent = workouts_list[:20][::-1]
            if recent:
                xp_vals = [w["total_xp"] for w in recent]
                mult_vals = [w.get("xp_multiplier", 1.0) for w in recent]
                dates_r  = [w["date"][5:] for w in recent]
                fig = go.Figure()
                fig.add_trace(go.Bar(x=dates_r, y=xp_vals,
                    marker_color=[f"rgba(249,115,22,{min(0.4+m*0.2,1.0)})" for m in mult_vals],
                    name="XP"))
                plotly_dark(fig, height=220)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet.")

        ch3, ch4 = st.columns(2)
        with ch3:
            st.markdown("#### 📦 Sets Per Workout")
            if workouts_list:
                recent20 = workouts_list[:20][::-1]
                fig = go.Figure(go.Scatter(
                    x=[w["date"][5:] for w in recent20],
                    y=[w["total_sets"] for w in recent20],
                    mode="lines+markers",
                    line=dict(color="#3b82f6", width=2),
                    marker=dict(color="#3b82f6", size=7),
                    fill="tozeroy", fillcolor="#3b82f620",
                ))
                plotly_dark(fig, height=220)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet.")

        with ch4:
            st.markdown("#### 🎯 XP per Workout (multiplier breakdown)")
            if workouts_list:
                recent15 = workouts_list[:15][::-1]
                fig = go.Figure()
                fig.add_trace(go.Bar(name="Base XP",  x=[w["date"][5:] for w in recent15],
                    y=[w.get("base_xp",w["total_xp"]) for w in recent15], marker_color="#3b82f6"))
                fig.add_trace(go.Bar(name="Bonus XP", x=[w["date"][5:] for w in recent15],
                    y=[w.get("bonus_xp",0) for w in recent15], marker_color="#f97316"))
                fig.update_layout(barmode="stack")
                plotly_dark(fig, height=220)
                fig.update_layout(showlegend=True)
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        ch5, ch6 = st.columns(2)
        with ch5:
            st.markdown("#### 💪 Sets by Muscle Group")
            if muscle_stats:
                sorted_ms = sorted(muscle_stats.items(), key=lambda x: x[1], reverse=True)
                colors = ["#f97316","#3b82f6","#22c55e","#a855f7","#fbbf24",
                          "#ef4444","#14b8a6","#ec4899","#8b5cf6","#f97316","#22c55e","#3b82f6","#ef4444"]
                fig = go.Figure(go.Bar(
                    x=[k for k,v in sorted_ms], y=[v for k,v in sorted_ms],
                    marker_color=colors[:len(sorted_ms)],
                    text=[v for k,v in sorted_ms], textposition="outside",
                ))
                plotly_dark(fig, height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet.")

        with ch6:
            st.markdown("#### 🍩 Muscle Balance")
            if muscle_stats:
                fig = go.Figure(go.Pie(
                    labels=list(muscle_stats.keys()),
                    values=list(muscle_stats.values()),
                    hole=0.55,
                    marker_colors=["#f97316","#3b82f6","#22c55e","#a855f7","#fbbf24","#ef4444","#14b8a6","#ec4899","#8b5cf6","#f97316","#22c55e","#3b82f6"],
                ))
                plotly_dark(fig, height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet.")

        # Muscle balance score
        if muscle_stats:
            st.markdown("#### 🌐 Muscle Balance Score")
            main_muscles = ["Chest","Back","Shoulders","Biceps","Triceps","Legs","Core","Glutes","Calves"]
            trained = [m for m in main_muscles if m in muscle_stats]
            balance_score = int(len(trained) / len(main_muscles) * 100)
            st.progress(balance_score / 100)
            st.markdown(f'<div style="color:#f97316;font-weight:700;">{balance_score}% muscle balance · {len(trained)}/{len(main_muscles)} muscle groups trained</div>', unsafe_allow_html=True)
            if balance_score < 60:
                missing = [m for m in main_muscles if m not in muscle_stats]
                st.markdown(f'<div style="color:#6b6b7e;font-size:13px;">Train these for better balance: {", ".join(missing)}</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("#### 🥇 Personal Records")
        if prs:
            import pandas as pd
            pr_rows = []
            for ex_id, pr in prs.items():
                ex = next((e for e in EXERCISES if str(e["id"]) == ex_id), None)
                if ex:
                    pr_rows.append({
                        "Exercise": ex["name"],
                        "Muscle":   ex["muscle"],
                        "Weight (kg)": pr.get("weight","—"),
                        "Reps":     pr.get("reps","—"),
                        "Est. 1RM": f'{pr["one_rep_max"]:.1f} kg' if pr.get("one_rep_max") else "—",
                        "Date":     pr.get("date","—"),
                    })
            if pr_rows:
                st.dataframe(pd.DataFrame(pr_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No PRs saved yet. Use the Exercise Library to set personal records.")

# ─────────────────────────────────────────────────────────────
# PAGE: HISTORY
# ─────────────────────────────────────────────────────────────
elif page == "📅 History":
    st.markdown('<div class="if-title">Workout History</div>', unsafe_allow_html=True)

    if not workouts_list:
        st.markdown('<div class="if-card" style="text-align:center;padding:48px;color:#6b6b7e;">No workouts recorded yet.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color:#6b6b7e;margin-bottom:20px;">{len(workouts_list)} workouts on record</div>', unsafe_allow_html=True)

        # Filter
        show_limit = st.select_slider("Show last", options=[10, 25, 50, 100, "All"], value=25)
        show_list  = workouts_list if show_limit == "All" else workouts_list[:show_limit]

        for entry in show_list:
            muscles_list = json.loads(entry.get("muscles_trained") or "[]")
            exs = db_get_workout_exercises(entry["id"])
            ex_names = ", ".join(e["exercise_name"] for e in exs[:5])
            if len(exs) > 5: ex_names += f" +{len(exs)-5} more"
            note_html = f'<div style="color:#6b6b7e;font-size:12px;margin-top:4px;">📝 {entry["note"]}</div>' if entry.get("note") else ""
            mult_html = f'<span style="color:#fbbf24;font-size:11px;">×{entry["xp_multiplier"]:.1f}</span>' if entry.get("xp_multiplier",1.0) > 1.0 else ""
            st.markdown(f"""
            <div class="if-card">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div>
                        <span style="color:#f97316; font-family:'Barlow Condensed'; font-weight:800; font-size:18px;">{entry['date']}</span>
                        <span style="color:#6b6b7e; font-size:12px;"> · {entry['duration_min']}min</span>
                    </div>
                    <span style="color:#22c55e; font-weight:700; font-size:16px;">+{entry['total_xp']} XP {mult_html}</span>
                </div>
                <div style="color:#9898ba; margin-top:6px; font-size:13px;">{entry['total_sets']} sets · {entry['exercise_count']} exercises · {", ".join(muscles_list)}</div>
                <div style="color:#6b6b7e; font-size:12px; margin-top:3px;">{ex_names}</div>
                {note_html}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: BODY WEIGHT
# ─────────────────────────────────────────────────────────────
elif page == "⚖️ Body Weight":
    st.markdown('<div class="if-title">Body Weight Tracker</div>', unsafe_allow_html=True)

    bw_c1, bw_c2 = st.columns([1, 3])
    with bw_c1:
        st.markdown("#### Log Today")
        weight_in = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, step=0.1, value=70.0)
        if st.button("Log Weight", use_container_width=True):
            db_log_bodyweight(user_id, weight_in, today_str)
            st.toast(f"✓ {weight_in} kg logged!", icon="⚖️")
            st.rerun()

    log = db_get_bodyweight_log(user_id)
    if log:
        weights  = [e["weight"] for e in log]
        change   = round(weights[0] - weights[-1], 1) if len(weights) > 1 else 0

        with bw_c2:
            bm1, bm2, bm3, bm4 = st.columns(4)
            with bm1: st.metric("Current",      f"{weights[0]} kg")
            with bm2: st.metric("Lowest",       f"{min(weights)} kg")
            with bm3: st.metric("Highest",      f"{max(weights)} kg")
            with bm4: st.metric("Total Change", f"{'+' if change>=0 else ''}{change} kg",
                                 delta_color="inverse")

        import pandas as pd
        df  = pd.DataFrame(list(reversed(log[:60])))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["weight"],
            mode="lines+markers",
            line=dict(color="#3b82f6", width=2),
            marker=dict(color="#3b82f6", size=7),
            fill="tozeroy", fillcolor="#3b82f620",
        ))
        # 7-day moving average
        if len(df) >= 7:
            ma = df["weight"].rolling(7, min_periods=1).mean()
            fig.add_trace(go.Scatter(
                x=df["date"], y=ma, mode="lines",
                line=dict(color="#f97316", width=1.5, dash="dot"),
                name="7-day avg"
            ))
        plotly_dark(fig, 300)
        fig.update_layout(title="Weight Progress", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Recent Entries")
        for entry in log[:15]:
            st.markdown(f"""
            <div class="if-card" style="display:flex;justify-content:space-between;padding:10px 20px;">
                <span style="color:#9898ba;">{entry['date']}</span>
                <span style="color:#3b82f6;font-weight:700;font-size:16px;">{entry['weight']} kg</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No weight entries yet. Log your first measurement above!")

# ─────────────────────────────────────────────────────────────
# PAGE: ACHIEVEMENTS
# ─────────────────────────────────────────────────────────────
elif page == "🏅 Achievements":
    st.markdown('<div class="if-title">Achievements</div>', unsafe_allow_html=True)
    earned_count = len(badges_earned)
    st.markdown(f'<div style="color:#6b6b7e;margin-bottom:16px;">{earned_count} / {len(BADGES)} badges earned</div>', unsafe_allow_html=True)
    st.progress(earned_count / len(BADGES))
    st.markdown("---")

    # Group by category
    cats = ["Milestone","Streak","Workouts","Volume","XP","Level","Balance","Special","Challenge"]
    for cat in cats:
        cat_badges = [b for b in BADGES if b.get("category") == cat]
        if not cat_badges: continue
        st.markdown(f'<div style="font-family:\'Barlow Condensed\';font-size:18px;font-weight:800;color:#9898ba;letter-spacing:2px;margin:16px 0 10px;">{cat.upper()}</div>', unsafe_allow_html=True)
        cols = st.columns(min(len(cat_badges), 5))
        for i, badge in enumerate(cat_badges):
            is_earned = badge["id"] in badges_earned
            css_cls   = "badge-earned" if is_earned else "badge-locked"
            with cols[i % 5]:
                st.markdown(f"""
                <div class="{css_cls}">
                    <div style="font-size:28px;">{badge['icon']}</div>
                    <div style="font-weight:700; margin-top:8px; color:{'#f0f0f5' if is_earned else '#4a4a6a'}; font-size:13px;">{badge['name']}</div>
                    <div style="font-size:11px; color:#5a5a7a; margin-top:4px;">{badge['desc']}</div>
                    {"<div style='color:#22c55e;font-size:10px;margin-top:6px;font-weight:700;'>✓ EARNED</div>" if is_earned else ""}
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: REST TIMER
# ─────────────────────────────────────────────────────────────
elif page == "⏱️ Rest Timer":
    st.markdown('<div class="if-title" style="text-align:center;">⏱️ Rest Timer</div>', unsafe_allow_html=True)

    st.markdown("#### Quick Presets")
    pc = st.columns(7)
    for i, (label, secs) in enumerate([("30s",30),("45s",45),("60s",60),("90s",90),("2 min",120),("3 min",180),("5 min",300)]):
        if pc[i].button(label, use_container_width=True, key=f"p_{secs}"):
            st.session_state.timer_end = time.time() + secs
            st.session_state.timer_dur = secs; st.rerun()

    st.markdown("#### Custom Duration")
    tc1, tc2 = st.columns([3, 1])
    with tc1:
        custom_secs = st.number_input("Seconds", min_value=5, max_value=600,
                                       value=st.session_state.timer_dur, step=5)
    with tc2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶ Start", use_container_width=True):
            st.session_state.timer_end = time.time() + custom_secs
            st.session_state.timer_dur = custom_secs; st.rerun()

    st.markdown("---")
    timer_ph = st.empty()
    prog_ph  = st.empty()
    status_ph = st.empty()
    end = st.session_state.timer_end

    if end:
        remaining = end - time.time()
        if remaining > 0:
            mins = int(remaining) // 60
            secs = int(remaining) % 60
            pct  = 1 - remaining / max(st.session_state.timer_dur, 1)
            color = "#f97316" if remaining > 10 else "#ef4444"
            timer_ph.markdown(f"""
            <div style="text-align:center; font-family:'Barlow Condensed'; font-size:96px;
                        font-weight:900; color:{color}; letter-spacing:6px;
                        padding:24px; background:#16161d; border-radius:20px;
                        border:2px solid {color}30; box-shadow: 0 0 40px {color}20;">
                {mins:02d}:{secs:02d}
            </div>
            """, unsafe_allow_html=True)
            prog_ph.progress(min(pct, 1.0))
            status_ph.markdown(f'<div style="text-align:center;color:#6b6b7e;margin-top:8px;">{int(remaining)}s remaining of {st.session_state.timer_dur}s</div>', unsafe_allow_html=True)
            time.sleep(1); st.rerun()
        else:
            st.session_state.timer_end = None
            timer_ph.markdown("""
            <div style="text-align:center; font-family:'Barlow Condensed'; font-size:96px;
                        font-weight:900; color:#22c55e; letter-spacing:6px;
                        padding:24px; background:#22c55e08; border-radius:20px; border:2px solid #22c55e;">
                00:00
            </div>
            """, unsafe_allow_html=True)
            status_ph.success("✅ Rest complete! Time to lift! 💪")
    else:
        timer_ph.markdown("""
        <div style="text-align:center; font-family:'Barlow Condensed'; font-size:96px;
                    font-weight:900; color:#252530; letter-spacing:6px;
                    padding:24px; background:#16161d; border-radius:20px; border:2px solid #252530;">
            00:00
        </div>
        """, unsafe_allow_html=True)
        status_ph.markdown('<div style="text-align:center;color:#6b6b7e;margin-top:12px;">Choose a duration above to start</div>', unsafe_allow_html=True)

    if end:
        if st.button("⏹ Stop Timer", key="stop_timer"):
            st.session_state.timer_end = None; st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: WORKOUT PLANS
# ─────────────────────────────────────────────────────────────
elif page == "🔄 Workout Plans":
    st.markdown('<div class="if-title">Workout Plans</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6b6b7e;margin-bottom:24px;">Load a plan straight into today\'s log and start training</div>', unsafe_allow_html=True)

    plan_cols = st.columns(2)
    for i, (plan_name, exercise_names) in enumerate(WORKOUT_PLANS.items()):
        ex_list = [e for e in EXERCISES if e["name"] in exercise_names]
        total_s = sum(e["sets"] for e in ex_list)
        total_x = sum(e["xp"]   for e in ex_list)
        muscles_in_plan = list(set(e["muscle"] for e in ex_list))

        with plan_cols[i % 2]:
            st.markdown(f"""
            <div class="if-card">
                <div style="font-family:'Barlow Condensed';font-size:20px;font-weight:900;color:#f97316;">{plan_name}</div>
                <div style="color:#9898ba;font-size:12px;margin:4px 0;">{len(ex_list)} exercises · {total_s} sets · +{total_x} XP base</div>
                <div style="color:#6b6b7e;font-size:12px;">Targets: {", ".join(muscles_in_plan[:4])}</div>
                <div style="color:#6b6b7e;font-size:11px;margin-top:4px;">{' · '.join(exercise_names[:4])}{'…' if len(exercise_names)>4 else ''}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Load Plan", key=f"plan_{i}", use_container_width=True):
                st.session_state.today_log = [e.copy() for e in ex_list]
                if not st.session_state.workout_start:
                    st.session_state.workout_start = time.time()
                earn_badge(user_id, "planner", badges_earned)
                st.session_state.page = "📋 Today's Log"
                st.toast(f"✓ {plan_name} loaded — {len(ex_list)} exercises!", icon="📋")
                st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: SETTINGS
# ─────────────────────────────────────────────────────────────
elif page == "⚙️ Settings":
    st.markdown('<div class="if-title">Settings</div>', unsafe_allow_html=True)

    st.markdown("#### 👤 Profile")
    new_name = st.text_input("Username", value=user.get("username",""))
    if st.button("Save Username"):
        db_update_user(user_id, username=new_name)
        st.session_state.user["username"] = new_name
        st.success(f"✓ Username updated to **{new_name}**")

    st.markdown("---")
    st.markdown("#### 🗄️ Database Info")
    st.markdown(f"""
    <div class="if-card">
        <div style="color:#9898ba;">Database: <code style="color:#f97316;">{os.path.abspath(DB_PATH)}</code></div>
        <div style="color:#6b6b7e;font-size:12px;margin-top:8px;">
            SQLite · Persistent across sessions · Set <code>IRONFORGE_DB</code> env var for custom path.
        </div>
        <div style="color:#6b6b7e;font-size:12px;margin-top:4px;">
            For cloud deployment: use a mounted disk or swap SQLite for PostgreSQL via the <code>DATABASE_URL</code> env variable.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_exp, col_imp = st.columns(2)
    with col_exp:
        st.markdown("#### 📥 Export Data")
        with get_db() as conn:
            export_data = {
                "user": dict(user),
                "workouts": [dict(w) for w in _exec(conn, "SELECT * FROM workouts WHERE user_id=%s", (user_id,)).fetchall()],
                "prs": [dict(r) for r in _exec(conn, "SELECT * FROM personal_records WHERE user_id=%s", (user_id,)).fetchall()],
                "bodyweight": [dict(r) for r in _exec(conn, "SELECT * FROM bodyweight_log WHERE user_id=%s", (user_id,)).fetchall()],
                "badges": db_get_badges(user_id),
                "muscle_stats": db_get_muscle_stats(user_id),
                "exported_at": str(datetime.datetime.now()),
            }
        st.download_button(
            "⬇️ Download JSON Backup",
            data=json.dumps(export_data, indent=2),
            file_name=f"ironforge_{user['username']}_{today_str}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col_imp:
        st.markdown("#### 📤 Import Data")
        uploaded = st.file_uploader("Upload JSON backup", type="json", label_visibility="collapsed")
        if uploaded:
            try:
                imp = json.load(uploaded)
                st.info(f"Found backup for **{imp.get('user',{}).get('username','?')}** — partial import available.")
                if st.button("Import muscle stats only"):
                    for muscle, sets_count in imp.get("muscle_stats",{}).items():
                        with get_db() as conn:
                            _exec(conn,
                                "INSERT INTO muscle_stats(user_id,muscle,total_sets) VALUES(%s,%s,%s) ON CONFLICT(user_id,muscle) DO UPDATE SET total_sets=%s",
                                (user_id, muscle, sets_count, sets_count)
                            )
                    st.success("✓ Muscle stats imported.")
            except Exception as e:
                st.error(f"Import failed: {e}")

    st.markdown("---")
    st.markdown("#### ⚠️ Danger Zone")
    with st.expander("⚠️ Reset all data (cannot be undone)"):
        confirm = st.text_input("Type your username to confirm", placeholder=f"Type '{user['username']}' to confirm")
        if st.button("🗑️ Delete all my data", type="secondary"):
            if confirm == user["username"]:
                with get_db() as conn:
                    for tbl in ["workouts","workout_exercises","personal_records","bodyweight_log",
                                "badges_earned","daily_challenges","xp_log","muscle_stats","unique_exercises"]:
                        _exec(conn, f"DELETE FROM {tbl} WHERE user_id=%s", (user_id,))
                    _exec(conn, "UPDATE users SET total_xp=0,level=0,streak=0,last_workout_date=NULL WHERE id=%s", (user_id,))
                st.session_state.today_log = []
                st.success("All data deleted.")
                st.rerun()
            else:
                st.error("Username doesn't match.")

    st.markdown("---")
    st.markdown("""
    <div class="if-card">
        <div style="font-family:'Barlow Condensed';font-size:20px;font-weight:900;color:#f97316;">IRONFORGE v3.0</div>
        <div style="color:#9898ba;margin-top:6px;">Python · Streamlit · SQLite · Plotly</div>
        <div style="color:#6b6b7e;font-size:12px;margin-top:6px;">
            123 exercises · 13 muscle groups · 36 badges · 10 levels · Daily challenges<br>
            XP multipliers · Muscle diagrams · YouTube tutorials · SQLite persistence<br>
            Multi-user support · JSON export/import · Deploy on Render / Railway / Fly.io
        </div>
    </div>
    """, unsafe_allow_html=True)