# Implementation Plan: Personal Knowledge Library

## Phase 1: Database Setup
- [ ] **Connect to Neon/PostgreSQL:** Sets up the secure storage for the notes and their search data.
- [ ] **Setup user auth:** Configure user authentication and session handling using Neon Auth.
- [ ] **Turn on `pgvector`:** Enables the database to perform high-speed similarity searches on the notes.
- [ ] **Create the notes table:** Sets up the structure for titles, text content, and vector embeddings.
- [ ] **Speed up searches:** Adds an HNSW index to keep search results instant as library grows.

## Phase 2: Backend Development (FastAPI)
- [ ] **Set up FastAPI:** Initializes the server to handle incoming requests.
- [ ] **Add text-to-vector tool:** Sets up the logic to convert text into searchable data.
- [ ] **Manage state:** Ensure UI reflects user auth status.
- [ ] **Add "save note" feature:** Stores new note along with its vector embedding.
- [ ] **Add "search notes" feature:** Compares query to notes and returns the most relevant ones.
- [ ] **Add "update note" feature:** Update existing note and ensure associated vectors are updated.
- [ ] **Add "delete note" feature:** Delete existing note and ensure associated vector is deleted.
- [ ] **Add relevance filter:** Ensures the search only returns notes that are actually similar to query, hiding irrelevant results.

## Phase 3: Frontend Development (React)
- [ ] **Build "Save Note" screen:** A simple form to input and save knowledge.
- [ ] **Add "Update Note" option:** Allow authenticated users to update an existing note.
- [ ] **Add "Delete Note" option:** Allow authenticated users to delete an existing note.
- [ ] **Build "Library Search" screen:** A search box to query notes and view matching results.
- [ ] **Implement result display:** Shows the titles and content of the most relevant notes found.
- [ ] **Add "No results" feedback:** Tells you clearly when no notes match query.

## Phase 4: Integration & Deployment
- [ ] **Launch the backend:** Deploys the search engine API to a container-friendly environment.
- [ ] **Launch the website:** Deploys the frontend for easy access.
- [ ] **Connect everything:** Links the frontend to backend securely.
