class SkillNormalizer:

    SKILL_MAP = {
        "js": "JavaScript",
        "javascript": "JavaScript",
        "java script": "JavaScript",

        "py": "Python",
        "python": "Python",

        "java": "Java",

        "reactjs": "React",
        "react": "React",

        "node": "Node.js",
        "nodejs": "Node.js",

        "aws": "AWS",

        "sql": "SQL",
        "mysql": "MySQL",

        "html": "HTML",
        "css": "CSS",

        "git": "Git",
        "docker": "Docker",

        "c": "C",
        "c++": "C++"
    }

    @staticmethod
    def normalize(skill: str) -> str:

        return SkillNormalizer.SKILL_MAP.get(
            skill.lower().strip(),
            skill.strip()
        )