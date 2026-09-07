# Beginner Semantic Movie Search: A Step-by-Step Full-Stack Project

## What are we building?

We are going to build a very small web app that lets someone search for movies using **meaning**, rather than requiring them to type the exact words that appear in a movie description.

For example, imagine our movie data contains:

> "A computer programmer discovers that the world he lives in is actually a simulated reality."

A normal keyword search might struggle if the user searches:

> "a movie about someone discovering that their reality isn't what they thought"

The words are different, but the **idea is very similar**.

Our app will learn to recognize that similarity.

By the end of the project, a user will be able to type a natural-language description into a website, and the app will return movies whose descriptions are semantically similar.

We will build this gradually:

```text
Movie descriptions
       ↓
Convert descriptions into embeddings
       ↓
Compare their meanings
       ↓
Find the most similar movies
       ↓
Put the search behind a web API
       ↓
Build a simple React website
       ↓
Move vectors into an online vector database
       ↓
Deploy the application
       ↓
Optionally add an LLM + RAG
```

The important part is that **we will not start by building the whole thing at once**.

Each phase should give us a small program that works before we add another layer.

---

# 1. The Big Ideas, Explained From Zero

Before writing code, it helps to understand what the words in this project actually mean.

You do **not** need prior knowledge of embeddings, vector databases, RAG, FastAPI, or React.

The project is specifically designed to teach these concepts as we encounter them.

---

## 1.1 What is semantic search?

The word **semantic** basically means "related to meaning."

So:

- **Keyword search** looks for matching words.
- **Semantic search** looks for matching meaning.

Imagine these two sentences:

```text
Movie A:
"A scientist discovers that humanity lives inside a computer simulation."

Movie B:
"A detective investigates a murder in New York."
```

Now search:

```text
"a story about someone realizing their reality is fake"
```

A keyword search may not find Movie A because the exact words "fake reality" aren't present.

A semantic search system can recognize that:

```text
"reality is fake"
```

and

```text
"humanity lives inside a computer simulation"
```

are conceptually related.

That is the main problem we are trying to solve.

### Beginner checkpoint

Before moving on, you should be able to explain:

> "Semantic search is different from keyword search because it tries to find things with similar meaning, not just things containing the same words."

If that sentence makes sense, continue.

---

# 2. What is an embedding?

This is the first major AI concept in the project.

An **embedding** is a list of numbers that represents some piece of information in a mathematical form.

For example, imagine turning a sentence into:

```text
[0.12, -0.43, 0.81, 0.07, ...]
```

The real embedding will usually contain many more numbers.

The important idea is:

```text
text → numbers
```

Why would we want to do that?

Because computers can perform mathematical comparisons on numbers.

If two pieces of text have similar meanings, a good embedding model will generally place their embeddings relatively close together in the model's mathematical space.

---

## 2.1 A mental model: a map

Imagine a giant map.

Instead of cities, the map contains pieces of text.

Movies about:

```text
space
aliens
astronauts
```

might end up in one general region.

Movies about:

```text
romance
relationships
dating
```

might end up somewhere else.

Movies about:

```text
crime
detectives
murders
```

might occupy another region.

The exact geometry is much more complicated than this, but the map is a useful beginner mental model.

An embedding model is essentially helping us turn text into coordinates in this mathematical space.

---

# 3. What is an embedding model?

An **embedding model** is the model that performs the conversion:

```text
text → embedding
```

We will use a pretrained embedding model from the Hugging Face / Sentence Transformers ecosystem.

We give it a movie description:

```text
"A scientist discovers that humanity lives inside a computer simulation."
```

and it gives us a vector:

```text
[0.12, -0.43, 0.81, ...]
```

We can do the same thing with the user's search:

```text
"movie about discovering reality is fake"
```

and get another vector:

```text
[0.10, -0.39, 0.78, ...]
```

We can then compare those vectors.

---

# 4. What is vector similarity?

Once text has become numbers, we need a way to compare the numbers.

One common measurement is **cosine similarity**.

You do not need to memorize the math yet.

At a high level:

```text
similar vectors → high similarity
different vectors → low similarity
```

For example:

```text
Query
"someone discovers reality is fake"

        ↓ embedding

[0.10, -0.39, 0.78, ...]


Movie
"humanity lives inside a computer simulation"

        ↓ embedding

[0.12, -0.43, 0.81, ...]

        ↓ compare

HIGH similarity
```

We can calculate this for every movie and return the highest-scoring ones.

That is the core of our search engine.

---

# 5. What exactly is our first program doing?

At the beginning, we are **not building a website**.

We are going to build a tiny Python program that does this:

```text
Movie descriptions
       ↓
Create embeddings
       ↓
Store embeddings locally
       ↓
User enters a search
       ↓
Create an embedding for the search
       ↓
Compare it with every movie
       ↓
Return the most similar movies
```

This is intentionally simple.

We want to understand the search algorithm before introducing APIs, websites, databases, deployment, or LLMs.

---

# 6. The Full Architecture

