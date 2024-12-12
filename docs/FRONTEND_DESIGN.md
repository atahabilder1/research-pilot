# Frontend Design Concept

## Overview

Research Pilot will have a modern, intuitive web interface built with **Streamlit** for rapid prototyping and **FastAPI** for the backend API.

## Technology Stack

### Frontend
- **Streamlit**: Primary UI framework (Python-based, fast development)
- **Plotly**: Interactive visualizations (citation graphs, timeline)
- **Streamlit-AgGrid**: Advanced table displays
- **Markdown**: Rich text rendering for paper summaries

### Backend API
- **FastAPI**: RESTful API server
- **WebSockets**: Real-time agent progress updates
- **Pydantic**: Request/response validation

### Alternative (Future)
- **React + TypeScript**: For production-grade UI
- **TailwindCSS**: Modern styling
- **Shadcn/ui**: Component library

## User Interface Concept

### 1. Home Page / Search Interface

```
┌─────────────────────────────────────────────────────────────┐
│  Research Pilot                          [Settings] [Docs]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│   🔍 What would you like to research?                        │
│   ┌───────────────────────────────────────────────────────┐ │
│   │ Recent advances in vision transformers for medical   │ │
│   │ imaging                                               │ │
│   └───────────────────────────────────────────────────────┘ │
│                                                               │
│   [ Search Papers ]  [ Upload PDFs ]  [ Browse Library ]    │
│                                                               │
│   Advanced Filters:                                          │
│   • Date Range: [2020] ─────── [2024]                       │
│   • Min Citations: [10]                                      │
│   • Sources: [✓] arXiv  [✓] Semantic Scholar  [ ] PubMed   │
│   • Max Papers: [20]                                         │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  Recent Searches                                              │
│  • Transformer architectures for NLP (2 days ago)           │
│  • RAG systems evaluation (1 week ago)                       │
│  • Diffusion models for image generation (2 weeks ago)      │
└─────────────────────────────────────────────────────────────┘
```

### 2. Agent Progress View

Real-time updates as the agent works:

```
┌─────────────────────────────────────────────────────────────┐
│  Researching: "Vision transformers for medical imaging"      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [✓] Query analyzed and decomposed                          │
│  [✓] Searching arXiv... (43 papers found)                   │
│  [✓] Searching Semantic Scholar... (37 papers found)        │
│  [→] Filtering and ranking papers... (25/80)                │
│  [ ] Downloading PDFs...                                     │
│  [ ] Processing and embedding...                             │
│  [ ] Generating literature review...                         │
│                                                               │
│  ████████████░░░░░░░░░░░░░░░ 45%                           │
│                                                               │
│  Estimated time remaining: 3 minutes                         │
│                                                               │
│  [View Details] [Pause] [Cancel]                            │
└─────────────────────────────────────────────────────────────┘
```

### 3. Results Page

