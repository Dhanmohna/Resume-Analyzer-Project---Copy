# import streamlit as st
# from resume_parser import extract_text_from_pdf, extract_text_from_docx
# from nlp_processor import clean_text
# from skill_extractor import extract_skills
# from matching_engine import calculate_similarity
# #from jobs_data import JOBS
# from groq_engine import analyze_resume_with_groq
# import pandas as pd
# import json
# from scraper import scrape_jobs
# from scraper_internshala import scrape_internshala
# from scraper_remoteok import scrape_remoteok
# from scoring_engine import calculate_skill_score, calculate_resume_score
# from required_skills import REQUIRED_SKILLS
# import spacy

# nlp = spacy.load("en_core_web_sm")


# data = []

# try:
#     with open("jobs.ldjson", "r", encoding="utf-8") as f:
#         for line in f:
#             try:
#                 data.append(json.loads(line))
#             except:
#                 continue   # skip bad lines

#     jobs_df = pd.DataFrame(data)
    
    
# except Exception as e:
#     st.error(f"❌ Error loading dataset: {e}")

# st.set_page_config(page_title="Intelligent Resume Analyzer",layout="centered")

# # # Initialize the visibility state
# # if "show_ai_analysis" not in st.session_state:
# #     st.session_state.show_ai_analysis = False

# if "page" not in st.session_state:
#     st.session_state.page = "home"

# if st.session_state.page == "home":    

#     st.markdown(
#         """
#         <style>
#         header {visibility: hidden;}
#         body {
#             background-image: url("https://static.vecteezy.com/system/resources/previews/000/633/705/original/abstract-gradient-geometric-background-simple-shapes-with-trendy-gradients-vector.jpg");
#             background-size: cover;
#             background-repeat: no-repeat;
#             background-attachment: fixed;
#         }

#         /* Optional: add a light transparent overlay to make text readable */
#         .stApp {
#             background-color: transparent;
#         }

#         .block-container {
#                 padding-top: 1.5rem;
#             }

#         div[data-testid="stFileUploader"] span {
#             color: black !important;
#             font-weight: 500;
#         }

#         div[data-testid="stFileUploader"] {
        
#             background-color: white;
#             padding: 10px 10px !important;
#             border-radius: 8px;
#             border-top:6px solid purple !important;
#         }

#         div[data-testid="stFileUploader"] label {
#     display: none !important;
# }

#         div[data-baseweb="notification"] {
#             background-color: #ffffff !important;
#             color: #1b5e20 !important;
#             border-left: 6px solid #2e7d32 !important;
#             font-weight: 600;
#         }

#         div[data-testid="stFileUploader"] button {
#             background-color: #7B2CBF !important;   /* Violet */
#             color: white !important;
#             border-radius: 8px !important;
#             border: none !important;
#             font-weight: 600 !important;
#         }

#         [data-testid="stFileUploaderDropzone"] {
#     min-height: 20px !important; /* Default is ~200px, this cuts it by more than half */
#     padding: 2px !important;
#     display: flex;
#     flex-direction: row !important; /* Makes items sit side-by-side to save space */
#     align-items: center;
#     justify-content: center;
#     gap: 10px;
    
# }

#         div[data-baseweb="select"] > div {
#             border-radius: 10px;
#             font-size: 16px;
#             border-top:rgb(239 29 76) solid 6px !important;
            
#         }

#         .custom-label {
#         font-size: 20px;
#         font-weight: bold;
#         color: white;
#         text-align:center;
#         margin-bottom: 10px;
#         margin-top: 20px;
#     } 

      

# /* Styling the button specifically inside the column */
# div[data-testid="stButton"] > button {
#     background-color: #5A189A !important; /* Professional Violet */
#     color: white !important;
#     font-size: 18px !important;
#     font-weight: bold; /* Bold font weight */
#     border-radius: 12px !important; /* Rounded corners */
#     padding: 10px 10px !important;
#     border: 2px solid #9D4EDD !important; /* Subtle border */
#     transition: all 0.3s ease-in-out !important;
#     box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important;
#     text-transform: uppercase; /* Makes it look like a CTA */
#     letter-spacing: 1px;
# }