Eventually, the project will look roughly like this:

```text
                    ┌─────────────────┐
                    │   React Website │
                    │                 │
                    │   Search bar    │
                    └────────┬────────┘
                             │
                             │ HTTP request
                             ↓
                    ┌─────────────────┐
                    │    FastAPI      │
                    │     Backend     │
                    └────────┬────────┘
                             │
                             ↓
                    ┌─────────────────┐
                    │ Vector Search   │
                    │                 │
                    │ Local / Pinecone│
                    └────────┬────────┘
                             │
                             ↓
                    ┌─────────────────┐
                    │ Movie Metadata  │
                    └─────────────────┘
```

Later, if we add RAG:

```text
User
 ↓
React
 ↓
FastAPI
 ↓
Vector Search
 ↓
Relevant Movies
 ↓
LLM
 ↓
Generated Answer
 ↓
React
```

We will not build all of this at once.

---

# 7. Technology Stack

We will use:

| Part | Technology | Why? |
|---|---|---|
| Programming language | Python | Simple and useful for AI/backend work |
| Embeddings | Sentence Transformers / Hugging Face | Easy way to generate embeddings |
| Local similarity search | NumPy or a simple vector library | Lets us understand the underlying idea |
| Backend API | FastAPI | Turns our Python search program into a web API |
| API testing | cURL | Lets us test the backend without a frontend |
| Frontend | React | Builds the webpage users interact with |
| Frontend tooling | Vite | Simple modern React development setup |
| Vector database | Pinecone | Lets us store/search vectors online |
| Deployment | A cloud hosting service | Makes the app accessible over the internet |
| Optional generation | LLM | Lets us generate natural-language answers from retrieved movies |

### Why aren't we using LangChain?

We deliberately aren't starting with LangChain.

Frameworks can be useful, but at the beginning they can hide what is actually happening.

We want to understand:

```text
text
→ embedding
→ similarity
→ retrieval
```

before introducing abstractions around it.

Once we understand the pieces, frameworks become much easier to learn.

---

# 8. GitHub: How We Will Work

We should use GitHub throughout the project rather than waiting until the end.

Git is a version-control system. It keeps a history of our code so we can see what changed and recover previous versions.

GitHub is a service where we can store that repository online and collaborate with other people or coding agents.

## Basic workflow

For each phase:

```text
Create a small change
        ↓
Run tests
        ↓
Inspect the code
        ↓
Commit
        ↓
Push to GitHub
        ↓
Move to the next phase
```

Try to make commits describe one meaningful change.

Good:

```text
add local movie dataset
generate movie embeddings
add cosine similarity search
add search API endpoint
```

Less useful:

```text
stuff
updates
fixed things
final
```

## Branches and pull requests

Once the project becomes more complicated, use branches:

```text
main
 │
 ├── phase-1-embeddings
 ├── phase-2-api
 ├── phase-3-react
 └── phase-5-pinecone
```

A pull request gives you an opportunity to review a change before merging it into `main`.

This is also a great way to use coding agents: have the agent implement a small task on a branch, then review its changes yourself.

---

# 9. How to Use a Coding Agent

A coding agent should not just be treated as:

> "Build the entire project for me."

For this project, it is much more useful as a **teacher + pair programmer**.

Good prompts ask the agent to:

1. Explain a concept.
2. Propose a small implementation.
3. Explain why the implementation works.
4. Add tests.
5. Tell you how to manually test it.
6. Point out assumptions and possible mistakes.
7. Keep the implementation appropriate for the current phase.

## A useful instruction to give the agent

```text
I am a beginner learning this project.

Please prioritize teaching me over generating a large amount of code.

For each change:
1. Explain what we are trying to accomplish.
2. Explain any new concepts or terminology.
3. Make the smallest reasonable implementation.
4. Explain the important parts of the code.
5. Tell me how to test it manually.
6. Add appropriate automated tests.
7. Explain what could go wrong.
8. Do not introduce additional frameworks or abstractions unless they are necessary for this phase.
```

This prevents the agent from jumping ahead and building an unnecessarily complicated architecture.

---

# Phase 0 — Set Up Python, Git, and GitHub

## Goal

Create the repository and establish a clean development workflow.

## What you are learning

- Git
- GitHub
- Python environments
- Project structure
- Why dependencies should be isolated

## Tasks

Create a repository with a simple structure:

```text
semantic-movie-search/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
├── src/
└── tests/
```

Create a Python virtual environment.

Install only the dependencies needed for Phase 1.

Add a small movie dataset.

For example:

```python
movies = [
    {
        "title": "Example Movie",
        "description": "A scientist discovers that reality is actually a simulation."
    },
    ...
]
```

At this point, do not worry about databases or web applications.

## Ask your coding agent

```text
Explain what a Python virtual environment is and why we should use one for this project.
```

```text
Help me create a beginner-friendly project structure for the first phase.
Explain why each folder exists before creating it.
```

```text
Review my .gitignore and explain what should and should not be committed.
```

## Test

Verify:

