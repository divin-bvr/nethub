import hashlib
import json
import os
import random
import secrets
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from flask import Flask, g, jsonify, redirect, request, send_from_directory
from werkzeug.utils import secure_filename

import exam_bank

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(os.path.dirname(__file__), "nethub.db")

app = Flask(__name__, static_folder=None)


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000)
    return salt + "$" + digest.hex()


def check_password(password, stored):
    if not stored or "$" not in stored:
        return False
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        return False
    return hash_password(password, salt) == stored


def row_user(row):
    if row is None:
        return None
    keys = row.keys()
    def has(name):
        return name in keys
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "username": row["username"] if has("username") else None,
        "campus": row["campus"] if has("campus") else None,
        "club_id": row["club_id"] if has("club_id") else None,
        "role": row["role"],
        "status": row["status"],
        "auth_provider": row["auth_provider"] if has("auth_provider") else "password",
        "is_owner": int(row["is_owner"] or 0) if has("is_owner") else 0,
        "created_at": row["created_at"] if has("created_at") else None,
    }


def issue_session(db, user_id):
    token = secrets.token_hex(32)
    db.execute(
        "INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)",
        (token, user_id, utcnow()),
    )
    db.commit()
    return token


GOOGLE_CLIENT_ID = os.environ.get("NETHUB_GOOGLE_CLIENT_ID", "").strip()
GITHUB_CLIENT_ID = os.environ.get("NETHUB_GITHUB_CLIENT_ID", "").strip()
GITHUB_CLIENT_SECRET = os.environ.get("NETHUB_GITHUB_CLIENT_SECRET", "").strip()
PUBLIC_URL = os.environ.get("NETHUB_PUBLIC_URL", "http://127.0.0.1:8765").rstrip("/")


def current_user():
    header = request.headers.get("Authorization") or ""
    token = header.replace("Bearer ", "").strip()
    if not token:
        token = request.cookies.get("nethub_token") or ""
    if not token:
        return None
    db = get_db()
    row = db.execute(
        """
        SELECT u.* FROM sessions s
        JOIN users u ON u.id = s.user_id
        WHERE s.token = ?
        """,
        (token,),
    ).fetchone()
    return row_user(row) if row else None


def require_user():
    user = current_user()
    if not user:
        return None, (jsonify({"error": "Sign in first."}), 401)
    return user, None


def require_admin():
    user, err = require_user()
    if err:
        return None, err
    if user["role"] != "admin":
        return None, (jsonify({"error": "Desk only."}), 403)
    return user, None


def user_is_owner(user):
    return bool(user and int(user.get("is_owner") or 0) == 1)


def require_owner():
    user, err = require_admin()
    if err:
        return None, err
    if not user_is_owner(user):
        return None, (jsonify({"error": "Only the owner desk can do that."}), 403)
    return user, None


UPLOAD_DIR = os.path.join(ROOT, "uploads", "cms")
ALLOWED_UPLOAD = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}


def dict_row(row):
    return dict(row) if row else None


PHOTO_STYLE_COLS = [
    ("overlay_color", "TEXT NOT NULL DEFAULT '#050a12'"),
    ("overlay_opacity", "INTEGER NOT NULL DEFAULT 50"),
    ("img_opacity", "INTEGER NOT NULL DEFAULT 100"),
    ("photo_h", "INTEGER NOT NULL DEFAULT 0"),
    ("bw", "INTEGER NOT NULL DEFAULT 0"),
    ("brightness", "INTEGER NOT NULL DEFAULT 100"),
]


def ensure_photo_style_cols(db, table):
    cols = [r[1] for r in db.execute("PRAGMA table_info(" + table + ")")]
    for name, spec in PHOTO_STYLE_COLS:
        if name not in cols:
            db.execute("ALTER TABLE " + table + " ADD COLUMN " + name + " " + spec)


def style_from(body, row=None):
    def pick(key, default):
        if isinstance(body, dict) and key in body and body[key] is not None and body[key] != "":
            return body[key]
        if row is not None:
            keys = row.keys()
            if key in keys and row[key] is not None:
                return row[key]
        return default

    color = str(pick("overlay_color", "#050a12")).strip()
    if not color.startswith("#"):
        color = "#050a12"
    try:
        overlay_opacity = int(pick("overlay_opacity", 50))
    except (TypeError, ValueError):
        overlay_opacity = 50
    try:
        img_opacity = int(pick("img_opacity", 100))
    except (TypeError, ValueError):
        img_opacity = 100
    try:
        photo_h = int(pick("photo_h", 0))
    except (TypeError, ValueError):
        photo_h = 0
    bw_raw = pick("bw", 0)
    bw = 1 if str(bw_raw).lower() in ("1", "true", "on", "yes") else 0
    try:
        brightness = int(pick("brightness", 100))
    except (TypeError, ValueError):
        brightness = 100
    return {
        "overlay_color": color[:16],
        "overlay_opacity": max(0, min(100, overlay_opacity)),
        "img_opacity": max(0, min(100, img_opacity)),
        "photo_h": max(0, min(800, photo_h)),
        "bw": bw,
        "brightness": max(20, min(200, brightness)),
    }


def style_tuple(st):
    return (
        st["overlay_color"],
        st["overlay_opacity"],
        st["img_opacity"],
        st["photo_h"],
        st["bw"],
        st["brightness"],
    )


