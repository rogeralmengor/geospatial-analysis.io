---
title: Building a Geo-Spatial Application with PostGIS, Python, and TDD
description: When I first started my journey as a geospatial application developer, my workflow was... well, let's just say it was "unique." Picture this..
---

### How I Evolved from Notepad++ Chaos to Test-Driven Development Bliss

When I first started my journey as a geospatial application developer, my workflow was... well, let's just say it was "unique." Picture this: I’d fire up Notepad++ (yes, that was my entire development setup — caveman style) and hammer out code like a man possessed. My debugging process? Sprinkle print statements everywhere until the errors stopped screaming at me. Logging systems? Never heard of them. It was pure chaos, and somehow, I managed to scrape by.
<div style="text-align: center;">
<img src="https://preview.redd.it/notepad-meme-lol-v0-douf2d3cphp81.jpg?width=1080&crop=smart&auto=webp&s=e88ddcd2a75edcb4ae46fe2850e13d21e17356e2" alt=, width=500>
<p style="font-size: 12px; color: gray;">Hellow Nodepad++!, my dear oldfriend! <a href="https://www.reddit.com/r/ProgrammerHumor/comments/tnhato/notepad_meme_lol/" target="_blank", style="color: blue;">Source</a>.</p>
</div>

It wasn’t until I started collaborating with coworkers, having my code reviewed (and shredded), reviewing theirs, and diving into blogs and books on software architecture that I realized there was a better way. My code slowly started improving, becoming more maintainable, and dare I say, cleaner.

But the real game-changer? Test-Driven Development (TDD). Writing tests first transformed the way I worked. It reduced the “surprise factor” in production and helped me iterate more effectively without the looming fear of things breaking.

This blog post is my tribute to that process. Here, we’ll build a small application and walk through the workflow I typically follow for solo projects that need to be maintainable for the long haul. (If it’s just a one-off script, don’t worry — no need to roll out the TDD parade for that!)

So, let’s dive in and build something awesome.

### Step:1 Defining the business ida and project's structure.

Before starting any project, I'd like to point out that good architecture begins with clearly defining the system requirements and the business problem we aim to solve.

```
"We want to build a simple tool that allows users to save and manage geometries (points, lines, polygons) in a PostGIS-compatible format, along with additional information such as a descriptive name, the user who created it, and the creation date. All of this will be accessible through an intuitive command-line interface (CLI), with a PostGIS database for storage, following a test-driven development (TDD) approach and clean architecture principles."
```


With that definition in mind, let's move on to the first step: defining the project's architecture. 

With the help of AI through Chat-GPT, I created the following project layout that we'll follow throughout this tutorial: 

```bash
my_geospatial_project/
│
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── entities.py         # Core business objects (e.g., Geometry)
│   │   ├── use_cases.py        # Business logic (e.g., add/retrieve geometries)
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── postgis_repository.py  # PostGIS database interactions
│   │
│   ├── cli/
│       ├── __init__.py
│       ├── main.py            # CLI entry point
│
├── tests/
│   ├── core/
│   │   ├── test_entities.py
│   │   ├── test_use_cases.py
│   │
│   ├── infrastructure/
│       ├── test_postgis_repository.py
│
├── Dockerfile                 # Docker setup for Python
├── docker-compose.yml         # Multi-container setup for PostGIS and the app
├── pyproject.toml             # Project dependencies and metadata
├── requirements.txt           # Python dependencies (optional)
├── README.md                  # Project documentation
```

This structure emphasizes separation of concerns: core logic is isolated in `core/`, database interaction in `infrastructure/`, and CLI handling in `cli/`. The `tests/` directory mirrors this layout to ensure modular and focused testing.

The essential project files (`Dockerfile, docker-compose, pyproject.toml, and README`) provide everything needed to set up and run the project, and in the future prepare the python package.