- Python runs.
- The virtual environment activates.
- Dependencies install.
- The movie dataset loads.
- The program can print the movie titles.

## Definition of done

You can clone the repository on another machine and understand how to set it up.

## Git checkpoint

Commit:

```text
initialize project structure
```

---

# Phase 1 — Build Semantic Search Locally

## Goal

Build the core search algorithm without a website or database.

This is the most important learning phase.

## What you are learning

- Embedding models
- Embeddings
- Vector representations
- Similarity
- Semantic search
- Query vs. document embeddings

## Step 1: Generate embeddings for movies

Use an embedding model to convert every movie description into a vector.

Conceptually:

```text
movie description
       ↓
embedding model
       ↓
vector
```

Store those vectors locally.

Do not regenerate the movie embeddings every time somebody searches.

The movie descriptions are relatively static, so we can generate their embeddings once and reuse them.

## Step 2: Embed the search query

When the user enters:

```text
"a movie where someone realizes their world isn't real"
```

we pass that query through the same embedding model.

```text
search query
     ↓
same embedding model
     ↓
query vector
```

Using the same model is important because we want the query and movie descriptions represented in the same vector space.

## Step 3: Compare the vectors

Calculate the similarity between the query vector and every movie vector.

Then sort by similarity.

Conceptually:

```text
query
 ↓
query vector
 ↓
compare against:
   movie 1 → score
   movie 2 → score
   movie 3 → score
   ...
 ↓
sort scores
 ↓
top results
```

## Step 4: Serialize the embeddings

Save the generated embeddings locally so you do not have to recompute them every time the program starts.

Keep the actual movie information separate from the vectors.

For example:

```text
movie metadata:
title
description
poster URL

embedding:
[0.12, -0.43, ...]
```

The embedding is primarily for search.

The metadata is what we eventually show to the user.

## Suggested agent questions

```text
Explain embeddings using our movie-search example without assuming I know machine learning.
```

```text
Why does semantic search sometimes find a movie even when the search query shares very few words with its description?
```

```text
Explain cosine similarity using a tiny numerical example.
```

```text
Why should the search query and movie descriptions be embedded using the same model?
```

```text
What exactly is being stored in an embedding file?
```

```text
Review this implementation. Tell me if I am accidentally recomputing embeddings unnecessarily.
```

## Manual tests

Try searches such as:

```text
a person discovers that their reality is fake
```

```text
a romantic relationship that falls apart
```

```text
people traveling through outer space
```

```text
someone trying to solve a murder
```

Look at the returned movies.

Do not just ask:

> "Did the program run?"

Ask:

> "Are the results actually semantically relevant?"

That distinction becomes important later.

## Automated tests

At minimum, test:

- Embeddings are generated.
- The number of embeddings matches the number of movies.
- Embeddings have the expected dimensionality.
- Similarity scores can be calculated.
- Results are sorted correctly.
- Asking for top 3 results returns at most 3 results.
- The program handles an empty query appropriately.

Do not write a brittle test that assumes a particular movie must always rank #1 unless you intentionally make that part of the dataset contract.

## Definition of done

You can run:

```text
python ...
```

and enter a natural-language query.

The program returns movies ranked by semantic similarity.

No FastAPI.

No React.

No Pinecone.

No LLM.

Just:

```text
text → embeddings → similarity → results
```

## Git checkpoint

Commit:

```text
implement local semantic search
```

---

# Phase 2 — Turn the Search Program Into an API

## Goal

Make another program capable of asking our Python search system for results.

This is where FastAPI comes in.

## What is an API?

An API is a way for one piece of software to communicate with another.

Instead of:

```text
you run Python
you type a query
Python prints results
```

we want:

```text
another program
      ↓
HTTP request
      ↓
FastAPI
      ↓
Python search code
      ↓
HTTP response
```

## What is FastAPI?

FastAPI is a Python framework for creating web APIs.

For this project, think of it as:

> "A tool that lets our Python program listen for requests from other programs."

We will create an endpoint such as:

```text
GET /search?q=space
```

The server receives the query, performs semantic search, and returns structured results.

## What is JSON?

JSON is a common text format used to send structured information between programs.

For example:

```json
{
  "title": "Example Movie",
  "score": 0.87
}
```

The React frontend will eventually receive JSON like this from FastAPI.

## Architecture

```text
HTTP request
     ↓
FastAPI route
     ↓
search function
     ↓
embeddings + similarity
     ↓
results
     ↓
JSON response
```

Keep the actual search logic separate from the FastAPI route.

For example:

```text
API layer
    ↓
search layer
    ↓
data / embeddings
```

That separation will make the project easier to test and extend.

## Suggested agent questions

```text
Explain HTTP GET requests using our movie search example.
```

```text
What is a FastAPI route, and what happens when a request reaches it?
```

```text
Why shouldn't we put all of the semantic-search logic directly inside the FastAPI route?
```

```text
Explain query parameters using /search?q=space.
```

```text
Explain JSON using the movie results our API will return.
```

## Manual tests with cURL

