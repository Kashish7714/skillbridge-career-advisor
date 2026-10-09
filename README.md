# SkillBridge: AI Career Advisor (SDG 8)

An AI career guidance prototype for job seekers in Tier-2/3 cities, built for the IBM SkillsBuild | AICTE | BharatCares ML & Applied AI Internship 2026.

**SDG 8: Decent Work and Economic Growth.** Learners often do not know which skills employers demand, which roles fit them, or what to learn next. SkillBridge turns a learner's skills and city into a ranked list of jobs, a skill-gap analysis and a learning path.

## How it works
1. The learner selects their skills and preferred city.
2. Skills are converted into TF-IDF vectors and compared with each job using cosine similarity (scikit-learn).
3. The top 5 jobs are shown with a match percentage.
4. The most frequent skills missing in those jobs are charted, with a free tutorial link for each.

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py`: Streamlit interface
- `matcher.py`: loading, TF-IDF matching and skill-gap logic
- `jobs_sample.csv`: small illustrative job dataset (columns: title, city, skills)

## Limitations (honest notes)
- The included dataset is a small hand-made sample for demonstration, not scraped or real market data.
- No accuracy figures are reported yet because the prototype has not been evaluated on a full real dataset.

## Next steps
- Replace the sample with a real job-postings dataset (same columns: title, city, skills).
- Evaluate with a top-5 retrieval test (hide part of each job's skills and check if the job is still found).
- Add live job data through an API, resume upload, and regional-language support.

Author: Kashish
