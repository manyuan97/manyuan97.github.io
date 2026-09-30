#!/usr/bin/env python3
"""Build the static homepage with Python's standard library only."""

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def news_row(item):
    year, month = item["date"].split("-")
    return (f'<li><time datetime="{escape(item["date"])}">{year}.{month}</time>'
            f'<span>{item["html"]}</span></li>')


def publication_row(paper):
    title = escape(paper["title"])
    url = escape(paper["url"], quote=True)
    heading = f'<a href="{url}">{title}</a>' if url else title
    links = []
    if url:
        label = "Paper" if "arxiv.org" in paper["url"] or ".pdf" in paper["url"] else "Publication"
        links.append(f'<a href="{url}">{label}</a>')
    for link in paper["links"]:
        links.append(f'<a href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a>')
    image = ""
    if paper.get("image"):
        src = escape(paper["image"], quote=True)
        if not (ROOT / paper["image"]).is_file():
            raise ValueError(f"Missing paper figure: {paper['image']}")
        image = (f'<a class="paper-figure" href="{url}" tabindex="-1" aria-hidden="true">'
                 f'<img src="{src}" alt="" loading="lazy" decoding="async" width="220" height="145">'
                 '</a>')
    distinction = (f'<span class="distinction">{escape(paper["distinction"])}</span>'
                   if paper.get("distinction") else "")
    summary = f'<p class="paper-summary">{escape(paper["summary"])}</p>' if paper.get("summary") else ""
    selected = str(paper["selected"]).lower()
    figure_class = " has-figure" if image else ""
    return f'''<article class="publication{figure_class}" id="{escape(paper['id'])}"
        data-year="{paper['year']}" data-selected="{selected}" data-selected-order="{paper.get('selected_order', 99)}">
      {image}
      <div class="paper-content">
        <h3>{heading}</h3>
        <p class="authors">{paper.get('authors_short_html', paper['authors_html'])}</p>
        <p class="venue"><span title="{escape(paper['venue_full'], quote=True)}">{escape(paper['venue'])} · {paper['year']}</span>{distinction}</p>
        <p class="paper-links">{'<span aria-hidden="true"> / </span>'.join(links)}</p>
        {summary}
      </div>
    </article>'''


def tech_report_card(paper):
    title = escape(paper["title"])
    url = escape(paper["url"], quote=True)
    image = ""
    if paper.get("image"):
        image = (f'<a class="tech-figure" href="{url}" tabindex="-1" aria-hidden="true">'
                 f'<img src="{escape(paper["image"], quote=True)}" alt="" loading="lazy" decoding="async" width="220" height="130">'
                 '</a>')
    links = [f'<a href="{url}">Paper ↗</a>'] if url else []
    for link in paper["links"]:
        links.append(f'<a href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a>')
    return f'''<article class="tech-card">
      {image}
      <div>
        <h3><a href="{url}">{title}</a></h3>
        <p class="tech-meta" title="{escape(paper['venue_full'], quote=True)}">{escape(paper['venue'])} · {paper["year"]}</p>
        <p class="authors">{paper.get('authors_short_html', paper['authors_html'])}</p>
        <p class="paper-links">{'<span aria-hidden="true"> / </span>'.join(links)}</p>
      </div>
    </article>'''


def main():
    data = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    all_publications = sorted(data["publications"], key=lambda p: -p["year"])
    tech_ids = set(data["tech_reports"])
    publications = [p for p in all_publications if p["id"] not in tech_ids]
    ids = [p["id"] for p in all_publications]
    if len(ids) != len(set(ids)):
        raise ValueError("Publication IDs must be unique")
    projects = "\n".join(
        f'<li><h3><a href="{escape(p["url"], quote=True)}">{escape(p["title"])}</a></h3>'
        f'<p>{escape(p["description"])}</p></li>' for p in data["projects"]
    )
    substitutions = {
        "RECENT_NEWS": "\n".join(news_row(n) for n in data["news"][:6]),
        "OLDER_NEWS": "\n".join(news_row(n) for n in data["news"][6:]),
        "PUBLICATIONS": "\n".join(publication_row(p) for p in publications),
        "PUBLICATION_COUNT": str(len(publications)),
        "SELECTED_COUNT": str(sum(p["selected"] for p in publications)),
        "TECH_REPORTS": "\n".join(tech_report_card(next(p for p in all_publications if p["id"] == pid))
                                     for pid in data["tech_reports"]),
        "AWARDS": "\n".join(f'<li>{a}</li>' for a in data["awards"]),
        "PROJECTS": projects,
    }
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    output = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: substitutions[m[1]], template)
    output = "\n".join(line.rstrip() for line in output.splitlines()) + "\n"
    (ROOT / "index.html").write_text(output, encoding="utf-8")
    print(f"Built index.html: {len(publications)} research publications, {len(data['tech_reports'])} tech reports, {len(data['news'])} news items.")


if __name__ == "__main__":
    main()