Run the server locally.

Then use cURL to make a request.

Conceptually:

```bash
curl "http://localhost:8000/search?q=a%20movie%20about%20space"
```

You should receive JSON.

Test:

- Normal query
- Empty query
- Very long query
- Special characters
- Different result counts if supported

The exact URL and parameters should match the API you implement.

## Automated tests

Add API tests that verify:

- The endpoint responds successfully.
- Valid queries return the expected response shape.
- Invalid input returns an appropriate error.
- Result objects contain the fields we expect.
- The endpoint does not crash on unusual input.

## Definition of done

You can start FastAPI and use cURL to search your movie dataset without directly running the search program yourself.

## Git checkpoint

Commit:

```text
add semantic search API
```

---

# Phase 3 — Build the Simplest Possible React Frontend

## Goal

Create a webpage containing:

```text
Search bar
Search button
Results
```

Nothing fancy.

## What is React?

React is a JavaScript library for building user interfaces.

For our project, think of it as:

> "The code that creates the webpage the user interacts with."

Our React app will send HTTP requests to our FastAPI backend.

```text
React
  ↓
HTTP request
  ↓
FastAPI
  ↓
search
  ↓
JSON
  ↓
React
  ↓
display results
```

## What is Vite?

Vite is a development/build tool commonly used with React.

It gives us a simple way to create and run the frontend during development.

## First UI

Keep it extremely simple:

```text
--------------------------------
| Search movies...             |
|                    [Search]  |
--------------------------------

Results:

Movie A
Movie B
Movie C
```

Do not start with:

- authentication
- complicated routing
- state-management libraries
- animations
- design systems
- a dozen components

We are learning the connection between frontend and backend.

## Suggested agent questions

```text
Explain React state using our search input as the example.
```

```text
Explain what happens from the moment I click Search until the results appear.
```

```text
How does React make an HTTP request to FastAPI?
```

```text
Explain JSON parsing in the frontend using our API response.
```

```text
Why should the API URL be stored in an environment variable rather than hard-coded throughout the application?
```

## Important concept: CORS

Once React and FastAPI run on different origins, the browser may block requests between them unless the backend explicitly allows the frontend origin.

This is called **Cross-Origin Resource Sharing (CORS)**.

You do not need to memorize the networking details yet.

The important idea is:

```text
Frontend origin ≠ Backend origin
                ↓
             browser
                ↓
         checks permission
```

Configure CORS carefully rather than simply allowing every origin in production.

## Manual tests

Open the React app.

Test:

1. Type a query.
2. Click Search.
3. Confirm a request is sent.
4. Confirm the backend receives it.
5. Confirm results appear.
6. Try an empty query.
7. Try a query with punctuation.
8. Try submitting repeatedly.

Open the browser developer tools and inspect the network request.

## Automated tests

Add appropriate frontend tests for:

- Search input rendering.
- Search button behavior.
- Loading state.
- Successful results.
- Error state.
- Empty results.

You do not need a huge frontend testing framework setup just for the sake of having one.

## Definition of done

A user can open the webpage, type a movie-search query, click Search, and see results from the Python backend.

## Git checkpoint

Commit:

```text
add basic React search interface
```

---

# Phase 4 — Make the Results Look Like a Movie App

## Goal

Now that the entire system works, improve the frontend without changing the search architecture.

## Add movie cards

Each result can display:

```text
┌─────────────────────────────┐
│       Movie Poster          │
│                             │
│ Movie Title                 │
│                             │
│ Description...              │
│                             │
│ Similarity: 0.87            │
└─────────────────────────────┘
```

If your dataset contains poster URLs, the frontend can use them.

## Important architecture lesson

The frontend should not need to know how embeddings work.

It should simply receive something like:

```json
{
  "title": "Example Movie",
  "description": "...",
  "poster_url": "...",
  "score": 0.87
}
```

The frontend's job is presentation.

The backend's job is search.

## Suggested agent questions

```text
Review my frontend architecture. Is the React app doing any work that belongs in the backend?
```

```text
Explain why movie metadata and embeddings should remain conceptually separate.
```

```text
Help me turn the result display into a reusable React component without overengineering it.
```

## Manual tests

Check:

- Images load.
- Missing images do not break the page.
- Long titles do not destroy the layout.
- Long descriptions remain readable.
- Results display their similarity score correctly.
- Mobile-sized windows remain usable.

## Definition of done

The search application looks like a basic movie-search website rather than a developer demo.

## Git checkpoint

Commit:

```text
add movie result cards
```

---

# Phase 5 — Move the Vectors Into a Vector Database

## Goal

Replace our local vector storage/search approach with an online vector database such as Pinecone.

This phase teaches **why vector databases exist**.

## First: why do we need one?

Our local implementation might do something like:

```text
query vector
     ↓
compare against movie 1
compare against movie 2
compare against movie 3
...
     ↓
sort everything
```

That is perfectly reasonable for a tiny dataset.

But imagine millions of documents.

We would want specialized infrastructure for storing and searching vectors efficiently.