# div[data-testid="stButton"] > button p{
# color: white !important;
# font-weight: bold;
# }


# /* Hover effect to make it interactive */
# div[data-testid="stButton"] > button:hover {
#     background-color: #5A189A !important; /* Darker purple on hover */
#     border-color: #ffffff !important;
#     transform: scale(1.03); /* Slight grow effect */
#     box-shadow: 0px 6px 15px rgba(123, 44, 191, 0.4) !important;
# }

# /* Active/Click effect */
# div[data-testid="stButton"] > button:active {
#     transform: scale(0.98);
# }

# /* Target the toast container */
#     div[data-testid="stToast"] {
#         position: fixed;
#         bottom: 90%; /* Move to middle vertically */
#         left: 50%;   /* Move to middle horizontally */
#         transform: translate(-50%, 50%); /* Adjust for its own width/height */
#         width: auto;
#         min-width: 300px;
#         text-align: center;
#         z-index: 9999;
#     }

#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown("<h1 style='text-align:center;'>Intelligent Resume Analyzer</h1>", unsafe_allow_html=True)

#     st.markdown(
#         "<h3 style='text-align:center; color:purple; font-size:25px; font-weight:bold;'>"
#         "Take your resume to the next level with AI-powered insights." 
#     "</h3>",
#         unsafe_allow_html=True
#     )
#     st.markdown("<p style='color:white; font-size:17px;font-weight:bold;text-align:center;' >Our intelligent analyzer evaluates your skills, experience, and overall impact to generate a detailed score. Discover job matches tailored to your profile and receive actionable recommendations to strengthen your resume instantly.</p>", unsafe_allow_html=True)

#     st.markdown(
#         "<p style='text-align:center; color:black; font-size:22px; font-weight:bold;margin-top:20px;'>"
#         "Upload your resume to analyze job alignment "
#         "</p>",
#         unsafe_allow_html=True
#     )


#     uploaded_file = st.file_uploader(
#         label="",
#         type=["pdf","docx"]
#     )

#     st.markdown('<div class="custom-label">Select Target Job Role</div>', unsafe_allow_html=True)

#     job_role = st.selectbox("",["Data Scientist","Python Developer","Software Engineer","Product Manager","UX Designer","DevOps Engineer","Cybersecurity Analyst","Cloud Architect","AI Researcher","Mobile App Developer","Full Stack Developer","Data Analyst","Machine Learning Engineer","Business Analyst","Project Manager","QA Engineer","Network Engineer","Database Administrator","Technical Writer","IT Support Specialist","Systems Administrator","Front-end Developer","Back-end Developer","Data Engineer","AI Engineer","Security Engineer","Cloud Engineer","UI/UX Designer","DevOps Specialist","Cybersecurity Specialist","Cloud Solutions Architect","AI Research Scientist","Mobile Developer","Full Stack Web Developer","Data Analyst","Machine Learning Scientist","Business Intelligence Analyst","Project Coordinator","QA Tester","Network Administrator","Database Manager","Technical Communicator","IT Support Technician","Systems Engineer"],label_visibility="collapsed")

#     # Create 3 columns with a 1:1:1 ratio
#     col1, col2, col3 = st.columns([1, 1, 1])

# #Initialzing the toast flag to prevent multiple toasts on re-render
#     if "toast_shown" not in st.session_state:
#        st.session_state.toast_shown = False

#     if uploaded_file:
#         if not st.session_state.toast_shown:
#             st.toast("Resume File Uploaded Successfully!", icon="✅")
#             st.session_state.toast_shown = True
#         file_type = uploaded_file.name.split(".")[-1]
        
