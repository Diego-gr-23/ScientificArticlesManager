# Scientific Articles Manager with GUI and Hash Tables

##  Overview
This project is a **Python application with a graphical interface (PyQt6)** for managing scientific articles stored in 
plain text format.

The system provides functionalities for:

- Loading and storing articles.

- Verifying existing entries.

- Searching and retrieving records.

- Editing article metadata.

- Deleting articles.

To guarantee **efficient lookups** and **duplicate detection**, the system uses **in-memory hash tables with chaining** 
as the main data structure and article in a separate file.  

----------

## Functional Requirements

### 1. Graphical User Interface (PyQt6)
- Input article metadata:
  - Title  
  - Author(s)  
  - Year of publication  
- Select a plain text file (`.txt`) containing the article content.

### 2. Hash Generation and Usage
- A **hash** (using FNV-1 or an equivalent algorithm) is computed from the file content.  
- This hash serves as the **unique identifier** of the article.  
- The file is stored under the name `<hash>.txt`.  

### 3. In-Memory Hash Table
- On startup, all records are loaded from articulos_db.txt and inserted into a hash table with chaining.
- All operations (search, update, delete) are executed first on the hash table.
- Changes are synchronized with the database file on every modification or when the application closes. 

### 4. Persistent Database
- The database is stored in a plain text file (`articulos_db.txt`) containing:  
hash | title | authors | year | filename | content

### 5. Duplicate Verification
- Before storing an article, the system checks if the hash already exists in memory.  
- If it does, the user is notified that the article is already registered, without scanning the database line by line.  

### 6. Management Options
- **Modify metadata:** Update author(s) or year of an article.  
- **Delete articles:** Remove the record from the database and delete the associated file.  
- **List articles:** Sort and list by author (alphabetically) or title (alphabetically).  

### 7. Search Optimization
- Search is supported through table filtering by title.
- Can be extended using secondary hash indices for author or year to improve query speed.  

----------

## Technoligies
- Pyhton 3.8 + 
- PyQt6 (GUI)
- FNV-1 Hash Algorithm
- File-based presisrence (.txt files)

----------

##  Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:Diego-gr-23/ScientificArticlesManager.git
   cd ScientificArticlesManager
   ```
2. Install dependencies (PyQt6):
  ```bash
    pip install PyQt6 
  ```
3. Run the application: 
  ```bash 
    python windowMain.py
  ```


----------

## Author 

- Luis Diego José Gómez Ramírez, 1510223 