That is where a **vector database** comes in.

## What is a vector database?

A vector database is a database designed to store and retrieve vector representations efficiently.

Think of it as:

```text
Local version:

Python + NumPy
      ↓
compare vectors yourself


Larger-scale version:

Application
     ↓
Vector database
     ↓
nearest/similar vectors
```

Pinecone is one example.

The important thing is not memorizing Pinecone's API.

The important thing is understanding the abstraction:

> "I have a query vector. Find the stored vectors that are most similar to it."

## Vector dimensions

Every embedding model produces vectors with a specific number of dimensions.

For example, if a model produces:

```text
[0.12, 0.43, ...]
```

with 384 numbers, then every vector stored in that index needs to have dimension 384.

The vector database index configuration therefore has to match the embedding model.

Ask the coding agent to explain this rather than blindly copying a configuration.

## Ingestion vs. querying

Separate these two jobs.

### Ingestion

```text
movie data
   ↓
embedding model
   ↓
vectors
   ↓
vector database
```

This should happen when we add/update movies.

### Querying

```text
user query
   ↓
embedding model
   ↓
query vector
   ↓
vector database
   ↓
top results
```

The API should not regenerate and upload every movie embedding every time someone searches.

## Suggested agent questions

```text
What does a vector database do that our local NumPy implementation does not?
```

```text
Explain a vector database using the movie-search example.
```

```text
Why does the vector database dimension need to match the embedding model's output dimension?
```

```text
Explain the difference between ingestion and querying.
```

```text
Review my Pinecone integration for unnecessary complexity.
```

```text
Explain what metadata should be stored with each vector and why.
```

## Migration strategy

Do not delete the local implementation immediately.

Instead:

```text
Local search
     ↓
known working behavior
     ↓
Pinecone implementation
     ↓
compare results
```

Use the local implementation as a reference point.

For the same queries, compare:

```text
local top results
vs.
Pinecone top results
```

They should be reasonably consistent, allowing for differences caused by implementation details.

## Secrets

Your Pinecone API key is a secret.

Never commit it to GitHub.

Use environment variables and a `.env` file locally.

Commit something like:

```text
.env.example
```

but never the real `.env`.

## Manual tests

Verify:

- Movie vectors are successfully inserted.
- You can query the index.
- Returned metadata matches the correct movie.
- Scores are returned.
- Re-running ingestion does not create unintended duplicates.
- Queries return sensible results.

## Definition of done

The application can search the online vector database instead of relying on local vector storage.

## Git checkpoint

Commit:

```text
replace local vector search with vector database
```

---

# Phase 6 — Deploy the Backend

## Goal

Make the FastAPI backend accessible over the internet.

Before this phase:

```text
React
  ↓
localhost
  ↓
FastAPI
```

After this phase:

```text
React
  ↓
Internet
  ↓
Hosted FastAPI
  ↓
Vector database
```

## What you are learning

- Servers
- Hosting
- Environment variables
- Production configuration
- Logs
- Deployment

## Suggested agent questions

```text
Explain what changes when a FastAPI application moves from localhost to a hosted server.
```

```text
What environment variables does the backend need in production?
```

```text
Explain why secrets should not be committed to GitHub.
```

```text
Help me make a production checklist without changing my application architecture.
```

```text
What should I look for in deployment logs if the application starts locally but fails in production?
```

## Manual tests

After deployment:

```text
curl https://your-api/search?q=space
```

Verify:

- The endpoint is reachable.
- Search works.
- The vector database connection works.
- Secrets are configured.
- Errors are visible in logs.
- The API does not expose secrets.

## Definition of done

The backend works without your computer running the development server.

## Git checkpoint

Commit:

```text
deploy backend
```

---

# Phase 7 — Deploy the Frontend

## Goal

Make the website publicly accessible.

The final basic architecture is now:

```text
User
 ↓
Hosted React frontend
 ↓
Hosted FastAPI backend
 ↓
Pinecone
```

## Important concept: frontend environment variables

The React app needs to know where the backend lives.

Instead of scattering this throughout the code:

```text
http://localhost:8000
```

use a configurable environment variable such as:

```text
VITE_API_URL
```

Then:

```text
development:
VITE_API_URL = local backend

production:
VITE_API_URL = hosted backend
```

The exact deployment platform may have its own configuration interface.

## Suggested agent questions

```text
Explain the difference between a development frontend URL and a production frontend URL.
```

```text
Why should the API URL be configurable?
```

```text
Explain what happens when the deployed frontend calls the deployed backend.
```

```text
Review my deployment configuration for secrets accidentally exposed to the browser.
```

## Manual tests

From a completely different machine/network if possible:

1. Open the website.
2. Search for a movie concept.
3. Confirm results load.
4. Open browser developer tools.
5. Inspect the network request.
6. Confirm the API is the deployed API.
7. Test error behavior.

## Definition of done

Someone can visit a URL and use the application without cloning the repository.

## Git checkpoint

Commit:

```text
deploy frontend
```

---

