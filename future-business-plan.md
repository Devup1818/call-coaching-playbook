# Future Business Plan: Apptech × Lakmé Academy
### Brainstorming & Strategy Document

> **Prepared for:** Rajesh Singh Sir (CT) | **Company:** Apptech | **Partnership:** Lakmé | **CRM:** Superleap

---

## 1. THE LANDSCAPE

### Industry Overview
| Metric | Value |
|--------|-------|
| India Beauty Services Market (2024) | **$9.28 Billion** |
| Projected Market (2033) | **$18.58 Billion** |
| CAGR (2025-2033) | **7.89%** |
| Beauty & Personal Care Market (2023) | **$28 Billion** |
| Skilled Professional Shortage | **1.2 Million** |
| Beauty Schools in India (2026) | **2,726** |
| Industry Growth Rate | **~8% annually** |

### Apptech (Aptech Ltd) — Current Scale
- Founded: **1986** | Publicly listed (BSE)
- Global presence: **1,026+ centers across 50+ countries**
- FY25 Revenue: **~₹476 Cr**
- Lakmé Academy launched: **2015**
- **150+ Lakmé Academy centers** across **56+ cities**
- **80,000+ students trained** to date
- **500+ Lakmé Certified Trainers**
- Placement network: **50+ brands** empanelled (Nykaa, Tira, Lakmé Salon, Tony & Guy, etc.)

### Current Lead-to-Trainee Pipeline (Superleap CRM)

```
Marketing Channels
(Google Ads, Instagram, Facebook, Central Media, Website)
        │
        ▼
    Lead calls in
        │
        ▼
    IVR receives call ───► Superleap CRM logs:
        │                      • Caller name & number
        │                      • Date/time/duration
        │                      • Conversation recording
        │                      • Lead source attribution
        ▼
    Team gets lead in "Opportunity" dashboard
        │
        ▼
    Follow-up (call back / WhatsApp / SMS)
        │
        ▼
    Invite to center (visit scheduled)
        │
        ▼
    Convert to trainee (admission)
        │
        ▼
    Recording & data stored in Superleap for tracking
```

**Key Superleap modules used:**
| Module | Purpose |
|--------|---------|
| **Opportunity** | Pipeline view — track lead stages from inquiry to admission |
| **Voice AI** | IVR + call recording + transcription |
| **Dashboards** | Metrics on lead sources, conversion rates, team performance |
| **Workflows** | Auto-assign leads, follow-up reminders, status updates |
| **Integrations** | Google Ads, Facebook, Instagram, website forms |

## 1C. DASHLOCAL — LOCAL DISCOVERY & REPUTATION LAYER

DashLocal manages the top-of-funnel — how people find the center on Google/local search.

### Modules (Left Menu)
| Module | Purpose |
|--------|---------|
| **Home** | Overview dashboard |
| **Listing** | Profile visibility, views, actions, search queries |
| **Product** | Course offerings listed, product enquiries (e.g., Nail Art Courses) |
| **Review** | Google reviews, ratings, reply management, promoter tracking |
| **Post** | Announcements/updates (232 posts created) |
| **Leads** | Raw inbound calls from listings — caller info, duration, missed/answered |

### Listing Dashboard Metrics (Sector 18)
- **1 verified listing**, 1 virtual number
- **1K+ total views**, 69 total actions
- 16 call actions, 44 direction actions, 9 website actions
- Month-over-month growth (April 2026 vs March 2026)

### Query Insights (What people search before finding you)
| Type | Examples | Impressions |
|------|----------|-------------|
| **Branded** | "lakme academy", "lakme academy noida", "lakme", "lakme salon", "lakme salon noida" | ~4,177 |
| **Non Branded** | "beautician course", "makeup artist course", "fees" | Mixed |
| **Navigational** | Direct brand searches | Moderate |
| **Transactional** | Low — few "near me" or "best" intent queries |

### Profile Completion
- Fields fully filled: logo, cover photo, videos, photos, posts, description, phone, website
- **Top listing**: Lakme Academy (La01), Noida Sector 18 — 1,010 views

### Current Gap: DashLocal → Superleap handoff
- DashLocal captures raw inbound intent (calls, product enquiries)
- Superleap should take over for qualification, follow-up, visit, conversion
- **Missing**: No automatic lead push from DashLocal into Superleap pipeline
- **Need**: Tag DashLocal-origin leads in Superleap to track full funnel ROI

### The Full Stack: DashLocal + Superleap

