# ResuMate: In-Depth Guide to Redis Integration

This document provides a comprehensive, step-by-step explanation of how Redis was integrated into the ResuMate project. The primary goals were to improve application performance, reduce database load, and implement these changes in a production-safe manner.

## 1. Overall Goal: Caching Layer

The core objective was to introduce Redis as a **caching layer**. A cache stores the results of expensive operations (like database queries) in a faster, in-memory data store.

**The Problem:** Endpoints like `/api/ai/models/` and `/api/example-job-applications/` query the database every time they are requested. This data changes infrequently, making the repeated database queries inefficient.

**The Solution:** By caching the responses of these endpoints in Redis, we can serve subsequent requests directly from memory, which is orders of magnitude faster and reduces the load on our primary PostgreSQL database.

---

## 2. Step 1: Environment Setup (`docker-compose.yml`)

Before writing any Python code, we first needed to make a Redis server available to our application in the local development environment.

**File Changed:** `docker-compose.yml`

### The `redis` Service

We added a new service definition to the file:

```yaml
  redis:
    image: redis:alpine
    container_name: resumate_redis
    restart: always
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
```

*   **`image: redis:alpine`**: We use the `alpine` variant of the official Redis image. It's a lightweight version that is ideal for development and resource-constrained servers.
*   **`command: ...`**: This is a critical production-safety feature.
    *   `--maxmemory 256mb`: Sets a hard limit on Redis's RAM usage to 256MB, preventing it from consuming all server memory.
    *   `--maxmemory-policy allkeys-lru`: If the memory limit is reached, Redis will delete the "Least Recently Used" key to make space. This is the perfect eviction strategy for a cache.
*   **`ports: - "6379:6379"`**: This maps the container's port to the host machine, allowing for direct connections to Redis for debugging if needed.

### The `backend` Service Modifications

We updated the `backend` service to make it aware of the new `redis` service:

```yaml
    depends_on:
      redis:
        condition: service_started
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
```

*   **`depends_on`**: This ensures that the `backend` container won't start until the `redis` container is running, preventing connection errors on startup.
*   **`environment`**: We pass the Redis connection details to Django as environment variables. Inside Docker's network, the `redis` service is reachable at the hostname `redis`.

---

## 3. Step 2: Django Integration (`settings.py` & `requirements.txt`)

With a Redis server running, we configured Django to use it.

**File Changed:** `requirements.txt`
*   **Added:** `django-redis`
*   **Why:** This library is the "translator" that allows Django's caching framework to communicate with a Redis server.

**File Changed:** `ResuMate_backend/settings.py`
*   **Added:** The `CACHES` setting.

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

*   **`"default"`**: This configures Django's primary, project-wide cache.
*   **`"BACKEND"`**: Tells Django to use the `django-redis` library as the engine.
*   **`"LOCATION"`**: This is the connection string. It's built dynamically from the environment variables we defined in `docker-compose.yml`. The `/1` at the end selects Redis database #1, which is a good practice to isolate cache data.

---

## 4. Step 3: Caching Implementation (`ai/views.py`)

This is where we implemented the caching logic itself, using a pattern known as **"cache-aside"**.

**File Changed:** `ai/views.py` (specifically the `ListAIModelsView`)

```python
from django.core.cache import cache # Import Django's cache interface

class ListAIModelsView(APIView):
    CACHE_KEY = "ai_models_list"
    CACHE_TIMEOUT = 60 * 60  # 1 hour in seconds

    def get(self, request, *args, **kwargs):
        # 1. Attempt to get data from cache
        cached_data = cache.get(self.CACHE_KEY)
        if cached_data:
            return Response(cached_data) # Cache Hit: Return immediately

        # 2. If not found, perform the original operation
        # Cache Miss:
        active_models = AIModel.objects.filter(is_active=True)
        serializer = AIModelSerializer(active_models, many=True)
        
        # 3. Store the new data in the cache for next time
        cache.set(self.CACHE_KEY, serializer.data, self.CACHE_TIMEOUT)
        
        return Response(serializer.data)
```

*   **The Flow:**
    1.  **Check Cache (`cache.get`)**: First, ask Redis if it has the data. This is extremely fast.
    2.  **Cache Hit**: If data is found, return it instantly, skipping the database query entirely.
    3.  **Cache Miss**: If data is not found, run the original database query.
    4.  **Populate Cache (`cache.set`)**: Before returning the response, save the newly fetched data to Redis with a 1-hour timeout. The next request within the hour will result in a cache hit.

---

## 5. Step 4: Production & CI/CD Configuration

To make our changes deployable, we mirrored the environment setup in our production and CI/CD files.

**File Changed:** `docker-compose.prod.yml`
*   We added the same `redis` service definition here, ensuring the production environment would also have a Redis container with the same memory cap and a persistent volume (`redis_data_prod`) for stability.

**File Changed:** `.github/workflows/main.yml`
*   We updated the deployment script to add the `REDIS_HOST` and `REDIS_PORT` variables to the `.env` file it creates on the server. This ensures the production Django container knows how to connect to the production Redis container.

---

## 6. How to Monitor Redis on the Droplet

You can inspect the live Redis instance on your production server.

**1. SSH into the Droplet:**
```bash
ssh your_user@your_droplet_ip
```

**2. Access the Redis CLI:**
```bash
docker exec -it resumate_redis_prod redis-cli
```

**3. Check Memory Stats:**
```bash
INFO memory
```

*   Look for `used_memory_human` to see current usage.
*   Look for `maxmemory_human` to confirm your memory cap is active.
*   Look for `maxmemory_policy` to confirm the eviction policy.