#         if(file_type) == "pdf":
#             resume_text = extract_text_from_pdf(uploaded_file)
#             st.session_state.resume_text = resume_text

#         elif(file_type) == "docx":
#             resume_text = extract_text_from_docx(uploaded_file)
#             st.session_state.resume_text = resume_text

#         else:
#             st.toast("Unsupported file type. Please upload a PDF or DOCX file.",icon="🚫")
#             resume_text = ""
    
    
#     with col2: # This places the button in the center column
#         if st.button("Analyze Resume", use_container_width=True):
#             if uploaded_file:
#                 st.session_state.page = "analysis"
#                 st.session_state.file = uploaded_file
#                 st.session_state.role = job_role
#                 st.rerun() 
#             else:
#                 st.toast("Please upload a resume file first!", icon="🚫")
    

# elif st.session_state.page == "analysis": 
#     st.set_page_config(page_title="Intelligent Resume Analyzer", layout="wide")

#     st.markdown("""
#         <style>
#         .stApp { background-image: none !important; background-color: white !important; }
#         header { visibility: visible !important; }
#         body { text-align: center !important; }
#         h1 { color: #6A0DAD !important; }
#         [data-testid="stHeader"] h1 {
#             color: purple;
#             text-align: center;
#             font-family: 'Arial';
#             font-size: 42px;
#         }
#         div[data-testid="stAppViewBlockContainer"] {
#             max-width: 95% !important;
#             width: 95% !important;
#             padding-left: 2rem !important;
#             padding-right: 2rem !important;
#         }
#         [data-testid="stVerticalBlock"] {
#             width: 100% !important;
#             max-width: 100% !important;
#         }
#         .analysis-title {
#             text-align: center;
#             width: 100%;
#             padding-bottom: 20px;
#             margin-bottom: 20px !important;
#         }
#         [data-testid="stMetric"] {
#             text-align: center;
#             padding: 10px;
#             background-color: #f0f2f6;
#             border-radius: 10px;
#             width: fit-content;
#         }
#         [data-testid="stVerticalBlock"] > div:first-child {
#             margin-top: -20px !important;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     # 1. Retrieve data from session state
#     uploaded_file = st.session_state.get("file")
#     job_role = st.session_state.get("role") 
#     resume_text = st.session_state.get("resume_text")   

#     # Navigation Header
#     with st.container():
#         st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
#         col_back, col_title, col_empty = st.columns([1, 6, 1])
#         with col_back:
#             st.markdown("<div style='padding-top: 28px;'>", unsafe_allow_html=True)
#             if st.button("⬅️ Back"):
#                 st.session_state.page = "home"
#                 st.rerun()
#         with col_title:
#             st.markdown(f"<h1 style='margin-bottom: 40px; text-align: center; color: violet;'>Analysis for {job_role}</h1>", unsafe_allow_html=True)

#     if uploaded_file is not None and resume_text:
#         # --- PRE-PROCESSING (Outside the Loop for Speed) ---
#         resume_cleaned = clean_text(resume_text)
#         candidate_skills = extract_skills(resume_cleaned)
#         resume_doc = nlp(resume_text)  # Process resume once with spaCy

#         st.subheader("Job Matching Results:")
        
#         with st.spinner("🔍 Scanning datasets and live job boards... Please wait."):
#             # This array will hold the raw listings from ALL sources
#             raw_jobs_pool = []

#             # ---------------------------------------------------------
#             # SOURCE 1: Static Dataset (Indeed Kaggle)
#             # ---------------------------------------------------------
#             try:
#                 if 'jobs_df' in globals():
#                     filtered_jobs = jobs_df[
#                         jobs_df["job_title"].str.contains(job_role, case=False, na=False)
#                     ].head(25)

