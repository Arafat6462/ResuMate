import os
import uuid
import threading
from locust import HttpUser, task, between

# ======================================================================================
#  docker compose -f docker-compose.locust.yml up
#  PERFORMANCE LOCUSTFILE
#
#  This file contains 3 main test scenarios:
#  1. Anonymous users browsing public, fast endpoints.
#  2. An authenticated user managing their job applications (listing and creating).
#  3. An authenticated user generating a resume using the AI endpoint.
#
#  TO RUN ONLY A SPECIFIC TEST:
#  Use the class name when starting Locust, e.g.:
#  locust -f locustfile.py AuthenticatedUser
#  locust -f locustfile.py AIResumeUser
#
# ======================================================================================


# --- Configuration & Test Data ---
TARGET_HOST = os.environ.get("TARGET_HOST", "https://arafat2.me")
TEST_USER_PASSWORD = "aVeryStrongPassword!123"


# ======================================================================================
#  TEST CASE 1: The Anonymous Visitor
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
#  TEST CASE 2: The Authenticated Core User (Job Tracker)
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

# ======================================================================================
#  TEST CASE 3: The Authenticated AI User (Resume Generation)
# ======================================================================================

class AIResumeUser(HttpUser):
    """
    Represents a LOGGED-IN user generating a resume via the AI endpoint.
    This test is designed for the slow, resource-intensive AI task.

    NOTE: This test is hard-coded to stop after a total of 5 AI generation
    requests have been sent across all users.
    """
    host = TARGET_HOST
    # Wait time is set to be long to account for the slow AI response
    wait_time = between(30, 65)

    # --- Request Limiter ---
    # To strictly limit requests, we use a thread-safe counter.
    # This ensures that across all running users of this class, a maximum
    # of 5 requests will be sent to the AI generation endpoint.
    request_count = 0
    request_limit = 5
    lock = threading.Lock()
    # ---

    def on_start(self):
        """
        Handles the registration and login flow once per user.
        """
        self.username = f"ai_user_{uuid.uuid4()}"
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
        else:
            print("Failed to get token for user", self.username)


    @task
    def generate_resume(self):
        """
        Task: Call the AI to generate a new resume, but only up to a total of 5 times.
        """
        if not hasattr(self, 'access_token'):
            # Don't run task if login failed
            return

        with self.lock:
            if self.request_count >= self.request_limit:
                # Once the limit is reached, stop this user from running further tasks.
                self.stop()
                return
            # Increment the counter before making the request
            self.request_count += 1
            print(f"AI Resume Request Count: {self.request_count}/{self.request_limit}")

        # IMPORTANT: Replace "GPT-3.5 Turbo" with a real, active model `display_name` from your database.
        # You can see available models at the /api/ai/models/ endpoint.
        self.client.post(
            "/api/ai/generate/",
            json={
                "model": "Google_Gemma_3n",
                "user_input": "I am a senior software engineer with over 10 years of experience in Python, Django, and React. I have a proven track record of leading teams and delivering high-quality software. I am looking for a challenging role where I can continue to grow my skills."
            },
            name="/api/ai/generate/",
        )
