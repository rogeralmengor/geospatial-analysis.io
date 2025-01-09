---
title: Building a Geo-Spatial Application with PostGIS, Python, and TDD
description: When I first started my journey as a geospatial application developer, my workflow was... well, let's just say it was "unique." Picture this..
---

## How I Evolved from Notepad++ Chaos to Test-Driven Development Bliss

When I first started my journey as a geospatial application developer, my workflow was... well, let's just say it was "unique." Picture this: I’d fire up Notepad++ (yes, that was my entire development setup — caveman style) and hammer out code like a man possessed. My debugging process? Sprinkle print statements everywhere until the errors stopped screaming at me. Logging systems? Never heard of them. It was pure chaos, and somehow, I managed to scrape by.

It wasn’t until I started collaborating with coworkers, having my code reviewed (and shredded), reviewing theirs, and diving into blogs and books on software architecture that I realized there was a better way. My code slowly started improving, becoming more maintainable, and dare I say, cleaner.

But the real game-changer? Test-Driven Development (TDD). Writing tests first transformed the way I worked. It reduced the “surprise factor” in production and helped me iterate more effectively without the looming fear of things breaking.

This blog post is my tribute to that process. Here, we’ll build a small application and walk through the workflow I typically follow for solo projects that need to be maintainable for the long haul. (If it’s just a one-off script, don’t worry — no need to roll out the TDD parade for that!)

So, let’s dive in and build something awesome.