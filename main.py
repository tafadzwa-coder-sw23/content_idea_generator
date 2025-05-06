# main_app.py
import customtkinter as ctk
import json
import datetime
import os
import random
import pyperclip  # For clipboard functionality
import tkinter  # Explicitly import tkinter for messagebox parent
from tkinter import messagebox # Use standard tkinter messagebox

# --- Constants ---
TEMPLATES_FILE = 'templates.json'
FAVORITES_FILE = 'favorites.json'
DEFAULT_NUMBER = 5 # Default number for listicles etc.

# --- Default Templates Structure (Used as fallback and for initial creation) ---
DEFAULT_TEMPLATES = {
  "howto": [
    "How to Get Started with {keyword} Step-by-Step",
    "A Beginner's Guide to Understanding {topic}",
    "How to Effectively Use {keyword} for Small Businesses"
  ],
  "listicle": [
    "Top {number} Tips for Mastering {keyword} in {year}",
    "{number} Common Mistakes to Avoid with {topic}",
    "The {number} Essential Tools for Anyone Using {keyword}"
  ],
  "questions": [
    "What Exactly Is {topic} and Why Does It Matter?",
    "Is {keyword} Still a Valuable Skill in {year}?",
    "How Can {topic} Improve [Specific Outcome e.g., Customer Engagement]?"
  ],
  "guides": [
    "The Ultimate {year} Guide to {topic}",
    "Everything You Need to Know About {keyword}"
  ]
}