#                     for _, job in filtered_jobs.iterrows():
#                         if pd.isna(job["job_description"]) or not str(job["job_description"]).strip():
#                             continue
#                         raw_jobs_pool.append({
#                             "title": job["job_title"],
#                             "company": job["company_name"],
#                             "description": str(job["job_description"]),
#                             "url": job["url"],
#                             "source": "Indeed Dataset"
#                         })
#             except Exception as e:
#                 st.warning(f"Error reading from static dataset: {e}")

#             # ---------------------------------------------------------
#             # SOURCE 2: Live Internshala Scraping
#             # ---------------------------------------------------------
#             try:
#                 internshala_jobs = scrape_internshala(job_role)
#                 for job in internshala_jobs:
#                     if job.get("description"):
#                         raw_jobs_pool.append({
#                             "title": job["title"],
#                             "company": job["company"],
#                             "description": job["description"],
#                             "url": job["url"],
#                             "source": "Internshala"
#                         })
#             except Exception as e:
#                 st.sidebar.warning(f"Internshala scraping skipped or failed: {e}")

#             # ---------------------------------------------------------
#             # SOURCE 3: Live RemoteOK Scraping
#             # ---------------------------------------------------------
#             try:
#                 remote_jobs = scrape_remoteok(job_role)
#                 for job in remote_jobs:
#                     if job.get("description"):
#                         raw_jobs_pool.append({
#                             "title": job["title"],
#                             "company": job["company"],
#                             "description": job["description"],
#                             "url": job["url"],
#                             "source": "RemoteOK"
#                         })
#             except Exception as e:
#                 st.sidebar.warning(f"RemoteOK scraping skipped or failed: {e}")

#             # ---------------------------------------------------------
#             # UNIFIED PROCESSING LOOP (Calculates Scores for Everything)
#             # ---------------------------------------------------------
#             processed_results = []

#             for job in raw_jobs_pool:
#                 # Dynamic Skill Extraction from the current listing description
#                 job_req_skills = extract_skills(clean_text(job["description"]))

#                 # Calculate Skill Match Score (40% weight input)
#                 skill_match_score = calculate_skill_score(candidate_skills, job_req_skills)

#                 # Calculate Semantic Similarity using the preprocessed doc (60% weight input)
#                 similarity_score = calculate_similarity(resume_doc, job["description"])

#                 processed_results.append({
#                     "title": job["title"],
#                     "company": job["company"],
#                     "description": job["description"],
#                     "url": job["url"],
#                     "source": job["source"],
#                     "req_skills": job_req_skills,
#                     "skill_match": skill_match_score,
#                     "similarity": similarity_score
#                 })

#             # Sort the entire combined pool by Semantic Similarity
#             processed_results = sorted(processed_results, key=lambda x: x["similarity"], reverse=True)

#             # ---------------------------------------------------------
#             # UI DISPLAY: RENDER RESULTS
#             # ---------------------------------------------------------
#             if processed_results:
#                 # Extract metrics from the absolute #1 best matching job card found across all sources
#                 top_match = processed_results[0]
#                 final_skill_match = top_match["skill_match"]
#                 final_sim_score = top_match["similarity"]
                
#                 # Case-insensitive skill gap tracking to avoid version conflicts
#                 missing_skills = []
#                 candidate_lower = [s.lower() for s in candidate_skills]
#                 for req in top_match["req_skills"]:
#                     if req.lower() not in candidate_lower:
#                         if not any(req.lower() in c.lower() for c in candidate_skills):
#                             missing_skills.append(req)

#                 # Run your math function to generate the Master "Overall Fit" score
#                 overall_score = calculate_resume_score(final_sim_score, final_skill_match)

#                 # --- TOP ROW: MASTER METRICS & JOB GAP ---
#                 col_score, col_ai, col_gap = st.columns([1, 1, 1])

#                 with col_score:
#                     st.subheader("📊 Performance Score")
#                     st.metric(label="Top Skill Match", value=f"{final_skill_match:.1f}%")
#                     st.caption(f"Source: {top_match['source']} ({top_match['company']})")

