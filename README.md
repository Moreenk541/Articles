# Object Relations Code Challenge - Articles

## Problem Statement
Build a system to model the relationship between Authors, Articles, and Magazines, with data persisted in a SQL database. In this domain:
- An `Author` can write many `Articles`
- A `Magazine` can publish many `Articles`
- An `Article` belongs to both an `Author` and a `Magazine`
- The `Author`-`Magazine` relationship is many-to-many

## Setup Instructions

### Option 1: Using Pipenv
1. Install dependencies
   ```bash
   pipenv install sqlite3
   ```
2. Activate the virtual environment
   ```bash
   pipenv shell
   ```

### Option 2: Using venv
1. Create a virtual environment
   ```bash
   python -m venv env
   ```
2. Activate virtual environment (Mac/Linux)
   ```bash
   source env/bin/activate
   ```
   OR (Windows)
   ```bash
   env\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install 
   ```

### Database Setup
This project uses SQLite for database persistence.

In `lib/db/connection.py`:
```python
import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row # This enables column access by name
    return conn
```

## Recommended Project Structure
```
code-challenge/
├── lib/ # Main code directory
│ ├── models/ # Model classes
│ │ ├── __init__.py # Makes models a package
│ │ ├── author.py # Author class with SQL methods
│ │ ├── article.py # Article class with SQL methods
│ │ └── magazine.py # Magazine class with SQL methods
│ ├── db/ # Database components
│ │ ├── __init__.py # Makes db a package
│ │ ├── connection.py # Database connection setup
│ │ ├── seed.py # Seed data for testing
│ │ └── schema.sql # SQL schema definitions
│ ├── controllers/ # Optional: Business logic
│ │ └── __init__.py # Makes controllers a package
│ ├── debug.py # Interactive debugging
│ └── __init__.py # Makes lib a package
├── scripts/ # Helper scripts
│ ├── setup_db.py # Script to set up the database
│ └── run_queries.py # Script to run example queries
└── README.md # Project documentation
```

### Structure Guidelines:
1.  **Models**: Python classes that interact with the database via SQL
    *   `author.py`: Author class with methods using SQL queries
    *   `article.py`: Article class with relationships to Author and Magazine
    *   `magazine.py`: Magazine class with relationships
2.  **Database Layer**:
    *   `connection.py`: Database connection handling
    *   `schema.sql`: Table definitions and constraints
    *   `seed.py`: Populate database with test data
3.  **Package Organization**:
    *   Use `__init__.py` files to make directories into packages
    *   Each model file should handle its own SQL queries

## Deliverables

### 1. Database Schema
Create SQL tables for Authors, Articles, and Magazines with appropriate relationships in `lib/db/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS magazines (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER,
    magazine_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(id)
);
```

### 2. Python Classes with SQL Methods

#### Author Class
- Implement an Author class with proper initialization
- Write SQL methods to:
    - Save an author to the database
    - Find an author by ID or name
- Properties and validations for name
- Include methods to work with relationships

#### Magazine Class
- Implement a Magazine class with proper initialization
- Write SQL methods to:
    - Save a magazine to the database
    - Find a magazine by ID, name, or category
- Properties and validations for name and category
- Include methods to work with relationships

#### Article Class
- Implement an Article class with proper initialization
- Write SQL methods to:
    - Save an article to the database
    - Find articles by ID, title, author, or magazine
- Properties and validations for title
- Include methods to work with relationships

### 3. SQL Query Methods
Implement these SQL queries within your model classes:

1.  Get all articles written by a specific author
2.  Find all magazines a specific author has contributed to
3.  Get all authors who have written for a specific magazine
4.  Find magazines with articles by at least 2 different authors
5.  Count the number of articles in each magazine
6.  Find the author who has written the most articles

### 4. Relationship Methods

#### Author Methods
- `articles()`: Returns list of all articles written by the author (using SQL)
- `magazines()`: Returns unique list of magazines the author has contributed to (using SQL)
- `add_article(magazine, title)`: Creates and inserts a new Article into the database
- `topic_areas()`: Returns unique list of categories of magazines the author has contributed to (using SQL)

#### Magazine Methods
- `articles()`: Returns list of all articles published in the magazine (using SQL)
- `contributors()`: Returns unique list of authors who have written for this magazine (using SQL)
- `article_titles()`: Returns list of titles of all articles in the magazine (using SQL)
- `contributing_authors()`: Returns list of authors with more than 2 articles in the magazine (using SQL)

### 5. Database Transactions
Implement transaction handling with Python's context managers.

## Version Control Requirements

### Repository Setup
1.  Create a new Git repository for this challenge (already done by the environment)
2.  Initialize with a README.md explaining the project (done)
3.  Set up a `.gitignore` file for Python (include virtual environments, cache files, database files, etc.)

### Commit Practices
1.  Make small, focused commits that represent logical units of work
2.  Commit frequently as you complete features or fix issues
3.  Write clear, concise commit messages following this format:
    ```
    [Feature/Fix/Refactor]: Brief description of what changed

    - More detailed explanation if needed
    - List specific changes made
    ```

### Recommended Commit Sequence
1.  Initial project setup and database connection
2.  Database schema creation
3.  Basic class implementation with SQL methods
4.  Relationship query methods
5.  More complex SQL query implementations
6.  Transaction handling and error management
8.  Documentation updates
