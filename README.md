<div align="center">

<h1>🚀 ResuMate</h1>

<p><strong>AI-Powered Resume Generation & Job Application Management Platform</strong></p>

[![Live API](https://img.shields.io/badge/Live%20API-arafat2.me-2196f3?style=for-the-badge&logo=link)](https://arafat2.me/api)
[![Documentation](https://img.shields.io/badge/Documentation-View%20Docs-4caf50?style=for-the-badge&logo=gitbook)](https://arafat2.me)
[![GitHub](https://img.shields.io/badge/Source-GitHub-24292e?style=for-the-badge&logo=github)](https://github.com/Arafat6462/ResuMate)

</div>

---

## ✨ **Overview**

Production-ready Django REST API that leverages multiple AI models (Google Gemini, OpenRouter) to generate professional resumes and provides comprehensive job application tracking functionality. Built with enterprise-grade architecture and modern development practices.

**🔗 Two-Part System:**
- **[Main Application](https://arafat2.me/api/)** - Core Django REST API with AI integration
- **[Documentation Hub](https://arafat2.me)** - Interactive API docs with live demos

---

## 🎯 **Key Features**

| Feature | Description |
|---------|-------------|
| **🤖 AI Resume Generation** | Multi-model integration with Google Gemini & OpenRouter APIs |
| **💼 Job Application Tracking** | Complete lifecycle management (Applied → Interviewing → Offer/Rejected) |
| **🔐 JWT Authentication** | Secure user management with token-based authentication |
| **📊 Resume Management** | Full CRUD operations for resume documents |
| **🏗️ Production Ready** | Docker containerization, CI/CD pipeline, PostgreSQL database |
| **📖 Interactive Documentation** | MkDocs with live API testing capabilities |

---

## 🛠️ **Technology Stack**

| Category | Technologies |
|----------|-------------|
| **Backend** | Django 5.2, Django REST Framework, PostgreSQL |
| **AI Integration** | Google Gemini API, OpenRouter API, OpenAI |
| **DevOps** | Docker, GitHub Actions, DigitalOcean, Nginx |
| **Testing** | Pytest, Locust (Load Testing) |

---

## 🚀 **Quick Start**

### **📋 Prerequisites**
- **cURL** or **Postman** for API testing
- **Optional:** Docker for local development

### **🎯 Three-Step Demo**

#### **1️⃣ Test Instantly** *(No authentication required)*
```bash
# 🧠 Available AI Models
curl https://arafat2.me/api/ai/models/

# 👁️ Sample Applications  
curl https://arafat2.me/api/example-job-applications/
```

#### **2️⃣ Get Access** *(Create account & authenticate)*
```bash
# 📝 Register
curl -X POST https://arafat2.me/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_user","email":"demo@example.com","password":"SecurePass123!","password2":"SecurePass123!"}'

# 🔑 Login  
curl -X POST https://arafat2.me/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_user","password":"SecurePass123!"}'
```

#### **3️⃣ Generate Resume** *(Use AI to create professional resume)*
```bash
# 🤖 AI Resume Generation
curl -X POST https://arafat2.me/api/ai/generate/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "model": "Deepseek",
    "user_input": "Software engineer with 5 years Python experience",
    "title": "My AI Resume"
  }'
```

### **📖 Documentation & Resources**

| Resource | Description | Access |
|----------|-------------|--------|
| **📚 [Interactive Docs](https://arafat2.me)** | Complete API documentation with live testing | 🆓 Free |
| **🔌 [API Explorer](https://arafat2.me/api/)** | Browsable API interface | 🆓 Free |
| **🚀 [Live Demo](https://arafat2.me/live-demo/)** | Try endpoints immediately | 🆓 Free |

---

## 📚 **API Endpoints**

<details>
<summary><strong>🔗 Click to view all endpoints</strong></summary>

### **🔐 Authentication**
```bash
POST /api/auth/register/          # User registration
POST /api/auth/token/             # JWT token creation
POST /api/auth/token/refresh/     # Token refresh
```

### **🤖 AI & Resume Management**
```bash
GET  /api/ai/models/              # List available AI models
POST /api/ai/generate/            # Generate resume with AI
GET  /api/resumes/                # List user resumes
POST /api/resumes/                # Create new resume
GET  /api/resumes/{id}/           # Get specific resume
PUT  /api/resumes/{id}/           # Update resume
DELETE /api/resumes/{id}/         # Delete resume
```

### **💼 Job Application Tracking**
```bash
GET  /api/job-applications/       # List user applications
POST /api/job-applications/       # Create application
GET  /api/job-applications/{id}/  # Get specific application
PUT  /api/job-applications/{id}/  # Update application
DELETE /api/job-applications/{id}/ # Delete application
GET  /api/example-job-applications/ # Demo data (no auth)
```

</details>

---

## 👨‍💻 **Developer**

<div align="center">

**Arafat Hossain** - *Full-Stack Software Engineer*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077b5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/arafat6462)
[![GitHub](https://img.shields.io/badge/GitHub-24292e?style=for-the-badge&logo=github)](https://github.com/Arafat6462)
[![Email](https://img.shields.io/badge/Email-FFFFFF?style=for-the-badge&logo=gmail&logoColor=d44638)](mailto:arafat6462@gmail.com)

</div>