#                 with col_ai:
#                     st.markdown("<div style='padding-top: 45px;'></div>", unsafe_allow_html=True)
#                     if st.button("✨ Run AI Career Deep Dive"):
#                         st.session_state.page = "ai_analysis"
#                         st.rerun()
                    
#                 with col_gap:
#                     st.markdown("<h3 style='text-align: right;'>⚠️ Skill Gap</h3>", unsafe_allow_html=True)
#                     if missing_skills:
#                         for s in missing_skills[:5]: 
#                             st.markdown(f"<p style='text-align: right; margin:0;'>❌ Missing: <b>{s.capitalize()}</b></p>", unsafe_allow_html=True)
#                     else:
#                         st.markdown("<p style='text-align: right; color: green;'>🎯 Perfect technical match!</p>", unsafe_allow_html=True)

#                 st.divider()

#                 # --- OVERALL FIT CARD ---
#                 st.markdown(f"""
#                 <div style="background-color: #fff3cd; padding: 25px; border-radius: 12px; text-align:center; border: 1px solid #ffeeba; margin-bottom: 25px;">
#                     <h2 style="color: #856404; margin-bottom:10px;">Overall Fit: {overall_score:.2f} / 100</h2>
#                     <p style="margin:0; font-weight: bold;">Matches {len(set(candidate_skills).intersection(set(top_match['req_skills'])))} out of {len(top_match['req_skills'])} detected skills.</p>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 # --- JOB CARDS DISPLAY (Top 15 listings across all platforms) ---
#                 for job in processed_results[:15]:
#                     st.markdown(f"""
#                     <div style="background-color: white; padding: 18px; border-radius: 12px; margin-top: 15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); border-left: 6px solid #6A0DAD;">
#                         <h4 style='margin-bottom: 5px;'>{job['title']}</h4>
#                         <p style='color:purple; font-weight:bold; margin-bottom:2px;'>{job['company']}</p>
#                         <p style='color:gray; font-size: 12px; margin-bottom:8px;'>Platform Source: <b>{job['source']}</b></p>
#                         <p style='font-size: 14px; margin-bottom: 10px;'>
#                             <span style='background:#e1bee7; padding:2px 8px; border-radius:4px;'><b>Skill Match:</b> {job['skill_match']:.1f}%</span> 
#                             <span style='background:#f3e5f5; padding:2px 8px; border-radius:4px; margin-left:10px;'><b>Similarity:</b> {job['similarity']:.1f}%</span>
#                         </p>
#                         <p style='font-size: 13px; color: #555;'>{job['description'][:220]}...</p>
#                         <a href="{job['url']}" target="_blank" style="text-decoration: none; color: #6A0DAD; font-weight: bold; font-size: 15px;">🔗 View Details</a>
#                     </div>
#                     """, unsafe_allow_html=True)
#             else:
#                 st.warning(f"No matching jobs found for '{job_role}' from any source.")

# elif st.session_state.page == "ai_analysis":
#             st.set_page_config(page_title="Intelligent Resume Analyzer",layout="wide")
#             job_role = st.session_state.get("role") 
#             resume_text = st.session_state.get("resume_text")   
#             if resume_text and job_role:
#                 if st.button("⬅️ Back"):
#                     st.session_state.page = "analysis"
#                     st.rerun()
#                 with st.spinner("Analyzing resume with AI..."):
#                     ai_response = analyze_resume_with_groq(resume_text, job_role)
#                     st.markdown(f"""
#                 <div style="
#             background-color: #f0f8ff; 
#             padding: 15px; 
#             border-radius: 10px; 
#             margin-bottom: 15px;
#             box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
#                 ">
#                 <h5 style='margin:0;font-weight:bold;'>AI Career Analysis</h5>
#                 <p style='margin:5px 0;'>{ai_response}</p>
#             </div>
#             """, unsafe_allow_html=True)

#             else:
#                 st.error("Could not extract text from resume")
    