# --- Main Application Class ---
class IdeaGeneratorApp(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("[DEBUG] Initializing IdeaGeneratorApp...") # DEBUG PRINT

        # --- Window Setup ---
        self.title("Content Idea Generator Pro")
        self.geometry("800x650")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # --- Load Data ---
        print("[DEBUG] Loading templates...") # DEBUG PRINT
        self.templates = self._load_json_data(TEMPLATES_FILE, default_data=DEFAULT_TEMPLATES)
        print("[DEBUG] Loading favorites...") # DEBUG PRINT
        self.favorites = self._load_json_data(FAVORITES_FILE, default_data=[])
        print("[DEBUG] Flattening templates...") # DEBUG PRINT
        self.all_template_strings = self._flatten_templates(self.templates)

        # --- DEBUG: Print loaded template info ---
        print("--- Templates Loaded ---")
        print(f"Loaded {len(self.all_template_strings)} template strings.")
        # print(self.all_template_strings) # Optional: Uncomment to see all loaded templates
        print("------------------------")
        # --- END DEBUG ---

        if not self.all_template_strings:
             print("Warning: No templates were loaded. Check templates.json and defaults.")
             messagebox.showwarning("Template Warning", "Could not load templates. Generator may not work.")

        # --- Main Layout Frames ---
        print("[DEBUG] Creating GUI Widgets...") # DEBUG PRINT
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)
        self.input_label = ctk.CTkLabel(self.input_frame, text="Keyword/Topic:")
        self.input_label.grid(row=0, column=0, padx=(10, 5), pady=10)
        self.keyword_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter primary keyword or topic...")
        self.keyword_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.keyword_entry.bind("<Return>", self._generate_ideas_event)

        # --- Button Frame ---
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.generate_button = ctk.CTkButton(self.button_frame, text="✨ Generate Ideas", command=self._generate_ideas_event)
        self.generate_button.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.clear_button = ctk.CTkButton(self.button_frame, text="🧹 Clear All", command=self._clear_fields, fg_color="grey")
        self.clear_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # --- Output Frame ---
        self.output_frame_label = ctk.CTkLabel(self, text="Generated Ideas:")
        self.output_frame_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.output_scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.output_scrollable_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.output_scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Favorites Frame ---
        self.favorites_frame_label = ctk.CTkLabel(self, text="⭐ Saved Favorites:")
        self.favorites_frame_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        self.favorites_scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.favorites_scrollable_frame.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.favorites_scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Status Bar ---
        self.status_bar = ctk.CTkLabel(self, text="Ready.", anchor="w")
        self.status_bar.grid(row=6, column=0, padx=20, pady=(5, 10), sticky="ew")

        # --- Initial Population ---
        print("[DEBUG] Displaying initial favorites...") # DEBUG PRINT
        self._display_favorites()
        print("[DEBUG] Initialization complete.") # DEBUG PRINT

    # --- Helper Methods ---
    def _load_json_data(self, filepath, default_data=None):
        """Safely loads data from a JSON file."""
        effective_default = default_data if default_data is not None else {}
        print(f"[DEBUG] Loading JSON from: {filepath}") # DEBUG PRINT
        if not os.path.exists(filepath):
            print(f"[DEBUG] File '{filepath}' not found. Using default data.") # DEBUG PRINT
            return json.loads(json.dumps(effective_default)) # Return copy
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"[DEBUG] Successfully loaded data from {filepath}.") # DEBUG PRINT
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"[ERROR] Error loading {filepath}: {e}. Using default data.") # DEBUG PRINT
            parent = self if hasattr(self, 'winfo_exists') and self.winfo_exists() else None
            messagebox.showerror("File Load Error", f"Error loading {os.path.basename(filepath)}:\n{e}\nUsing default data.", parent=parent)
            return json.loads(json.dumps(effective_default)) # Return copy

    def _save_json_data(self, filepath, data):
        """Safely saves data to a JSON file."""
        print(f"[DEBUG] Saving data to: {filepath}") # DEBUG PRINT
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[DEBUG] Successfully saved data to {filepath}.") # DEBUG PRINT
            return True
        except IOError as e:
            print(f"[ERROR] Error saving {filepath}: {e}") # DEBUG PRINT
            messagebox.showerror("File Save Error", f"Error saving {os.path.basename(filepath)}:\n{e}", parent=self)
            return False

    def _flatten_templates(self, template_data):
        """Converts categorized templates into a single list."""
        print("[DEBUG] Flattening templates...") # DEBUG PRINT
        flat_list = []
        if isinstance(template_data, dict):
            for category, category_list in template_data.items():
                if isinstance(category_list, list):
                    print(f"[DEBUG] Adding {len(category_list)} templates from category '{category}'") # DEBUG PRINT
                    flat_list.extend(category_list)
                else:
                    print(f"[WARN] Expected list for template category '{category}', got {type(category_list)}") # DEBUG PRINT
        elif isinstance(template_data, list):
             print("[DEBUG] Template data is already a list.") # DEBUG PRINT
             flat_list = template_data
        else:
             print(f"[WARN] Template data is not a dict or list, type is {type(template_data)}") # DEBUG PRINT
        print(f"[DEBUG] Total flattened templates: {len(flat_list)}") # DEBUG PRINT
        return flat_list

    def _update_status(self, message):
        """Updates the status bar text."""
        # Check if status_bar exists and is valid before configuring
        if hasattr(self, 'status_bar') and isinstance(self.status_bar, ctk.CTkLabel) and self.status_bar.winfo_exists():
             self.status_bar.configure(text=message)
             self.update_idletasks() # Force UI update
        else:
             print(f"[WARN] Status bar not ready. Message: {message}") # DEBUG PRINT

    # --- Core Logic ---
    def _perform_generation(self, keyword):
        """Generates ideas using loaded templates."""
        print(f"[DEBUG] Performing generation for keyword: '{keyword}'") # DEBUG PRINT
        if not self.all_template_strings:
            print("[ERROR] No templates available for generation.") # DEBUG PRINT
            messagebox.showerror("Template Error", "No templates available. Please check templates.json or defaults.", parent=self)
            return []

        generated = []
        current_year = datetime.datetime.now().year
        idea_set = set()

        print(f"[DEBUG] Processing {len(self.all_template_strings)} templates...") # DEBUG PRINT
        for i, template in enumerate(self.all_template_strings):
            # print(f"[DEBUG]  Template {i+1}: {template}") # Optional: Very verbose
            try:
                format_dict = {
                    "keyword": keyword, "topic": keyword, "year": current_year,
                    "number": DEFAULT_NUMBER, "competitor_placeholder": "[Competitor]",
                    "benefit_placeholder": "[Benefit]"
                }
                idea = template
                placeholders_found = 0
                for key, value in format_dict.items():
                    placeholder = "{" + key + "}"
                    if placeholder in idea:
                         idea = idea.replace(placeholder, str(value))
                         placeholders_found += 1
                # Only add if at least one placeholder was replaced (or be less strict?)
                # if placeholders_found > 0:
                idea_set.add(idea)
                # else:
                #     print(f"[DEBUG]  Skipping template (no placeholders found/replaced): {template}")

            except Exception as e:
                print(f"[ERROR] Error processing template '{template}': {e}") # DEBUG PRINT

        generated = list(idea_set)
        random.shuffle(generated)
        print(f"[DEBUG] Generated {len(generated)} unique ideas.") # DEBUG PRINT
        return generated

    # --- Event Handlers ---
    def _generate_ideas_event(self, event=None):
        print("\n--- Generate Event Triggered ---") # DEBUG PRINT
        keyword = self.keyword_entry.get().strip()
        print(f"Keyword entered: '{keyword}'") # DEBUG PRINT
        if not keyword:
            messagebox.showwarning("Input Required", "Please enter a keyword or topic first.", parent=self)
            return

        self._update_status("Generating ideas...")
        ideas = self._perform_generation(keyword)
        print(f"Ideas generated internally (list): {ideas}") # DEBUG PRINT

        # Clear previous output widgets first
        print("[DEBUG] Clearing previous output widgets...") # DEBUG PRINT
        for widget in self.output_scrollable_frame.winfo_children():
            widget.destroy()
        print("[DEBUG] Previous output widgets cleared.") # DEBUG PRINT

        if ideas:
            print(f"[DEBUG] Attempting to add {len(ideas)} idea widgets...") # DEBUG PRINT
            for i, idea_text in enumerate(ideas):
                # print(f"[DEBUG] Adding widget {i+1}...") # Optional: Verbose
                self._add_idea_widget(self.output_scrollable_frame, idea_text)
            self._update_status(f"Generated {len(ideas)} ideas.")
            print(f"[DEBUG] Finished adding {len(ideas)} widgets.") # DEBUG PRINT
        else:
            self._update_status("No ideas generated.")
            print("[DEBUG] No ideas generated or returned list was empty.") # DEBUG PRINT
            no_ideas_label = ctk.CTkLabel(self.output_scrollable_frame, text="No ideas generated. Check templates or input.")
            no_ideas_label.pack(pady=10)

    def _add_idea_widget(self, parent_frame, idea_text):
        # DEBUG PRINT inside the function
        print(f"  [DEBUG] Adding widget for idea: '{idea_text[:50]}...'")
        """Creates a frame for a single generated idea with buttons."""
        try: # Add try-except around widget creation for safety
            idea_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            idea_frame.pack(fill="x", pady=2, padx=5)
            idea_frame.grid_columnconfigure(0, weight=1)

            idea_label = ctk.CTkLabel(idea_frame, text=idea_text, wraplength=550, justify="left", anchor="w")
            idea_label.grid(row=0, column=0, padx=(5, 10), pady=2, sticky="ew")

            button_frame = ctk.CTkFrame(idea_frame, fg_color="transparent")
            button_frame.grid(row=0, column=1, padx=(0, 5), pady=2, sticky="e")

            fav_button = ctk.CTkButton(
                button_frame, text="⭐", width=30,
                command=lambda t=idea_text: self._add_to_favorites(t)
            )
            fav_button.pack(side=tkinter.LEFT, padx=(0, 5))

            copy_button = ctk.CTkButton(
                button_frame, text="📋", width=30,
                command=lambda t=idea_text: self._copy_to_clipboard(t)
            )
            copy_button.pack(side=tkinter.LEFT)
        except Exception as e:
            print(f"[ERROR] Failed to create widget for idea '{idea_text[:50]}...': {e}") # DEBUG PRINT

    def _add_favorite_widget(self, parent_frame, idea_text):
        """Creates a frame for a single favorite idea."""
        print(f"  [DEBUG] Adding favorite widget for: '{idea_text[:50]}...'") # DEBUG PRINT
        try:
            fav_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            fav_frame.pack(fill="x", pady=2, padx=5)
            fav_frame.grid_columnconfigure(0, weight=1)

            fav_label = ctk.CTkLabel(fav_frame, text=idea_text, wraplength=550, justify="left", anchor="w")
            fav_label.grid(row=0, column=0, padx=(5, 10), pady=2, sticky="ew")

            remove_button = ctk.CTkButton(
                fav_frame, text="❌", width=30, fg_color="grey",
                command=lambda t=idea_text: self._remove_from_favorites(t)
            )
            remove_button.grid(row=0, column=1, padx=(0, 5), pady=2, sticky="e")
        except Exception as e:
             print(f"[ERROR] Failed to create favorite widget for idea '{idea_text[:50]}...': {e}") # DEBUG PRINT


    def _add_to_favorites(self, idea_text):
        """Adds an idea to the favorites list and saves."""
        print(f"[DEBUG] Attempting to add to favorites: '{idea_text[:50]}...'") # DEBUG PRINT
        if idea_text not in self.favorites:
            self.favorites.append(idea_text)
            if self._save_json_data(FAVORITES_FILE, self.favorites):
                self._update_status(f"'{idea_text[:30]}...' added to favorites.")
                self._display_favorites()
            else:
                self._update_status("Error saving favorites.")
                self.favorites.remove(idea_text)
        else:
            self._update_status("Already in favorites.")

    def _remove_from_favorites(self, idea_text):
        """Removes an idea from favorites and saves."""
        print(f"[DEBUG] Attempting to remove from favorites: '{idea_text[:50]}...'") # DEBUG PRINT
        if idea_text in self.favorites:
            try:
                self.favorites.remove(idea_text)
                if self._save_json_data(FAVORITES_FILE, self.favorites):
                    self._update_status(f"Removed '{idea_text[:30]}...' from favorites.")
                    self._display_favorites()
                else:
                    self._update_status("Error saving favorites after removal.")
                    self.favorites.append(idea_text)
            except ValueError:
                 self._update_status("Item not found in favorites list (internal state error).")
        else:
             self._update_status("Item not found in favorites.")

    def _copy_to_clipboard(self, text):
        """Copies the given text to the system clipboard."""
        print(f"[DEBUG] Attempting to copy: '{text[:50]}...'") # DEBUG PRINT
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            self._update_status(f"Copied: '{text[:30]}...'")
            print("[DEBUG] Copy successful (using tkinter).") # DEBUG PRINT
        except Exception as e:
            print(f"[ERROR] Failed to copy using tkinter clipboard: {e}") # DEBUG PRINT
            # Optional: Try pyperclip as fallback
            try:
                pyperclip.copy(text)
                self._update_status(f"Copied: '{text[:30]}...'")
                print("[DEBUG] Copy successful (using pyperclip fallback).") # DEBUG PRINT
            except Exception as pe:
                 print(f"[ERROR] Failed to copy using pyperclip: {pe}") # DEBUG PRINT
                 self._update_status("Error copying to clipboard.")
                 messagebox.showerror("Clipboard Error", f"Could not copy text to clipboard.\nTkinter error: {e}\nPyperclip error: {pe}", parent=self)


    def _clear_fields(self):
        """Clears input, output, and status."""
        print("[DEBUG] Clearing fields...") # DEBUG PRINT
        self.keyword_entry.delete(0, tkinter.END)
        for widget in self.output_scrollable_frame.winfo_children():
            widget.destroy()
        self._update_status("Ready.")
        print("[DEBUG] Fields cleared.") # DEBUG PRINT

    def _display_favorites(self):
        """Clears and repopulates the favorites list display."""
        print("[DEBUG] Displaying favorites...") # DEBUG PRINT
        # Clear previous favorite widgets first
        for widget in self.favorites_scrollable_frame.winfo_children():
            widget.destroy()

        if self.favorites:
            print(f"[DEBUG] Found {len(self.favorites)} favorites to display.") # DEBUG PRINT
            # Display in reverse order so newest appear at top
            for i, fav_text in enumerate(reversed(self.favorites)):
                # print(f"[DEBUG] Adding favorite widget {i+1}...") # Optional: Verbose
                self._add_favorite_widget(self.favorites_scrollable_frame, fav_text)
        else:
            print("[DEBUG] No favorites found to display.") # DEBUG PRINT
            no_favs_label = ctk.CTkLabel(self.favorites_scrollable_frame, text="No favorites saved yet.")
            no_favs_label.pack(pady=10)
        print("[DEBUG] Finished displaying favorites.") # DEBUG PRINT


# --- Run the Application ---
if __name__ == "__main__":
    print("[DEBUG] Starting application setup...") # DEBUG PRINT
    # Ensure necessary files exist or are created with default content
    if not os.path.exists(TEMPLATES_FILE):
         print(f"'{TEMPLATES_FILE}' not found. Creating default file...")
         try:
             with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
                 json.dump(DEFAULT_TEMPLATES, f, indent=2, ensure_ascii=False)
             print(f"Default '{TEMPLATES_FILE}' created successfully.")
         except IOError as e:
             print(f"ERROR: Could not create default template file: {e}")

    if not os.path.exists(FAVORITES_FILE):
        print(f"'{FAVORITES_FILE}' not found. Creating empty file...")
        try:
            with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print(f"Empty '{FAVORITES_FILE}' created successfully.")
        except IOError as e:
            print(f"ERROR: Could not create default favorites file: {e}")

    print("[DEBUG] Creating App instance...") # DEBUG PRINT
    app = IdeaGeneratorApp()
    print("[DEBUG] Starting main loop...") # DEBUG PRINT
    app.mainloop()
    print("[DEBUG] Main loop finished.") # DEBUG PRINT