import os
import uuid
from locust import HttpUser, task, between

# ======================================================================================
#  docker compose -f docker-compose.locust.yml up
#  BASELINE PERFORMANCE LOCUSTFILE (NO AI / RESUME GENERATION)
#
#  This file is specifically designed to test the core performance of the application,
#  EXCLUDING the slow AI and resume generation endpoints.
#
#  The 3 main test scenarios included are:
#  1. Anonymous users browsing public, fast endpoints.
#  2. The complete user registration and login flow.
#  3. An authenticated user managing their job applications (listing and creating).
#
# ======================================================================================


# --- Configuration & Test Data ---
TARGET_HOST = os.environ.get("TARGET_HOST", "https://arafat2.me")
TEST_USER_PASSWORD = "aVeryStrongPassword!123"


# ======================================================================================
#  TEST CASE 1 & 2: The Anonymous Visitor & Registration
# ======================================================================================

class AnonymousVisitor(HttpUser):
    """
    Represents a user who is NOT logged in.
    They browse public content and might decide to sign up.
    """
    host = TARGET_HOST
    wait_time = between(2, 5)

    @task(10)
    def view_public_endpoints(self):
        """
        Task: Browse the two main public, read-only endpoints.
        This simulates a visitor exploring the site's features.
        """
        self.client.get("/api/ai/models/", name="/api/ai/models/ (Public)")
        self.client.get("/api/example-job-applications/", name="/api/example-job-applications/")

    @task(1)
    def register_new_account(self):
        """
        Task: A visitor signs up for a new account.
        This tests the user creation endpoint.
        """
        username = f"visitor_user_{uuid.uuid4()}"
        self.client.post(
            "/api/auth/register/",
            json={"username": username, "email": f"{username}@example.com", "password": TEST_USER_PASSWORD, "password2": TEST_USER_PASSWORD},
            name="/api/auth/register/",
        )


# ======================================================================================
#  TEST CASE 3: The Authenticated Core User (Job Tracker)
# ======================================================================================

class AuthenticatedUser(HttpUser):
    """
    Represents a LOGGED-IN user managing their job applications.
    This simulates the core interactive loop for a registered user.
    """
    host = TARGET_HOST
    wait_time = between(2, 6)

    def on_start(self):
        """
        Handles the registration and login flow once per user.
        """
        self.username = f"core_user_{uuid.uuid4()}"
        self.client.post(
            "/api/auth/register/",
            json={"username": self.username, "email": f"{self.username}@example.com", "password": TEST_USER_PASSWORD, "password2": TEST_USER_PASSWORD},
        )
        res = self.client.post(
            "/api/auth/token/",
            json={"username": self.username, "password": TEST_USER_PASSWORD},
            name="/api/auth/token/",
        )
        if res.status_code == 200:
            self.access_token = res.json()["access"]
            self.client.headers["Authorization"] = f"Bearer {self.access_token}"

    @task(10)
    def view_own_job_applications(self):
        """
        Primary task: viewing the list of tracked job applications.
        """
        self.client.get("/api/job-applications/", name="/api/job-applications/ (List Own)")

    @task(3)
    def create_job_application(self):
        """
        Secondary task: creating a new job application entry.
        """
        self.client.post(
            "/api/job-applications/",
            json={
                "job_title": "Data Analyst",
                "company_name": f"Baseline Test Inc {uuid.uuid4()}",
                "status": "Interviewing"
            },
            name="/api/job-applications/ (Create)",
        )