```
DashLocal (Discovery Layer)                    Superleap (Conversion Layer)
══════════════════════════                     ══════════════════════════
Google Maps / Listings                          Opportunity Pipeline
Publisher Networks                             IVR + Call Recording
Reviews & Reputation                           Lead Follow-up & Tracking
Product Enquiries                              Visit Scheduling
Local Search (Branded/Non-Branded)             Admission Conversion
        │                                               ▲
        │                                               │
        └─────────────── Lead Flow ─────────────────────┘
                    (Tighter mapping needed)
```

| Layer | Tool | Function |
|-------|------|----------|
| **Top of Funnel** | DashLocal | Local discovery, listings, reviews, product enquiries, visibility metrics |
| **Middle/Bottom** | Superleap | Lead intake, IVR, call tracking, disposition, follow-up, conversion |

**Superleap Dashboard — Live Analysis (Opportunities View)**

**Fields tracked per lead:**
| Field | Example Values |
|-------|---------------|
| Name | vikasanchal pal19, Sonali, Sakshi Kharade, etc. |
| Brand Name | Lakme Academy |
| Stage | Enquiry, Ringing/Unable to Connect, Follow-up, Interested, Not Interested, Not Eligible |
| Owner | Sonia (single owner for all leads shown) |
| Created at | 26 May 2026, 03:46 PM |
| Source of Enquiry | Meta Form - Center, Aptech Website |
| A. Center | DELHI NCR-NOIDA-SECTOR 18 |
| Next Follow Up Date | 27 May 2026, 12:00 AM |
| Time to first call (in min) | 0, 9, 14, 22, 45, 55, 59, 64, 70, 74, 77, 96, 106, 109, 110, 111, 115, 131, 149, 178, 233, 404, 408, 414 |
| Category | N.A |
| Origin | API |
| Last Agent Assigned at | Timestamp |
| Last Disposition Status | Ringing/Unable to Connect, Follow-up, Not Interested, Not Eligible, Interested |
| Last Sub Disposition Status | Not Answering, Call Back Later, Did Not Enquire, Location Issue, Click By Mistake, Will Walk-in 30+ Days, Number Not in Service, Number Busy |

**Critical Observations:**
1. **Only Sector 18 leads visible** — No leads for Sector 62 or Greater Noida in this view. Either other centers get no web leads, or this view is filtered.
2. **Speed-to-lead is a major issue** — Time to first call ranges from 0 to 414 minutes. Many leads take 100+ minutes to get first contact. Industry best practice is under 5 minutes.
3. **High drop-off at "Ringing/Unable to Connect"** — Most leads die here with sub-disposition "Not Answering." Multiple call attempts needed.
4. **Only 2 lead sources** — "Meta Form - Center" and "Aptech Website." No Google Ads, Instagram DM, or other channels visible.
5. **"Location Issue" is the #1 rejection** — People outside Noida enquiring but unable to travel. Suggests demand in areas where there's no center.
6. **Single owner** — All leads assigned to "Sonia." No distribution across team members or centers.
7. **No conversion data visible** — No lead shown in "Admitted" or "Converted" stage in this view.

**Immediate Fixes Needed:**
| Problem | Fix |
|---------|-----|
| Slow first response | Auto-trigger WhatsApp/SMS within 1 min of lead creation |
| Leads not answering | Set up automated reminder sequence (3 calls + WhatsApp + SMS over 24 hrs) |
| Only 2 lead sources | Add Google Ads, Instagram DM, YouTube, and referral tracking |
| Location Issue rejections | Route out-of-catchment leads to nearest center or offer online course |
| Single owner bottleneck | Auto-distribute leads by center or by round-robin across team |
| No conversion tracking | Define clear stage progression: Enquiry → Contacted → Visit Scheduled → Visit Done → Admitted
| Center | Location Type | Potential Catchment |
|--------|--------------|-------------------|
| **Lakmé Academy — Noida Sector 18** | Prime commercial hub | High footfall, offices, malls, metro-connected |
| **Lakmé Academy — Noida Sector 62** | IT/Corporate hub | Electronic City, 1000+ companies, young workforce |
| **Lakmé Academy — Greater Noida** | Educational hub | Universities (Sharda, Galgotias, etc.), residential boom |

**Context**: These 3 centers sit in the Noida-Greater Noida region — one of India's fastest-growing urban corridors with massive young population, IT workforce, and educational institutions. Strong base for scaling both locally and as a pilot for expansion playbook.

### Key Competitors in Beauty Training
| Competitor | Centers | Franchise Fee | Notes |
|-----------|---------|--------------|-------|
| VLCC Academy | Pan-India | Varies | Also offers nutrition courses |
| Orane International | 115+ | ₹10 Lakhs | 18+ states, 2 Canada colleges |
| Naturals Beauty Academy | 30+ | ₹5 Lakhs | Part of 800+ salon chain |
| Femina Flaunt Academy | Growing | TBD | Times of India group |
| Shahnaz Husain | Select cities | High | Premium positioning |
| YLG Institut | 54 stores | ₹30-75 Lakhs | South India focused |