```
┌─────────────────────────────────────────────────────────────┐
│  Results: "Vision transformers for medical imaging"          │
│  25 papers found • Generated in 4m 23s                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [Summary] [Papers] [Timeline] [Citations] [Export]         │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📝 Literature Review Summary                           ││
│  │                                                          ││
│  │  Vision Transformers (ViTs) have revolutionized        ││
│  │  medical image analysis since 2020, offering            ││
│  │  superior performance compared to traditional CNNs...   ││
│  │                                                          ││
│  │  Key Findings:                                          ││
│  │  • ViTs achieve 94.2% accuracy on chest X-ray          ││
│  │    classification (Dosovitskiy et al., 2024)           ││
│  │  • Hybrid CNN-ViT architectures show promise           ││
│  │  • Main challenge: Data efficiency                     ││
│  │                                                          ││
│  │  [Read Full Review] [Regenerate]                        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📚 Top Papers                                          ││
│  │                                                          ││
│  │  1. ⭐ [Highly Relevant]                                ││
│  │     "Medical Vision Transformers: A Survey"             ││
│  │     Chen et al. • arXiv • 2024 • 247 citations         ││
│  │     Comprehensive survey of ViT applications in        ││
│  │     medical imaging...                                  ││
│  │     [Read] [Cite] [Similar Papers]                      ││
│  │                                                          ││
│  │  2. ⭐ [Highly Relevant]                                ││
│  │     "TransMed: Transformers for Medical Image Analysis"││
│  │     Wang et al. • CVPR 2023 • 189 citations           ││
│  │     Novel architecture combining CNN and ViT...        ││
│  │     [Read] [Cite] [Similar Papers]                      ││
│  │                                                          ││
│  │  ... (23 more)                                          ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 4. Paper Detail View

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Results                         [Add to Library] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Medical Vision Transformers: A Survey                       │
│  Chen, Li, Wang et al. • arXiv:2401.12345 • Jan 2024        │
│  247 citations • 98% relevance                               │
│                                                               │
│  [Abstract] [Key Findings] [Methodology] [Citations]        │
│                                                               │
│  Abstract                                                    │
│  ────────────────────────────────────────────────────────── │
│  This paper presents a comprehensive survey of Vision        │
│  Transformers (ViTs) in medical imaging. We analyze 150+    │
│  papers and identify key trends, challenges, and future     │
│  directions...                                               │
│                                                               │
│  Key Contributions                                           │
│  • First comprehensive survey of medical ViTs               │
│  • Taxonomy of architectures (pure, hybrid, hierarchical)   │
│  • Benchmark comparison across 10 datasets                  │
│                                                               │
│  Relevant Sections (AI-Extracted)                            │
│  ────────────────────────────────────────────────────────── │
│  Section 3.2: "Hybrid CNN-ViT Architectures"               │
│  "Recent work combines CNNs for local features with ViTs   │
│   for global context. TransMed (Wang et al.) achieves..."   │
│                                                               │
│  Section 4.1: "Data Efficiency"                             │
│  "A major challenge is ViTs require large datasets. Self-  │
│   supervised pretraining reduces this requirement by..."     │
│                                                               │
│  [View Full PDF] [Export Citation] [Find Related]           │
└─────────────────────────────────────────────────────────────┘
```

### 5. Citation Graph Visualization

```
┌─────────────────────────────────────────────────────────────┐
│  Citation Network                                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│       ●────────●                                             │
│      /│\       │\                                            │
│     / │ \      │ \                                           │
│    ●  ●  ●─────●  ●                                         │
│    │   \│     / \ │                                          │
│    │    ●────●   \│                                          │
│    │         │    ●                                          │
│    ●─────────●                                               │
│                                                               │
│  Node size: citation count                                   │
│  Edge: cites relationship                                    │
│  Color: publication year (blue=old, red=new)                │
│                                                               │
│  Hover for details • Click to open paper                     │
└─────────────────────────────────────────────────────────────┘
```

### 6. Timeline View

```
┌─────────────────────────────────────────────────────────────┐
│  Research Timeline                                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  2020  ├─●──────────────────────────────────────────────   │
│         "Attention Is All You Need"                          │
│                                                               │
│  2021  ├────●─────●────────────────────────────────────    │
│            ViT   BERT-Medical                                │
│                                                               │
│  2022  ├─────────●──●──────●──────────────────────────    │
│                Swin  TransMed  MedViT                       │
│                                                               │
│  2023  ├───────────────────●─●─●───────────────────────    │
│                           (10 papers)                        │
│                                                               │
│  2024  ├──●────●──────────────────●────────────────────    │
│         Survey  New SOTA      This work                     │
│                                                               │
│  Click on timeline to filter by year                         │
└─────────────────────────────────────────────────────────────┘
```

### 7. Library Management

```
┌─────────────────────────────────────────────────────────────┐
│  My Library                     [Upload PDFs] [New Search]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Search library: [________________]  🔍                      │
│                                                               │
│  Collections:                                                │
│  • All Papers (247)                                          │
│  • Vision Transformers (42)                                  │
│  • Medical Imaging (38)                                      │
│  • RAG Systems (25)                                          │
│  • + New Collection                                          │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Title ▼           Authors       Year   Citations   Tags ││
│  ├─────────────────────────────────────────────────────────┤│
│  │ Medical Vision... Chen et al.  2024     247     ViT,Med││
│  │ TransMed: Tra...  Wang et al.  2023     189     ViT    ││
│  │ Attention Is...   Vaswani      2017   >10000    NLP    ││
│  │ ... (244 more)                                          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  [Export Library] [Sync to Zotero/Notion]                   │
└─────────────────────────────────────────────────────────────┘
```

### 8. Settings Page