def seed_cms(db):
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS cms_instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT,
            bio TEXT,
            photo_url TEXT,
            sort_order INTEGER NOT NULL DEFAULT 0,
            published INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS cms_photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot TEXT NOT NULL UNIQUE,
            url TEXT NOT NULL,
            alt TEXT,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS cms_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT,
            href TEXT,
            cta TEXT,
            image_url TEXT,
            color TEXT,
            sort_order INTEGER NOT NULL DEFAULT 0,
            published INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS cms_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )
    if db.execute("SELECT COUNT(*) AS c FROM cms_instructors").fetchone()["c"] == 0:
        db.executemany(
            """
            INSERT INTO cms_instructors (name, title, bio, photo_url, sort_order, published)
            VALUES (?, ?, ?, ?, ?, 1)
            """,
            [
                (
                    "Sunday lab desk",
                    "Facilitator",
                    "Sits with the room on Sunday. Everyone is a mentor — we teach each other.",
                    "assets/nethub/photos/uganda-pair.jpg",
                    1,
                ),
                (
                    "Campus club lead",
                    "Instructor",
                    "Helps a club pick a path and a terminal. No skill required to start.",
                    "assets/nethub/photos/uganda-cohort.jpg",
                    2,
                ),
                (
                    "SOC practice mentor",
                    "Instructor",
                    "Walks packet paths and practice exams with whoever just joined.",
                    "assets/nethub/photos/uganda-terminal.jpg",
                    3,
                ),
            ],
        )
    if db.execute("SELECT COUNT(*) AS c FROM cms_photos").fetchone()["c"] == 0:
        now = utcnow()
        slots = [
            ("fan-1", "assets/nethub/cards/army-soc-wall.png", "US Army cyber operations"),
            ("fan-2", "assets/nethub/photos/lab-students.jpg", "Campus cybersecurity lab"),
            ("fan-3", "assets/nethub/cards/nethub-soc-staff-dark.jpg", "Professional SOC analysts"),
            ("train-sunday", "assets/nethub/photo-analyst.jpg", "SOC analyst"),
            ("train-exams", "assets/nethub/photo-command.jpg", "Professional SOC floor"),
            ("train-catalog", "assets/nethub/nethub-lab-room.jpg", "Dark Nethub lab"),
            ("uganda-1", "assets/nethub/photos/uganda-cohort.jpg", "Uganda lab cohort"),
            ("uganda-2", "assets/nethub/photos/uganda-pair.jpg", "Students on laptops in Uganda"),
            ("uganda-3", "assets/nethub/photos/uganda-terminal.jpg", "Terminal practice in Uganda"),
            ("places-uganda", "assets/nethub/photos/uganda-cohort.jpg", "Uganda campus lab"),
            ("places-drc", "assets/nethub/photos/assurance-mbula-presenting.jpg", "Assurance Mbula presenting in Kinshasa"),
            ("places-community", "assets/nethub/photos/lab-students.jpg", "Community lab"),
            ("logo-nav", "assets/nethub/logo-nav.png", "Nethub"),
            ("logo-footer", "assets/nethub/logo-nav.png", "Nethub"),
        ]
        db.executemany(
            "INSERT INTO cms_photos (slot, url, alt, updated_at) VALUES (?, ?, ?, ?)",
            [(s, u, a, now) for s, u, a in slots],
        )
    if db.execute("SELECT COUNT(*) AS c FROM cms_cards").fetchone()["c"] == 0:
        db.executemany(
            """
            INSERT INTO cms_cards (section, title, body, href, cta, image_url, color, sort_order, published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            [
                (
                    "community",
                    "Everyone is a mentor",
                    "You share what you just learned. Someone else takes the next step. We grow in one room.",
                    "community.html",
                    "See community",
                    "",
                    "#1b4f8a",
                    1,
                ),
                (
                    "community",
                    "Eight subjects",
                    "Linux, AI, forensics, network, SOC, cloud, operating systems, pentest — for learners only.",
                    "about.html#learn",
                    "Learning tracks",
                    "",
                    "#16324f",
                    2,
                ),
                (
                    "community",
                    "No skill required",
                    "You do not need a baseline. Create a seat and start on a track.",
                    "register.html",
                    "Create a seat",
                    "",
                    "#1a3a38",
                    3,
                ),
                (
                    "train",
                    "Sunday lab",
                    "Weekend block plus one shared Sunday room.",
                    "sunday-lab.html",
                    "Open Sunday lab",
                    "assets/nethub/photo-analyst.jpg",
                    "#1b4f8a",
                    1,
                ),
                (
                    "train",
                    "Practice exams",
                    "Cybersecurity questions — network, phishing, SOC, cloud.",
                    "practice-exams.html",
                    "Start a set",
                    "assets/nethub/photo-command.jpg",
                    "#16324f",
                    2,
                ),
                (
                    "train",
                    "Labs catalog",
                    "Hands-on paths you can open after you have a seat.",
                    "catalog.html",
                    "Browse labs",
                    "assets/nethub/nethub-lab-room.jpg",
                    "#1a3a38",
                    3,
                ),
            ],
        )
    if db.execute("SELECT COUNT(*) AS c FROM cms_settings").fetchone()["c"] == 0:
        db.executemany(
            "INSERT INTO cms_settings (key, value) VALUES (?, ?)",
            [
                ("card_color_1", "#1b4f8a"),
                ("card_color_2", "#16324f"),
                ("card_color_3", "#1a3a38"),
                ("accent", "#4a8ad4"),
                ("site_tagline", "The talent exists. Nethub is the pathway."),
            ],
        )
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS cms_pages (
            page_key TEXT PRIMARY KEY,
            kicker TEXT,
            title TEXT,
            lead TEXT
        );
        CREATE TABLE IF NOT EXISTS cms_gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            caption TEXT,
            photo_url TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            published INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS cms_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            starts_at TEXT,
            join_url TEXT,
            notes TEXT,
            published INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS cms_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER,
            from_name TEXT,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    if db.execute("SELECT COUNT(*) AS c FROM cms_pages").fetchone()["c"] == 0:
        db.executemany(
            "INSERT INTO cms_pages (page_key, kicker, title, lead) VALUES (?, ?, ?, ?)",
            [
                ("places", "", "Places", "Pick a room. Each card is its own page."),
                ("uganda", "Uganda", "Bugema and Makerere", "Partner clubs. Weekend machines. No uniform required."),
                ("drc", "DRC", "Kinshasa DRC", "Partner lab in Kinshasa. Same terminals as Sunday."),
                ("community", "Community", "Refugees and host community", "Same room. Sponsored chairs when a partner covers the month."),
                ("sunday", "", "Sunday lab", "Weekend block on campus. One Sunday room for every club."),
                ("gallery", "Gallery", "Labs, rooms, and people", "Photos from campus, Sunday, and Community. The desk updates this wall."),
                ("home-train", "", "How we train", "Three rooms. Each one is its own page."),
                ("home-community", "", "Community", "This is not a country list. It is one room: we teach each other, and we grow together."),
            ],
        )
    if db.execute("SELECT COUNT(*) AS c FROM cms_gallery").fetchone()["c"] == 0:
        db.executemany(
            "INSERT INTO cms_gallery (title, caption, photo_url, sort_order, published) VALUES (?, ?, ?, ?, 1)",
            [
                ("Uganda cohort", "Bugema and Makerere students in the lab.", "assets/nethub/photos/uganda-cohort.jpg", 1),
                ("Pair work", "We sit together. Someone else shares the next step.", "assets/nethub/photos/uganda-pair.jpg", 2),
                ("Kinshasa DRC", "Assurance Mbula presenting in the Kinshasa room.", "assets/nethub/photos/assurance-mbula-presenting.jpg", 3),
                ("Community", "Refugees and host community at the same tables.", "assets/nethub/photos/lab-students.jpg", 4),
            ],
        )
    if db.execute("SELECT COUNT(*) AS c FROM cms_cards WHERE section = 'places'").fetchone()["c"] == 0:
        db.executemany(
            """
            INSERT INTO cms_cards (section, title, body, href, cta, image_url, color, sort_order, published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            [
                ("places", "Uganda", "Bugema and Makerere.", "uganda.html", "", "assets/nethub/photos/uganda-cohort.jpg", "", 1),
                ("places", "Kinshasa DRC", "", "drc.html", "", "assets/nethub/photos/assurance-mbula-presenting.jpg", "", 2),
                ("places", "Community", "Refugees and host community.", "community.html", "", "assets/nethub/photos/lab-students.jpg", "", 3),
            ],
        )
    for table in ("cms_photos", "cms_gallery", "cms_cards", "cms_instructors"):
        ensure_photo_style_cols(db, table)


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            campus TEXT,
            role TEXT NOT NULL DEFAULT 'student',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS mentor_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            meeting_time TEXT,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'requested',
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS career_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'requested',
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            field TEXT NOT NULL,
            duration TEXT,
            youtube_id TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS roadmaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            steps TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS user_roadmaps (
            user_id INTEGER NOT NULL,
            roadmap_id INTEGER NOT NULL,
            picked_at TEXT NOT NULL,
            PRIMARY KEY (user_id, roadmap_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            country TEXT,
            kind TEXT NOT NULL DEFAULT 'university'
        );
        CREATE TABLE IF NOT EXISTS clubs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'approved',
            created_at TEXT NOT NULL,
            FOREIGN KEY (university_id) REFERENCES universities(id)
        );
        CREATE TABLE IF NOT EXISTS term_leaders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            term TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (club_id) REFERENCES clubs(id)
        );
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            topic TEXT,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS quote_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            scope TEXT,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS facilitator_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            campus TEXT,
            notes TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS exam_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    cols = [r[1] for r in db.execute("PRAGMA table_info(users)")]
    if "club_id" not in cols:
        db.execute("ALTER TABLE users ADD COLUMN club_id INTEGER")
    if "username" not in cols:
        db.execute("ALTER TABLE users ADD COLUMN username TEXT")
    if "auth_provider" not in cols:
        db.execute("ALTER TABLE users ADD COLUMN auth_provider TEXT NOT NULL DEFAULT 'password'")
    if "google_sub" not in cols:
        db.execute("ALTER TABLE users ADD COLUMN google_sub TEXT")
    if "github_id" not in cols:
        db.execute("ALTER TABLE users ADD COLUMN github_id TEXT")
    if "is_owner" not in cols:
        db.execute("ALTER TABLE users ADD COLUMN is_owner INTEGER NOT NULL DEFAULT 0")
    exam_cols = [r[1] for r in db.execute("PRAGMA table_info(exam_attempts)")]
    for name, spec in (
        ("category", "TEXT"),
        ("guest_key", "TEXT"),
        ("question_ids", "TEXT"),
        ("payload", "TEXT"),
        ("started_at", "TEXT"),
        ("ends_at", "TEXT"),
        ("submitted_at", "TEXT"),
        ("answers_json", "TEXT"),
    ):
        if name not in exam_cols:
            db.execute("ALTER TABLE exam_attempts ADD COLUMN " + name + " " + spec)
    admin_hash = hash_password("admin1234")
    admin_row = db.execute(
        """
        SELECT id FROM users
        WHERE email IN ('admin@nethub.club', 'admin@nethub.africa') OR username = 'admin'
        """
    ).fetchone()
    if admin_row:
        db.execute(
            """
            UPDATE users
            SET name = ?, email = ?, username = ?, role = 'admin',
                status = 'approved', auth_provider = 'password', campus = ?, is_owner = 1
            WHERE id = ?
            """,
            ("admin", "admin@nethub.club", "admin", "Desk", admin_row["id"]),
        )
    else:
        db.execute(
            """
            INSERT INTO users (name, email, username, password_hash, campus, role, status, auth_provider, is_owner, created_at)
            VALUES (?, ?, ?, ?, ?, 'admin', 'approved', 'password', 1, ?)
            """,
            ("admin", "admin@nethub.club", "admin", admin_hash, "Desk", utcnow()),
        )
    if db.execute("SELECT COUNT(*) AS c FROM videos").fetchone()["c"] == 0:
        db.executemany(
            "INSERT INTO videos (title, field, duration, youtube_id) VALUES (?, ?, ?, ?)",
            [
                ("Networking in 4 minutes — OSI mental model", "Network", "4 min", "3-Fd7nBBaUA"),
                ("What is cybersecurity?", "Foundations", "8 min", "inWWhr5tnEA"),
                ("Linux for hackers — crash path", "Foundations", "12 min", "iv8rSLsi1xo"),
                ("SOC analyst day in the life", "SOC", "10 min", "XQcfv6rgUes"),
                ("Intro to penetration testing", "Pentest", "11 min", "sc5RHnKoBAc"),
                ("Incident response explained", "Forensics", "9 min", "8aeg-xUAcA0"),
            ],
        )
    if db.execute("SELECT COUNT(*) AS c FROM roadmaps").fetchone()["c"] == 0:
        db.executemany(
            "INSERT INTO roadmaps (field, title, summary, steps) VALUES (?, ?, ?, ?)",
            [
                (
                    "Pentest",
                    "Offensive path",
                    "Web, network, and report writing for scoped tests.",
                    json.dumps(
                        [
                            "Linux, Python, and how packets move",
                            "OWASP Top 10 on a legal lab",
                            "Nmap, Burp, and a written finding",
                            "Join a Nethub weekend pentest block",
                        ]
                    ),
                ),
                (
                    "SOC",
                    "Defensive operations",
                    "Alerts, triage, and what to escalate.",
                    json.dumps(
                        [
                            "Logs, SIEM vocabulary, false positives",
                            "Windows and Linux telemetry",
                            "A tabletop incident on Sunday lab",
                            "Shadow a facilitator on a real ticket shape",
                        ]
                    ),
                ),
                (
                    "Network",
                    "Routing and hardening",
                    "Cables, subnets, wifi that is not a hallway.",
                    json.dumps(
                        [
                            "Addressing, VLANs, DNS",
                            "Firewall defaults closed",
                            "Campus wifi lab",
                            "Document a small-shop network",
                        ]
                    ),
                ),
                (
                    "Forensics",
                    "After an incident",
                    "Preserve, reconstruct, tell leadership the truth.",
                    json.dumps(
                        [
                            "Evidence handling",
                            "Disk and memory basics",
                            "Timeline of a lab compromise",
                            "Write a one-page brief",
                        ]
                    ),
                ),
                (
                    "Cloud",
                    "Identity and cloud",
                    "Accounts, keys, and the control plane.",
                    json.dumps(
                        [
                            "IAM and least privilege",
                            "Storage buckets that leak",
                            "A small AWS or Azure lab",
                            "Harden a student project account",
                        ]
                    ),
                ),
                (
                    "GRC",
                    "People and policy",
                    "Awareness that staff will sit through.",
                    json.dumps(
                        [
                            "Risk in plain language",
                            "Phishing session design",
                            "A policy one page long",
                            "Run awareness for a campus club",
                        ]
                    ),
                ),
            ],
        )
    if db.execute("SELECT COUNT(*) AS c FROM universities").fetchone()["c"] == 0:
        db.executemany(
            "INSERT INTO universities (name, country, kind) VALUES (?, ?, ?)",
            [
                ("Bugema University", "Uganda", "university"),
                ("Makerere University", "Uganda", "university"),
                ("Kyambogo University", "Uganda", "university"),
                ("Mbarara University of Science and Technology", "Uganda", "university"),
                ("Uganda Christian University", "Uganda", "university"),
                ("Université de Kinshasa (UNIKIN)", "DRC", "university"),
                ("Université Officielle de Bukavu", "DRC", "university"),
                ("University of Nairobi", "Kenya", "university"),
                ("Strathmore University", "Kenya", "university"),
                ("University of Rwanda", "Rwanda", "university"),
                ("Community — refugees and host community", "Regional", "community"),
            ],
        )
        unis = {r["name"]: r["id"] for r in db.execute("SELECT id, name FROM universities")}
        now = utcnow()
        seed_clubs = [
            (unis["Bugema University"], "Nethub Bugema club"),
            (unis["Makerere University"], "Nethub Makerere club"),
            (unis["Kyambogo University"], "Nethub Kyambogo club"),
            (unis["Mbarara University of Science and Technology"], "Nethub MUST club"),
            (unis["Uganda Christian University"], "Nethub UCU club"),
            (unis["Université de Kinshasa (UNIKIN)"], "Nethub UNIKIN club"),
            (unis["Université Officielle de Bukavu"], "Nethub Bukavu club"),
            (unis["University of Nairobi"], "Nethub Nairobi club"),
            (unis["Strathmore University"], "Nethub Strathmore club"),
            (unis["University of Rwanda"], "Nethub Kigali club"),
            (unis["Community — refugees and host community"], "Refugee learners club"),
            (unis["Community — refugees and host community"], "Host community club"),
        ]
        db.executemany(
            "INSERT INTO clubs (university_id, name, status, created_at) VALUES (?, ?, 'approved', ?)",
            [(uid, name, now) for uid, name in seed_clubs],
        )
        clubs = {r["name"]: r["id"] for r in db.execute("SELECT id, name FROM clubs")}
        db.executemany(
            "INSERT INTO term_leaders (club_id, name, email, term, created_at) VALUES (?, ?, ?, ?, ?)",
            [
                (clubs["Nethub Makerere club"], "Club desk", "makerere@nethub.africa", "2026 Term 2", now),
                (clubs["Nethub UNIKIN club"], "Club desk", "unikin@nethub.africa", "2026 Term 2", now),
                (clubs["Refugee learners club"], "Community desk", "community@nethub.africa", "2026 Term 2", now),
            ],
        )
    seed_cms(db)
    db.commit()
    db.close()


