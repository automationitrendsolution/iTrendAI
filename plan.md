# 1. Project Overview
Please understand and review the Excel file carefully, as I am currently working on new product research. The main objective is to analyze market demand and competitor performance in detail. First, analyze the units sold and overall sales performance to understand the market demand and identify high-potential opportunities. Then, perform a detailed brand and competitor analysis to understand whether the market is dominated by specific brands or if there is room for new entrants. We have included the seller creation date, so please divide the sellers into two categories: old sellers (more than 2 years old) and new sellers (less than 2 years old). Analyze which brands and sellers are performing best in both categories and provide insights on the advantages and disadvantages if we launch our product in this market. Additionally, analyze the price ranges, keywords used in product titles, product images, listing quality, and any other important factors that can help in understanding the competition and market trends. Please add your own observations and analytical points wherever necessary and provide the final updated Excel file along with the complete analysis.

## Goal

Build an AI-powered Amazon product research and competitor intelligence platform using:

- Python
- Django
- Django REST Framework
- OpenAI SDK
- Pandas
- db.sqlite3

The platform will analyze:

- Market demand
- Units sold
- Revenue performance
- Brand dominance
- Seller maturity
- Old vs new sellers
- Listing quality
- Keywords
- Pricing
- Product images
- Competitive opportunities

The system should generate AI-powered strategic insights and downloadable reports.

---

# 2. Main Features

## Core Features

### 1. Excel Upload System

User uploads:
- Helium10 Excel data
- Product niche
- ASIN

Supported:
- XLSX
- CSV

---

### 2. Raw Data Viewer

Display:
- Excel rows
- Filters
- Search
- Sorting
- Pagination

---

### 3. Market Overview Analysis

Analyze:
- Total revenue
- Total units sold
- Average price
- Median price
- Market size
- Revenue concentration
- Sales distribution

---

### 4. Brand Analysis

Analyze:
- Top brands
- Brand revenue share
- Brand sales share
- Brand concentration
- Dominant brands

---

### 5. Old vs New Seller Analysis

Classify sellers:

- Old Seller → More than 2 years
- New Seller → Less than 2 years

Analyze:
- Revenue comparison
- Sales comparison
- Review comparison
- Market penetration
- New seller success rate

---

### 6. Listing Quality Analysis

Analyze:
- Title SEO
- Bullet points
- Description quality
- Keyword optimization
- Image quality
- Branding strength

Generate listing quality scores.

---

### 7. Keyword Analysis

Extract:
- Most used keywords
- Long-tail keywords
- Emotional words
- Conversion keywords

---

### 8. Price Analysis

Analyze:
- Low-price segment
- Mid-price segment
- Premium segment

Identify:
- Best-performing price range

---

### 9. AI Strategic Insights

Generate:
- Market opportunity
- Entry difficulty
- Competition level
- Pricing strategy
- Branding strategy
- Launch recommendation

---

### 10. Export Reports

Generate:
- Excel reports
- PDF reports

---

# 3. Recommended Tech Stack

## Backend

- Python 3.12
- Django
- Django REST Framework

---

## Database

- db.sqlite3

## AI

- OpenAI SDK

Recommended Models:
- GPT-5.5
- GPT-4.1

---

## Data Processing

- Pandas
- NumPy
- OpenPyXL

---

## NLP

- scikit-learn
- nltk

---

## Frontend
- Django Templates
- Bootstrap
---

## Charts

- ApexCharts
- Chart.js

---

# 4. System Architecture

```text
Frontend
    ↓
Django REST API
    ↓
Service Layer
    ↓
Analytics Engine
    ↓
AI Insight Engine
    ↓
Database + File Storage
```

---

# 5. Django Project Structure

```text
iTrendAI/
├── app/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsig.py
│   
│
├── iTrendAI/  # my company all department dashboard
│   ├── templates
│   ├── admin.py
│   ├── models.py
│   └── tests.py
│   ├── urls.py
│   └── views.py
├── agents/  # agents are create here
│   ├── admin.py
│   ├── models.py
│   └── tests.py
│   ├── urls.py
│   └── views.py
└── manage.py
```

---

# 6. Database Design

## ResearchProject

```python
class ResearchProject(models.Model):
    niche = models.CharField(max_length=255)

    asin = models.CharField(max_length=20)

    uploaded_file = models.FileField()

    created_at = models.DateTimeField(auto_now_add=True)
```

---

## ProductListing

```python
class ProductListing(models.Model):

    project = models.ForeignKey(ResearchProject)

    asin = models.CharField(max_length=20)

    title = models.TextField()

    brand = models.CharField(max_length=255)

    seller_name = models.CharField(max_length=255)

    seller_creation_date = models.DateField()

    price = models.DecimalField()

    monthly_sales = models.IntegerField()

    monthly_revenue = models.DecimalField()

    review_count = models.IntegerField()

    rating = models.FloatField()

    image_url = models.URLField()
```

# 8. Core Analytics Engine

## Market Demand Engine

Calculate:
- Total market revenue
- Units sold
- Avg monthly sales
- Avg reviews
- Competition score

---

## Brand Analysis Engine

Calculate:
- Top brands
- Revenue share
- Sales share
- Dominance score

---

## Seller Intelligence Engine

Logic:

```python
if seller_age_days > 730:
    category = "OLD"
else:
    category = "NEW"
```

Analyze:
- Old seller dominance
- New seller growth

---

## Listing Quality Engine

Generate scores:
- SEO Score
- Content Score
- Image Score
- Branding Score

---

## Keyword Engine

Use:
- TF-IDF
- NLP
- Frequency analysis

---

# 9. OpenAI Integration

## Use Cases

### Market Insights

Generate:
- Competition analysis
- Market opportunity

---

### Listing Analysis

Analyze:
- Titles
- Bullets
- Descriptions

---

### Strategy Generation

Generate:
- Launch strategy
- Pricing strategy
- Branding strategy

---

# 10. AI Agent Design

## Market Agent

Analyzes:
- Demand
- Revenue
- Saturation

---

## Brand Agent

Analyzes:
- Brand concentration
- Brand dominance

---

## Seller Agent

Analyzes:
- Seller maturity
- Seller performance

---

## SEO Agent

Analyzes:
- Keywords
- Listing quality

---

## Strategy Agent

Generates:
- Launch recommendation
- Risks
- Opportunities

---

# 11. Frontend Dashboard Sections

## 1. Raw Data Table

Features:
- Filters
- Search
- Export
- Pagination

---

## 2. KPI Cards

Show:
- Total Revenue
- Total Units Sold
- Avg Price
- Avg Reviews

---

## 3. Market Charts

Charts:
- Revenue distribution
- Sales distribution
- Price distribution

---

## 4. Brand Analysis

Charts:
- Brand market share
- Brand revenue share

---

## 5. Old vs New Sellers

Charts:
- Seller age distribution
- Revenue comparison

---

## 6. Listing Quality

Show:
- SEO scores
- Listing quality ranking

---

## 7. Strategic Insights

AI-generated recommendations.

---

# 12. Excel Export Structure

## Sheet 1
Raw Data

## Sheet 2
Market Overview

## Sheet 3
Brand Analysis

## Sheet 4
Seller Analysis

## Sheet 5
Listing Quality

## Sheet 6
Keyword Analysis

## Sheet 7
AI Strategic Insights