```
┌─────────────────────────────────────────────────────────────┐
│  Settings                                                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  LLM Configuration                                           │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Provider: [Claude API ▼]                              │ │
│  │ Model: [claude-3-5-sonnet-20241022 ▼]                │ │
│  │ API Key: [••••••••••••••••••••••] [Test Connection]  │ │
│  │                                                         │ │
│  │ ☐ Use local LLM (requires GPU)                        │ │
│  │   Model: [Llama-3.1-8B ▼]                             │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                               │
│  Embedding Configuration                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Model: [all-mpnet-base-v2 ▼]                          │ │
│  │ Device: [CUDA (NVIDIA A6000) ▼]                       │ │
│  │ Batch Size: [128]                                      │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                               │
│  Vector Store                                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Provider: [Qdrant ▼]                                   │ │
│  │ URL: [http://localhost:6333]                           │ │
│  │ Collection: [research_papers]                          │ │
│  │                                                         │ │
│  │ Status: ● Connected (247 vectors)                      │ │
│  │ [Clear Database] [Reindex All]                         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                               │
│  Search Preferences                                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Default date range: [Last 2 years]                     │ │
│  │ Min citations: [10]                                     │ │
│  │ Max papers per search: [20]                            │ │
│  │ Auto-download PDFs: [✓]                                │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                               │
│  [Save Settings]                                             │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Streamlit MVP (Weeks 1-2)
```python
# app.py structure
import streamlit as st
from research_pilot import ResearchAgent

st.set_page_config(page_title="Research Pilot", layout="wide")

# Home page
st.title("🔬 Research Pilot")
query = st.text_area("What would you like to research?")

if st.button("Search Papers"):
    with st.spinner("Researching..."):
        agent = ResearchAgent()
        results = agent.research(query)

    # Display results
    st.subheader("Literature Review")
    st.markdown(results.summary)

    st.subheader("Top Papers")
    for paper in results.papers:
        with st.expander(f"{paper.title} ({paper.year})"):
            st.write(paper.abstract)
            st.write(f"Citations: {paper.citations}")
```

### Phase 2: FastAPI Backend (Weeks 3-4)
```python
# api/main.py
from fastapi import FastAPI, WebSocket
from research_pilot import ResearchAgent

app = FastAPI()

@app.post("/api/search")
async def search_papers(query: str):
    agent = ResearchAgent()
    results = await agent.research_async(query)
    return results

@app.websocket("/ws/progress")
async def progress_updates(websocket: WebSocket):
    await websocket.accept()
    # Stream agent progress in real-time
    async for update in agent.stream_progress():
        await websocket.send_json(update)
```

### Phase 3: Enhanced UI (Weeks 5-6)
- Interactive visualizations with Plotly
- Citation graph with NetworkX + Plotly
- Timeline view
- PDF viewer integration
- Export functionality (BibTeX, Markdown, Notion)

### Phase 4: Advanced Features (Weeks 7-8)
- User authentication
- Multi-user support
- Saved searches and collections
- Integration with note-taking apps (Notion, Obsidian)
- Collaborative features

## Key Features

### 1. Real-time Agent Monitoring
- WebSocket connection shows live progress
- Step-by-step visualization of agent actions
- Ability to pause/resume/cancel

### 2. Interactive Results
- Expandable paper cards
- Inline PDF preview
- One-click citation export
- Related papers suggestions

### 3. Smart Filtering
- Date range slider
- Citation threshold
- Source selection
- Topic clustering

### 4. Visualization
- Citation network graph
- Publication timeline
- Author collaboration network
- Topic evolution over time

### 5. Export Options
- Markdown report
- PDF summary
- BibTeX citations
- Notion/Obsidian sync
- CSV for spreadsheet analysis

## Design Principles

1. **Simplicity**: One text box to start researching
2. **Transparency**: Show what the agent is doing
3. **Interactivity**: Drill down into any result
4. **Efficiency**: Keyboard shortcuts, quick actions
5. **Flexibility**: Multiple views (list, graph, timeline)

## Mockup Tools Used

For actual UI design:
- Figma: High-fidelity mockups
- Streamlit: Rapid prototyping
- Excalidraw: Wireframes and diagrams

## Future Enhancements

- Mobile-responsive design
- Dark mode
- Keyboard shortcuts (Vim-style)
- Browser extension for quick searches
- VS Code extension
- Slack/Discord bot integration
- Email digest of new papers
