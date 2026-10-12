"""
MatchCrewAI - Team Matching Engine (Logical / Rule-Based AI)

Idea: score any team with a transparent weighted formula, then build the
team greedily: at each step add the student who raises the team score most.
"""
import ast
from collections import Counter
import pandas as pd

# Weights add up to 1.0 - easy to explain and easy to change
WEIGHTS = {"skills": 0.40, "domains": 0.20, "roles": 0.15,
           "availability": 0.15, "experience": 0.10}


def load_students(path="data/students_clean.csv"):
    df = pd.read_csv(path)
    students = []
    for _, r in df.iterrows():
        students.append({
            "name": r["Full Name"],
            "skills": {s.strip().lower() for s in ast.literal_eval(r["Technical Skills"])},
            "domains": {d.strip().lower() for d in ast.literal_eval(r["Preferred Domain(s)"])},
            "role": r["Preferred Role"],
            "availability": r["Availability"],
            "experience": r["Overall Experience Level"],
        })
    return students


def score_team(team, req_skills, req_domains):
    """Return each component as 0-1, plus the weighted total."""
    team_skills = set().union(*[m["skills"] for m in team])
    team_domains = set().union(*[m["domains"] for m in team])

    skills = len(req_skills & team_skills) / len(req_skills) if req_skills else 1.0
    domains = len(req_domains & team_domains) / len(req_domains) if req_domains else 1.0
    roles = len({m["role"] for m in team}) / len(team)
    availability = Counter(m["availability"] for m in team).most_common(1)[0][1] / len(team)
    experience = len({m["experience"] for m in team}) / min(3, len(team))

    parts = {"skills": skills, "domains": domains, "roles": roles,
             "availability": availability, "experience": experience}
    total = sum(parts[k] * WEIGHTS[k] for k in WEIGHTS)
    return parts, total


def form_team(students, req_skills, req_domains, team_size=4):
    """Greedy: repeatedly add the student who increases the team score most."""
    team, pool = [], students[:]
    while len(team) < team_size and pool:
        best = max(pool, key=lambda s: score_team(team + [s], req_skills, req_domains)[1])
        team.append(best)
        pool.remove(best)
    return team


def explain(parts, missing):
    lines = []
    lines.append("Strong skill coverage" if parts["skills"] >= 0.8 else
                 "Partial skill coverage" if parts["skills"] >= 0.5 else "Weak skill coverage")
    lines.append("Domain interests match the project" if parts["domains"] >= 0.7
                 else "Some project domains are not covered")
    lines.append("Good role diversity" if parts["roles"] >= 0.75
                 else "Role overlap: several members want the same role")
    lines.append("High availability overlap" if parts["availability"] >= 0.6
                 else "Availability may cause scheduling conflicts")
    lines.append("Balanced experience levels" if parts["experience"] >= 0.66
                 else "Experience levels are uneven")
    if missing:
        lines.append("Skill gap - nobody in the team has: " + ", ".join(sorted(missing)))
    return lines


def match(project_name, req_skills, req_domains, team_size=4):
    students = load_students()
    req_skills = {s.lower() for s in req_skills}
    req_domains = {d.lower() for d in req_domains}

    team = form_team(students, req_skills, req_domains, team_size)
    parts, total = score_team(team, req_skills, req_domains)
    team_skills = set().union(*[m["skills"] for m in team])
    missing = req_skills - team_skills

    print(f"\nProject: {project_name}")
    print(f"Required skills : {', '.join(sorted(req_skills))}")
    print(f"Required domains: {', '.join(sorted(req_domains))}\n")
    print("Recommended team:")
    for m in team:
        print(f"  - {m['name']:<18} {m['role']:<24} {m['availability']:<16} {m['experience']}")
    print(f"\nTeam compatibility score: {total * 100:.1f}%")
    for k in WEIGHTS:
        print(f"  {k:<13} {parts[k] * 100:5.1f}%   (weight {int(WEIGHTS[k] * 100)}%)")
    print("\nWhy this team:")
    for line in explain(parts, missing):
        print("  *", line)


if __name__ == "__main__":
    match(
        "AI-powered healthcare assistant",
        req_skills=["Python", "Machine Learning", "React", "SQL", "Figma"],
        req_domains=["AI/ML", "Web Development", "UI/UX"],
        team_size=5,
    )