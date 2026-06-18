#!/usr/bin/env python3
"""Generate README.md from config.yaml.

Eliminates duplicated badge patterns, color constants, and structural
boilerplate by deriving everything from a single config source.
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"
OUTPUT_PATH = ROOT / "README.md"

# ─── Shared Badge Utilities ─────────────────────────────────────────────────


def shields_badge(
    label: str,
    message: str,
    *,
    color: str,
    style: str,
    logo: str | None = None,
    logo_color: str | None = None,
    label_color: str | None = None,
) -> str:
    """Build a shields.io badge URL."""
    encoded_label = label.replace(" ", "%20").replace("/", "%2F")
    encoded_msg = message.replace(" ", "%20").replace("-", "--")
    url = f"https://img.shields.io/badge/{encoded_label}-{encoded_msg}-{color}?style={style}"
    if logo:
        url += f"&logo={logo}"
    if logo_color:
        url += f"&logoColor={logo_color}"
    if label_color:
        url += f"&labelColor={label_color}"
    return url


def simple_badge(name: str, *, bg: str, style: str, logo: str, logo_color: str) -> str:
    """Build a simple single-message badge (no label/message split)."""
    encoded = name.replace(" ", "%20").replace("-", "--")
    return f"https://img.shields.io/badge/{encoded}-{bg}?style={style}&logo={logo}&logoColor={logo_color}"


def resolve_color(color_name: str, theme: dict) -> str:
    """Resolve a color name to its hex value using the theme palette."""
    return theme["colors"].get(color_name, color_name)


# ─── Section Generators ─────────────────────────────────────────────────────


def gen_header(cfg: dict) -> str:
    profile = cfg["profile"]
    theme = cfg["theme"]
    bg = theme["bg"]
    blue = resolve_color("blue", theme)

    lines_param = ";".join(profile["typing_lines"])

    header_badges = []
    badge_items = [
        ("Email", f"sakshibhatia696%40gmail.com", f"mailto:{profile['email']}", "gmail"),
        ("LinkedIn", "sakshibhatia", profile["linkedin_url"], "linkedin"),
        ("GitHub", profile["username"], profile["github_url"], "github"),
    ]
    logo_colors = [blue, blue, "e6edf3"]
    for (label, msg, url, logo), lc in zip(badge_items, logo_colors):
        badge_url = shields_badge(
            label,
            msg,
            color=bg,
            style=theme["badge_style_header"],
            logo=logo,
            logo_color=lc,
            label_color=theme["bg_secondary"],
        )
        header_badges.append(f"[![{label}]({badge_url})]({url})")

    edu_badges = []
    for b in cfg["education"]["header_badges"]:
        color = resolve_color(b["color"], theme)
        badge_url = shields_badge(
            b["label"],
            b["message"],
            color=color,
            style=theme["badge_style"],
            label_color=bg,
        )
        alt_text = b["label"].replace("_", " ")
        edu_badges.append(f"![{alt_text}]({badge_url})")

    location_badge = f"![Location](https://img.shields.io/badge/\U0001f4cd_India-{bg}?style={theme['badge_style']}&labelColor={bg}&color={theme['border']})"

    return f"""<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:{bg},50:1a2a3a,100:{bg}&height=130&section=header&text=Sakshi%20Bhatia&fontColor={blue}&fontSize=42&fontAlignY=65&animation=fadeIn" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=17&pause=1000&color={blue.upper()}&center=true&width=620&lines={lines_param}" />

<br/>

{chr(10).join(header_badges)}

<br/>

{chr(10).join(edu_badges)}
{location_badge}

</div>"""


def gen_about(cfg: dict) -> str:
    return """---

## 👩‍💻 Who Am I?

```python
class SakshiBhatia:
    def __init__(self):
        self.role       = "Full-Stack Developer & Software Engineer"
        self.education  = [
            "IIIT Jabalpur — B.Tech ECE (2024–Present)",
            "IIT Madras   — BS Data Science (2024–Present)"
        ]
        self.stack      = ["Next.js", "React", "FastAPI", "PostgreSQL", "Docker", "GCP"]
        self.ml_tools   = ["PyTorch", "OpenCV", "HuggingFace", "scikit-learn"]
        self.superpower = ["Hackathons", "Open Source", "Robotics", "IoT", "Chess ♟"]
        self.values     = ["Ship fast", "Think deep", "Build for real users"]
        self.open_to    = ["Internships", "Open Source Collabs", "Research", "SWE Roles"]
        self.fun_fact   = "I program drones AND debug at 3 AM — sometimes both at once"
        self.currently  = "Building things that actually matter 🚀"

    def greet(self):
        print("Thanks for stopping by — let's build something great together!")

me = SakshiBhatia()
me.greet()
```

> 🎯 **I am a dual-degree student** (ECE + Data Science) who bridges hardware intuition with software craftsmanship. I thrive at the intersection of **web engineering**, **ML systems**, and **competitive problem solving** — and I bring that cross-domain thinking to every project I touch."""


def gen_education(cfg: dict) -> str:
    rows = cfg["education"]["table"]
    table_rows = "\n".join(
        f"| {r.get('prefix', '**')}{r['institution']}{r.get('suffix', '**')} | {r['degree']} | {r['year']} |"
        for r in rows
    )
    return f"""---

## 🎓 Education

| 🏛️ Institution | 📘 Degree | 📅 Year |
|---|---|---|
{table_rows}