# Phase 8 — Add an LLM and Introduce RAG

## Goal

Only now do we add an LLM.

At this point, you already understand retrieval.

That makes RAG much easier to understand.

## What is an LLM?

A large language model (LLM) is a model designed to understand and generate language.

For example, it can turn information into a natural-language response.

But we do **not** want the LLM to be responsible for discovering the relevant movies by itself.

We already have a retrieval system.

---

# 8.1 What is RAG?

RAG stands for:

**Retrieval-Augmented Generation**

The name sounds complicated, but the basic idea is simple:

```text
Retrieve relevant information
          ↓
Give that information to an LLM
          ↓
Generate an answer
```

For our movie app:

```text
User query
     ↓
Embedding
     ↓
Vector search
     ↓
Relevant movies
     ↓
Give movies to LLM
     ↓
LLM generates response
```

For example:

```text
User:
"What movies are similar to a story about discovering that reality isn't real?"
```

Vector search might retrieve:

```text
Movie A — simulated reality
Movie B — virtual world
Movie C — unreliable perception
```

We then provide those retrieved movies to the LLM.

The LLM might produce:

```text
Here are three movies that fit your description...

1. Movie A — ...
2. Movie B — ...
3. Movie C — ...
```

The key is that the LLM is generating language **from retrieved context**.

---

# 8.2 Why not just ask the LLM?

Because an LLM and a retrieval system are solving different problems.

### Retrieval

Answers:

> "Which pieces of our movie database are relevant?"

### LLM

Answers:

> "How should I explain these relevant pieces of information to the user?"

So:

```text
Retrieval = finding information
LLM = generating language
```

RAG combines them.

---

# 8.3 What exactly is being retrieved?

This is an important question.

The vector database is not magically retrieving "knowledge."

It is retrieving the movie records whose embeddings are most similar to the query embedding.

For example:

```text
query vector
     ↓
vector search
     ↓
movie IDs + scores + metadata
```

Those retrieved records become the context given to the LLM.

---

# 8.4 RAG testing

Do not test only:

> "Does the LLM give a nice answer?"

Test three separate things.

### Test 1 — Retrieval correctness

Did we retrieve relevant movies?

### Test 2 — Generation correctness

Did the LLM correctly describe the retrieved movies?

### Test 3 — Grounding

Did the LLM stay within the information provided to it?

For example, if the database says:

```text
Movie A:
A scientist discovers a simulated reality.
```

the LLM should not invent:

```text
The scientist was played by Tom Hanks.
```

unless that information was actually provided in the context.

This is one reason RAG is useful: we can constrain generation with retrieved information.

## Suggested agent questions

```text
Explain RAG without assuming I know what retrieval or generation means.
```

```text
What exactly is retrieved before the LLM is called?
```

```text
Why not simply ask the LLM to recommend movies?
```

```text
What could happen if vector search retrieves an irrelevant movie?
```

```text
How can we test whether the LLM is grounded in the retrieved context?
```

```text
Design tests for retrieval correctness, generation correctness, and grounding separately.
```

## Definition of done

The app can:

```text
user query
    ↓
semantic retrieval
    ↓
relevant movies
    ↓
LLM
    ↓
natural-language response
```

and you understand what each component is doing.

## Git checkpoint

Commit:

```text
add retrieval augmented generation
```

---

# Phase 9 — Optional Advanced Features

Only after the core system is understood should you consider adding more sophisticated features.

Possible directions include:

## Hybrid search

Combine:

```text
keyword search
+
semantic search
```

This can help when exact terms matter.

## Reranking

Retrieve a larger group of candidates, then use another model to rank them more carefully.

```text
query
 ↓
retrieve top 50
 ↓
reranker
 ↓
best 10
```

## Query expansion

Transform a short query into additional related search terms or descriptions before retrieval.

## Filtering

Allow filters such as:

```text
genre
year
rating
language
```

## Evaluation

Create a small test set:

```text
Query:
"a detective solving a murder"

Expected relevant movies:
Movie A
Movie C
Movie F
```

Then measure whether your search system retrieves the expected results.

This is much more useful than judging search quality only by looking at the UI.

## Model comparison

Try different embedding models and compare their retrieval quality.

Questions to investigate:

- Which model produces better results?
- How large are its vectors?
- How fast is it?
- How much memory does it use?
- Does it handle short queries well?
- Does it handle long descriptions well?

## Conversation

Allow users to ask follow-up questions.

For example:

```text
User:
Find movies about simulated realities.

App:
...

User:
Which of those are more like science fiction?
```

This introduces additional problems around conversation state and query interpretation.

Do not add these features until the simpler system is understood.

---

# 10. Testing Strategy

Testing should happen throughout the project, not at the end.

There are several levels of testing.

## Unit tests

Test individual pieces of logic.

Example:

```text
Does our similarity function correctly rank vectors?
```

## Integration tests

Test multiple components together.

Example:

```text
Can the search service load embeddings and return movies?
```

## API tests

Test the HTTP interface.

Example:

```text
GET /search?q=space
```

