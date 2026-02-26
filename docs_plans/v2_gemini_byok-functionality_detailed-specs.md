# Implementation Plan: Bring Your Own Key (BYOK) Functionality

## Approach
Currently, the Orchestrator runs without a direct connection to live LLM APIs. To make it functional, it needs to authenticate with models like Google Gemini or OpenAI. Since this is an open-source, locally run dashboard, the most secure approach is **Bring Your Own Key (BYOK)**.

**Why this solution:**
- **Zero Liability:** The backend never stores user API keys on disk or in a database.
- **Frontend Persistence:** We will use the browser's `localStorage` to save the API key across refreshes so the user doesn't have to enter it every time, passing it securely to the FastAPI backend via a Bearer Token or custom header on each request.
- **Dynamic Configuration:** The `ClawOrchestrator` will accept the key dynamically during the `execute_plan` invocation, allowing seamless swapping of keys or models.

**Alternatives considered:**
- `.env` file configuration: This requires users to touch the file system, which breaks the seamless "Dashboard" experience.
- Backend database storage: Unnecessary complexity and security risk for a local-first application.

## Steps
1. **Frontend UI Implementation** (20 min)
   - Files to modify: `static/index.html`
   - Add a settings cog/modal in the `architect-bar` for "API Key Configuration".
   - Implement JavaScript to save/load the key from `localStorage`.
   - Update the `deployClaw()` fetch request to include the key in the headers:
   ```javascript
   const apiKey = localStorage.getItem('llm_api_key');
   await fetch("/api/orchestrate", {
       method: "POST",
       headers: { 
           "Content-Type": "application/json",
           "Authorization": `Bearer ${apiKey}`
       },
       body: JSON.stringify({ objective })
   });
   ```

2. **Backend API Update** (15 min)
   - Files to modify: `main.py`
   - Add FastAPI `Depends` or `Header` extraction to securely intercept the Bearer token.
   - Update the `/api/orchestrate` endpoint to pass the intercepted key down to the `ClawOrchestrator`.
   ```python
   from fastapi import Depends, HTTPException
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

   security = HTTPBearer()

   @app.post("/api/orchestrate")
   async def start_orchestration(req: ObjectiveRequest, creds: HTTPAuthorizationCredentials = Depends(security)):
       api_key = creds.credentials
       if not api_key:
           raise HTTPException(status_code=401, detail="API Key required")
       
       claw = ClawOrchestrator(api_key=api_key)
       asyncio.create_task(claw.execute_plan(req.objective))
       return {"status": "started"}
   ```

3. **Orchestrator Injection** (10 min)
   - Files to modify: `src/orchestrator/claw.py` & `src/worker/code_instance.py`
   - Update `__init__` methods to accept the `api_key` and hold it in memory exclusively for the duration of the execution context.
   - Ensure the key is available when the actual LLM call logic is built.

4. **Testing** (15 min)
   - Create a test endpoint to validate the key format.
   - Verify the UI correctly prompts the user if the key is missing before allowing deployment.

## Timeline
| Phase | Duration |
|-------|----------|
| Frontend UI Implementation | 20 min |
| Backend API Update | 15 min |
| Orchestrator Injection | 10 min |
| Testing | 15 min |
| **Total** | **1 hour** |

## Rollback Plan
1. Revert changes to `main.py` to remove the `HTTPBearer` dependency.
2. Revert `static/index.html` to remove the settings modal and the `Authorization` header injection.
3. Remove `api_key` arguments from `ClawOrchestrator` and `CodeInstance`.

## Security Checklist
- [x] Input validation: Ensure the key is present and follows a basic format (e.g., `sk-...` for OpenAI or `AIza...` for Gemini) before sending.
- [x] Auth checks: The backend must explicitly reject requests missing the Authorization header (401 Unauthorized).
- [x] Storage: The key must ONLY be stored in `localStorage` on the client side, and never logged or written to disk on the backend.
- [x] Error handling: Provide a clear UI message to the user if the key is missing or invalid.