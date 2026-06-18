"""Profile module for Sakshi Bhatia — extracted from README.md."""


class SakshiBhatia:
    """Represents Sakshi Bhatia's developer profile."""

    def __init__(self):
        self.role = "Full-Stack Developer & Software Engineer"
        self.education = [
            "IIIT Jabalpur — B.Tech ECE (2024–Present)",
            "IIT Madras   — BS Data Science (2024–Present)",
        ]
        self.stack = ["Next.js", "React", "FastAPI", "PostgreSQL", "Docker", "GCP"]
        self.ml_tools = ["PyTorch", "OpenCV", "HuggingFace", "scikit-learn"]
        self.superpower = ["Hackathons", "Open Source", "Robotics", "IoT", "Chess ♟"]
        self.values = ["Ship fast", "Think deep", "Build for real users"]
        self.open_to = ["Internships", "Open Source Collabs", "Research", "SWE Roles"]
        self.fun_fact = (
            "I program drones AND debug at 3 AM — sometimes both at once"
        )
        self.currently = "Building things that actually matter"

    def greet(self):
        """Return a greeting message."""
        return "Thanks for stopping by — let's build something great together!"

    def has_skill(self, skill):
        """Check whether *skill* appears in the tech stack or ML tools."""
        combined = [s.lower() for s in self.stack + self.ml_tools]
        return skill.lower() in combined

    def is_open_to(self, opportunity):
        """Check whether *opportunity* is in the open-to list (case-insensitive)."""
        return opportunity.lower() in [o.lower() for o in self.open_to]

    def add_skill(self, skill, category="stack"):
        """Add a skill to the given category ('stack' or 'ml_tools').

        Raises ValueError for an unknown category.
        Returns True if the skill was added, False if it already existed.
        """
        if category not in ("stack", "ml_tools"):
            raise ValueError(f"Unknown category: {category!r}")
        target = getattr(self, category)
        if skill in target:
            return False
        target.append(skill)
        return True

    def remove_skill(self, skill):
        """Remove a skill from stack or ml_tools.

        Returns the category it was removed from, or None if not found.
        """
        for cat in ("stack", "ml_tools"):
            target = getattr(self, cat)
            if skill in target:
                target.remove(skill)
                return cat
        return None

    def summary(self):
        """Return a concise one-line profile summary."""
        return f"{self.role} | {len(self.stack)} stack items | {len(self.ml_tools)} ML tools"

    def education_count(self):
        """Return the number of education entries."""
        return len(self.education)

    def all_skills(self):
        """Return the union of stack and ml_tools as a sorted list."""
        return sorted(set(self.stack + self.ml_tools))