Does it return valid JSON?

## End-to-end tests

Test the application the way a user experiences it.

```text
Open website
 ↓
type query
 ↓
click Search
 ↓
results appear
```

## Retrieval evaluation

This deserves special attention.

A search system can be technically functional while being terrible at search.

For example:

```text
HTTP request: SUCCESS
Embedding generation: SUCCESS
Vector database: SUCCESS

Search quality: TERRIBLE
```

The first three being successful does not mean the application works well.

Create a small evaluation set of queries and manually identify which movies should be considered relevant.

Then track retrieval quality as you change:

- embedding models
- similarity methods
- chunking/description formats
- vector databases
- rerankers
- query processing

---

# 11. A Useful Testing Prompt for Your Coding Agent

Ask:

```text
Before writing any tests, explain which parts of this feature should be tested at the unit, integration, API, and end-to-end levels.

For each test, explain what failure it would catch.

Then implement only the tests that are appropriate for the current phase.
```

This is better than asking:

```text
Write tests.
```

because you learn what the tests are actually proving.

---

# 12. Beginner Vocabulary as We Go

Here is the vocabulary you should gradually become comfortable with.

| Term | Beginner definition |
|---|---|
| Semantic | Related to meaning |
| Semantic search | Search based on meaning rather than exact words |
| Embedding | A numerical representation of information |
| Embedding model | A model that converts text into embeddings |
| Vector | A list of numbers |
| Vector similarity | A measurement of how similar two vectors are |
| Cosine similarity | A common way to compare the direction of vectors |
| API | A way for programs to communicate |
| HTTP | A protocol commonly used for communication over the web |
| JSON | A common format for structured data |
| Backend | The part of the application that performs server-side work |
| Frontend | The part of the application the user interacts with |
| React | A JavaScript library for building user interfaces |
| FastAPI | A Python framework for creating APIs |
| Database | A system for storing and retrieving data |
| Vector database | A database specialized for storing/searching vectors |
| Metadata | Information describing another piece of data |
| Ingestion | Preparing and inserting data into a system |
| LLM | A large language model that processes and generates language |
| Retrieval | Finding relevant information |
| Generation | Producing a response, usually with an LLM |
| RAG | Retrieval-Augmented Generation: retrieve information, then use it as context for generation |
| Grounding | Keeping generated answers supported by provided information |
| Deployment | Making the application available outside your computer |
| CORS | Browser security rules governing requests between different origins |

You do not need to memorize this table.

The goal is to understand each word when it becomes relevant.

---

# 13. Stop-and-Explain Checkpoints

After each major phase, pause and explain the system in your own words.

## After Phase 1

Can you explain:

```text
text
→ embedding
→ vector
→ similarity
→ search result
```

without looking at the code?

## After Phase 2

Can you explain:

```text
HTTP request
→ FastAPI
→ search function
→ JSON response
```

?

## After Phase 3

Can you explain:

```text
React
→ HTTP request
→ FastAPI
→ JSON
→ React
```

?

## After Phase 5

Can you explain why a vector database exists and how it differs from simply storing vectors in a Python list?

## After Phase 8

Can you explain:

```text
retrieval
+
generation
=
RAG
```

?

If you cannot explain one of these, do not be afraid to pause and ask your coding agent to teach the concept again.

---

# 14. Useful Coding-Agent Prompts

## Concept explanations

```text
Explain embeddings from zero using only our movie-search example.
```

```text
Explain semantic search as if I understand programming but have never worked with machine learning.
```

```text
Explain cosine similarity with a tiny numerical example.
```

```text
Explain why two sentences with different words can have similar embeddings.
```

```text
What happens if I embed the query using a different embedding model from the movies?
```

---

## Architecture questions

```text
Explain the entire architecture of our current project and the job of each component.
```

```text
Why is this code in the backend instead of the frontend?
```

```text
What responsibilities should the React frontend have?
```

```text
What responsibilities should the FastAPI backend have?
```

```text
What would become difficult if we put all of the code into one Python file?
```

---

## Review prompts

```text
Review this code as a teacher, not just as a code generator.

Identify:
- bugs
- security issues
- unnecessary complexity
- missing tests
- confusing architecture
- concepts a beginner might misunderstand

Do not rewrite the code yet. Explain the problems first.
```

---

## Simplicity prompt

Use this throughout the project:

```text
Prefer the simplest implementation that teaches the concept clearly.

Do not introduce additional frameworks, abstractions, databases, Docker, LangChain, or other dependencies unless they are necessary for the current phase.

If there are multiple reasonable approaches, explain the tradeoffs and recommend the simplest one for a beginner.
```

---

## Testing prompt

```text
Before implementing this feature, tell me:

1. What can go wrong?
2. What should we test?
3. Which tests should be unit tests?
4. Which should be integration/API tests?
5. What manual test should I perform?

Then implement the smallest useful test suite.
```

---

# 15. Common Beginner Mistakes

## Mistake 1: Starting with an LLM

It is tempting to immediately ask:

