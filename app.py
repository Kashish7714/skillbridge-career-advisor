import urllib.parse

import streamlit as st

from matcher import load_jobs, match_jobs, missing_skills

st.set_page_config(page_title="SkillBridge", page_icon="🌉", layout="wide")

st.title("SkillBridge: AI Career Advisor")
st.caption("SDG 8: Decent Work and Economic Growth | Skill-job matching for learners in Tier-2/3 cities")

jobs = load_jobs()
all_skills = sorted({skill for skills in jobs["skill_list"] for skill in skills})
cities = ["All"] + sorted(jobs["city"].unique())

left, right = st.columns([2, 1])
with left:
    my_skills = st.multiselect("Your skills", all_skills, default=["python", "pandas", "sql"])
with right:
    city = st.selectbox("Preferred city", cities)

if st.button("Find my best-fit jobs", type="primary"):
    top = match_jobs(jobs, my_skills, city, top_n=5)

    if top.empty or top["match_score"].max() == 0:
        st.warning("No matching jobs found. Try adding more skills or choosing another city.")
    else:
        st.subheader("Top matching jobs")
        st.dataframe(
            top[["title", "city", "match_pct", "skills"]].rename(
                columns={"title": "Job title", "city": "City", "match_pct": "Match %", "skills": "Required skills"}
            ),
            hide_index=True,
        )

        gaps = missing_skills(top, my_skills)
        st.subheader("Skills you are missing")
        if gaps.empty:
            st.success("You already have every skill listed in these top jobs.")
        else:
            st.bar_chart(gaps.set_index("skill")["jobs_needing_it"])
            st.subheader("Learning path (start from the top)")
            for skill in gaps["skill"].head(5):
                link = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(f"{skill} tutorial for beginners")
                st.markdown(f"- **{skill}**: [find free tutorials]({link})")

st.divider()
st.caption("Prototype note: this demo runs on a small illustrative job dataset (jobs_sample.csv). "
           "The same pipeline can be pointed at a real job-postings CSV with the columns title, city, skills.")
