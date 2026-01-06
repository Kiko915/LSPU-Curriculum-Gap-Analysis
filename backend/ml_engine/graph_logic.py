# backend/ml_engine/graph_logic.py

import re

class KnowledgeEngine:
    def __init__(self):
        # 📚 The "Standard of Care" Dictionary (Role Requirements)
        # This defines what skills are REQUIRED for each role.
        self.role_requirements = {
            "AI Engineer": {"python", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "sql", "scikit-learn", "computer vision"},
            "Web Developer": {"html", "css", "javascript", "react", "node.js", "git", "api", "json", "restful apis"},
            "Software Engineer": {"java", "python", "c++", "git", "sql", "algorithms", "data structures", "oop", "problem solving"},
            "Data Analyst": {"excel", "sql", "python", "tableau", "power bi", "statistics", "data analysis", "r"},
            "Data Engineer": {"sql", "python", "spark", "hadoop", "aws", "etl", "database management", "data warehousing"},
            "Cybersecurity Engineer": {"linux", "networking", "firewall", "python", "security", "penetration testing", "incident response", "encryption"},
            "Network Engineer": {"cisco", "networking", "tcp/ip", "switching", "routing", "troubleshooting", "eigrp", "ospf", "dns", "dhcp"},
            "Cloud Architect": {"aws", "azure", "docker", "kubernetes", "terraform", "cloud security", "linux"},
            "DevOps Engineer": {"docker", "kubernetes", "jenkins", "aws", "linux", "ci/cd", "bash", "automation"},
            "Mobile App Developer": {"android", "ios", "react native", "flutter", "dart", "swift", "firebase"},
            "Game Developer": {"unity", "c#", "unreal engine", "c++", "3d modeling", "mathematics", "animation", "physics"},
            "UI/UX Designer": {"figma", "adobe xd", "wireframing", "prototyping", "user research", "color theory", "typography", "design thinking"},
            "Project Manager": {"agile", "scrum", "jira", "communication", "planning", "risk management", "leadership", "project management"},
            "QA Engineer": {"selenium", "testing", "automation", "python", "java", "bug tracking", "unit testing"},
            "Robotics Engineer": {"c++", "python", "ros", "arduino", "electronics", "embedded systems", "sensors", "bluetooth"},
            "Sales Executive": {"communication", "crm", "negotiation", "marketing", "salesforce", "leadership"},
            "Digital Marketer": {"seo", "social media", "google analytics", "content marketing", "copywriting"},
            "Content Specialist": {"writing", "editing", "seo", "blogging", "wordpress", "content creation"},
            "Business Analyst": {"requirements gathering", "sql", "excel", "communication", "modeling", "data analysis"}
        }

        # 🎓 1. Define the Curriculum Map (Code -> Skills)
        # Mapped from your extracted PDF data
        self.course_map = {
            # --- BSCS MAJOR SUBJECTS ---
            "CMSC 101": ["algorithms", "data structures", "functions", "java", "r", "research", "security", "communication", "documentation", "innovation"],
            "CMSC 202": ["algorithms", "data structures", "functions", "problem solving", "r", "research", "security", "statistics", "documentation", "innovation"],
            "CMSC 203": ["algorithms", "data structures", "design patterns", "encapsulation", "inheritance", "java", "oop", "polymorphism", "python", "research", "security", "testing"],
            "CMSC 204": ["algorithms", "data structures", "problem solving", "r", "research", "security", "functions", "testing"],
            "CMSC 305": ["algorithms", "data structures", "r", "research", "security", "analytical skills", "documentation", "innovation"],
            "CMSC 306": ["bash", "classification", "communication", "data structures", "database management", "deep learning", "dynamics", "innovation", "linux", "matlab", "networking", "r", "research", "storage", "system architecture"],
            "CMSC 307": ["communication", "compliance", "data structures", "database management", "documentation", "encryption", "incident response", "mentoring", "monitoring", "research", "risk assessment", "risk management", "security", "testing", "cloud", "cryptography", "cybersecurity"],
            "CMSC 308": ["algorithms", "c++", "classification", "data structures", "encapsulation", "java", "javascript", "python", "r", "research", "security", "debugging", "version control"],
            "CMSC 309": ["accessibility", "agile", "communication", "concurrency", "data structures", "database management", "design patterns", "documentation", "functional testing", "html", "innovation", "java", "oop", "project management", "prototyping", "r", "research", "reverse engineering", "risk management", "security", "system design", "testing", "unit testing", "version control"],
            "CMSC 310": ["automation", "collaboration", "eigrp", "networking", "ospf", "r", "research", "security", "tcp/ip", "cloud", "network security", "switching"],
            "CMSC 311": ["communication", "concurrency", "data structures", "documentation", "monitoring", "project execution", "project management", "r", "requirement elicitation", "research", "risk management", "scheduling", "security", "testing", "unit testing"],
            "CMSC 501": ["algorithms", "data collection", "data structures", "deep learning", "machine learning", "project management", "prototyping", "r", "research", "security", "testing", "report writing"],
            "CMSC 502": ["algorithms", "data structures", "excel", "project management", "r", "research", "security", "statistics", "testing", "compliance", "data collection"],
            "CMSC 503": ["database management", "networking", "r", "research", "documentation", "innovation"],
            "CSEL 301": ["animation", "algorithms", "data structures", "r", "research", "security", "color theory", "problem-solving"],
            "CSST 101": ["communication", "data structures", "database management", "deep learning", "documentation", "github", "jupyter", "machine learning", "python", "r", "research", "scheduling", "scikit-learn", "system design"],
            "CSST 102": ["classification", "communication", "data structures", "database management", "deep learning", "github", "jupyter", "keras", "machine learning", "neural networks", "python", "regression", "research", "scikit-learn", "tensorflow", "algorithms", "cloud", "data preprocessing"],
            "CSST 105": ["algorithms", "bluetooth", "communication", "data structures", "dynamics", "embedded systems", "r", "research", "security", "monitoring"],
            "CSST 106": ["classification", "communication", "computer vision", "data structures", "database management", "deep learning", "documentation", "dynamics", "keras", "machine learning", "neural networks", "opencv", "pytorch", "python", "r", "research", "tensorflow", "algorithms"],
            
            # --- ITEC / CSST / IT SUBJECTS ---
            "ITEC 101": ["agile", "css", "communication", "cybersecurity", "dns", "data analysis", "data structures", "database management", "html", "r", "research", "security", "tcp/ip", "analytics", "networking", "social media platforms"],
            "ITEC 102": ["algorithms", "c#", "css", "classification", "code review", "communication", "data structures", "data types", "database management", "encapsulation", "problem solving", "r", "visual studio", "debugging", "testing"],
            "ITEC 104": ["algorithms", "code review", "data structures", "innovation", "networking", "problem solving", "python", "research", "security", "testing", "wireframes"],
            "ITEC 105": ["advanced sql", "algorithms", "communication", "data modeling", "data analysis", "data structures", "data warehousing", "hadoop", "innovation", "mysql", "r", "research", "sql", "security"],
            "ITEC 106": ["apis", "accessibility", "database management", "debugging", "documentation", "firebase", "functions", "json", "networking", "restful apis", "research", "testing", "vs code", "visual studio"],
            "ITEP 413": ["classification", "cloud", "cloud security", "compliance", "database management", "encryption", "incident response", "leadership", "monitoring", "networking", "r", "reporting", "research", "risk assessment", "risk management", "security", "network security"],
            "ITEP 414": ["aws", "antivirus", "azure", "cloud", "content creation", "dhcp", "dns", "firewall configuration", "linux", "monitoring", "monitoring tools", "networking", "performance tuning", "research", "security", "vmware", "virtualbox", "excel", "network troubleshooting", "subnetting"],
            "ITEP 415": ["basic statistics", "database management", "mentorship", "networking", "qualitative research", "r", "research", "statistics", "project management", "risk management", "testing"],
            "ITST 306": ["accessibility", "adobe xd", "agile", "agile ux", "bootstrap", "css", "color theory", "cross-platform development", "design patterns", "design systems", "design thinking", "documentation", "figma", "html5", "mvp", "material design", "networking", "performance optimization", "prototyping", "r", "react", "research", "responsive design", "security", "sketch", "testing", "typography", "ui/ux design", "wcag", "wireframes"],
            
            # --- MATH & GENERAL ED ---
            "MATH24": ["algorithms", "data structures", "dynamics", "functions", "r", "research", "security", "problem-solving"],
            "GEC 102": ["r", "reporting", "research", "analytical skills", "communication", "problem solving"],
            "GEC 103": ["classification", "communication", "dynamics", "go", "r", "research", "security", "problem solving", "teamwork"],
            "GEC 104": ["classification", "go", "problem solving", "r", "research", "statistics", "documentation"],
            "GEC 105": ["communication", "critical thinking", "functions", "r", "research", "creativity"],
            "GEC 106": ["animation", "dynamics", "unity", "classification", "communication", "problem solving"],
            "GEC 107": ["collaboration", "communication", "creativity", "monitoring", "physics", "r", "research", "teamwork", "critical thinking"],
            "GEC 108": ["r", "research", "active listening", "communication", "critical thinking", "reporting"],
            "KOMFIL": ["collaboration", "innovation", "leadership", "research"],
            "PATHFIT": ["communication", "r", "research", "testing"],
            "PI 100": ["research", "communication", "documentation", "principle", "problem solving"],
            "SOSLIT": ["communication", "r", "research", "critical thinking"]
        }

        # 🎓 2. Define the Departments (Which codes do they take?)
        # Based on your curriculum list
        self.academic_baselines = {
            "BSCS": [
                "CMSC 502", "CMSC 306", "CMSC 307", "CMSC 309", "CMSC 310", 
                "CSST 101", "CSST 102", "CSST 106", "ITEC 105", "CMSC 101", 
                "CMSC 202", "CMSC 203", "CMSC 204", "CMSC 305", "CMSC 308", 
                "CMSC 311", "CMSC 501", "CMSC 503", "CSEL 301", "CSST 105", 
                "ITEC 101", "ITEC 102", "ITEC 104", "MATH24",
                # Include Minors for completeness
                "PATHFIT", "FILDIS", "GEC 102", "GEC 103", "GEC 104", 
                "GEC 105", "GEC 106", "GEC 107", "GEC 108", "KOMFIL", "PI 100", "SOSLIT"
            ],
            "BSIT": [
                "ITEP 413", "ITEP 414", "ITEC 106", "ITEP 415", "ITST 306",
                "ITEC 101", "ITEC 102", "ITEC 104", "MATH24", # Assuming common subjects
                # Include Minors
                "PATHFIT", "FILDIS", "GEC 102", "GEC 103", "GEC 104", 
                "GEC 105", "GEC 106", "GEC 107", "GEC 108", "KOMFIL", "PI 100", "SOSLIT"
            ],
            "MINOR": [
                "PATHFIT", "FILDIS", "GEC 102", "GEC 103", "GEC 104", 
                "GEC 105", "GEC 106", "GEC 107", "GEC 108", "KOMFIL", "PI 100", "SOSLIT"
            ]
        }
        
        # Alias for backward compatibility with main.py
        self.curriculum_map = self.academic_baselines

        # 🛣️ 3. Define Standard Roadmaps
        self.role_roadmaps = {
            "AI Engineer": [
                {"title": "Phase 1: Foundations", "description": "Master Python and Mathematics.", "duration": "4 Weeks", "resources": ["CS50 AI", "Kaggle Python"], "skills": ["python", "statistics", "calculus"]},
                {"title": "Phase 2: Machine Learning", "description": "Learn Scikit-Learn and core ML algorithms.", "duration": "6 Weeks", "resources": ["Andrew Ng ML Course"], "skills": ["machine learning", "scikit-learn", "pandas"]},
                {"title": "Phase 3: Deep Learning", "description": "Build neural networks with TensorFlow/PyTorch.", "duration": "8 Weeks", "resources": ["Fast.ai", "DeepLearning.aio"], "skills": ["deep learning", "tensorflow", "pytorch"]}
            ],
            "Web Developer": [
                {"title": "Phase 1: Frontend Basics", "description": "HTML, CSS, and JavaScript.", "duration": "4 Weeks", "resources": ["FreeCodeCamp", "MDN Docs"], "skills": ["html", "css", "javascript"]},
                {"title": "Phase 2: Modern Frameworks", "description": "React.js or Vue.js.", "duration": "6 Weeks", "resources": ["React Docs", "FullStackOpen"], "skills": ["react", "vue"]},
                {"title": "Phase 3: Backend & APIs", "description": "Node.js, Databases, and REST APIs.", "duration": "6 Weeks", "resources": ["The Odin Project"], "skills": ["node.js", "sql", "api"]}
            ],
            "Data Scientist": [
                {"title": "Phase 1: Python & Data Viz", "description": "Pandas, Matplotlib, Seaborn.", "duration": "4 Weeks", "resources": ["DataCamp", "Kaggle"], "skills": ["python", "pandas", "visualization"]},
                {"title": "Phase 2: Statistics & SQL", "description": "Probability, Hypothesis Testing, SQL.", "duration": "5 Weeks", "resources": ["Khan Academy"], "skills": ["statistics", "sql"]},
                {"title": "Phase 3: Advanced ML", "description": "Feature Engineering, Model Tuning.", "duration": "6 Weeks", "resources": ["Hands-on ML Book"], "skills": ["machine learning", "feature engineering"]}
            ],
            "Cybersecurity Engineer": [
                {"title": "Phase 1: Networking Basics", "description": "OSI Model, TCP/IP, Linux.", "duration": "4 Weeks", "resources": ["Network+"], "skills": ["networking", "linux"]},
                {"title": "Phase 2: Security Fundamentals", "description": "Encryption, Firewalls, Threat Vectors.", "duration": "5 Weeks", "resources": ["Security+"], "skills": ["security", "encryption"]},
                {"title": "Phase 3: Penetration Testing", "description": "Ethical Hacking tools and methodologies.", "duration": "8 Weeks", "resources": ["TryHackMe", "HackTheBox"], "skills": ["penetration testing", "ethical hacking"]}
            ],
            "Game Developer": [
                {"title": "Phase 1: Game Dev Foundation", "description": "C# and Unity Basics.", "duration": "4 Weeks", "resources": ["Unity Learn", "C# Docs"], "skills": ["c#", "unity", "mathematics"]},
                {"title": "Phase 2: Game Physics & Graphics", "description": "3D Math, Physics Engines.", "duration": "6 Weeks", "resources": ["GDC Talks"], "skills": ["physics", "3d modeling", "animation"]},
                {"title": "Phase 3: Advanced Optimizations", "description": "Shaders, Multiplayer Netcode.", "duration": "8 Weeks", "resources": ["GPU Gems"], "skills": ["c++", "unreal engine"]}
            ],
            "Software Engineer": [
                {"title": "Phase 1: CS Fundamentals", "description": "Algorithms and Data Structures.", "duration": "4 Weeks", "resources": ["LeetCode", "Cracking the Coding Interview"], "skills": ["algorithms", "data structures", "java", "c++"]},
                {"title": "Phase 2: System Design", "description": "Scalable Systems and Databases.", "duration": "5 Weeks", "resources": ["System Design Primer"], "skills": ["sql", "oop", "problem solving"]},
                {"title": "Phase 3: Large Scale Development", "description": "CI/CD, Testing, Maintainability.", "duration": "6 Weeks", "resources": ["Clean Code"], "skills": ["git", "testing"]}
            ],
            "Network Engineer": [
                {"title": "Phase 1: Networking Core", "description": "CCNA concepts, OSI Model.", "duration": "4 Weeks", "resources": ["Cisco NetAcad"], "skills": ["networking", "tcp/ip", "switching", "routing"]},
                {"title": "Phase 2: Advanced Routing", "description": "OSPF, EIGRP, BGP.", "duration": "5 Weeks", "resources": ["CCNP Route"], "skills": ["eigrp", "ospf", "troubleshooting"]},
                {"title": "Phase 3: Network Security", "description": "Firewalls, VPNs.", "duration": "4 Weeks", "resources": ["Palo Alto Certs"], "skills": ["firewall", "dns", "dhcp"]}
            ],
            "Data Engineer": [
                {"title": "Phase 1: SQL & Scripting", "description": "Advanced SQL and Python.", "duration": "4 Weeks", "resources": ["DataCamp"], "skills": ["sql", "python", "etl"]},
                {"title": "Phase 2: Big Data Frameworks", "description": "Hadoop, Spark.", "duration": "6 Weeks", "resources": ["Apache Spark Docs"], "skills": ["spark", "hadoop"]},
                {"title": "Phase 3: Cloud Data Platforms", "description": "AWS Glue, Redshift, Data Lakes.", "duration": "6 Weeks", "resources": ["AWS Data Engineer"], "skills": ["aws", "data warehousing", "database management"]}
            ],
            "Cloud Architect": [
                {"title": "Phase 1: Cloud Basics", "description": "AWS/Azure core services.", "duration": "4 Weeks", "resources": ["AWS CSA"], "skills": ["aws", "azure", "linux"]},
                {"title": "Phase 2: Infrastructure as Code", "description": "Terraform and CloudFormation.", "duration": "5 Weeks", "resources": ["HashiCorp Learn"], "skills": ["terraform", "docker"]},
                {"title": "Phase 3: Container Orchestration", "description": "Kubernetes at scale.", "duration": "6 Weeks", "resources": ["Kubernetes The Hard Way"], "skills": ["kubernetes", "cloud security"]}
            ],
            "DevOps Engineer": [
                {"title": "Phase 1: Linux & Scripting", "description": "Bash, Automation.", "duration": "3 Weeks", "resources": ["Linux Academy"], "skills": ["linux", "bash", "automation"]},
                {"title": "Phase 2: CI/CD & Containers", "description": "Jenkins, Docker.", "duration": "5 Weeks", "resources": ["Docker Docs"], "skills": ["docker", "jenkins", "ci/cd"]},
                {"title": "Phase 3: Orchestration & Cloud", "description": "Kubernetes and AWS.", "duration": "6 Weeks", "resources": ["EKS Docs"], "skills": ["kubernetes", "aws"]}
            ],
            "Mobile App Developer": [
                {"title": "Phase 1: Mobile Basics", "description": "Android/iOS native or generic.", "duration": "4 Weeks", "resources": ["Android Developers"], "skills": ["android", "ios", "react native", "flutter"]},
                {"title": "Phase 2: App Architecture", "description": "State management, navigation.", "duration": "4 Weeks", "resources": ["Flutter Docs"], "skills": ["dart", "swift"]},
                {"title": "Phase 3: Backend Integration", "description": "Firebase, REST APIs.", "duration": "4 Weeks", "resources": ["Firebase Docs"], "skills": ["firebase"]}
            ],
            "UI/UX Designer": [
                {"title": "Phase 1: Design Fundamentals", "description": "Color theory, typography.", "duration": "3 Weeks", "resources": ["Refactoring UI"], "skills": ["color theory", "typography", "design thinking"]},
                {"title": "Phase 2: Wireframing & Prototyping", "description": "Figma, Adobe XD.", "duration": "5 Weeks", "resources": ["Figma 101"], "skills": ["figma", "adobe xd", "wireframing", "prototyping"]},
                {"title": "Phase 3: User Research", "description": "Usability testing, personae.", "duration": "4 Weeks", "resources": ["NNGroup"], "skills": ["user research"]}
            ],
            "QA Engineer": [
                {"title": "Phase 1: Testing Basics", "description": "Types of testing, bug tracking.", "duration": "3 Weeks", "resources": ["ISTQB"], "skills": ["testing", "bug tracking"]},
                {"title": "Phase 2: Automation", "description": "Selenium to automate tests.", "duration": "5 Weeks", "resources": ["Selenium Docs"], "skills": ["selenium", "automation", "python", "java"]},
                {"title": "Phase 3: Performance Testing", "description": "Load testing, unit testing integration.", "duration": "4 Weeks", "resources": ["JMeter"], "skills": ["unit testing"]}
            ],
            "Robotics Engineer": [
                {"title": "Phase 1: Electronics & C++", "description": "Arduino, Circuits, C++.", "duration": "5 Weeks", "resources": ["Arduino Starter"], "skills": ["c++", "arduino", "electronics"]},
                {"title": "Phase 2: ROS & Sensors", "description": "Robot Operating System fundamentals.", "duration": "6 Weeks", "resources": ["ROS Wiki"], "skills": ["ros", "sensors", "python"]},
                {"title": "Phase 3: Embedded AI", "description": "Computer vision on edge devices.", "duration": "6 Weeks", "resources": ["OpenCV"], "skills": ["embedded systems", "bluetooth"]}
            ]
        }

    def get_baseline(self, dept: str):
        """
        1. Looks up the curriculum codes for the department.
        2. Translates codes into a unique list of industry skills.
        """
        dept_codes = self.academic_baselines.get(dept.upper(), [])
        if not dept_codes:
            raise KeyError(f"Department '{dept}' not found")
            
        skills_list = []
        
        for code in dept_codes:
            # Fetch skills for this code (default to empty if not found)
            # Use upper case to match keys
            subjects_skills = self.course_map.get(code.upper(), [])
            skills_list.extend(subjects_skills)
            
        # Return unique skills only, lowercased
        unique_skills = list(set([s.lower() for s in skills_list]))
        return unique_skills

    def analyze_gap(self, predicted_role, user_skills):
        """
        Compares User Skills vs. Required Skills for the predicted role.
        """
        required_skills = self.role_requirements.get(predicted_role, set())
        
        # 1. Pre-process User Skills (Split compound skills)
        normalized_user_skills = set()
        for skill in user_skills:
            # Split by comma or forward slash
            parts = re.split(r'[,\/]', str(skill))
            for part in parts:
                clean_part = part.strip().lower()
                if clean_part:
                    normalized_user_skills.add(clean_part)
        
        # 2. Smart Matching Loop
        present_skills = []
        missing_skills = []
        
        for req in required_skills:
            req_lower = req.lower()
            is_present = False
            
            # Check 1: Exact Match (Fast)
            if req_lower in normalized_user_skills:
                is_present = True
            else:
                # Check 2: Substring/Token Match (Slower but smarter)
                # e.g. "api" matches "api testing", "sql" matches "advanced sql"
                # But "java" should NOT match "javascript" -> Use word boundaries
                pattern = r'\b' + re.escape(req_lower) + r'\b'
                
                for user_skill in normalized_user_skills:
                    if re.search(pattern, user_skill):
                        is_present = True
                        break
            
            if is_present:
                present_skills.append(req)
            else:
                missing_skills.append(req)
        
        # Calculate Match Score
        total_required = len(required_skills)
        if total_required == 0:
            match_score = 0
        else:
            match_score = (len(present_skills) / total_required) * 100
            
        # Generate Advice
        advice = ""
        if match_score > 80:
            advice = f"You are highly qualified for {predicted_role}! Focus on advanced projects."
        elif match_score > 50:
            advice = f"Good progress. Focus on learning: {', '.join(missing_skills[:3])}."
        else:
            advice = f"To become a {predicted_role}, you need to build a strong foundation in: {', '.join(missing_skills[:3])}."

        return {
            "target_role": predicted_role,
            "match_score": round(match_score, 1),
            "total_required": total_required,
            "present_skills": present_skills,
            "missing_skills": missing_skills,
            "advice": advice
        }

    def generate_roadmap(self, role, user_skills):
        """
        Generates a personalized roadmap.
        Marks steps as 'completed' if user has the skills.
        """
        # Get standard roadmap or default to Web Developer if not found
        roadmap_template = self.role_roadmaps.get(role, self.role_roadmaps["Web Developer"])
        
        # Normalize user skills
        user_skills_normalized = set()
        for s in user_skills:
            parts = re.split(r'[,\/]', str(s))
            for p in parts:
                if p.strip():
                    user_skills_normalized.add(p.strip().lower())
                    
        personalized_steps = []
        for step in roadmap_template:
            # Check if user has skills for this step
            step_skills = step.get("skills", [])
            skills_found = 0
            
            for skill in step_skills:
                # Use smart matching logic here too
                skill_lower = skill.lower()
                if skill_lower in user_skills_normalized:
                    skills_found += 1
                else:
                    pattern = r'\b' + re.escape(skill_lower) + r'\b'
                    for us in user_skills_normalized:
                        if re.search(pattern, us):
                            skills_found += 1
                            break
            
            # Determine status
            total_step_skills = len(step_skills)
            if total_step_skills == 0:
                status = "pending"
            elif skills_found == total_step_skills:
                status = "completed"
            elif skills_found > 0:
                status = "in-progress"
            else:
                status = "pending"
                
            personalized_steps.append({
                "title": step["title"],
                "description": step["description"],
                "duration": step["duration"],
                "resources": step["resources"],
                "status": status
            })
            
        return personalized_steps