```text
"How do I build a RAG app?"
```

But then it is easy to use a framework without understanding what retrieval is actually doing.

Learn:

```text
embedding
→ similarity
→ retrieval
```

first.

---

## Mistake 2: Starting with Pinecone

A vector database is useful, but it can hide the fundamental idea.

First understand:

```text
query vector
     ↓
compare against vectors
     ↓
rank results
```

Then let a vector database handle that job.

---

## Mistake 3: Letting the coding agent build everything

You might end up with:

```text
React
FastAPI
LangChain
Pinecone
LLM
Docker
authentication
PostgreSQL
Redis
Kubernetes
```

for an application that basically needs:

```text
search box → search results
```

More technology does not automatically mean more learning.

---

## Mistake 4: Testing only whether code runs

A search engine can run perfectly while producing terrible results.

Always test:

```text
Does it run?
```

and:

```text
Does it return useful results?
```

---

## Mistake 5: Committing secrets

Never commit:

```text
API keys
passwords
tokens
private credentials
```

Use environment variables and `.env` files.

Commit a `.env.example` showing which variables are needed, without their secret values.

---

## Mistake 6: Mixing responsibilities

Try to keep the architecture understandable:

```text
React
→ presentation

FastAPI
→ API + backend coordination

Search service
→ retrieval logic

Vector database
→ vector storage/search

Embedding model
→ text → vector
```

Clear boundaries make the project easier to understand and modify.

---

# 16. Final Project Structure

By the end, a reasonable repository might look something like:

```text
semantic-movie-search/
│
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
│
├── data/
│   └── movies.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   └── models/
│   │
│   ├── scripts/
│   │   └── ingest.py
│   │
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── ...
│   │
│   └── tests/
│
└── docs/
    └── ...
```

The exact structure is not sacred.

The important thing is that the structure reflects the responsibilities of the application.

---

# 17. Final Architecture

Once everything is complete:

```text
                         USER
                           │
                           ↓
                  ┌─────────────────┐
                  │ React Frontend  │
                  │                 │
                  │ Search bar      │
                  │ Movie cards     │
                  └────────┬────────┘
                           │
                           │ HTTP / JSON
                           ↓
                  ┌─────────────────┐
                  │    FastAPI      │
                  │    Backend      │
                  └────────┬────────┘
                           │
                           ↓
                  ┌─────────────────┐
                  │ Embedding Model │
                  │                 │
                  │ Query → Vector  │
                  └────────┬────────┘
                           │
                           ↓
                  ┌─────────────────┐
                  │ Vector Database │
                  │                 │
                  │ Pinecone        │
                  └────────┬────────┘
                           │
                           ↓
                  ┌─────────────────┐
                  │ Relevant Movies │
                  └────────┬────────┘
                           │
                           ↓
                    ┌──────────────┐
                    │     LLM      │
                    │   (optional) │
                    └──────┬───────┘
                           │
                           ↓
                    Natural-language
                       response
```

The key conceptual pipeline is still:

```text
TEXT
 ↓
EMBEDDING
 ↓
VECTOR
 ↓
SIMILARITY
 ↓
RETRIEVAL
 ↓
(optional) LLM
 ↓
RESPONSE
```

Everything else exists to make that pipeline usable, scalable, and accessible through a website.

---

# 18. The Entire Learning Path at a Glance

| Phase | Build | Main concept |
|---|---|---|
| 0 | Python/Git/GitHub setup | Development workflow |
| 1 | Local semantic search | Embeddings + similarity |
| 2 | FastAPI API | Backend/API |
| 3 | React search page | Frontend |
| 4 | Movie cards | UI/data presentation |
| 5 | Pinecone | Vector databases |
| 6 | Hosted backend | Deployment |
| 7 | Hosted frontend | Full-stack deployment |
| 8 | LLM + RAG | Retrieval + generation |
| 9 | Advanced features | Evaluation, reranking, hybrid search |

The progression is intentional:

```text
Understand the idea
        ↓
Build it locally
        ↓
Expose it through an API
        ↓
Build a UI
        ↓
Replace local infrastructure
        ↓
Deploy it
        ↓
Add generation
        ↓
Experiment
```

That way, when something breaks, you have a much better chance of understanding **which layer broke and why**.

---

# 19. Final Principle

The goal of this project is not simply to end up with a website.

The goal is to be able to look at the final application and explain what every major component is doing.

You should eventually be able to answer:

> **What happens when I type a search query?**

A good answer would look roughly like:

```text
1. React reads the user's query.
2. React sends it to the FastAPI backend.
3. The backend converts the query into an embedding.
4. The vector database compares that query vector with stored movie vectors.
5. The most relevant movies are returned.
6. FastAPI sends the results back as JSON.
7. React displays the movies.
8. If RAG is enabled, the retrieved movies are provided to an LLM.
9. The LLM generates a response using that retrieved context.
```

If you can explain that pipeline without relying on the coding agent to explain it for you, you have learned the core architecture.

And that understanding is much more valuable than simply having a working application.