---

## 1B. HYPERLOCAL STRATEGY: NOIDA-GREATER NOIDA CORRIDOR

Our 3 centers as the launchpad for expansion.

### Current Strengths
| Center | Advantage | Student Sources |
|--------|-----------|----------------|
| **Sector 18** | Prime location, brand visibility, walk-ins | Mall traffic, office workers, nearby residents |
| **Sector 62** | IT corridor, working professionals | Techies looking for upskilling, evening/weekend batches |
| **Greater Noida** | University belt, affordable catchment | College students, freshers, homemakers |

### Cross-Center Synergies
- **Centralized lead management** — no prospect falls through cracks
- **Batch consolidation** — if one center lacks enrollment for a course, redirect to another
- **Shared placement network** — single ICAP cell serving all 3
- **Master trainer rotation** — specialists rotate across centers
- **One Noida campaign** — market collectively as "Lakmé Academy — Noida"

### Immediate Expansion Candidates (within 30 km radius)
| Area | Why |
|------|-----|
| **Indirapuram/Vaishali** | Dense residential, metro connectivity, no Lakmé Academy |
| **Ghaziabad (Raj Nagar/Kaushambi)** | Large population, underserved |
| **Noida Extension** | Rapidly growing residential sector |
| **Crossings Republik** | High-density township |
| **Jewar** | Airport city coming up — future goldmine |

### Noida-Specific Enrollment Tactics
- **Corporate tie-ups** in Sector 62: HR partnerships for employee upskilling
- **College ambassador program** in Greater Noida universities
- **Weekend batches** for working professionals (Sector 62)
- **Bridal makeup workshops** targeting wedding season (Sector 18 footfall)
- **Referral program**: Current students refer → get discount on next course

---

## 2. CORE STRATEGY: MAXIMIZE TRAINEE ENROLLMENT

### Problem Statement
The beauty industry needs **1.2M trained professionals** but current training capacity is far below. Lakmé Academy has trained 80K in ~10 years. We need to **accelerate** this.

### Strategic Pillars

#### Pillar A: Geographic Expansion — Go Deep into Tier 2/3/4 Cities
- **Current reach**: 56 cities. India has ~4,000 cities/towns.
- **Target**: Open in **200+ cities** within 3 years
- **Why**: Tier 2/3 cities are growing faster than metros for beauty services. Lower rent, less competition, high aspirational demand.
- **Model**: 
  - FOFO (Franchise Owned, Franchise Operated) for smaller cities
  - FOCO (Franchise Owned, Company Operated) for investors who want passive income
  - Lakmé Studio format (700-900 sq ft) for small cities — lower investment ₹20-30 Lakhs

#### Pillar B: Course Innovation — Modular, Affordable, Bite-Sized
- **Current**: Full courses ₹60K-2Lakhs
- **Propose**:
  - **Micro-courses**: ₹5K-15K for specific skills (bridal makeup, hair coloring, nail art)
  - **Certification tiers**: Foundation → Advanced → Master → International
  - **Subscription model**: Monthly classes for working professionals
  - **Free basic course + paid placement fee**: Reduce entry barrier
  - **GenAI / Digital Beauty courses**: New-age curriculum

#### Pillar C: Digital & Tech-Driven Enrollment
- **i-Aspire platform** (already built): Centralized digital placement — expand to all LAPA centers
- **Online + Hybrid courses**: Reach students in cities without physical centers
- **WhatsApp/Influencer marketing**: Target 18-25 demographic
- **YouTube/Facebook Live workshops**: Free sessions → paid enrollment funnel
- **Gamification**: Referral bonuses, early-bird discounts, batch discounts

#### Pillar D: Placement-Linked Enrollment
- **Job guarantee courses**: "Pay after placement" model
- **Placement pipeline expansion**:
  - 50+ brands today → target **200+ brand partnerships**
  - International placements: Dubai (already started), Canada, Australia, Middle East
  - Lakmé Salon network: 450+ salons — guaranteed absorption
- **ICAP (Industry Connects Alliances & Placements)** cell at every center

#### Pillar E: Government & Institutional Tie-Ups
- Already empanelled with: **B&WSSC, PMKVY 4.0, DDUGKY, NICSI, SWAYAM Plus**
- **Target**: Empanel with every state skill development mission
- **CSR partnerships**: Corporates funding training for underprivileged women
- **School/College integration**: Beauty as vocational subject in 10+2

---

## 3. FRANCHISE EXPANSION MODEL

