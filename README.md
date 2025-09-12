# Scientific Articles Manager with GUI and Hash Tables

##  Overview
The goal of this project is to develop a **Python application with a graphical interface (Tkinter)** to manage scientific articles stored in plain text format.  

The system provides functionalities for:  
- Loading and storing articles  
- Verifying existing entries  
- Searching and retrieving records  
- Editing article metadata  
- Deleting articles  

To guarantee **efficient lookups** and **duplicate detection**, the system uses **in-memory hash tables with chaining** as the main data structure.  

----------

## Functional Requirements

### 1. Graphical User Interface (Tkinter)
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
- On startup, the system loads all records from the database file and builds an **in-memory hash table with chaining** for fast access.  
- All operations (search, update, delete) are executed on the hash table first.  
- On closing the application or modifying records, changes are synchronized with the database file.  

### 4. Persistent Database
- The database is stored in a plain text file (`articulos_db.txt`) containing:  
  - Hash  
  - Title  
  - Author(s)  
  - Year  
  - Associated filename  

### 5. Duplicate Verification
- Before storing an article, the system checks if the hash already exists in memory.  
- If it does, the user is notified that the article is already registered, without scanning the database line by line.  

### 6. Management Options
- **Modify metadata:** Update author(s) or year of an article.  
- **Delete articles:** Remove the record from the database and delete the associated file.  
- **List articles:** Sort and list by author (alphabetically) or title (alphabetically).  

### 7. Search Optimization
- Secondary hash-based indices are implemented for faster queries:  
  - **Index by author:** Key = author, value = list of articles.  
  - **Index by year:** Key = year, value = list of articles.  

----------

## Technoligies
- Pyhton 3.8 + 
- Tkinter (GUI)

----------

##  Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:Diego-gr-23/ScientificArticlesManager.git
   cd ScientificArticlesManager

----------

## Author 

- Luis Diego José Gómez Ramírez, 1510223 