@app.route("/api/register", methods=["POST"])
def register():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    campus = (body.get("campus") or "").strip()
    club_id = body.get("club_id")
    try:
        club_id = int(club_id) if club_id else None
    except (TypeError, ValueError):
        club_id = None
    if len(name) < 2 or "@" not in email or len(password) < 8:
        return jsonify({"error": "Name, a real email, and a password of 8+ characters."}), 400
    db = get_db()
    if club_id:
        club = db.execute(
            "SELECT c.name AS club, u.name AS university FROM clubs c JOIN universities u ON u.id = c.university_id WHERE c.id = ?",
            (club_id,),
        ).fetchone()
        if not club:
            return jsonify({"error": "Pick a club from the list."}), 400
        campus = club["university"] + " · " + club["club"]
    if db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
        return jsonify({"error": "That email already has a seat. Sign in instead."}), 409
    username = (body.get("username") or email.split("@")[0]).strip().lower()
    role = (body.get("role") or "student").strip().lower()
    if role not in ("student", "mentor"):
        role = "student"
    db.execute(
        """
        INSERT INTO users (name, email, username, password_hash, campus, club_id, role, status, auth_provider, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', 'password', ?)
        """,
        (name, email, username, hash_password(password), campus, club_id, role, utcnow()),
    )
    db.commit()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    token = issue_session(db, user["id"])
    return jsonify({"token": token, "user": row_user(user), "just_registered": True})


