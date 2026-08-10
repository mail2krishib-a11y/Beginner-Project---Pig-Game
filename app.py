import streamlit as st
from pypdf import PdfReader
from google import genai
import json
import re

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="CareerOS", page_icon="🛠️", layout="wide")
st.title("🛠️ CareerOS")
st.caption("Upload your resume → get a skill gap report, project recommendations, interview prep, and a 6-month roadmap — powered by Google Gemini.")

# ----------------------------
# Sidebar: API key + target role
# ----------------------------
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Google AI (Gemini) API Key", type="password",
                             help="Get a free key at https://aistudio.google.com/apikey")
    target_role = st.text_input("Target Role", placeholder="e.g. Data Scientist, SDE-1, ML Engineer")
    st.divider()
    st.markdown("**Pipeline**")
    st.markdown("1. Upload Resume\n2. Extract Skills\n3. AI Analysis\n4. Skill Gap Report\n5. Project Recommendations\n6. Interview Questions\n7. 6-Month Roadmap")

client = None

if api_key:
    client = genai.Client(api_key=api_key)

MODEL_NAME = "models/gemini-flash-latest"

# ----------------------------
# Helpers
# ----------------------------
def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def call_gemini(prompt: str) -> str:

    if client is None:
        raise Exception("API key not provided")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def extract_json(raw: str):
    """Gemini sometimes wraps JSON in ```json fences — strip and parse safely."""
    cleaned = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


# ----------------------------
# Session state
# ----------------------------
for key in ["resume_text", "skills", "analysis", "gap_report",
            "projects", "interview_qs", "roadmap"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ----------------------------
# Step 1: Upload Resume
# ----------------------------
st.subheader("1️⃣ Upload Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
    st.success(f"Extracted {len(st.session_state.resume_text)} characters from resume.")
    with st.expander("Preview extracted text"):
        st.text(st.session_state.resume_text[:2000] + ("..." if len(st.session_state.resume_text) > 2000 else ""))

# ----------------------------
# Run pipeline button
# ----------------------------
run_disabled = not (uploaded_file and api_key and target_role)
if run_disabled:
    st.info("Upload a resume, enter your Gemini API key, and specify a target role to continue.")

if st.button("🚀 Run Full Analysis", disabled=run_disabled, type="primary"):
    resume_text = st.session_state.resume_text

    # 2. Extract Skills
    with st.spinner("Extracting skills..."):
        skills_prompt = f"""You are a resume parser. Extract the technical and soft skills from this resume as a JSON list of strings only, no explanation.
Resume:
{resume_text}

Respond ONLY with valid JSON in this exact format: {{"skills": ["skill1", "skill2", ...]}}"""
        raw = call_gemini(skills_prompt)
        st.session_state.skills = extract_json(raw).get("skills", [])

    # 2b.Score tracer
    with st.spinner("Scoring resume against ATS criteria..."):
        score_prompt = f"""
Act as an ATS system.
Score this resume from 0-100.
Resume:
{resume_text}
Return ONLY:
{{
"score": 85,
"feedback": "..."
}}
"""
        raw = call_gemini(score_prompt)
        st.session_state.ats_score = extract_json(raw)
    # 3 & 4. AI Analysis + Skill Gap Report
    with st.spinner("Analyzing skill gaps for target role..."):
        gap_prompt = f"""You are a career coach AI. The candidate has these skills: {st.session_state.skills}
Their target role is: {target_role}

Respond ONLY with valid JSON in this exact format:
{{
  "matched_skills": ["skill", ...],
  "missing_skills": ["skill", ...],
  "skill_gap_summary": "2-3 sentence summary of overall readiness for the role"
}}"""
        raw = call_gemini(gap_prompt)
        st.session_state.gap_report = extract_json(raw)

    # 5. Project Recommendations
    with st.spinner("Generating project recommendations..."):
        proj_prompt = f"""The candidate is missing these skills for the role of {target_role}: {st.session_state.gap_report.get('missing_skills', [])}
Suggest 3 hands-on portfolio projects that would help close these gaps.

Respond ONLY with valid JSON in this exact format:
{{"projects": [{{"title": "...", "description": "...", "skills_covered": ["...", "..."]}}]}}"""
        raw = call_gemini(proj_prompt)
        st.session_state.projects = extract_json(raw).get("projects", [])

    # 6. Interview Questions
    with st.spinner("Preparing interview questions..."):
        interview_prompt = f"""Generate 6 likely interview questions for a candidate applying to {target_role}, based on their skills: {st.session_state.skills}.
Mix technical and behavioral questions.

Respond ONLY with valid JSON in this exact format:
{{"questions": [{{"question": "...", "type": "technical or behavioral", "tip": "short answering tip"}}]}}"""
        raw = call_gemini(interview_prompt)
        st.session_state.interview_qs = extract_json(raw).get("questions", [])

    # 7. 6-Month Roadmap
    with st.spinner("Building 6-month roadmap..."):
        roadmap_prompt = f"""Create a 6-month learning roadmap (month by month) to help this candidate go from their current skills {st.session_state.skills} to being job-ready for {target_role}, closing these gaps: {st.session_state.gap_report.get('missing_skills', [])}.

Respond ONLY with valid JSON in this exact format:
{{"roadmap": [{{"month": 1, "focus": "...", "goals": ["...", "..."]}}]}}"""
        raw = call_gemini(roadmap_prompt)
        st.session_state.roadmap = extract_json(raw).get("roadmap", [])

    st.success("Analysis complete! Scroll down to see your results.")

# ----------------------------
# Display results in tabs
# ----------------------------
if st.session_state.skills:
    tabs = st.tabs(["Skills", "Gap Report", "Project Recommendations", "Interview Questions", "6-Month Roadmap"])

    with tabs[0]:
        st.subheader("Extracted Skills")
        st.write(", ".join(st.session_state.skills))

    with tabs[1]:
        st.subheader("Skill Gap Report")
        gr = st.session_state.gap_report
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Matched Skills**")
            for s in gr.get("matched_skills", []):
                st.markdown(f"- {s}")
        with col2:
            st.markdown("**❌ Missing Skills**")
            for s in gr.get("missing_skills", []):
                st.markdown(f"- {s}")
        st.info(gr.get("skill_gap_summary", ""))

    with tabs[2]:
        st.subheader("Recommended Projects")
        for p in st.session_state.projects:
            with st.expander(f"📌 {p.get('title')}"):
                st.write(p.get("description"))
                st.caption("Skills covered: " + ", ".join(p.get("skills_covered", [])))

    with tabs[3]:
        st.subheader("Likely Interview Questions")
        for q in st.session_state.interview_qs:
            with st.expander(f"❓ {q.get('question')} ({q.get('type')})"):
                st.write("**Tip:** " + q.get("tip", ""))

    with tabs[4]:
        st.subheader("6-Month Roadmap")
        for m in st.session_state.roadmap:
            with st.expander(f"Month {m.get('month')}: {m.get('focus')}"):
                for g in m.get("goals", []):
                    st.markdown(f"- {g}")
