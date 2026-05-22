# Implementation Plan: Personal Knowledge Library

## Phase 1: Database Setup
- [x] **Connect to Neon/PostgreSQL:** Sets up the secure storage for the notes and their search data.
- [ ] **Setup user auth:** Configure user authentication and session handling using Neon Auth.
- [x] **Turn on `pgvector`:** Enables the database to perform high-speed similarity searches on the notes.
- [x] **Create the notes table:** Sets up the structure for titles, text content, and vector embeddings.
- [x] **Create the users table:** Sets up the structure for user sign up.
- [ ] **Speed up searches:** Adds an HNSW index to keep search results instant as library grows.

## Phase 2: Backend Development (FastAPI)
- [ ] **Set up FastAPI:** Initializes the server to handle incoming requests.
- [ ] **Add text-to-vector tool:** Sets up the logic to convert text into searchable data.
- [ ] **Manage state:** Ensure UI reflects user auth status.
- [ ] **Add "save note" route:** Stores new note along with its vector embedding.
- [ ] **Add "search notes" route:** Compares query to notes and returns the most relevant ones.
- [ ] **Add "update note" route:** Update existing note and ensure associated vectors are updated.
- [ ] **Add "delete note" route:** Delete existing note and ensure associated vector is deleted.
- [ ] **Add "Create User" route:** Implement endpoint to save new user profile via Neon Auth ID.
- [ ] **Add "Update User" route:** Implement endpoint to update user profile info (username/email).
- [ ] **Add relevance filter:** Ensures the search only returns notes that are actually similar to query, hiding irrelevant results.


## Phase 3: Frontend Development (React)
- [ ] **Build "Save Note" screen:** A simple form to input and save knowledge.
- [ ] **Add "Update Note" option:** Allow authenticated users to update an existing note.
- [ ] **Add "Delete Note" option:** Allow authenticated users to delete an existing note.
- [ ] **Build "Sign Up/User Profile" form:** Connect frontend to the "Create User" endpoint.
- [ ] **Build "Edit Profile" screen:** Connect frontend to the "Update User" endpoint.
- [ ] **Build "Library Search" screen:** A search box to query notes and view matching results.
- [ ] **Implement result display:** Shows the titles and content of the most relevant notes found.
- [ ] **Add "No results" feedback:** Tells you clearly when no notes match query.
- [ ] **Configure auth rules:** Configure password complexity and security policies in Neon Auth (using `auth.ts`).

## Phase 4: Integration & Deployment
- [ ] **Launch the backend:** Deploys the search engine API to a container-friendly environment.
- [ ] **Launch the website:** Deploys the frontend for easy access.
- [ ] **Connect everything:** Links the frontend to backend securely.
