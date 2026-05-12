# EV Charging Analytics Platform

Production-ready analytics platform for automated PowerPoint generation based on Google Sheets data.

## Stack

- Streamlit
- pandas
- Plotly
- python-pptx
- Pillow
- loguru
- pydantic

## Features

- Google Sheets integration
- Automated analytics
- Slide preview system
- PPTX generation
- Unified rendering pipeline
- Modern BI dashboard UI
- Export history tracking
- Template-based PPT rendering
- PNG chart rendering
- Layout engine

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud Deploy

1. Push repository to GitHub
2. Open Streamlit Cloud
3. Create new app
4. Select repository
5. Main file path:

```bash
app.py
```

6. Deploy application

## PPT Template

Place your corporate PowerPoint template in:

```bash
templates/base_template.pptx
```

If template is not provided, fallback rendering will be used.
