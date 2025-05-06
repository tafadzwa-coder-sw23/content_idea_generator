
# Content Idea Generator ✨

A desktop application built with Python and CustomTkinter to help content creators, marketers, and writers brainstorm engaging content ideas and titles based on keywords and customizable templates.

## Screenshot

*(Ensure your `Screenshot (169).png` file is in your GitHub repository. Adjust the path if you place it in a subfolder like `assets/`)*
![Content Idea Generator Pro Screenshot](Screenshot%20(169).png)

## Features

* **Keyword-Based Idea Generation:** Enter a keyword or topic to get a list of relevant content ideas.
* **Customizable Templates:** Uses an external `templates.json` file, allowing users to add, edit, and categorize their own title structures and content angles. The application creates a default `templates.json` with examples if one is not found.
* **Modern GUI:** Built with `CustomTkinter` for a clean, modern look and feel (supports system light/dark modes).
* **Save Favorites:** Mark generated ideas as favorites, which are saved locally in `favorites.json`.
* **Copy to Clipboard:** Easily copy generated ideas or favorite ideas to your clipboard.
* **Clear Inputs/Outputs:** Quickly clear the keyword field and generated ideas list.
* **Status Bar Feedback:** Provides real-time feedback on actions (e.g., "Generating ideas...", "Idea copied!").
* **Cross-Platform (Potential):** Built with Python and Tkinter (via CustomTkinter), which is generally cross-platform (Windows, macOS, Linux).

## Technologies Used

* **Python 3:** Core programming language.
* **CustomTkinter:** For building the modern graphical user interface.
* **Tkinter:** Underlying GUI toolkit (used for `messagebox` and core elements).
* **JSON:** For storing and managing templates and saved favorites.
* **Pyperclip:** For cross-platform clipboard functionality (used as a fallback).

## Setup and Installation

1.  **Clone or Download the Repository:**
    *(If your project is on GitHub, replace the URL below with your repository's URL)*
    ```bash
    git clone [https://github.com/tafadzwa-coder-sw23/content_idea_generator.git](https://github.com/tafadzwa-coder-sw23/content_idea_generator.git)
    cd content_idea_generator
    ```
    If you downloaded the files manually, ensure `main_app.py` is in your project folder.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    Activate it:
    * On Windows:
        ```bash
        venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    Create a `requirements.txt` file in your project root with the following content:
    ```txt
    customtkinter
    pyperclip
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```
    * **Linux Note:** If `tkinter` is not installed with your Python distribution (which `customtkinter` relies on), you might need to install it system-wide. For example, on Debian/Ubuntu:
        ```bash
        sudo apt-get update
        sudo apt-get install python3-tk
        ```

## How to Run

1.  Ensure all dependencies are installed (see Setup).
2.  Navigate to the project directory in your terminal (if you're not already there).
3.  Run the application:
    ```bash
    python main_app.py
    ```
    * On the first run, if `templates.json` or `favorites.json` are missing, the application will create default versions for you.

## File Structure