@app.route("/api/login", methods=["POST"])
def login():
    body = request.get_json(silent=True) or {}
    ident = (body.get("email") or body.get("username") or "").strip().lower()
    password = body.get("password") or ""
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE lower(email) = ? OR lower(username) = ?",
        (ident, ident),
    ).fetchone()
    if not user or not check_password(password, user["password_hash"]):
        return jsonify({"error": "Email, username, or password does not match."}), 401
    token = issue_session(db, user["id"])
    return jsonify({"token": token, "user": row_user(user)})


@app.route("/api/me")
def me():
    user, err = require_user()
    if err:
        return err
    db = get_db()
    picked = [
        dict(r)
        for r in db.execute(
            """
            SELECT r.id, r.field, r.title, r.summary, r.steps, ur.picked_at
            FROM user_roadmaps ur
            JOIN roadmaps r ON r.id = ur.roadmap_id
            WHERE ur.user_id = ?
            ORDER BY ur.picked_at DESC
            """,
            (user["id"],),
        ).fetchall()
    ]
    for item in picked:
        item["steps"] = json.loads(item["steps"])
    mentors = [dict(r) for r in db.execute(
        "SELECT * FROM mentor_requests WHERE user_id = ? ORDER BY id DESC",
        (user["id"],),
    ).fetchall()]
    careers = [dict(r) for r in db.execute(
        "SELECT * FROM career_requests WHERE user_id = ? ORDER BY id DESC",
        (user["id"],),
    ).fetchall()]
    return jsonify({"user": row_user(user), "roadmaps": picked, "mentor_requests": mentors, "career_requests": careers})