### Proposed Franchise Tiers

| Tier | City Type | Investment | Area | Target Centers |
|------|-----------|-----------|------|---------------|
| **Lakmé Studio** | Tier 3/4 | ₹20-30 Lakhs | 700-900 sqft | 500 |
| **Lakmé Academy Standard** | Tier 2 | ₹35-50 Lakhs | 1000-1500 sqft | 200 |
| **Lakmé Academy Premium** | Tier 1/Metro | ₹50-70 Lakhs | 1500-2500 sqft | 50 |
| **Lakmé Absolute Academy** | Top Metros | ₹75 Lakhs+ | 2500+ sqft | 20 |

### Incentives for Franchise Partners
- Business loan assistance (up to ₹40L through partner banks)
- 100% placement support = higher enrollment = faster ROI
- Train-the-trainer program (4-6 weeks at Lakmé HQ)
- Centralized marketing & lead generation
- Revenue share flexibility

---

## 4. TARGET METRICS (3-Year Plan)

| Metric | Current | Year 1 | Year 2 | Year 3 |
|--------|---------|--------|--------|--------|
| Centers | 150+ | 200 | 300 | 500 |
| Cities | 56 | 80 | 120 | 200 |
| Students Trained (cumulative) | 80,000 | 1,20,000 | 1,80,000 | 3,00,000 |
| Annual Enrollment Run Rate | ~15,000 | 40,000 | 60,000 | 1,20,000 |
| Certified Trainers | 500 | 800 | 1,200 | 2,000 |
| Placement Partners | 50 | 100 | 150 | 200 |
| Avg Revenue per Center (annual) | ~₹25L | ₹30L | ₹35L | ₹40L |

---

## 5. INTERNATIONAL EXPANSION

### Already In Motion
- **Dubai**: International Pathway Program with L'Amour Institute (launched 2025)
- **Nigeria, Uganda, Zambia, Vietnam**: Aptech presence — cross-sell Lakmé Academy

### Target Markets
| Market | Opportunity | Strategy |
|--------|------------|----------|
| **Middle East** (Dubai, Saudi, Qatar) | High demand, high spending | Pathway programs, franchise |
| **South Asia** (Nepal, Bangladesh, Sri Lanka) | Low cost, high volume | Franchise + placement |
| **Africa** (Nigeria, Kenya, Uganda) | Aptech already present | Cross-sell beauty courses |
| **Southeast Asia** (Vietnam, Indonesia) | Growing beauty consciousness | Partner with local institutes |
| **Canada/Australia** | Indian diaspora, skilled migration | Direct pathway programs |

---

## 6. UNIQUE DIFFERENTIATORS VS COMPETITORS

| Factor | Apptech (Lakmé Academy) | Competitors |
|--------|------------------------|-------------|
| **Brand Power** | Lakmé (since 1952) + HUL + Aptech (since 1986) | Most lack dual-brand strength |
| **Placement Network** | 450+ Lakmé salons + 50+ brands | Few have captive placement |
| **Curriculum** | Designed by Lakmé National Creative Directors | Generic industry curriculum |
| **Fashion Week Access** | Lakmé Fashion Week backstage exposure | None |
| **International Pathway** | Dubai program (2025) | Very few offer this |
| **Certification** | B&WSSC + CIDESCO international | Most are only national |
| **Scale** | 150+ centers, 80K trained | VLCC, Orane (30-115 centers) |
| **Government Ties** | PMKVY, DDUGKY, NICSI, SWAYAM Plus | Limited |

---

## 7. IMMEDIATE ACTION ITEMS

1. **Data gathering**: Map all existing centers, their enrollment, revenue, profitability
2. **Identify top 50 untapped cities** with highest potential
3. **Design micro-courses** (1-3 month) for price-sensitive markets
4. **Launch digital marketing campaign** targeting Tier 2/3 youth
5. **Expand placement partnerships** from 50 to 100 brands
6. **International Pathway Program** — roll out to more countries
7. **Franchisee recruitment drive** in untapped states
8. **Government empanelment** in all states

---

## 8. OPEN QUESTIONS (To Discuss with Rajesh Singh Sir)

- What is the current **center-wise P&L**? Which centers are profitable?
- What's the **conversion rate** from inquiry to enrollment?
- What is the **average cost per acquisition** of a student?
- Are there **capacity constraints** at existing centers?
- What's the **appetite for online/hybrid** courses?
- What is the **budget/annual target** from leadership?
- Can we pilot a **"Lakmé Academy Lite"** model in a small city first?

---

> **Next Steps**: Use this document as a living brainstorming canvas. Let's add details, challenge assumptions, and build the execution roadmap together.

*Last updated: 26 May 2026*
