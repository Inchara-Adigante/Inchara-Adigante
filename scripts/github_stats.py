"""
Build the profile's GitHub activity cards from GitHub's own API, so they're never stale or cached by a third party.

Writes three SVGs into assets/:
    stats.svg          contributions this year and all time, current and longest streak, PRs, repos, stars
    contributions.svg  the last 12 months as a heatmap, like the profile calendar
    languages.svg      top languages across public repositories (by code size)

Runs daily in .github/workflows/stats.yml. Uses STATS_TOKEN if set (a personal token, so private
contributions are included), otherwise the workflow's GITHUB_TOKEN (public activity).

Local preview with sample data:  python scripts/github_stats.py --sample
"""
import argparse
import json
import os
import random
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

LOGIN = os.getenv("STATS_LOGIN", "Inchara-Adigante")
OUT = Path(__file__).resolve().parents[1] / "assets"

YEAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""
PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
  }
}"""


def graphql(query: str, **variables) -> dict:
    token = os.getenv("STATS_TOKEN") or os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.load(resp)
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]["user"]


def fetch() -> dict:
    profile = graphql(PROFILE_QUERY, login=LOGIN)
    today = datetime.now(timezone.utc).date()
    first_year = int(profile["createdAt"][:4])
    days: dict[date, int] = {}
    totals = defaultdict(int)
    for year in range(first_year, today.year + 1):
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), datetime.now(timezone.utc))
        cc = graphql(YEAR_QUERY, login=LOGIN, **{"from": start.isoformat(), "to": end.isoformat()})["contributionsCollection"]
        for week in cc["contributionCalendar"]["weeks"]:
            for d in week["contributionDays"]:
                days[date.fromisoformat(d["date"])] = d["contributionCount"]
        totals["prs"] += cc["totalPullRequestContributions"]
        totals["issues"] += cc["totalIssueContributions"]
    langs = defaultdict(lambda: [0, "#8b949e"])
    stars = 0
    for repo in profile["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]][0] += e["size"]
            langs[e["node"]["name"]][1] = e["node"]["color"] or "#8b949e"
    return dict(days=days, today=today, prs=totals["prs"], issues=totals["issues"],
                repos=profile["repositories"]["totalCount"], stars=stars, followers=profile["followers"]["totalCount"],
                languages=sorted(((n, s, c) for n, (s, c) in langs.items()), key=lambda x: -x[1]))


def sample() -> dict:
    """Plausible fake data for previewing the design without an API token."""
    r = random.Random(7)
    today = datetime.now(timezone.utc).date()
    days = {}
    for i in range(700):
        d = today - timedelta(days=i)
        busy = d.month in (3, 4, 7, 9, 10)
        days[d] = r.choice([0, 0, 1, 2, 3, 5, 8]) if busy or r.random() < .25 else 0
    return dict(days=days, today=today, prs=6, issues=2, repos=7, stars=3, followers=12,
                languages=[("Python", 900_000, "#3572A5"), ("PLpgSQL", 260_000, "#336790"), ("HTML", 150_000, "#e34c26"),
                           ("TSQL", 90_000, "#e38c00"), ("HCL", 30_000, "#844FBA"), ("Shell", 9_000, "#89e051")])


# ---------------------------------------------------------------- streaks
def streaks(days: dict, today: date) -> tuple[int, int, date | None]:
    """Current streak (counting today only if it already has activity), longest streak and its end date."""
    longest, run, best_end = 0, 0, None
    for d in sorted(days):
        run = run + 1 if days[d] > 0 else 0
        if run > longest:
            longest, best_end = run, d
    current, d = 0, today if days.get(today, 0) > 0 else today - timedelta(days=1)
    while days.get(d, 0) > 0:
        current += 1
        d -= timedelta(days=1)
    return current, longest, best_end


# ---------------------------------------------------------------- SVG
STYLE = """
<style>
  .bg { fill: #ffffff; stroke: #d0d7de; }
  .title { font: 600 15px 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif; fill: #1f2328; }
  .label { font: 400 12px 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif; fill: #59636e; }
  .value { font: 700 22px 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif; fill: #1f2328; }
  .small { font: 400 11px 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif; fill: #59636e; }
  .accent { fill: #8250df; }
  .l0 { fill: #eff2f5; } .l1 { fill: #d8c7ff; } .l2 { fill: #b392f0; } .l3 { fill: #8250df; } .l4 { fill: #5a32a3; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #0d1117; stroke: #30363d; }
    .title, .value { fill: #e6edf3; }
    .label, .small { fill: #9198a1; }
    .accent { fill: #a371f7; }
    .l0 { fill: #161b22; } .l1 { fill: #3c2a6b; } .l2 { fill: #5a3ea8; } .l3 { fill: #8957e5; } .l4 { fill: #bc8cff; }
  }
</style>"""


def svg(w: int, h: int, body: str, title: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{escape(title)}"><title>{escape(title)}</title>{STYLE}'
            f'<rect class="bg" x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8"/>{body}</svg>\n')


def stats_card(data) -> str:
    days, today = data["days"], data["today"]
    current, longest, best_end = streaks(days, today)
    year_total = sum(c for d, c in days.items() if d.year == today.year)
    last_12 = sum(c for d, c in days.items() if d > today - timedelta(days=365))
    all_time = sum(days.values())
    active = sum(1 for d, c in days.items() if c > 0 and d > today - timedelta(days=365))
    tiles = [
        (f"{year_total:,}", f"Contributions in {today.year}"),
        (f"{all_time:,}", "Total contributions"),
        (f"{current} day{'s' if current != 1 else ''}", "Current streak"),
        (f"{longest} day{'s' if longest != 1 else ''}", "Longest streak" + (f" (to {best_end:%b %d})" if best_end else "")),
        (f"{active}", "Active days, last 12 months"),
        (f"{data['prs']:,}", "Pull requests"),
        (f"{data['repos']}", "Public repositories"),
        (f"{data['stars']}", "Stars earned"),
    ]
    w, h = 720, 190
    body = [f'<text class="title" x="24" y="34">GitHub activity</text>',
            f'<text class="small" x="{w - 24}" y="34" text-anchor="end">{last_12:,} contributions in the last 12 months</text>']
    for i, (value, label) in enumerate(tiles):
        x, y = 24 + (i % 4) * 172, 78 + (i // 4) * 62
        body.append(f'<rect class="accent" x="{x}" y="{y - 22}" width="3" height="40" rx="1.5"/>'
                    f'<text class="value" x="{x + 12}" y="{y}">{escape(value)}</text>'
                    f'<text class="label" x="{x + 12}" y="{y + 18}">{escape(label)}</text>')
    return svg(w, h, "".join(body), "GitHub activity")


def calendar_card(data) -> str:
    days, today = data["days"], data["today"]
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)            # weeks start on Sunday, like GitHub
    counts = [days.get(start + timedelta(days=i), 0) for i in range((today - start).days + 1)]
    nonzero = sorted(c for c in counts if c > 0)

    def level(c):
        if c == 0:
            return 0
        q = [nonzero[int(len(nonzero) * p)] for p in (.25, .5, .75)] if nonzero else [1, 2, 3]
        return 1 + sum(c > t for t in q)

    cell, gap, x0, y0 = 11, 3, 44, 50
    weeks = (len(counts) + 6) // 7
    w, h = x0 + weeks * (cell + gap) + 20, y0 + 7 * (cell + gap) + 44
    total = sum(c for d, c in days.items() if d > today - timedelta(days=365))
    body = [f'<text class="title" x="20" y="28">{total:,} contributions in the last year</text>']
    for i, c in enumerate(counts):
        d = start + timedelta(days=i)
        x, y = x0 + (i // 7) * (cell + gap), y0 + (i % 7) * (cell + gap)
        body.append(f'<rect class="l{level(c)}" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2">'
                    f'<title>{c} contribution{"s" if c != 1 else ""} on {d:%b %d, %Y}</title></rect>')
        if d.day <= 7 and i % 7 == 0:
            body.append(f'<text class="small" x="{x}" y="{y0 - 8}">{d:%b}</text>')
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        body.append(f'<text class="small" x="12" y="{y0 + row * (cell + gap) + 9}">{name}</text>')
    ly = y0 + 7 * (cell + gap) + 18
    body.append(f'<text class="small" x="{w - 168}" y="{ly + 9}">Less</text>')
    for k in range(5):
        body.append(f'<rect class="l{k}" x="{w - 136 + k * 15}" y="{ly}" width="{cell}" height="{cell}" rx="2"/>')
    body.append(f'<text class="small" x="{w - 56}" y="{ly + 9}">More</text>')
    return svg(w, h, "".join(body), "Contribution calendar")


def languages_card(data) -> str:
    langs = [l for l in data["languages"] if l[1] > 0][:6]
    total = sum(s for _, s, _ in langs) or 1
    w, h = 360, 70 + 26 * ((len(langs) + 1) // 2)
    body = ['<text class="title" x="20" y="30">Top languages</text>']
    x = 20.0
    for name, size, color in langs:
        width = 320 * size / total
        body.append(f'<rect x="{x:.1f}" y="44" width="{max(width, 1):.1f}" height="8" fill="{color}"/>')
        x += width
    for i, (name, size, color) in enumerate(langs):
        cx, cy = 26 + (i % 2) * 165, 78 + (i // 2) * 26
        body.append(f'<circle cx="{cx}" cy="{cy - 4}" r="5" fill="{color}"/>'
                    f'<text class="label" x="{cx + 12}" y="{cy}">{escape(name)} {100 * size / total:.1f}%</text>')
    return svg(w, h, "".join(body), "Top languages")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", action="store_true", help="render with fake data (no token needed)")
    args = ap.parse_args()
    data = sample() if args.sample else fetch()
    OUT.mkdir(exist_ok=True)
    (OUT / "stats.svg").write_text(stats_card(data))
    (OUT / "contributions.svg").write_text(calendar_card(data))
    (OUT / "languages.svg").write_text(languages_card(data))
    current, longest, _ = streaks(data["days"], data["today"])
    print(f"wrote 3 cards: {sum(data['days'].values())} contributions, streak {current} (longest {longest})")


if __name__ == "__main__":
    main()