@app.route("/api/mentor-requests", methods=["POST"])
def mentor_create():
    user, err = require_user()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    topic = (body.get("topic") or "").strip()
    if not topic:
        return jsonify({"error": "Say what the Zoom should cover."}), 400
    db = get_db()
    db.execute(
        """
        INSERT INTO mentor_requests (user_id, topic, meeting_time, notes, status, created_at)
        VALUES (?, ?, ?, ?, 'requested', ?)
        """,
        (user["id"], topic, (body.get("meeting_time") or "").strip(), (body.get("notes") or "").strip(), utcnow()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/career-requests", methods=["POST"])
def career_create():
    user, err = require_user()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    goal = (body.get("goal") or "").strip()
    if not goal:
        return jsonify({"error": "Name the career question."}), 400
    db = get_db()
    db.execute(
        """
        INSERT INTO career_requests (user_id, goal, notes, status, created_at)
        VALUES (?, ?, ?, 'requested', ?)
        """,
        (user["id"], goal, (body.get("notes") or "").strip(), utcnow()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/videos")
def videos():
    user, err = require_user()
    if err:
        return err
    rows = get_db().execute("SELECT * FROM videos ORDER BY field, id").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/roadmaps")
def roadmaps():
    user, err = require_user()
    if err:
        return err
    rows = get_db().execute("SELECT * FROM roadmaps ORDER BY field").fetchall()
    out = []
    for r in rows:
        item = dict(r)
        item["steps"] = json.loads(item["steps"])
        out.append(item)
    return jsonify(out)



def _exam_guest(body=None):
    body = body or {}
    key = (body.get("guest_key") or request.headers.get("X-Exam-Guest") or "").strip()
    if len(key) < 8:
        key = secrets.token_hex(12)
    return key[:64]


def _parse_ids(raw):
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return [str(x) for x in data]
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


@app.route("/api/exam/categories")
def exam_categories():
    out = []
    for cat in exam_bank.CATEGORIES:
        row = dict(cat)
        row["questions"] = len(exam_bank.pool_for(cat["slug"]))
        row["set_size"] = exam_bank.NEED
        out.append(row)
    return jsonify(out)


@app.route("/api/exam")
def exam_questions():
    return exam_categories()


@app.route("/api/exam/start", methods=["POST"])
def exam_start():
    body = request.get_json(silent=True) or {}
    slug = (body.get("category") or body.get("slug") or "").strip()
    cat = exam_bank.category_by_slug(slug)
    if not cat:
        return jsonify({"error": "Pick a category card."}), 400
    user = current_user()
    guest = _exam_guest(body)
    db = get_db()
    prev_row = None
    if user:
        prev_row = db.execute(
            """
            SELECT question_ids FROM exam_attempts
            WHERE category = ? AND submitted_at IS NOT NULL AND user_id = ?
            ORDER BY id DESC LIMIT 1
            """,
            (slug, user["id"]),
        ).fetchone()
    if not prev_row:
        prev_row = db.execute(
            """
            SELECT question_ids FROM exam_attempts
            WHERE category = ? AND submitted_at IS NOT NULL AND guest_key = ?
            ORDER BY id DESC LIMIT 1
            """,
            (slug, guest),
        ).fetchone()
    previous_ids = _parse_ids(prev_row["question_ids"] if prev_row else None)
    try:
        picked = exam_bank.pick_attempt_questions(slug, previous_ids)
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400
    public, secret = exam_bank.present_set(picked)
    started = datetime.now(timezone.utc)
    ends = started + timedelta(minutes=int(cat["minutes"]))
    ids = [q["id"] for q in picked]
    cur = db.execute(
        """
        INSERT INTO exam_attempts (
            user_id, score, total, created_at, category, guest_key, question_ids, payload,
            started_at, ends_at
        ) VALUES (?, 0, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user["id"] if user else None,
            len(public),
            utcnow(),
            slug,
            guest,
            json.dumps(ids),
            json.dumps(secret),
            started.strftime("%Y-%m-%d %H:%M:%S"),
            ends.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    db.commit()
    return jsonify(
        {
            "attempt_id": cur.lastrowid,
            "guest_key": guest,
            "category": cat,
            "minutes": cat["minutes"],
            "ends_at": ends.isoformat(),
            "questions": public,
            "total": len(public),
        }
    )


NEWS_FEEDS = [
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
    ("CISA", "https://www.cisa.gov/cybersecurity-advisories/all.xml"),
    ("Microsoft Security", "https://www.microsoft.com/en-us/security/blog/feed/"),
    ("Unit 42 (Palo Alto)", "https://unit42.paloaltonetworks.com/feed/"),
    ("Dark Reading", "https://www.darkreading.com/rss.xml"),
    ("SANS ISC", "https://isc.sans.edu/rssfeed.xml"),
    ("Cisco Talos", "https://blog.talosintelligence.com/feeds/posts/default"),
    ("CrowdStrike", "https://www.crowdstrike.com/blog/feed/"),
]

_news_cache = {"at": 0, "items": []}


def _rss_items(name, url, limit=5):
    req = urllib.request.Request(url, headers={"User-Agent": "NethubNews/1.0 (training lab)"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
    root = ET.fromstring(raw)
    items = []
    for item in root.findall(".//item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        date = (item.findtext("pubDate") or "").strip()
        if title and link:
            items.append({"source": name, "title": title, "url": link, "date": date})
    if not items:
        atom = "{http://www.w3.org/2005/Atom}"
        for entry in root.findall(".//" + atom + "entry")[:limit]:
            title_el = entry.find(atom + "title")
            title = (title_el.text if title_el is not None else "") or ""
            link = ""
            for el in entry.findall(atom + "link"):
                if el.get("rel") in (None, "alternate"):
                    link = el.get("href") or ""
                    if link:
                        break
            date_el = entry.find(atom + "updated") or entry.find(atom + "published")
            date = (date_el.text if date_el is not None else "") or ""
            if title and link:
                items.append({"source": name, "title": title.strip(), "url": link, "date": date})
    return items


@app.route("/api/news")
def news():
    now = datetime.now(timezone.utc).timestamp()
    if _news_cache["items"] and now - _news_cache["at"] < 1800:
        return jsonify(_news_cache["items"])
    collected = []
    for name, url in NEWS_FEEDS:
        try:
            collected.extend(_rss_items(name, url, 4))
        except Exception:
            continue
    collected = collected[:28]
    if not collected:
        collected = [
            {
                "source": name,
                "title": "Open the live desk — feed timed out from this lab",
                "url": url.split("/feed")[0].rstrip("/") if "feed" in url else url,
                "date": "",
            }
            for name, url in NEWS_FEEDS[:6]
        ]
    _news_cache["at"] = now
    _news_cache["items"] = collected
    return jsonify(collected)


@app.route("/api/roadmaps/<int:rid>/pick", methods=["POST"])
def pick_roadmap(rid):
    user, err = require_user()
    if err:
        return err
    db = get_db()
    if not db.execute("SELECT id FROM roadmaps WHERE id = ?", (rid,)).fetchone():
        return jsonify({"error": "That path is not on the board."}), 404
    db.execute(
        """
        INSERT OR REPLACE INTO user_roadmaps (user_id, roadmap_id, picked_at)
        VALUES (?, ?, ?)
        """,
        (user["id"], rid, utcnow()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/universities")
def universities():
    rows = get_db().execute("SELECT id, name, country, kind FROM universities ORDER BY kind DESC, name").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/clubs")
def clubs_list():
    db = get_db()
    uid = request.args.get("university_id")
    sql = """
        SELECT c.id, c.name, c.status, c.university_id, u.name AS university, u.kind
        FROM clubs c JOIN universities u ON u.id = c.university_id
        WHERE c.status = 'approved'
    """
    args = []
    if uid:
        sql += " AND c.university_id = ?"
        args.append(uid)
    sql += " ORDER BY u.name, c.name"
    return jsonify([dict(r) for r in db.execute(sql, args).fetchall()])


@app.route("/api/term-leaders")
def term_leaders():
    rows = get_db().execute(
        """
        SELECT t.id, t.name, t.term, t.email, c.name AS club, u.name AS university, u.kind
        FROM term_leaders t
        JOIN clubs c ON c.id = t.club_id
        JOIN universities u ON u.id = c.university_id
        ORDER BY t.term DESC, u.name
        """
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/clubs", methods=["POST"])
def clubs_create():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    leader = (body.get("leader_name") or "").strip()
    email = (body.get("leader_email") or "").strip().lower()
    term = (body.get("term") or "2026 Term 2").strip()
    try:
        university_id = int(body.get("university_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "Pick a university."}), 400
    if len(name) < 3 or len(leader) < 2:
        return jsonify({"error": "Club name and a term leader are required."}), 400
    db = get_db()
    if not db.execute("SELECT id FROM universities WHERE id = ?", (university_id,)).fetchone():
        return jsonify({"error": "That university is not on the list."}), 400
    db.execute(
        "INSERT INTO clubs (university_id, name, status, created_at) VALUES (?, ?, 'pending', ?)",
        (university_id, name, utcnow()),
    )
    club_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    db.execute(
        "INSERT INTO term_leaders (club_id, name, email, term, created_at) VALUES (?, ?, ?, ?, ?)",
        (club_id, leader, email, term, utcnow()),
    )
    db.commit()
    return jsonify({"ok": True, "club_id": club_id, "status": "pending"})


@app.route("/api/admin/pending")
def admin_pending():
    user, err = require_user()
    if err:
        return err
    if user["role"] != "admin":
        return jsonify({"error": "Desk only."}), 403
    rows = get_db().execute(
        "SELECT id, name, email, campus, status, created_at FROM users WHERE role = 'student' ORDER BY id DESC"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/admin/users/<int:uid>/approve", methods=["POST"])
def admin_approve(uid):
    user, err = require_user()
    if err:
        return err
    if user["role"] != "admin":
        return jsonify({"error": "Desk only."}), 403
    db = get_db()
    db.execute("UPDATE users SET status = 'approved' WHERE id = ? AND role = 'student'", (uid,))
    db.commit()
    return jsonify({"ok": True})


def _oauth_upsert(db, *, name, email, provider, google_sub=None, github_id=None):
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if not user and google_sub:
        user = db.execute("SELECT * FROM users WHERE google_sub = ?", (google_sub,)).fetchone()
    if not user and github_id:
        user = db.execute("SELECT * FROM users WHERE github_id = ?", (github_id,)).fetchone()
    if user:
        db.execute(
            """
            UPDATE users SET name = COALESCE(NULLIF(?, ''), name),
                auth_provider = ?, google_sub = COALESCE(?, google_sub),
                github_id = COALESCE(?, github_id)
            WHERE id = ?
            """,
            (name, provider, google_sub, github_id, user["id"]),
        )
        db.commit()
        return db.execute("SELECT * FROM users WHERE id = ?", (user["id"],)).fetchone(), False
    username = email.split("@")[0].lower()
    db.execute(
        """
        INSERT INTO users (name, email, username, password_hash, campus, role, status, auth_provider, google_sub, github_id, created_at)
        VALUES (?, ?, ?, '', '', 'student', 'approved', ?, ?, ?, ?)
        """,
        (name or username, email, username, provider, google_sub, github_id, utcnow()),
    )
    db.commit()
    return db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone(), True


@app.route("/api/auth/config")
def auth_config():
    return jsonify(
        {
            "googleClientId": GOOGLE_CLIENT_ID,
            "github": bool(GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET),
        }
    )


@app.route("/api/auth/google", methods=["POST"])
def auth_google():
    if not GOOGLE_CLIENT_ID:
        return jsonify({"error": "Set NETHUB_GOOGLE_CLIENT_ID on the lab server, then restart Flask."}), 501
    body = request.get_json(silent=True) or {}
    credential = body.get("credential") or ""
    if not credential:
        return jsonify({"error": "Google did not return a token."}), 400
    url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + urllib.parse.quote(credential)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            info = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return jsonify({"error": "Google could not verify that token."}), 401
    if info.get("aud") != GOOGLE_CLIENT_ID:
        return jsonify({"error": "That Google token is not for this Nethub lab."}), 401
    email = (info.get("email") or "").lower()
    if not email:
        return jsonify({"error": "Google did not share an email."}), 400
    db = get_db()
    user, created = _oauth_upsert(
        db,
        name=info.get("name") or email.split("@")[0],
        email=email,
        provider="google",
        google_sub=info.get("sub"),
    )
    token = issue_session(db, user["id"])
    return jsonify({"token": token, "user": row_user(user), "just_registered": created})


@app.route("/api/auth/github")
def auth_github_start():
    if not (GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET):
        return jsonify({"error": "Set NETHUB_GITHUB_CLIENT_ID and NETHUB_GITHUB_CLIENT_SECRET."}), 501
    qs = urllib.parse.urlencode(
        {
            "client_id": GITHUB_CLIENT_ID,
            "scope": "user:email",
            "redirect_uri": PUBLIC_URL + "/api/auth/github/callback",
        }
    )
    return redirect("https://github.com/login/oauth/authorize?" + qs)


@app.route("/api/auth/github/callback")
def auth_github_callback():
    code = request.args.get("code") or ""
    if not code:
        return redirect("/login.html?oauth=denied")
    payload = urllib.parse.urlencode(
        {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": PUBLIC_URL + "/api/auth/github/callback",
        }
    ).encode()
    req = urllib.request.Request(
        "https://github.com/login/oauth/access_token",
        data=payload,
        headers={"Accept": "application/json", "User-Agent": "Nethub"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return redirect("/login.html?oauth=fail")
    access = token_data.get("access_token")
    if not access:
        return redirect("/login.html?oauth=fail")

    def gh(path):
        r = urllib.request.Request(
            "https://api.github.com" + path,
            headers={"Authorization": "Bearer " + access, "User-Agent": "Nethub", "Accept": "application/json"},
        )
        with urllib.request.urlopen(r, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))

    profile = gh("/user")
    emails = gh("/user/emails")
    primary = ""
    for item in emails:
        if item.get("primary") and item.get("verified"):
            primary = item.get("email") or ""
            break
    if not primary:
        for item in emails:
            if item.get("verified"):
                primary = item.get("email") or ""
                break
    if not primary:
        return redirect("/login.html?oauth=fail")
    db = get_db()
    user, created = _oauth_upsert(
        db,
        name=profile.get("name") or profile.get("login") or primary.split("@")[0],
        email=primary.lower(),
        provider="github",
        github_id=str(profile.get("id") or ""),
    )
    token = issue_session(db, user["id"])
    dest = "/admin.html" if user["role"] == "admin" else "/dashboard.html"
    if created:
        dest = "/dashboard.html?welcome=1"
    return redirect(dest + ("&" if "?" in dest else "?") + "session=" + token)


@app.route("/api/forms/contact", methods=["POST"])
def form_contact():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip().lower()
    topic = (body.get("topic") or "").strip()
    message = (body.get("message") or "").strip()
    if len(name) < 2 or "@" not in email or len(message) < 8:
        return jsonify({"error": "Name, email, and a real message."}), 400
    db = get_db()
    db.execute(
        "INSERT INTO contact_messages (name, email, topic, message, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, email, topic, message, utcnow()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/forms/quote", methods=["POST"])
def form_quote():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip().lower()
    company = (body.get("company") or "").strip()
    scope = (body.get("scope") or "").strip()
    message = (body.get("message") or "").strip()
    if len(name) < 2 or "@" not in email or len(message) < 8:
        return jsonify({"error": "Name, email, and a scope note."}), 400
    db = get_db()
    db.execute(
        "INSERT INTO quote_requests (name, email, company, scope, message, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (name, email, company, scope, message, utcnow()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/forms/facilitate", methods=["POST"])
def form_facilitate():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip().lower()
    campus = (body.get("campus") or "").strip()
    notes = (body.get("notes") or "").strip()
    if len(name) < 2 or "@" not in email:
        return jsonify({"error": "Name and email."}), 400
    db = get_db()
    db.execute(
        "INSERT INTO facilitator_applications (name, email, campus, notes, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, email, campus, notes, utcnow()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/exam/submit", methods=["POST"])
def exam_submit():
    body = request.get_json(silent=True) or {}
    attempt_id = body.get("attempt_id")
    user = current_user()
    db = get_db()
    if not attempt_id:
        try:
            score = int(body.get("score") or 0)
            total = int(body.get("total") or 0)
        except (TypeError, ValueError):
            return jsonify({"error": "Need a score."}), 400
        db.execute(
            "INSERT INTO exam_attempts (user_id, score, total, created_at) VALUES (?, ?, ?, ?)",
            (user["id"] if user else None, score, total, utcnow()),
        )
        db.commit()
        return jsonify({"ok": True})
    try:
        attempt_id = int(attempt_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Bad attempt."}), 400
    row = db.execute("SELECT * FROM exam_attempts WHERE id = ?", (attempt_id,)).fetchone()
    if not row:
        return jsonify({"error": "Attempt not found."}), 404
    guest = _exam_guest(body)
    owner_ok = (user and row["user_id"] and user["id"] == row["user_id"]) or (
        row["guest_key"] and row["guest_key"] == guest
    )
    if not owner_ok:
        return jsonify({"error": "That attempt is not yours."}), 403
    if row["submitted_at"]:
        return jsonify(
            {
                "ok": True,
                "score": row["score"],
                "total": row["total"],
                "already": True,
            }
        )
    secret = json.loads(row["payload"] or "[]")
    answers = body.get("answers") or {}
    score, detail = exam_bank.score_answers(secret, answers)
    db.execute(
        """
        UPDATE exam_attempts
        SET score = ?, total = ?, submitted_at = ?, answers_json = ?
        WHERE id = ?
        """,
        (score, len(secret), utcnow(), json.dumps(answers), attempt_id),
    )
    db.commit()
    return jsonify({"ok": True, "score": score, "total": len(secret), "detail": detail})


@app.route("/api/admin/inbox")
def admin_inbox():
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    return jsonify(
        {
            "contact": [dict(r) for r in db.execute("SELECT * FROM contact_messages ORDER BY id DESC LIMIT 50")],
            "quotes": [dict(r) for r in db.execute("SELECT * FROM quote_requests ORDER BY id DESC LIMIT 50")],
            "facilitate": [dict(r) for r in db.execute("SELECT * FROM facilitator_applications ORDER BY id DESC LIMIT 50")],
            "exams": [dict(r) for r in db.execute("SELECT * FROM exam_attempts ORDER BY id DESC LIMIT 50")],
            "clubs": [dict(r) for r in db.execute("SELECT id, name, status, created_at FROM clubs ORDER BY id DESC LIMIT 50")],
            "mentor": [dict(r) for r in db.execute("SELECT * FROM mentor_requests ORDER BY id DESC LIMIT 50")],
            "career": [dict(r) for r in db.execute("SELECT * FROM career_requests ORDER BY id DESC LIMIT 50")],
        }
    )


def cms_payload(db):
    photos = {r["slot"]: dict(r) for r in db.execute("SELECT * FROM cms_photos ORDER BY slot")}
    settings = {r["key"]: r["value"] for r in db.execute("SELECT key, value FROM cms_settings")}
    instructors = [
        dict(r)
        for r in db.execute(
            "SELECT * FROM cms_instructors WHERE published = 1 ORDER BY sort_order, id"
        )
    ]
    cards = [
        dict(r)
        for r in db.execute("SELECT * FROM cms_cards WHERE published = 1 ORDER BY section, sort_order, id")
    ]
    pages = {r["page_key"]: dict(r) for r in db.execute("SELECT * FROM cms_pages")}
    gallery = [
        dict(r)
        for r in db.execute("SELECT * FROM cms_gallery WHERE published = 1 ORDER BY sort_order, id")
    ]
    sessions = [
        dict(r) for r in db.execute("SELECT * FROM cms_sessions WHERE published = 1 ORDER BY id DESC")
    ]
    messages = [
        dict(r) for r in db.execute("SELECT * FROM cms_messages ORDER BY id DESC LIMIT 20")
    ]
    return {
        "photos": photos,
        "settings": settings,
        "instructors": instructors,
        "cards": cards,
        "pages": pages,
        "gallery": gallery,
        "sessions": sessions,
        "messages": messages,
    }


@app.route("/api/cms")
def cms_public():
    return jsonify(cms_payload(get_db()))


@app.route("/api/admin/cms")
def admin_cms():
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    data = cms_payload(db)
    data["instructors"] = [dict(r) for r in db.execute("SELECT * FROM cms_instructors ORDER BY sort_order, id")]
    data["cards"] = [dict(r) for r in db.execute("SELECT * FROM cms_cards ORDER BY section, sort_order, id")]
    data["gallery"] = [dict(r) for r in db.execute("SELECT * FROM cms_gallery ORDER BY sort_order, id")]
    data["sessions"] = [dict(r) for r in db.execute("SELECT * FROM cms_sessions ORDER BY id DESC")]
    data["messages"] = [dict(r) for r in db.execute("SELECT * FROM cms_messages ORDER BY id DESC LIMIT 80")]
    data["users"] = [row_user(r) for r in db.execute("SELECT * FROM users ORDER BY id DESC LIMIT 200")]
    data["me"] = user if isinstance(user, dict) else row_user(user)
    return jsonify(data)


@app.route("/api/admin/upload", methods=["POST"])
def admin_upload():
    user, err = require_admin()
    if err:
        return err
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "Pick a photo."}), 400
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_UPLOAD:
        return jsonify({"error": "Use jpg, png, webp, gif, or svg."}), 400
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    name = secrets.token_hex(8) + "-" + secure_filename(file.filename)
    path = os.path.join(UPLOAD_DIR, name)
    file.save(path)
    url = "/uploads/cms/" + name
    slot = (request.form.get("slot") or "").strip()
    db = get_db()
    if slot:
        existing = db.execute("SELECT id FROM cms_photos WHERE slot = ?", (slot,)).fetchone()
        if existing:
            db.execute(
                "UPDATE cms_photos SET url = ?, alt = ?, updated_at = ? WHERE slot = ?",
                (url, request.form.get("alt") or slot, utcnow(), slot),
            )
        else:
            db.execute(
                "INSERT INTO cms_photos (slot, url, alt, updated_at) VALUES (?, ?, ?, ?)",
                (slot, url, request.form.get("alt") or slot, utcnow()),
            )
        db.commit()
    return jsonify({"url": url, "slot": slot})


@app.route("/api/admin/instructors", methods=["POST"])
def admin_instructor_create():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    if len(name) < 2:
        return jsonify({"error": "Instructor name."}), 400
    db = get_db()
    st = style_from(body)
    cur = db.execute(
        """
        INSERT INTO cms_instructors (name, title, bio, photo_url, sort_order, published, overlay_color, overlay_opacity, img_opacity, photo_h, bw, brightness)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            (body.get("title") or "").strip(),
            (body.get("bio") or "").strip(),
            (body.get("photo_url") or "").strip(),
            int(body.get("sort_order") or 0),
            1 if body.get("published", 1) else 0,
        )
        + style_tuple(st),
    )
    db.commit()
    row = db.execute("SELECT * FROM cms_instructors WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row))


@app.route("/api/admin/instructors/<int:iid>", methods=["PUT"])
def admin_instructor_update(iid):
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM cms_instructors WHERE id = ?", (iid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found."}), 404
    db.execute(
        """
        UPDATE cms_instructors
        SET name = ?, title = ?, bio = ?, photo_url = ?, sort_order = ?, published = ?,
            overlay_color = ?, overlay_opacity = ?, img_opacity = ?, photo_h = ?, bw = ?, brightness = ?
        WHERE id = ?
        """,
        (
            (body.get("name") or row["name"]).strip(),
            (body.get("title") if "title" in body else row["title"]) or "",
            (body.get("bio") if "bio" in body else row["bio"]) or "",
            (body.get("photo_url") if "photo_url" in body else row["photo_url"]) or "",
            int(body.get("sort_order") if body.get("sort_order") is not None else row["sort_order"]),
            1 if body.get("published", row["published"]) else 0,
            *style_tuple(style_from(body, row)),
            iid,
        ),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_instructors WHERE id = ?", (iid,)).fetchone()))


@app.route("/api/admin/instructors/<int:iid>", methods=["DELETE"])
def admin_instructor_delete(iid):
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    db.execute("DELETE FROM cms_instructors WHERE id = ?", (iid,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/photos", methods=["POST"])
def admin_photo_create():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    slot = (body.get("slot") or "").strip()
    url = (body.get("url") or "").strip()
    if not slot or not url:
        return jsonify({"error": "Slot and photo URL."}), 400
    db = get_db()
    try:
        st = style_from(body)
        cur = db.execute(
            "INSERT INTO cms_photos (slot, url, alt, updated_at, overlay_color, overlay_opacity, img_opacity, photo_h, bw, brightness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (slot, url, (body.get("alt") or slot).strip(), utcnow()) + style_tuple(st),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "That slot already exists. Edit it instead."}), 409
    return jsonify(dict(db.execute("SELECT * FROM cms_photos WHERE id = ?", (cur.lastrowid,)).fetchone()))


@app.route("/api/admin/photos/<int:pid>", methods=["PUT"])
def admin_photo_update(pid):
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM cms_photos WHERE id = ?", (pid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found."}), 404
    st = style_from(body, row)
    db.execute(
        """
        UPDATE cms_photos
        SET slot = ?, url = ?, alt = ?, updated_at = ?,
            overlay_color = ?, overlay_opacity = ?, img_opacity = ?, photo_h = ?, bw = ?, brightness = ?
        WHERE id = ?
        """,
        (
            (body.get("slot") or row["slot"]).strip(),
            (body.get("url") or row["url"]).strip(),
            (body.get("alt") if "alt" in body else row["alt"]) or "",
            utcnow(),
            *style_tuple(st),
            pid,
        ),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_photos WHERE id = ?", (pid,)).fetchone()))


@app.route("/api/admin/photos/<int:pid>", methods=["DELETE"])
def admin_photo_delete(pid):
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    db.execute("DELETE FROM cms_photos WHERE id = ?", (pid,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/cards", methods=["POST"])
def admin_card_create():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    title = (body.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Card title."}), 400
    db = get_db()
    st = style_from(body)
    cur = db.execute(
        """
        INSERT INTO cms_cards (section, title, body, href, cta, image_url, color, sort_order, published, overlay_color, overlay_opacity, img_opacity, photo_h, bw, brightness)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            (body.get("section") or "home").strip(),
            title,
            (body.get("body") or "").strip(),
            (body.get("href") or "").strip(),
            (body.get("cta") or "").strip(),
            (body.get("image_url") or "").strip(),
            (body.get("color") or "").strip(),
            int(body.get("sort_order") or 0),
            1 if body.get("published", 1) else 0,
        )
        + style_tuple(st),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_cards WHERE id = ?", (cur.lastrowid,)).fetchone()))


@app.route("/api/admin/cards/<int:cid>", methods=["PUT"])
def admin_card_update(cid):
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM cms_cards WHERE id = ?", (cid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found."}), 404
    db.execute(
        """
        UPDATE cms_cards
        SET section = ?, title = ?, body = ?, href = ?, cta = ?, image_url = ?, color = ?, sort_order = ?, published = ?,
            overlay_color = ?, overlay_opacity = ?, img_opacity = ?, photo_h = ?, bw = ?, brightness = ?
        WHERE id = ?
        """,
        (
            (body.get("section") if "section" in body else row["section"]) or "",
            (body.get("title") or row["title"]).strip(),
            (body.get("body") if "body" in body else row["body"]) or "",
            (body.get("href") if "href" in body else row["href"]) or "",
            (body.get("cta") if "cta" in body else row["cta"]) or "",
            (body.get("image_url") if "image_url" in body else row["image_url"]) or "",
            (body.get("color") if "color" in body else row["color"]) or "",
            int(body.get("sort_order") if body.get("sort_order") is not None else row["sort_order"]),
            1 if body.get("published", row["published"]) else 0,
            *style_tuple(style_from(body, row)),
            cid,
        ),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_cards WHERE id = ?", (cid,)).fetchone()))


@app.route("/api/admin/cards/<int:cid>", methods=["DELETE"])
def admin_card_delete(cid):
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    db.execute("DELETE FROM cms_cards WHERE id = ?", (cid,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/settings", methods=["PUT"])
def admin_settings():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    db = get_db()
    for key, value in body.items():
        db.execute(
            "INSERT INTO cms_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (str(key), str(value)),
        )
    db.commit()
    return jsonify({r["key"]: r["value"] for r in db.execute("SELECT key, value FROM cms_settings")})


@app.route("/api/admin/users")
def admin_users():
    user, err = require_admin()
    if err:
        return err
    return jsonify([row_user(r) for r in get_db().execute("SELECT * FROM users ORDER BY id DESC LIMIT 300")])


@app.route("/api/admin/users/<int:uid>", methods=["DELETE"])
def admin_user_delete(uid):
    user, err = require_admin()
    if err:
        return err
    if uid == user["id"]:
        return jsonify({"error": "You cannot delete the desk you are using."}), 400
    db = get_db()
    target = db.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    if not target:
        return jsonify({"error": "Not found."}), 404
    target_u = row_user(target)
    if target_u.get("is_owner"):
        return jsonify({"error": "The owner desk cannot be deleted."}), 403
    if target_u.get("role") == "admin" and not user_is_owner(user):
        return jsonify({"error": "Staff cannot delete another desk."}), 403
    db.execute("DELETE FROM users WHERE id = ?", (uid,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/staff", methods=["POST"])
def admin_staff_create():
    user, err = require_owner()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip().lower()
    username = (body.get("username") or "").strip().lower()
    password = body.get("password") or ""
    if len(name) < 2 or "@" not in email or len(username) < 3 or len(password) < 8:
        return jsonify({"error": "Name, email, username (3+), and a password of 8+ characters."}), 400
    db = get_db()
    try:
        cur = db.execute(
            """
            INSERT INTO users (name, email, username, password_hash, campus, role, status, auth_provider, is_owner, created_at)
            VALUES (?, ?, ?, ?, ?, 'admin', 'approved', 'password', 0, ?)
            """,
            (name, email, username, hash_password(password), "Desk", utcnow()),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "That email or username is already on a seat."}), 409
    row = db.execute("SELECT * FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_user(row))


@app.route("/api/admin/pages", methods=["PUT"])
def admin_pages_update():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    page_key = (body.get("page_key") or "").strip()
    if not page_key:
        return jsonify({"error": "Page key."}), 400
    db = get_db()
    db.execute(
        """
        INSERT INTO cms_pages (page_key, kicker, title, lead)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(page_key) DO UPDATE SET
            kicker = excluded.kicker,
            title = excluded.title,
            lead = excluded.lead
        """,
        (
            page_key,
            (body.get("kicker") or "").strip(),
            (body.get("title") or "").strip(),
            (body.get("lead") or "").strip(),
        ),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_pages WHERE page_key = ?", (page_key,)).fetchone()))


@app.route("/api/admin/pages/<page_key>", methods=["DELETE"])
def admin_pages_delete(page_key):
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    db.execute("DELETE FROM cms_pages WHERE page_key = ?", (page_key,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/gallery", methods=["POST"])
def admin_gallery_create():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    title = (body.get("title") or "").strip()
    photo = (body.get("photo_url") or "").strip()
    if not title or not photo:
        return jsonify({"error": "Title and photo."}), 400
    db = get_db()
    st = style_from(body)
    cur = db.execute(
        "INSERT INTO cms_gallery (title, caption, photo_url, sort_order, published, overlay_color, overlay_opacity, img_opacity, photo_h, bw, brightness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (title, (body.get("caption") or "").strip(), photo, int(body.get("sort_order") or 0), 1 if body.get("published", 1) else 0) + style_tuple(st),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_gallery WHERE id = ?", (cur.lastrowid,)).fetchone()))


@app.route("/api/admin/gallery/<int:gid>", methods=["PUT"])
def admin_gallery_update(gid):
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM cms_gallery WHERE id = ?", (gid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found."}), 404
    db.execute(
        """
        UPDATE cms_gallery
        SET title = ?, caption = ?, photo_url = ?, sort_order = ?, published = ?,
            overlay_color = ?, overlay_opacity = ?, img_opacity = ?, photo_h = ?, bw = ?, brightness = ?
        WHERE id = ?
        """,
        (
            (body.get("title") or row["title"]).strip(),
            (body.get("caption") if "caption" in body else row["caption"]) or "",
            (body.get("photo_url") or row["photo_url"]).strip(),
            int(body.get("sort_order") if body.get("sort_order") is not None else row["sort_order"]),
            1 if body.get("published", row["published"]) else 0,
            *style_tuple(style_from(body, row)),
            gid,
        ),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_gallery WHERE id = ?", (gid,)).fetchone()))


@app.route("/api/admin/gallery/<int:gid>", methods=["DELETE"])
def admin_gallery_delete(gid):
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    db.execute("DELETE FROM cms_gallery WHERE id = ?", (gid,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/sessions", methods=["POST"])
def admin_session_create():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    title = (body.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Session title."}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO cms_sessions (title, starts_at, join_url, notes, published) VALUES (?, ?, ?, ?, ?)",
        (
            title,
            (body.get("starts_at") or "").strip(),
            (body.get("join_url") or "").strip(),
            (body.get("notes") or "").strip(),
            1 if body.get("published", 1) else 0,
        ),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_sessions WHERE id = ?", (cur.lastrowid,)).fetchone()))


@app.route("/api/admin/sessions/<int:sid>", methods=["PUT"])
def admin_session_update(sid):
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM cms_sessions WHERE id = ?", (sid,)).fetchone()
    if not row:
        return jsonify({"error": "Not found."}), 404
    db.execute(
        "UPDATE cms_sessions SET title = ?, starts_at = ?, join_url = ?, notes = ?, published = ? WHERE id = ?",
        (
            (body.get("title") or row["title"]).strip(),
            (body.get("starts_at") if "starts_at" in body else row["starts_at"]) or "",
            (body.get("join_url") if "join_url" in body else row["join_url"]) or "",
            (body.get("notes") if "notes" in body else row["notes"]) or "",
            1 if body.get("published", row["published"]) else 0,
            sid,
        ),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_sessions WHERE id = ?", (sid,)).fetchone()))


@app.route("/api/admin/sessions/<int:sid>", methods=["DELETE"])
def admin_session_delete(sid):
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    db.execute("DELETE FROM cms_sessions WHERE id = ?", (sid,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/admin/messages", methods=["POST"])
def admin_message_create():
    user, err = require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    text = (body.get("body") or "").strip()
    if not text:
        return jsonify({"error": "Write a note."}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO cms_messages (from_user_id, from_name, body, created_at) VALUES (?, ?, ?, ?)",
        (user["id"], user.get("name") or "Desk", text, utcnow()),
    )
    db.commit()
    return jsonify(dict(db.execute("SELECT * FROM cms_messages WHERE id = ?", (cur.lastrowid,)).fetchone()))


@app.route("/api/admin/messages/<int:mid>", methods=["DELETE"])
def admin_message_delete(mid):
    user, err = require_admin()
    if err:
        return err
    db = get_db()
    db.execute("DELETE FROM cms_messages WHERE id = ?", (mid,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/uploads/<path:path>")
def uploaded_file(path):
    return send_from_directory(os.path.join(ROOT, "uploads"), path)


@app.route("/")
def root():
    return send_from_directory(ROOT, "index.html")


@app.route("/<path:path>")
def static_proxy(path):
    full = os.path.join(ROOT, path)
    if os.path.isdir(full):
        return send_from_directory(full, "index.html")
    if os.path.isfile(full):
        return send_from_directory(ROOT, path)
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()
    print("Nethub lab server  http://127.0.0.1:8765")
    print("Student signup     /register.html")
    print("Desk login         admin@nethub.club  /  admin  /  admin1234")
    app.run(host="127.0.0.1", port=8765, debug=False)
