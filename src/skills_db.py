# src/skills_db.py

# Categorized skills database
SKILLS_DB = {
    "programming_languages": [
        "python", "java", "c", "c++", "c#", "r", "go", "scala",
        "javascript", "typescript", "kotlin", "swift", "php", "ruby",
        "perl", "objective-c", "rust", "matlab", "shell scripting",
        "bash", "powershell"
    ],

    "web_development": [
        "html", "html5", "css", "css3", "sass", "less", "jquery",
        "bootstrap", "react", "angular", "vue", "node.js", "express",
        "next.js", "nuxt.js", "svelte"
    ],

    "backend_frameworks": [
        "spring", "spring boot", "spring mvc", "hibernate", "jsp",
        "servlets", "django", "flask", "fastapi", "laravel", "symfony",
        "rails", "asp.net"
    ],

    "databases": [
        "mysql", "postgresql", "mongodb", "oracle", "sql server", "sqlite",
        "redis", "cassandra", "dynamodb", "couchdb", "snowflake", "bigquery"
    ],

    "cloud_devops": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "jenkins", "terraform", "ansible", "puppet", "chef", "openshift",
        "linux", "unix", "git", "github", "gitlab", "bitbucket",
        "devops", "ci/cd", "helm"
    ],

    "data_engineering": [
        "hadoop", "spark", "pyspark", "airflow", "kafka", "etl",
        "databricks", "hive", "pig", "oozie"
    ],

    "machine_learning": [
        "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn",
        "tensorflow", "keras", "pytorch", "nlp", "deep learning",
        "machine learning", "computer vision", "opencv", "transformers"
    ],

    "mobile_development": [
        "android", "ios", "react native", "flutter", "xamarin", "ionic"
    ],

    "tools_ides": [
        "postman", "eclipse", "intellij", "pycharm", "netbeans",
        "visual studio", "visual studio code", "vscode", "jira",
        "confluence", "trello", "slack", "maven", "gradle", "ant"
    ],

    "testing_qa": [
        "selenium", "junit", "testng", "cucumber", "jest", "mocha",
        "chai", "karma", "pytest", "unittest", "postman testing"
    ],

    "soft_skills": [
        "communication", "teamwork", "problem solving", "leadership",
        "adaptability", "collaboration", "time management",
        "critical thinking", "creativity", "self-motivation",
        "analytical skills", "presentation", "negotiation", "mentoring",
        "decision making"
    ],

    "methodologies": [
        "agile", "scrum", "kanban", "waterfall", "sdlc", "project management",
        "stakeholder management", "requirements analysis", "design patterns",
        "uml", "risk management", "quality assurance"
    ]
}

# Aliases / Synonyms for better matching
ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "psql": "postgresql",
    "postgres": "postgresql",
    "node": "node.js",
    "expressjs": "express",
    "oop": "object oriented programming",
    "ci/cd": "cicd",
    "c sharp": "c#",
    "cpp": "c++",
    "dot net": "asp.net"
}

# Flatten all categories into one set for easy matching
ALL_SKILLS = set()
for category, skills in SKILLS_DB.items():
    ALL_SKILLS.update(skill.lower() for skill in skills)

# Also include alias values so they are recognized
ALL_SKILLS.update(ALIASES.values())
