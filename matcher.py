import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_jobs(path="jobs_sample.csv"):
    """Load job postings and turn the 'skills' column (a;b;c) into a clean list of skills."""
    df = pd.read_csv(path)
    df["skill_list"] = df["skills"].apply(
        lambda text: [s.strip().lower() for s in str(text).split(";") if s.strip()]
    )
    return df


def match_jobs(df, user_skills, city="All", top_n=5):
    """Rank jobs by TF-IDF + cosine similarity between the user's skills and each job's skills."""
    user_skills = [s.strip().lower() for s in user_skills if s.strip()]
    pool = df if city == "All" else df[df["city"] == city]
    pool = pool.reset_index(drop=True).copy()
    if pool.empty or not user_skills:
        return pool.head(0)

    # Each skill is one token, so multi-word skills like "machine learning" stay intact
    vectorizer = TfidfVectorizer(tokenizer=lambda t: t.split(";"), lowercase=False, token_pattern=None)
    job_matrix = vectorizer.fit_transform([";".join(skills) for skills in pool["skill_list"]])
    user_vector = vectorizer.transform([";".join(user_skills)])

    pool["match_score"] = cosine_similarity(user_vector, job_matrix).ravel()
    top = pool.sort_values("match_score", ascending=False).head(top_n).copy()
    top["match_pct"] = (top["match_score"] * 100).round(1)
    return top


def missing_skills(top_jobs, user_skills):
    """Count how often each skill the user lacks appears in the top matching jobs."""
    have = {s.strip().lower() for s in user_skills}
    counter = Counter()
    for skills in top_jobs["skill_list"]:
        for skill in skills:
            if skill not in have:
                counter[skill] += 1
    return pd.DataFrame(counter.most_common(), columns=["skill", "jobs_needing_it"])
