import streamlit as st
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set page config
st.set_page_config(
    page_title="Student AI Learning Plan - Dr. C",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
    }
    .required-note {
        color: #666;
        font-size: 0.9em;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# Email notification function
def send_email_notification(student_data):
    """Send email notification with student assessment data"""
    try:
        sender_email = st.secrets.get("email", {}).get("sender", "")
        sender_password = st.secrets.get("email", {}).get("password", "")
        receiver_email = st.secrets.get("email", {}).get("receiver", "drc@frank-coyle.ai")
        
        if not sender_email or not sender_password:
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"[STUDENT-AI-HELP] {student_data['name']} - {student_data['student_type']}"
        
        # Format email body
        body = f"""
NEW STUDENT AI LEARNING PLAN REQUEST
=====================================

CONTACT INFO:
Name: {student_data['name']}
Email: {student_data['email']}
Student Type: {student_data['student_type']}
Major/Field: {student_data['major']}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TECHNICAL BACKGROUND:
Programming Languages: {', '.join(student_data['prog_langs']) if student_data['prog_langs'] else 'None'}
Courses Completed: {', '.join(student_data['courses_completed']) if student_data['courses_completed'] else 'None'}
AI/ML Experience: {student_data['ai_experience']}

SHORT-TERM GOALS (3 months):
{student_data['short_term_goals']}

LONG-TERM GOALS:
{student_data['long_term_goals']}

CAREER OPTIONS EXPLORING:
{student_data['career_options']}

STRENGTHS:
{student_data['strengths']}

AREAS NEEDING WORK:
{student_data['needs_work']}

INTERESTS:
{student_data['interests']}

STARTUP INTEREST: {student_data['startup_interest']}
{f"Startup Ideas: {student_data['startup_ideas']}" if student_data.get('startup_ideas') else ''}

TOPICS TO LEARN:
{student_data['topics_to_learn']}

LEARNING PREFERENCES:
Formats: {', '.join(student_data['learning_formats']) if student_data['learning_formats'] else 'Not specified'}
Time Available: {student_data['time_available']}

COURSE INTEREST:
Py4AI Interest: {student_data['py4ai_interest']}
MAKE with AI Interest: {student_data['make_interest']}

OPTIONAL DEEP DIVE:
Background: {student_data.get('background', 'Not provided')}
Current Projects: {student_data.get('current_projects', 'Not provided')}
Challenges: {student_data.get('challenges', 'Not provided')}
Resources Used: {student_data.get('resources_used', 'Not provided')}
Additional Info: {student_data.get('additional_info', 'Not provided')}

=====================================
Reply to student at: {student_data['email']}
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        return False

# Header
st.title("🎓 AI Learning Plan for Students")
st.markdown("### Get Your Personalized 3-Month AI Roadmap from Dr. C")

st.markdown("""
Welcome! I'm Dr. C (Frank Coyle), and I've been teaching CS and AI for 32 years. I want to help you 
create a personalized learning plan that fits YOUR goals, background, and learning style.

**What you'll get (via email in 24-48 hours):**
- 📋 Personalized 3-month action plan
- 📚 Custom reading/video/podcast recommendations
- 💻 Specific coding exercises and projects
- 🎯 Career guidance based on your goals
- 🚀 Quick wins you can implement immediately

**The more detail you provide, the better your personalized plan will be!**

> *"Nothing is a mistake. There's no win and no fail. Only MAKE."* - John Cage
""")

st.markdown("---")
st.markdown('<p class="required-note">* Required fields | ⭐ Optional but recommended for better plan</p>', 
            unsafe_allow_html=True)

# Main form
with st.form("student_assessment"):
    
    # SECTION 1: BASIC INFO (Required)
    st.subheader("📝 Basic Information")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name*", placeholder="Your full name")
        email = st.text_input("Email*", placeholder="your.email@university.edu")
    
    with col2:
        student_type = st.selectbox(
            "Student Type*",
            ["", "Undergraduate", "Graduate (MS/PhD)", "Other (bootcamp, self-learner, etc.)"]
        )
        major = st.text_input("Major/Field of Study*", placeholder="e.g., Computer Science, Information Systems")
    
    # SECTION 2: TECHNICAL BACKGROUND (Required)
    st.markdown("---")
    st.subheader("💻 Technical Background")
    
    col1, col2 = st.columns(2)
    with col1:
        prog_langs = st.multiselect(
            "Programming Languages You Know*",
            ["None", "Python", "Java", "C/C++", "JavaScript", "SQL", "R", "MATLAB", "Go", "Rust", "Other"],
            help="Select all that apply"
        )
        
        courses_completed = st.multiselect(
            "CS Courses Completed*",
            ["None", "Data Structures", "Algorithms", "Machine Learning", "AI", "Databases", 
             "Web Development", "Software Engineering", "Systems Programming", "Other"]
        )
    
    with col2:
        ai_experience = st.selectbox(
            "AI/ML Experience Level*",
            ["", "None - Complete beginner", "Basic - Used ChatGPT/AI tools", 
             "Intermediate - Taken ML course", "Advanced - Built ML projects", 
             "Expert - Research/production ML"]
        )
        
        coding_comfort = st.select_slider(
            "Overall Coding Comfort Level*",
            options=["Beginner", "Learning", "Comfortable", "Proficient", "Expert"],
            value="Comfortable"
        )
    
    # SECTION 3: GOALS (Required)
    st.markdown("---")
    st.subheader("🎯 Your Goals")
    
    short_term_goals = st.text_area(
        "Short-Term Goals (Next 3 Months)*",
        placeholder="What do you want to accomplish in the next 3 months? Be specific!\nExamples:\n- Learn Python for AI/ML\n- Build a portfolio project\n- Land an internship\n- Understand transformers and LLMs",
        height=120
    )
    
    long_term_goals = st.text_area(
        "Long-Term Goals (1-3 Years)*",
        placeholder="Where do you want to be in 1-3 years?\nExamples:\n- Data scientist at tech company\n- AI researcher\n- Start my own AI company\n- Product manager for AI products",
        height=120
    )
    
    career_options = st.text_area(
        "Career Options You're Exploring*",
        placeholder="What career paths interest you? (open-ended)\nExamples:\n- Software engineering at startups\n- ML engineering\n- AI product management\n- Entrepreneurship\n- Academic research",
        height=100
    )
    
    # SECTION 4: SELF-ASSESSMENT (Required)
    st.markdown("---")
    st.subheader("💪 Self-Assessment")
    
    col1, col2 = st.columns(2)
    with col1:
        strengths = st.text_area(
            "Your Strengths*",
            placeholder="What are you good at?\nExamples:\n- Quick learner\n- Strong math background\n- Good at explaining concepts\n- Creative problem solver",
            height=120
        )
    
    with col2:
        needs_work = st.text_area(
            "Areas Needing Work*",
            placeholder="What do you want to improve?\nExamples:\n- Coding speed\n- Understanding ML theory\n- Building complete projects\n- Time management",
            height=120
        )
    
    # SECTION 5: INTERESTS & ASPIRATIONS (Required)
    st.markdown("---")
    st.subheader("🌟 Interests & Aspirations")
    
    interests = st.text_area(
        "Topics/Areas That Interest You*",
        placeholder="What excites you in tech/AI?\nExamples:\n- Natural language processing\n- Computer vision\n- Robotics\n- AI ethics\n- Game development with AI",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        startup_interest = st.selectbox(
            "Interest in Creating a Startup?*",
            ["", "No interest", "Curious", "Seriously considering", "Already working on one"]
        )
    
    with col2:
        if startup_interest in ["Curious", "Seriously considering", "Already working on one"]:
            startup_ideas = st.text_input(
                "Startup Ideas (if any)",
                placeholder="Brief description of your startup idea..."
            )
        else:
            startup_ideas = ""
    
    topics_to_learn = st.text_area(
        "Specific Topics You Want to Learn*",
        placeholder="What specific things do you want to learn about?\nExamples:\n- How transformers work\n- Building RAG systems\n- Prompt engineering\n- Fine-tuning models\n- Deploying ML models",
        height=120
    )
    
    # SECTION 6: LEARNING PREFERENCES (Required)
    st.markdown("---")
    st.subheader("📚 Learning Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        learning_formats = st.multiselect(
            "Preferred Learning Formats* (select all that apply)",
            ["Video tutorials", "Written articles/books", "Audio (podcasts)", 
             "Hands-on coding", "Interactive courses", "Live workshops"]
        )
    
    with col2:
        time_available = st.selectbox(
            "Time Available Per Week for Learning*",
            ["", "<5 hours", "5-10 hours", "10-20 hours", "20+ hours (full-time)"]
        )
    
    # SECTION 7: COURSE INTEREST (Required)
    st.markdown("---")
    st.subheader("🎓 Course Interest")
    
    st.markdown("""
    **Dr. C is developing specialized courses:**
    
    **1. Py4AI** - "Just enough Python to be dangerous" - Focus on practical AI applications, not CS theory
    
    **2. MAKE with AI** - Short video lessons + hands-on assignments covering:
    - Building AI Tools
    - Creating AI Agents  
    - Designing AI Workflows
    
    *Based on John Cage's philosophy: "Nothing is a mistake. There's no win and no fail. Only MAKE."*
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        py4ai_interest = st.selectbox(
            "Interest in Py4AI Course?*",
            ["", "Not interested", "Somewhat interested", "Very interested", "Definitely want to sign up"]
        )
    
    with col2:
        make_interest = st.selectbox(
            "Interest in MAKE with AI Course?*",
            ["", "Not interested", "Somewhat interested", "Very interested", "Definitely want to sign up"]
        )
    
    # SECTION 8: OPTIONAL DEEP DIVE
    st.markdown("---")
    st.subheader("⭐ Optional Deep Dive (Recommended for Better Plan)")
    
    with st.expander("📖 Click to expand - Provide more context for a highly personalized plan"):
        background = st.text_area(
            "Your Background Story",
            placeholder="Tell me about your journey... How did you get interested in CS/AI? What's your story?\n\nThe more context, the better I can tailor recommendations!",
            height=150
        )
        
        current_projects = st.text_area(
            "Current Projects or Work",
            placeholder="What are you working on now? School projects? Personal projects? Internships?\n\nExamples:\n- Building a chatbot for...\n- Working on data analysis project for...\n- Intern at XYZ doing...",
            height=120
        )
        
        challenges = st.text_area(
            "Biggest Challenges You're Facing",
            placeholder="What's holding you back or frustrating you?\n\nExamples:\n- Can't finish projects I start\n- Don't know where to start with AI\n- Struggle with math in ML courses\n- Time management with coursework",
            height=120
        )
        
        resources_used = st.text_area(
            "Resources You Currently Use or Follow",
            placeholder="What do you already read/watch/listen to?\n\nExamples:\n- YouTube channels (3Blue1Brown, Sentdex...)\n- Podcasts (Lex Fridman...)\n- Blogs/newsletters\n- Online courses you've taken",
            height=120
        )
        
        additional_info = st.text_area(
            "Anything Else I Should Know?",
            placeholder="Any other context that would help me create the perfect plan for you?\n\nExamples:\n- Financial constraints\n- Geographic location\n- Health considerations\n- Family commitments\n- Unique circumstances",
            height=120
        )
    
    # Submit button
    st.markdown("")
    submitted = st.form_submit_button("🚀 Get My Personalized Learning Plan", type="primary")

# Handle form submission
if submitted:
    # Validation
    required_fields = [
        name, email, student_type, major, ai_experience, coding_comfort,
        short_term_goals, long_term_goals, career_options, strengths,
        needs_work, interests, topics_to_learn, time_available,
        py4ai_interest, make_interest, startup_interest
    ]
    
    if not all(required_fields) or not prog_langs or not courses_completed or not learning_formats:
        st.error("❌ Please fill in all required fields (marked with *).")
    elif "@" not in email:
        st.error("❌ Please enter a valid email address.")
    else:
        # Create student data object
        student_data = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "email": email,
            "student_type": student_type,
            "major": major,
            "prog_langs": prog_langs,
            "courses_completed": courses_completed,
            "ai_experience": ai_experience,
            "coding_comfort": coding_comfort,
            "short_term_goals": short_term_goals,
            "long_term_goals": long_term_goals,
            "career_options": career_options,
            "strengths": strengths,
            "needs_work": needs_work,
            "interests": interests,
            "startup_interest": startup_interest,
            "startup_ideas": startup_ideas,
            "topics_to_learn": topics_to_learn,
            "learning_formats": learning_formats,
            "time_available": time_available,
            "py4ai_interest": py4ai_interest,
            "make_interest": make_interest,
            "background": background if 'background' in locals() else "",
            "current_projects": current_projects if 'current_projects' in locals() else "",
            "challenges": challenges if 'challenges' in locals() else "",
            "resources_used": resources_used if 'resources_used' in locals() else "",
            "additional_info": additional_info if 'additional_info' in locals() else ""
        }
        
        # Save to JSON
        json_file = "student_assessments.json"
        try:
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
            else:
                data = []
            
            data.append(student_data)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            pass
        
        # Send email notification
        email_sent = send_email_notification(student_data)
        
        # Success message
        st.success(f"✅ Thanks {name}! Your personalized learning plan is being created.")
        st.balloons()
        
        st.markdown("---")
        st.subheader("🎯 What Happens Next?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **📧 Check Your Email**
            
            Within 24-48 hours, you'll receive at:
            **{email}**
            
            Your personalized plan will include:
            - 3-month action roadmap
            - Custom resource recommendations
            - Specific projects to build
            - Learning path tailored to your goals
            """)
        
        with col2:
            st.success("""
            **🤖 How Your Plan is Created**
            
            1. AI analyzes your responses
            2. Dr. C reviews and personalizes
            3. Custom resources matched to YOUR:
               - Learning style
               - Goals
               - Current level
               - Time available
            
            **You'll get the BEST of both!**
            """)
        
        # Course interest follow-up
        if py4ai_interest in ["Very interested", "Definitely want to sign up"] or \
           make_interest in ["Very interested", "Definitely want to sign up"]:
            st.markdown("---")
            st.warning("""
            **🎓 Course Interest Noted!**
            
            Based on your interest in:
            """ + 
            (f"- **Py4AI** (Practical Python for AI)\n" if py4ai_interest in ["Very interested", "Definitely want to sign up"] else "") +
            (f"- **MAKE with AI** (Tools, Agents, Workflows)\n" if make_interest in ["Very interested", "Definitely want to sign up"] else "") +
            """
            I'll include early access information and special student pricing in your personalized plan!
            """)
        
        # Immediate suggestions based on level
        st.markdown("---")
        st.subheader("⚡ Quick Wins While You Wait")
        
        if ai_experience in ["None - Complete beginner", "Basic - Used ChatGPT/AI tools"]:
            st.write("""
            **Start Here (Beginner-Friendly):**
            - 🎬 Watch: Andrew Ng's "AI for Everyone" (Coursera - free to audit)
            - 🤖 Practice: Use ChatGPT daily for learning - ask it to explain concepts
            - 📚 Read: "The Coming Wave" by Mustafa Suleyman (big picture AI)
            - 💻 Code: Try Python basics on Codecademy or freeCodeCamp
            """)
        elif ai_experience == "Intermediate - Taken ML course":
            st.write("""
            **Level Up (Intermediate):**
            - 🎬 Watch: 3Blue1Brown's Neural Network series
            - 🤖 Build: Create a simple chatbot using OpenAI or Anthropic API
            - 📚 Read: "Hands-On Machine Learning" by Aurélien Géron
            - 💻 Code: Implement a small ML project from scratch
            """)
        else:
            st.write("""
            **Advanced Track:**
            - 🎬 Watch: Stanford CS224N (NLP) or CS231N (Computer Vision)
            - 🤖 Build: Contribute to open-source AI projects
            - 📚 Read: Latest papers on arXiv in your interest area
            - 💻 Code: Build a production-ready AI application
            """)

# Sidebar
with st.sidebar:
    st.markdown("### 🎓 About Dr. C")
    st.write("""
    **Frank Coyle, PhD**
    
    • 32 years teaching CS & AI
    • UC Berkeley Lecturer
    • Former SMU Professor
    • Creator: AI Career Accelerator
    • Creator: Py4AI
    • Developer: MAKE with AI course
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Student Stats")
    
    json_file = "student_assessments.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    st.write(f"**Plans created:** {len(data)}")
                    
                    # Show student types
                    types = [s.get('student_type', 'Unknown') for s in data]
                    type_counts = {}
                    for t in types:
                        if t != 'Unknown' and t:
                            type_counts[t] = type_counts.get(t, 0) + 1
                    
                    if type_counts:
                        st.write("**By type:**")
                        for t, count in type_counts.items():
                            st.write(f"• {t}: {count}")
        except:
            pass
    
    st.markdown("---")
    st.markdown("### 💡 Philosophy")
    st.info("""
    *"Nothing is a mistake. There's no win and no fail. Only MAKE."*
    
    — John Cage
    """)
    
    st.markdown("---")
    st.write("📧 drc@frank-coyle.ai")
    st.write("🔗 [LinkedIn](https://linkedin.com/in/frank-coyle)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem 0;'>
    <p><strong>Dr. C's AI Education</strong></p>
    <p style='font-size: 0.9em;'>Personalized learning paths powered by 32 years of teaching experience + AI</p>
</div>
""", unsafe_allow_html=True)