📚 **Key Courses:** {cfg['education']['courses']}"""


def gen_tech_stack(cfg: dict) -> str:
    theme = cfg["theme"]
    bg = theme["bg"]
    style = theme["badge_style"]

    def render_column(col_cfg: dict) -> str:
        lines = [f"### {col_cfg['title']}"]
        for b in col_cfg["badges"]:
            logo_color = resolve_color(b["color"], theme)
            if "level" in b:
                url = shields_badge(
                    b["name"],
                    b["level"],
                    color=logo_color,
                    style=style,
                    logo=b["logo"],
                    logo_color="white",
                    label_color=bg,
                )
            else:
                url = simple_badge(
                    b["name"], bg=bg, style=style, logo=b["logo"], logo_color=logo_color
                )
            lines.append(f"![{b['name']}]({url})")
        return "\n".join(lines)

    languages = render_column(cfg["tech_stack"]["languages"])
    frameworks = render_column(cfg["tech_stack"]["frameworks"])
    ml = render_column(cfg["tech_stack"]["ml"])

    return f"""---

## ⚙️ Tech Stack & Toolkit

<table>
<tr>
<td valign="top" width="33%">

{languages}

</td>
<td valign="top" width="33%">

{frameworks}

</td>
<td valign="top" width="33%">

{ml}

</td>
</tr>
</table>"""


def gen_projects(cfg: dict) -> str:
    sections = ["---\n\n## 🚀 Featured Projects\n\n> Each project below solves a real problem. Click to explore the code."]
    for p in cfg["projects"]:
        tags = " ".join(f"`{t}`" for t in p["tags"])
        title = f"{p['icon']} [{p['name']}]({p['url']})"
        if p.get("subtitle"):
            title += f" — {p['subtitle']}"
        highlights = "\n".join(f"- {h}" for h in p["highlights"])
        sections.append(
            f"---\n\n### {title}\n{tags}\n\n> {p['description']}\n\n{highlights}"
        )
    return "\n\n".join(sections)


def gen_achievements(cfg: dict) -> str:
    rows = "\n".join(
        f"| {a['icon']} **{a['title']}** | {a['details']} |"
        for a in cfg["achievements"]
    )
    return f"""---

## 🏆 Achievements & Recognition

| 🏅 Achievement | 📋 Details |
|---|---|
{rows}"""


def gen_open_source() -> str:
    return """---

## 🌱 Open Source & Problem Solving

```text
💡 Philosophy: Code should be readable by humans first, machines second.

🔍 Areas I contribute to:
   ├── Developer tools & productivity extensions
   ├── Computer vision & real-time ML systems
   ├── Backend APIs & database-optimized architectures
   └── IoT & embedded systems (drone programming ✈️)

📬 Open to:
   ├── Open source collaborations — especially in AI/ML, web, or systems
   ├── Pair programming, code reviews & mentoring
   └── Hackathon teams — I've won before, let's win together
```

> 🤝 If you're working on something interesting, [reach out](mailto:sakshibhatia696@gmail.com) — I love collaborating on real-world problems."""


def gen_stats(cfg: dict) -> str:
    theme = cfg["theme"]
    bg = theme["bg"]
    blue = resolve_color("blue", theme)
    green = resolve_color("green", theme)
    yellow = resolve_color("yellow", theme)
    border = theme["border"]
    username = cfg["profile"]["username"]

    return f"""---

## 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme=github_dark&hide_border=true&bg_color={bg}&title_color={blue}&icon_color={green}&include_all_commits=true&count_private=true" height="170"/>
  &nbsp;
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme=github_dark&hide_border=true&bg_color={bg}&title_color={blue}&langs_count=8" height="170"/>
</p>

<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user={username}&theme=github-dark-blue&hide_border=true&background={bg}&stroke={border}&ring={blue}&fire={yellow}&currStreakLabel={blue}" width="520"/>
</p>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username={username}&bg_color={bg}&color={blue}&line={green}&point={yellow}&area=true&hide_border=true" width="100%"/>
</p>"""


def gen_leadership(cfg: dict) -> str:
    sections = []
    for item in cfg["leadership"]:
        org_part = f" *({item['org']})*" if item.get("org") else ""
        sections.append(f"**{item['role']}**{org_part}\n{item['description']}")
    return "---\n\n## 🤝 Leadership & Community\n\n" + "\n\n".join(sections)


def gen_contact(cfg: dict) -> str:
    profile = cfg["profile"]
    return f"""---

## 📬 Let's Connect & Collaborate

<div align="center">

| 🌐 Platform | 🔗 Link |
|---|---|
| 📧 Email | [{profile['email']}](mailto:{profile['email']}) |
| 💼 LinkedIn | [linkedin.com/in/sakshibhatia]({profile['linkedin_url']}) |
| 🐙 GitHub | [github.com/{profile['username']}]({profile['github_url']}) |
| 📱 Phone | {profile['phone']} |

</div>

> 💬 I'm always open to discussing **new projects**, **open source ideas**, **internship opportunities**, or just a good tech conversation. Don't hesitate to ping me!"""


def gen_footer(cfg: dict) -> str:
    bg = cfg["theme"]["bg"]
    return f"""---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:{bg},50:1a2a3a,100:{bg}&height=90&section=footer" width="100%"/>

**"Build with intention. Ship with pride. Learn always."**

<sub>ECE × Data Science × Open Source × Robotics × Chess ♟ · Made with 💙 by Sakshi</sub>
</div>"""


# ─── Main ───────────────────────────────────────────────────────────────────


def main() -> None:
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)

    sections = [
        gen_header(cfg),
        gen_about(cfg),
        gen_education(cfg),
        gen_tech_stack(cfg),
        gen_projects(cfg),
        gen_achievements(cfg),
        gen_open_source(),
        gen_stats(cfg),
        gen_leadership(cfg),
        gen_contact(cfg),
        gen_footer(cfg),
    ]

    readme = "\n\n".join(sections) + "\n"
    OUTPUT_PATH.write_text(readme)
    print(f"✓ Generated {OUTPUT_PATH} ({len(readme)} bytes)")


if __name__ == "__main__":
    main()
