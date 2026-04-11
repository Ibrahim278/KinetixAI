# AI Based Content Generation

A Flask web app that generates marketing and content-writing suggestions using GenAI.

This project provides multiple content tools in one UI, including:
- Product descriptions
- Job descriptions
- Tweet ideas
- Cold emails
- Social media ad copy
- Business pitch ideas
- YouTube video ideas
- YouTube video descriptions
- Blog topic ideas

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [How It Works](#how-it-works)
6. [Prerequisites](#prerequisites)
7. [Installation](#installation)
8. [Configuration](#configuration)
9. [Run the Application](#run-the-application)
10. [Run with Docker](#run-with-docker)
11. [Available Routes](#available-routes)
12. [Known Issues and Limitations](#known-issues-and-limitations)
13. [Troubleshooting](#troubleshooting)
14. [Security Notes](#security-notes)
15. [Recommended Improvements](#recommended-improvements)
16. [Future Work](#future-work)
17. [Upcoming Updates](#upcoming-updates)
18. [License](#license)

## Project Overview

This application is a multi-tool AI content generator built with Flask and server-rendered Jinja templates.

Each feature page collects a short user prompt from a form, sends a task-specific query to OpenAI, and renders the generated result directly on the same page.

The app is designed for fast idea generation workflows for creators, marketers, and business users.

## Features

- Clean, multi-page UI using Bootstrap 5
- Dedicated generation flow for each content type
- Basic 404 page handling
- Single Flask server with route-per-feature architecture
- Reusable layout template for consistent navigation

## Tech Stack

- Python
- Flask
- OpenAI Python SDK (legacy ChatCompletion-style usage)
- Jinja2 templates
- Bootstrap 5 (CDN)

## Project Structure

```text
AI Based Content Generation/
├── app.py                  # Main Flask app and routes
├── aicontent.py            # Core OpenAI helper used by most routes
├── blog.py                 # Additional blog helper functions (currently not wired to routes)
├── config.py               # Flask config + OpenAI key placeholder
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Local container orchestration
├── LICENSE
├── README.md
└── templates/
    ├── 404.html
    ├── index.html
    ├── product-description.html
    ├── job-description.html
    ├── tweet-ideas.html
    ├── cold-emails.html
    ├── social-media.html
    ├── business-pitch.html
    ├── video-ideas.html
    ├── video-description.html
    ├── blog-ideas.html
    ├── blogs.html          # Legacy/extra template not currently routed
    ├── amazon-descriptions.html # Extra template not currently routed
    └── includes/
        └── layout.html
```

## How It Works

1. User opens a feature page.
2. User submits a form field (for example, product title or topic).
3. The route in app.py creates a prompt string.
4. The prompt is sent to aicontent.openAI().
5. OpenAI returns text output.
6. The template renders prompt and generated answer.

## Prerequisites

- Python 3.9+ recommended
- pip
- OpenAI API key

## Installation

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install flask "openai<1"
```

Why openai<1?
- The current code uses the older ChatCompletion API style.
- Newer SDK versions require updated client syntax.

## Configuration

### Current State in Repository

The current codebase includes hardcoded API keys in files. This is unsafe and should be replaced.

### Recommended Local Setup

Use an environment variable instead:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Then update code to read from environment, for example:

```python
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
```

## Run the Application

```bash
python app.py
```

The app starts in debug mode and is available at:

- http://127.0.0.1:5000/

## Run with Docker

### Option A: Docker Compose (recommended)

```bash
export OPENAI_API_KEY="your_api_key_here"
docker compose up --build
```

Then open:

- http://127.0.0.1:5000/

### Option B: Docker only

```bash
docker build -t ai-content-generator .
docker run --rm -p 5000:5000 -e OPENAI_API_KEY="your_api_key_here" ai-content-generator
```

Notes:
- The image uses Python 3.11 slim.
- Flask listens on `0.0.0.0:5000` inside the container.

## Available Routes

| Route | Methods | Purpose |
|---|---|---|
| / | GET, POST | Home/dashboard |
| /product-description | GET, POST | Generate product descriptions |
| /job-description | GET, POST | Generate job descriptions |
| /tweet-ideas | GET, POST | Generate tweet content |
| /cold-emails | GET, POST | Generate cold email text |
| /social-media | GET, POST | Generate social media ad copy |
| /business-pitch | GET, POST | Generate business proposal/pitch text |
| /video-ideas | GET, POST | Generate video topic ideas |
| /video-description | GET, POST | Generate video descriptions |
| /blog-ideas | GET, POST | Generate blog topic ideas |

## Known Issues and Limitations

- Hardcoded secrets are present in source files.
- OpenAI response parsing in aicontent.py expects choice text in a legacy format.
- blog.py functions are not connected to live routes.
- templates/blogs.html and templates/amazon-descriptions.html exist but are not currently active in app.py routes.
- No automated tests included.
- No rate-limiting, auth, or abuse protection.

## Troubleshooting

### Error: ModuleNotFoundError: No module named 'flask' or 'openai'

Install dependencies in the active virtual environment:

```bash
pip install flask "openai<1"
```

### Error: OpenAI authentication failed

- Confirm OPENAI_API_KEY is set.
- Confirm key has billing/usage access.
- Restart terminal/session after exporting environment variable.

### Error with newer OpenAI SDK

If you installed openai>=1 accidentally, either:
- Pin to openai<1, or
- Refactor the code to the new OpenAI client API.

## Security Notes

- Immediately revoke and rotate any exposed API key.
- Never commit API keys to git history.
- Move all sensitive configuration to environment variables or a .env file (ignored by git).
- Consider adding input validation and request throttling before production use.

## Recommended Improvements

- Migrate to the latest OpenAI Python client syntax.
- Centralize prompt templates and response formatting.
- Add loading/error states in templates.
- Add pytest coverage for route behavior and helper functions.
- Add .env support with python-dotenv and remove hardcoded secrets.
- Add production configuration (gunicorn, logging, debug=False).

## Future Work

### Product and UX

- Add generation controls for tone, audience, output length, and format.
- Add reusable prompt templates for each content category.
- Add one-click actions: copy, export (`.txt`, `.md`), regenerate section, and rewrite selected text.
- Add generation progress and streaming output to improve user feedback.

### Content Expansion

- Add SEO tools: meta title/description generation, FAQs, and keyword clusters.
- Add ad-copy tools: Google ads, social ad variants, and CTA libraries.
- Add email workflows: welcome sequence, nurture sequence, and sales follow-up templates.
- Add support and technical writing categories: help docs, release notes, and changelog generation.

#### Proposed New Categories

- LinkedIn Posts
- Instagram Captions
- Facebook Ad Copy
- Google Ads Headlines and Descriptions
- Email Subject Lines
- Newsletter Drafts
- Landing Page Copy
- SEO Meta Titles and Descriptions
- FAQ Generator
- Product Comparison Copy
- Testimonial Requests and Replies
- Press Release Drafts
- Case Study Outline
- Webinar and Event Promotion Copy
- Sales Follow-up Messages
- Customer Support Responses
- Script Hooks for Reels, Shorts, and TikTok
- Call-to-Action Variations
- Brand Taglines and Slogans
- Content Repurposer (Blog to Thread, Email, and Social Post)

#### Priority Categories (First 5)

- LinkedIn Posts
- Google Ads Copy
- Email Subject Lines
- Landing Page Copy
- SEO Meta Titles and Descriptions

### Platform and Collaboration

- Add user accounts, saved history, and project-based organization.
- Add brand voice profiles to apply consistent writing style across all outputs.
- Add team collaboration with shared workspaces and review/approval flow.

### Engineering and Security

- Add retry logic, telemetry, and robust API error handling.
- Add request rate limits and abuse protection.
- Add automated testing for routes, generation handlers, and formatting pipeline.
- Add CI secret scanning and stronger configuration validation.

## Upcoming Updates

### Phase 1: Immediate Updates

- Improve markdown output consistency and enforce cleaner section hierarchy.
- Add enhanced output actions (copy, download, regenerate).
- Improve loading and error states across all generator pages.

### Phase 2: Feature Growth

- Introduce new content categories (SEO, ad copy, and email sequences).
- Add user history and project grouping.
- Introduce brand profile presets for writing tone and messaging consistency.

### Phase 3: Scale and Reliability

- Add authentication and usage tracking.
- Add monitoring/logging for production reliability.
- Add optional billing/plan controls for quota-based usage.

## License

This project is licensed under the MIT License.

MIT License

Copyright (c) 2026 Ibrahim Irfan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
