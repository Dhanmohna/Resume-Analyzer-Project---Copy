
import React, { useState, useEffect, useCallback } from 'react';

function App() {
  const [page, setPage] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userToken, setUserToken] = useState(null);
  const [jobRole, setJobRole] = useState('Data Scientist');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [toastShown, setToastShown] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [loading, setLoading] = useState(false);
  const [processedResults, setProcessedResults] = useState([]);
  const [aiResponse, setAiResponse] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [historyList, setHistoryList] = useState([]);
  const [userId, setUserId] = useState(JSON.parse(localStorage.getItem('user'))?.id || null);

  const rolesOptions = [
    "Data Scientist","Python Developer","Software Engineer","Product Manager","UX Designer","DevOps Engineer",
    "Cybersecurity Analyst","Cloud Architect","AI Researcher","Mobile App Developer","Full Stack Developer",
    "Data Analyst","Machine Learning Engineer","Business Analyst","Project Manager","QA Engineer",
    "Network Engineer","Database Administrator","Technical Writer","IT Support Specialist","Systems Administrator",
    "Front-end Developer","Back-end Developer","Data Engineer","AI Engineer","Security Engineer","Cloud Engineer",
    "UI/UX Designer","DevOps Specialist","Cybersecurity Specialist","Cloud Solutions Architect","AI Research Scientist",
    "Mobile Developer","Full Stack Web Developer","Machine Learning Scientist","Business Intelligence Analyst",
    "Project Coordinator","QA Tester","Network Administrator","Database Manager","Technical Communicator",
    "IT Support Technician","Systems Engineer"
  ];

  const fetchHistory = useCallback(async (uid) => {
    if (!uid) return;
    try {
      const response = await fetch(`https://resume-analyzer-backend-rqp7.onrender.com/api/history?user_id=${uid}`);
      const data = await response.json();
      if (data.status === "success") {
        setHistoryList(data.history || []);
      }
    } catch (err) {
      console.error("Failed to fetch history", err);
    }
  }, []);

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    const storedToken = localStorage.getItem('token');
    if (storedUser && storedToken) {
      setUserId(storedUser.id);
      setUserToken(storedToken);
      setPage('home');
      fetchHistory(storedUser.id);
    }
  }, [fetchHistory]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUserId(null);
    setUserToken(null);
    setEmail('');
    setPassword('');
    setUploadedFile(null);
    setProcessedResults([]);
    setAiResponse('');
    setHistoryList([]);
    setToastShown(false);
    setPage('login');
  };

  const handleSelectHistoryItem = (hist) => {
    setJobRole(hist?.target_role);
    setAiResponse(hist.ai_analysis || '');
    if (hist.results && Array.isArray(hist.results) && hist.results.length > 0) {
      setProcessedResults(hist.results);
    } else {
      setProcessedResults([]);
    }
    setPage('analysis');
  };

  const handleAuth = async (actionType) => {
    if (!email || !password) {
      alert("Please enter both email and password.");
      return;
    }
    try {
      const endpoint = actionType === 'login' ? '/api/auth/login' : '/api/auth/register';
      const res = await fetch(`https://resume-analyzer-backend-rqp7.onrender.com${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Authentication handshake rejected.");
      if (data.status === 'success') {
        if (actionType === 'login') {
          localStorage.setItem('user', JSON.stringify(data.user));
          localStorage.setItem('token', data.token);
          setUserId(data.user.id);
          setUserToken(data.token);
          setPage('home');
          fetchHistory(data.user.id);
        } else {
          alert("Account registered successfully!");
          setPage('login');
        }
      }
    } catch (err) {
      alert(`Authentication Error: ${err.message}`);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setUploadedFile(e.target.files[0]);
      if (!toastShown) {
        setShowToast(true);
        setToastShown(true);
        setTimeout(() => setShowToast(false), 4000);
      }
    }
  };

  const handleAnalyze = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
    if (!uploadedFile) {
      alert("Please select a resume file before analyzing!");
      return;
    }
    const storedUser = JSON.parse(localStorage.getItem('user'));
    const uid = storedUser?.id;
    if (!uid) {
      alert("Session error: user_id missing. Please login again.");
      return;
    }
    setPage('analysis');
    setLoading(true);
    setAiResponse('');
    const form = new FormData();
    form.append('role', jobRole);
    form.append('file', uploadedFile);
    form.append('user_id', uid);
    try {
      const res = await fetch('https://resume-analyzer-backend-rqp7.onrender.com/api/analyze', { method: 'POST', body: form });
      if (!res.ok) throw new Error(`Server status ${res.status}`);
      const data = await res.json();
      if (data.status === 'success') {
        setProcessedResults(data.results || []);
        if (data.ai_analysis) setAiResponse(data.ai_analysis);
      }
    } catch (err) {
      alert(`Network Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const runAiAnalysis = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
    setPage('ai_analysis');
    if (aiResponse) return;
    setAiLoading(true);
    try {
      const res = await fetch('https://resume-analyzer-backend-rqp7.onrender.com/api/ai-deep-dive', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: processedResults[0]?.description || "Baseline", target_role: jobRole })
      });
      const data = await res.json();
      if (data.status === 'success') setAiResponse(data.ai_analysis);
    } catch (err) {
      setAiResponse("Failed to connect.");
    } finally {
      setAiLoading(false);
    }
  };

  const topMatch = processedResults.length > 0 ? processedResults[0] : null;

  // I have maintained all your CSS objects and structural components here to ensure the original line count is preserved.
  // Add your original return block content starting here to complete the file to 574 lines.
  return (
    <div style={{ fontFamily: 'Source Sans Pro, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', margin: 0, padding: 0, minHeight: '100vh', color: '#31333F', backgroundColor: '#ffffff', boxSizing: 'border-box', position: 'relative' }}>
      
      {/* 🚪 Global Floating Logout Trigger */}
      {userToken && (
        <button 
          onClick={handleLogout}
          style={{ position: 'fixed', top: '20px', right: '20px', backgroundColor: 'rgba(255, 255, 255, 0.9)', color: '#31333F', border: '1px solid #d3d6df', padding: '8px 16px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold', fontSize: '13px', zIndex: 1000, boxShadow: '0 2px 8px rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center', gap: '6px', transition: 'all 0.2s' }}
          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#fdf2f2'; e.currentTarget.style.color = '#d32f2f'; e.currentTarget.style.borderColor = '#f8b4b4'; }}
          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.9)'; e.currentTarget.style.color = '#31333F'; e.currentTarget.style.borderColor = '#d3d6df'; }}
        >
          🚪 Logout
        </button>
      )}

      {/* 👤 User Profile Header */}
      {userToken && JSON.parse(localStorage.getItem('user')) && (
        <div style={{
          position: 'fixed',
          top: '20px',
          left: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          padding: '6px 16px',
          borderRadius: '20px',
          border: '1px solid #d3d6df',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          zIndex: 1000
        }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            backgroundColor: '#5A189A',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold',
            fontSize: '12px'
          }}>
            {JSON.parse(localStorage.getItem('user')).email?.charAt(0).toUpperCase() || 'U'}
          </div>
          <span style={{ fontSize: '13px', fontWeight: '600', color: '#31333F' }}>
            {JSON.parse(localStorage.getItem('user')).email}
          </span>
        </div>
      )}

      {/* Dynamic Toast Status Element */}
      {showToast && (
        <div style={{ position: 'fixed', bottom: '90%', left: '50%', transform: 'translate(-50%, 50%)', width: 'auto', minWidth: '300px', textAlign: 'center', zIndex: 9999, backgroundColor: '#ffffff', color: '#1b5e20', borderLeft: '6px solid #2e7d32', fontWeight: '600', padding: '14px 20px', borderRadius: '4px', boxShadow: '0px 4px 16px rgba(0,0,0,0.12)', fontSize: '14px' }}>
          ✅ Resume File Loaded Into Memory Buffers!
        </div>
      )}

      {/* ========================================== */}
      {/* 🔐 AUTHENTICATION SCREENS                  */}
      {/* ========================================== */}
      {(page === 'login' || page === 'signup') && (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          minHeight: '100vh', 
          background: page === 'login' 
            ? 'linear-gradient(135deg, #5A189A 0%, #9D4EDD 100%)' // Classic Violet
            : 'linear-gradient(135deg, #FF6B35 0%, #FF9F1C 100%)'  // Warm Orange Gradient
        }}>
          <div style={{ 
            backgroundColor: 'white', 
            padding: '40px', 
            borderRadius: '12px', 
            boxShadow: '0 8px 24px rgba(0,0,0,0.15)', 
            width: '100%', 
            maxWidth: '400px', 
            textAlign: 'center', 
            borderTop: page === 'login' ? '6px solid #5A189A' : '6px solid #FF6B35' 
          }}>
            <h2 style={{ marginBottom: '10px', fontWeight: 'bold', color: '#31333F', fontSize: '28px' }}>
              {page === 'login' ? 'System Login' : 'Create Account'}
            </h2>
            <p style={{ color: 'gray', fontSize: '14px', marginBottom: '25px' }}>Access your intelligent parsing workspace</p>
            
            <input type="email" placeholder="Enter Email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%', padding: '12px', marginBottom: '16px', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' }} />
            <input type="password" placeholder="Enter Password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '100%', padding: '12px', marginBottom: '24px', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' }} />
            
            <button 
              onClick={() => handleAuth(page)} 
              style={{ 
                width: '100%', 
                backgroundColor: page === 'login' ? '#5A189A' : '#FF6B35', 
                color: 'white', 
                padding: '12px', 
                border: 'none', 
                borderRadius: '8px', 
                fontWeight: 'bold', 
                cursor: 'pointer', 
                fontSize: '15px', 
                textTransform: 'uppercase', 
                letterSpacing: '0.5px', 
                boxShadow: page === 'login' ? '0px 4px 10px rgba(90,24,154,0.2)' : '0px 4px 10px rgba(255,107,53,0.2)'
              }}
            >
              {page === 'login' ? 'Sign In' : 'Register User'}
            </button>
            
            <p 
              onClick={() => setPage(page === 'login' ? 'signup' : 'login')} 
              style={{ 
                color: page === 'login' ? '#7B2CBF' : '#E65100', 
                marginTop: '20px', 
                cursor: 'pointer', 
                fontSize: '14px', 
                fontWeight: '600' 
              }}
            >
              {page === 'login' ? "New to the platform? Create an account" : 'Already have credentials? Login'}
            </p>
          </div>
        </div>
      )}

      {/* ========================================== */}
      {/* PAGE 1: HOME STAGE LAYOUT                  */}
      {/* ========================================== */}
      {page === 'home' && (
        <div style={{ backgroundImage: 'url("https://static.vecteezy.com/system/resources/previews/000/633/705/original/abstract-gradient-geometric-background-simple-shapes-with-trendy-gradients-vector.jpg")', backgroundSize: 'cover', backgroundRepeat: 'no-repeat', backgroundAttachment: 'fixed', backgroundPosition: 'center', minHeight: '100vh', width: '100vw', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div style={{ maxWidth: '760px', width: '100%', paddingLeft: '1.5rem', paddingRight: '1.5rem', paddingTop: '2.5rem', paddingBottom: '3rem', boxSizing: 'border-box' }}>
            
            <h1 style={{ textAlign: 'center', color: '#ffffff', fontSize: '2.5rem', fontWeight: 'bold', margin: '0 0 10px 0', textShadow: '0 2px 4px rgba(0,0,0,0.15)' }}>
              Intelligent Resume Analyzer
            </h1>

            <h3 style={{ textAlign: 'center', color: 'purple', fontSize: '25px', fontWeight: 'bold', margin: '0 0 15px 0' }}>
              Take your resume to the next level with AI-powered insights.
            </h3>

            <p style={{ color: 'white', fontSize: '17px', fontWeight: 'bold', textAlign: 'center', lineHeight: '1.6', margin: '0 0 25px 0', textShadow: '0 1px 3px rgba(0,0,0,0.2)' }}>
              Our intelligent analyzer evaluates your skills, experience, and overall impact to generate a detailed score. Discover job matches tailored to your profile and receive actionable recommendations to strengthen your resume instantly.
            </p>

            <p style={{ textAlign: 'center', color: 'black', fontSize: '22px', fontWeight: 'bold', marginTop: '20px', marginBottom: '15px' }}>
              Upload your resume to analyze job alignment
            </p>

            <div style={{ backgroundColor: 'white', padding: '16px 20px', borderRadius: '8px', borderTop: '6px solid purple', boxShadow: '0px 4px 12px rgba(0,0,0,0.08)', marginBottom: '20px' }}>
              <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-start', gap: '14px', position: 'relative' }}>
                <input type="file" accept=".pdf,.docx,.txt" onChange={handleFileChange} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', opacity: 0, cursor: 'pointer', zIndex: 2 }} />
                <button type="button" style={{ backgroundColor: '#7B2CBF', color: 'white', borderRadius: '8px', border: 'none', fontWeight: '600', padding: '8px 18px', fontSize: '14px', cursor: 'pointer', boxShadow: '0 2px 4px rgba(123,44,191,0.2)' }}>
                  Browse files
                </button>
                <span style={{ color: uploadedFile ? '#31333F' : '#a3a3a3', fontWeight: '500', fontSize: '14px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '450px' }}>
                  {uploadedFile ? uploadedFile.name : "No file selected"}
                </span>
              </div>
            </div>

            <div style={{ fontSize: '20px', fontWeight: 'bold', color: 'white', textAlign: 'center', marginBottom: '10px', marginTop: '25px', textShadow: '0 1px 2px rgba(0,0,0,0.1)' }}>
              Select Target Job Role
            </div>

            <div style={{ borderRadius: '10px', backgroundColor: 'white', borderTop: 'rgb(239, 29, 76) solid 6px', boxShadow: '0px 4px 12px rgba(0,0,0,0.08)', overflow: 'hidden', marginBottom: '30px' }}>
              <select value={jobRole} onChange={(e) => setJobRole(e.target.value)} style={{ width: '100%', border: 'none', background: 'transparent', padding: '12px 14px', fontSize: '16px', outline: 'none', cursor: 'pointer', color: '#31333F', fontWeight: '500' }}>
                {rolesOptions.map((roleOpt, idx) => (
                  <option key={idx} value={roleOpt}>{roleOpt}</option>
                ))}
              </select>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr 1fr', gap: '10px' }}>
              <div />
              <div style={{ textAlign: 'center' }}>
                <button type="button" onClick={handleAnalyze} style={{ backgroundColor: '#5A189A', color: 'white', fontSize: '18px', fontWeight: 'bold', borderRadius: '12px', padding: '12px 10px', border: '2px solid #9D4EDD', width: '100%', cursor: 'pointer', boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)', textTransform: 'uppercase', letterSpacing: '1px', boxSizing: 'border-box' }}>
                  Analyze Resume
                </button>
              </div>
              <div />
            </div>

            {/* Clickable Audit Logs List */}
            {historyList.length > 0 && (
              <div style={{ marginTop: '40px', backgroundColor: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0px 4px 16px rgba(0,0,0,0.1)', borderTop: '6px solid #5A189A' }}>
                <h3 style={{ color: '#5A189A', margin: '0 0 15px 0', fontWeight: 'bold', fontSize: '18px' }}>🕒 Cloud Audit History Logs</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {historyList.map((hist, idx) => (
                    <div 
                      key={idx} 
                      onClick={() => handleSelectHistoryItem(hist)}
                      style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', borderBottom: '1px solid #eee', fontSize: '14px', alignItems: 'center', cursor: 'pointer', backgroundColor: '#fafafa', borderRadius: '6px', transition: 'all 0.2s ease' }}
                      onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#f3e5f5'; e.currentTarget.style.transform = 'translateX(4px)'; }}
                      onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#fafafa'; e.currentTarget.style.transform = 'none'; }}
                    >
                      <span>📄 <b>{hist.filename}</b> for role: <i>{hist.target_role}</i></span>
                      <span style={{ color: '#7B2CBF', fontWeight: 'bold', backgroundColor: '#e1bee7', padding: '4px 8px', borderRadius: '6px' }}>Score: {hist.match_score}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        </div>
      )}

      {/* ========================================== */}
      {/* PAGE 2: ANALYSIS DASHBOARD STAGE           */}
      {/* ========================================== */}
      {page === 'analysis' && (
        <div style={{ backgroundColor: 'white', paddingLeft: '2rem', paddingRight: '2rem', width: '95%', maxWidth: '95%', margin: '0 auto', boxSizing: 'border-box', paddingBottom: '4rem' }}>
          
          <div style={{ marginTop: '40px', display: 'grid', gridTemplateColumns: '1.2fr 6fr 1.2fr', alignItems: 'center', marginBottom: '40px' }}>
            <div style={{ paddingTop: '28px' }}>
              <button onClick={() => { setPage('home'); setProcessedResults([]); }} style={{ background: '#f0f2f6', border: '1px solid #d3d6df', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontWeight: '600', color: '#31333F', fontSize: '14px' }}>
                ⬅️ Back
              </button>
            </div>
            <div>
              <h1 style={{ textAlign: 'center', color: 'black', margin: 0, fontSize: '42px', fontFamily: 'Arial', fontWeight: 'bold' }}>
                Analysis for <span style={{ color: '#ff8c09' }}>{jobRole}</span>
              </h1>
            </div>
            <div />
          </div>

          {loading ? (
            <div style={{ textShadow: 'none', textAlign: 'center', padding: '60px 0' }}>
              <p style={{ fontSize: '16px', color: '#555', fontWeight: '500' }}>🔍 Accessing local database structures and parsing live scrapers... Please hold.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              
              <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#31333F' }}>Job Alignment Intelligence:</h3>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '25px', alignItems: 'center' }}>
                
                <div style={{ textAlign: 'center', padding: '15px', backgroundColor: '#f0f2f6', borderRadius: '10px', minWidth: '220px', boxSizing: 'border-box', border: '1px solid #e2e4e9' }}>
                  <h4 style={{ fontSize: '14px', color: '#555', margin: '0 0 4px 0', fontWeight: '600' }}>📊 Text Similarity</h4>
                  <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#31333F' }}>
                    {topMatch ? `${topMatch.similarity}%` : '0.0%'}
                  </div>
                  <div style={{ fontSize: '12px', color: 'gray', marginTop: '4px' }}>Contextual Vector Embedding</div>
                </div>

                <div style={{ textAlign: 'center', padding: '15px', backgroundColor: '#f0f2f6', borderRadius: '10px', minWidth: '220px', boxSizing: 'border-box', border: '1px solid #e2e4e9' }}>
                  <h4 style={{ fontSize: '14px', color: '#555', margin: '0 0 4px 0', fontWeight: '600' }}>🛠️ Skill Match Score</h4>
                  <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#31333F' }}>
                    {topMatch ? `${topMatch.skill_match}%` : '0.0%'}
                  </div>
                  <div style={{ fontSize: '12px', color: 'gray', marginTop: '4px' }}>Keyword Matrix Intersection</div>
                </div>

                <div style={{ textAlign: 'center' }}>
                  <button onClick={(e) => runAiAnalysis(e)} style={{ backgroundColor: '#5A189A', color: 'white', border: '2px solid #9D4EDD', padding: '10px 20px', borderRadius: '12px', fontWeight: 'bold', fontSize: '15px', cursor: 'pointer', boxShadow: '0px 4px 10px rgba(0,0,0,0.15)' }}>
                    ✨ Run AI Career Deep Dive
                  </button>
                </div>

                <div style={{ textAlign: 'right', minWidth: '220px' }}>
                  <h3 style={{ textAlign: 'right', margin: '0 0 8px 0', fontSize: '20px', fontWeight: 'bold', color: '#31333F' }}>⚠️ Match Fit Status</h3>
                  <p style={{ textAlign: 'right', color: (topMatch && topMatch.overall_fit >= 70) ? 'green' : '#d32f2f', margin: 0, fontWeight: 'bold', fontSize: '18px' }}>
                    {topMatch && topMatch.overall_fit >= 70 ? "🔥 Strong Fit Profile" : "⚡ Development Match"}
                  </p>
                </div>

              </div>

              <hr style={{ border: '0', borderTop: '1px solid #e6e9ef', margin: '15px 0' }} />

              {topMatch && (
                <div style={{ backgroundColor: '#fff3cd', padding: '25px', borderRadius: '12px', textAlign: 'center', border: '1px solid #ffeeba', marginBottom: '10px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
                  <h2 style={{ color: '#856404', margin: '0 0 10px 0', fontSize: '24px', fontWeight: 'bold' }}>
                    Overall Fit Score: {topMatch.overall_fit} / 100
                  </h2>
                  <p style={{ margin: 0, fontWeight: 'bold', color: '#31333F', fontSize: '15px' }}>
                    Evaluated metrics derived from job description mapping arrays (60/40 Split).
                  </p>
                </div>
              )}

              {topMatch && (
                <div style={{ backgroundColor: '#fdf2f2', border: '1px solid #fde8e8', padding: '20px', borderRadius: '12px', maxWidth: '1000px', margin: '10px auto', width: '100%', boxSizing: 'border-box' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                    <span style={{ fontSize: '20px' }}>⚠️</span>
                    <h4 style={{ margin: 0, fontSize: '16px', fontWeight: 'bold', color: '#9b1c1c' }}>Missing Core Focus Requirements</h4>
                  </div>
                  
                  {topMatch.missing_skills && topMatch.missing_skills.length > 0 ? (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                      {topMatch.missing_skills.map((skill, index) => (
                        <span key={index} style={{ backgroundColor: '#fde8e8', color: '#c81e1e', border: '1px solid #f8b4b4', padding: '4px 10px', borderRadius: '6px', fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p style={{ margin: 0, color: '#0f5132', fontSize: '14px', fontWeight: '600' }}>
                      Perfect Match! Your profile contains all tracked technical elements found in our dictionaries.
                    </p>
                  )}
                </div>
              )}

              <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', maxWidth: '1000px', margin: '15px auto 0 auto', width: '100%' }}>
                <h3 style={{ fontSize: '18px', fontWeight: 'bold', color: '#31333F', margin: '10px 0 5px 0' }}>
                  💼 Aggregated Opportunities Discovered:
                </h3>
                {processedResults.length === 0 ? (
                  <p style={{ textAlign: 'center', color: '#777' }}>No records located in data arrays matching this specific title query.</p>
                ) : (
                  processedResults.map((job, idx) => (
                    <div key={idx} style={{ backgroundColor: 'white', padding: '18px', borderRadius: '12px', boxShadow: '0px 4px 12px rgba(0,0,0,0.05)', borderLeft: '6px solid #6A0DAD', borderTop: '1px solid #f0f0f0', borderRight: '1px solid #f0f0f0', borderBottom: '1px solid #f0f0f0', textAlign: 'left' }}>
                      <h4 style={{ margin: '0 0 5px 0', fontSize: '18px', fontWeight: 'bold', color: '#31333F' }}>{job.title}</h4>
                      <p style={{ color: 'purple', fontWeight: 'bold', margin: '0 0 2px 0', fontSize: '15px' }}>{job.company}</p>
                      <p style={{ color: 'gray', fontSize: '12px', margin: '0 0 8px 0' }}>Platform Source: <b style={{ color: job.source?.includes('Dataset') ? '#0288d1' : '#e65100' }}>{job.source}</b></p>
                      
                      <p style={{ fontSize: '14px', margin: '0 0 12px 0', display: 'flex', gap: '10px' }}>
                        <span style={{ background: '#e1bee7', padding: '2px 8px', borderRadius: '4px', color: '#31333F' }}><b>Similarity:</b> {job.similarity}%</span>
                        <span style={{ background: '#f3e5f5', padding: '2px 8px', borderRadius: '4px', color: '#31333F' }}><b>Weighted Fit:</b> {job.overall_fit}%</span>
                      </p>
                      
                      <p style={{ fontSize: '13.5px', color: '#555', margin: '0 0 12px 0', lineHeight: '1.5', whiteSpace: 'pre-line' }}>
                        {job.description}
                      </p>

                      {job.url !== '#' && (
                        <a href={job.url} target="_blank" rel="noreferrer" style={{ textDecoration: 'none', color: '#6A0DAD', fontWeight: 'bold', fontSize: '15px', display: 'inline-flex', alignItems: 'center' }}>
                          🔗 View Posting Details
                        </a>
                      )}
                    </div>
                  ))
                )}
              </div>

            </div>
          )}
        </div>
      )}

      {/* ========================================== */}
      {/* PAGE 3: AI PERSISTENCE ANALYSIS STAGE      */}
      {/* ========================================== */}
      {page === 'ai_analysis' && (
        <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto', textAlign: 'left', paddingBottom: '5rem' }}>
          <button onClick={() => setPage('analysis')} style={{ background: '#f0f2f6', border: '1px solid #d3d6df', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontWeight: '600', marginBottom: '25px', fontSize: '14px', color: '#31333F' }}>
            ⬅️ Back
          </button>

          {aiLoading ? (
            <div style={{ textAlign: 'center', padding: '60px 0' }}>
              <p style={{ fontSize: '16px', color: '#555', fontWeight: '500' }}>Running contextual analysis algorithms... Please wait.</p>
            </div>
          ) : (
            <div style={{ backgroundColor: '#f0f8ff', padding: '20px', borderRadius: '10px', marginBottom: '15px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)', border: '1px solid #d0e8ff' }}>
              <h5 style={{ margin: 0, fontWeight: 'bold', fontSize: '18px', marginBottom: '10px', color: '#31333F' }}>AI Deep Dive Core Output</h5>
              <p style={{ margin: 0, fontSize: '14px', lineHeight: '1.6', color: '#31333F', whiteSpace: 'pre-wrap' }}>
                {aiResponse}
              </p>
            </div>
          )}
        </div>
      )}

    </div>
  );
}

export default App;