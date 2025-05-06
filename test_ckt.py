# main_app.py (v3 - Enhanced Diagnostics - Includes the correct line)
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
        print(f"[DEBUG] Initializing IdeaGeneratorApp...")
        print(f"[DEBUG] Current Working Directory: {os.getcwd()}") # Print CWD
        print(f"[DEBUG] Looking for '{TEMPLATES_FILE}' and '{FAVORITES_FILE}' here.")

        # --- Window Setup ---
        self.title("Content Idea Generator Pro (v3)")
        self.geometry("800x650")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # --- Load Data ---
        print("[DEBUG] Loading templates...")
        self.templates = self._load_json_data(TEMPLATES_FILE, default_data=DEFAULT_TEMPLATES)
        print("[DEBUG] Loading favorites...")
        self.favorites = self._load_json_data(FAVORITES_FILE, default_data=[])
        print("[DEBUG] Flattening templates...")
        self.all_template_strings = self._flatten_templates(self.templates)

        print("--- Templates Info ---")
        print(f"Loaded {len(self.all_template_strings)} template strings in total.")
        # print(self.all_template_strings) # Optional: For very detailed debugging
        print("----------------------")

        if not self.all_template_strings:
             print("[CRITICAL WARNING] No templates loaded from file or defaults! Generation will likely fail.")
             messagebox.showwarning("Template Warning", "Could not load any templates. Please ensure 'templates.json' exists and is valid, or check default templates in the script.")

        # --- Main Layout Frames ---
        print("[DEBUG] Creating GUI Widgets...")
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
        self.output_scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Output")
        self.output_scrollable_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.output_scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Favorites Frame ---
        self.favorites_frame_label = ctk.CTkLabel(self, text="⭐ Saved Favorites:")
        self.favorites_frame_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        self.favorites_scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Favorites")
        self.favorites_scrollable_frame.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.favorites_scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Status Bar ---
        self.status_bar = ctk.CTkLabel(self, text="Ready.", anchor="w")
        self.status_bar.grid(row=6, column=0, padx=20, pady=(5, 10), sticky="ew")

        # --- Initial Population ---
        print("[DEBUG] Displaying initial favorites...")
        self._display_favorites()
        print("[DEBUG] Initialization complete.")

    # --- Helper Methods ---
    def _load_json_data(self, filepath, default_data=None):
        effective_default = default_data if default_data is not None else {}
        absolute_path = os.path.abspath(filepath)
        print(f"[DEBUG] Attempting to load JSON from: {absolute_path}")
        if not os.path.exists(filepath):
            print(f"[WARN] File '{filepath}' (abs: {absolute_path}) not found. Using default data provided to function.")
            return json.loads(json.dumps(effective_default)) # Return copy of default
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Add a check to see if loaded data is empty and if so, use default
                if not data and default_data is not None:
                    print(f"[WARN] File '{filepath}' was empty. Using default data.")
                    return json.loads(json.dumps(effective_default))
                print(f"[DEBUG] Successfully loaded data from {filepath}.")
                return data
        except (json.JSONDecodeError, IOError, TypeError) as e:
            print(f"[ERROR] Error loading {filepath}: {e}. Using default data provided to function.")
            parent = self if hasattr(self, 'winfo_exists') and self.winfo_exists() else None
            messagebox.showerror("File Load Error", f"Error loading {os.path.basename(filepath)}:\n{e}\nPlease ensure it's valid JSON.\nUsing default data.", parent=parent)
            return json.loads(json.dumps(effective_default)) # Return copy of default
        except Exception as e:
             print(f"[ERROR] Unexpected error loading {filepath}: {e}. Using default data provided to function.")
             parent = self if hasattr(self, 'winfo_exists') and self.winfo_exists() else None
             messagebox.showerror("File Load Error", f"Unexpected error loading {os.path.basename(filepath)}:\n{e}\nUsing default data.", parent=parent)
             return json.loads(json.dumps(effective_default)) # Return copy of default

    def _save_json_data(self, filepath, data):
        absolute_path = os.path.abspath(filepath)
        print(f"[DEBUG] Attempting to save data to: {absolute_path}")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[DEBUG] Successfully saved data to {filepath}.")
            return True
        except (IOError, TypeError) as e:
            print(f"[ERROR] Error saving {filepath}: {e}")
            messagebox.showerror("File Save Error", f"Error saving {os.path.basename(filepath)}:\n{e}", parent=self)
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error saving {filepath}: {e}")
            messagebox.showerror("File Save Error", f"Unexpected error saving {os.path.basename(filepath)}:\n{e}", parent=self)
            return False

    def _flatten_templates(self, template_data):
        print("[DEBUG] Flattening templates...")
        flat_list = []
        if isinstance(template_data, dict):
             for category, category_list in template_data.items():
                 if isinstance(category_list, list):
                     print(f"[DEBUG] Adding {len(category_list)} templates from category '{category}'")
                     flat_list.extend(category_list)
                 else:
                     print(f"[WARN] Expected list for template category '{category}', got {type(category_list)}. Skipping.")
        elif isinstance(template_data, list):
              print("[DEBUG] Template data is a list. Using as is.")
              flat_list = template_data
        else:
              print(f"[ERROR] Template data is not a dict or list, type is {type(template_data)}. Cannot flatten.")
        print(f"[DEBUG] Total flattened templates: {len(flat_list)}")
        return flat_list

    def _update_status(self, message):
        if hasattr(self, 'status_bar') and isinstance(self.status_bar, ctk.CTkLabel) and self.status_bar.winfo_exists():
             try:
                 self.status_bar.configure(text=message)
                 self.update_idletasks()
             except Exception as e:
                 print(f"[ERROR] Failed to update status bar: {e}")
        else:
             print(f"[WARN] Status bar not ready or destroyed. Message: {message}")

    # --- Core Logic ---
    def _perform_generation(self, keyword):
        print(f"[DEBUG] Performing generation for keyword: '{keyword}'")
        if not self.all_template_strings:
            print("[ERROR] No templates available for generation in _perform_generation.")
            return []

        generated = []
        current_year = datetime.datetime.now().year
        idea_set = set()
        errors_encountered = 0

        print(f"[DEBUG] Processing {len(self.all_template_strings)} templates...")
        for i, template in enumerate(self.all_template_strings):
            try:
                if not isinstance(template, str):
                    print(f"[WARN] Template item {i+1} is not a string, skipping: {type(template)}")
                    errors_encountered += 1
                    continue

                format_dict = {
                    "keyword": keyword, "topic": keyword, "year": current_year,
                    "number": DEFAULT_NUMBER, "competitor_placeholder": "[Competitor]",
                    "benefit_placeholder": "[Benefit]"
                }
                idea = template
                for key, value in format_dict.items():
                    placeholder = "{" + key + "}"
                    idea = idea.replace(placeholder, str(value))
                idea_set.add(idea)
            except Exception as e:
                print(f"[ERROR] Error processing template #{i+1} '{str(template)[:50]}...': {e}")
                errors_encountered += 1

        generated = list(idea_set)
        random.shuffle(generated)
        print(f"[DEBUG] Generated {len(generated)} unique ideas with {errors_encountered} template errors.")
        return generated

    # --- Event Handlers ---
    def _generate_ideas_event(self, event=None):
        print("\n--- Generate Event Triggered ---")
        keyword = self.keyword_entry.get().strip()
        print(f"Keyword entered: '{keyword}'")
        if not keyword:
            messagebox.showwarning("Input Required", "Please enter a keyword or topic first.", parent=self)
            return

        self._update_status("Generating ideas...")
        ideas = []
        try:
            ideas = self._perform_generation(keyword)
            print(f"Ideas generated internally (list count: {len(ideas)}): {ideas[:5]}")
        except Exception as e:
            print(f"[ERROR] Unexpected error during _perform_generation: {e}")
            messagebox.showerror("Generation Error", f"An error occurred during idea generation:\n{e}", parent=self)
            self._update_status("Error during generation.")
            return

        print("[DEBUG] Clearing previous output widgets...")
        try:
            for widget in self.output_scrollable_frame.winfo_children(): # CORRECTED LINE
                widget.destroy()
            print("[DEBUG] Previous output widgets cleared.")
        except Exception as e:
             print(f"[ERROR] Failed to clear output widgets: {e}")
             self._update_status("Error clearing output.")

        if ideas:
            print(f"[DEBUG] Attempting to add {len(ideas)} idea widgets...")
            widgets_added = 0
            for i, idea_text in enumerate(ideas):
                try:
                    self._add_idea_widget(self.output_scrollable_frame, idea_text)
                    widgets_added += 1
                except Exception as e:
                     print(f"[ERROR] Failed adding widget for idea #{i+1} ('{str(idea_text)[:30]}...'): {e}")
            self._update_status(f"Generated {widgets_added}/{len(ideas)} ideas.")
            print(f"[DEBUG] Finished adding widgets (attempted {len(ideas)}, added {widgets_added}).")
        else:
            self._update_status("No ideas generated or list was empty.")
            print("[DEBUG] No ideas generated or returned list was empty.")
            try:
                no_ideas_label = ctk.CTkLabel(self.output_scrollable_frame, text="No ideas generated. Check templates or input.")
                no_ideas_label.pack(pady=10)
            except Exception as e:
                 print(f"[ERROR] Failed to add 'No ideas' label: {e}")

    def _add_idea_widget(self, parent_frame, idea_text):
        print(f"  [DEBUG] Adding widget for idea: '{str(idea_text)[:50]}...'")
        try:
            idea_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            idea_frame.pack(fill="x", pady=2, padx=5)
            idea_frame.grid_columnconfigure(0, weight=1)
            display_text = str(idea_text)
            idea_label = ctk.CTkLabel(idea_frame, text=display_text, wraplength=550, justify="left", anchor="w")
            idea_label.grid(row=0, column=0, padx=(5, 10), pady=2, sticky="ew")
            button_frame = ctk.CTkFrame(idea_frame, fg_color="transparent")
            button_frame.grid(row=0, column=1, padx=(0, 5), pady=2, sticky="e")
            fav_button = ctk.CTkButton(
                button_frame, text="⭐", width=30,
                command=lambda t=display_text: self._add_to_favorites(t)
            )
            fav_button.pack(side=tkinter.LEFT, padx=(0, 5))
            copy_button = ctk.CTkButton(
                button_frame, text="📋", width=30,
                command=lambda t=display_text: self._copy_to_clipboard(t)
            )
            copy_button.pack(side=tkinter.LEFT)
        except Exception as e:
            print(f"[ERROR] Failed to create widget for idea '{str(idea_text)[:50]}...': {e}")

    def _add_favorite_widget(self, parent_frame, idea_text):
        print(f"  [DEBUG] Adding favorite widget for: '{str(idea_text)[:50]}...'")
        try:
            fav_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            fav_frame.pack(fill="x", pady=2, padx=5)
            fav_frame.grid_columnconfigure(0, weight=1)
            display_text = str(idea_text)
            fav_label = ctk.CTkLabel(fav_frame, text=display_text, wraplength=550, justify="left", anchor="w")
            fav_label.grid(row=0, column=0, padx=(5, 10), pady=2, sticky="ew")
            remove_button = ctk.CTkButton(
                fav_frame, text="❌", width=30, fg_color="grey",
                command=lambda t=display_text: self._remove_from_favorites(t)
            )
            remove_button.grid(row=0, column=1, padx=(0, 5), pady=2, sticky="e")
        except Exception as e:
             print(f"[ERROR] Failed to create favorite widget for idea '{str(idea_text)[:50]}...': {e}")

    def _add_to_favorites(self, idea_text):
        print(f"[DEBUG] Attempting to add to favorites: '{str(idea_text)[:50]}...'")
        idea_str = str(idea_text)
        self.favorites = [str(fav) for fav in self.favorites if isinstance(fav, str) and fav is not None]
        if idea_str not in self.favorites:
            self.favorites.append(idea_str)
            if self._save_json_data(FAVORITES_FILE, self.favorites):
                self._update_status(f"'{idea_str[:30]}...' added to favorites.")
                self._display_favorites()
            else:
                self._update_status("Error saving favorites.")
                try: self.favorites.remove(idea_str)
                except ValueError: pass
        else:
            self._update_status("Already in favorites.")

    def _remove_from_favorites(self, idea_text):
        print(f"[DEBUG] Attempting to remove from favorites: '{str(idea_text)[:50]}...'")
        idea_str = str(idea_text)
        self.favorites = [str(fav) for fav in self.favorites if isinstance(fav, str) and fav is not None]
        if idea_str in self.favorites:
            original_favorites = list(self.favorites)
            try:
                self.favorites.remove(idea_str)
                if self._save_json_data(FAVORITES_FILE, self.favorites):
                    self._update_status(f"Removed '{idea_str[:30]}...' from favorites.")
                    self._display_favorites()
                else:
                    self._update_status("Error saving favorites after removal.")
                    self.favorites = original_favorites
            except ValueError:
                 print("[ERROR] Item disappeared from favorites list before removal.")
                 self._update_status("Error removing favorite (not found).")
                 self.favorites = original_favorites
        else:
             self._update_status("Item not found in favorites.")

    def _copy_to_clipboard(self, text):
        print(f"[DEBUG] Attempting to copy: '{str(text)[:50]}...'")
        text_str = str(text)
        try:
            self.clipboard_clear()
            self.clipboard_append(text_str)
            self.update()
            self._update_status(f"Copied: '{text_str[:30]}...'")
            print("[DEBUG] Copy successful (using tkinter).")
        except Exception as e_tk:
            print(f"[WARN] Failed to copy using tkinter clipboard: {e_tk}")
            try:
                pyperclip.copy(text_str)
                self._update_status(f"Copied: '{text_str[:30]}...'")
                print("[DEBUG] Copy successful (using pyperclip fallback).")
            except Exception as e_pc:
                 print(f"[ERROR] Failed to copy using pyperclip: {e_pc}")
                 self._update_status("Error copying to clipboard.")
                 messagebox.showerror("Clipboard Error", f"Could not copy text to clipboard.\nTkinter error: {e_tk}\nPyperclip error: {e_pc}", parent=self)

    def _clear_fields(self):
        print("[DEBUG] Clearing fields...")
        try:
            self.keyword_entry.delete(0, tkinter.END)
            for widget in self.output_scrollable_frame.winfo_children(): # CORRECTED LINE
                widget.destroy()
            self._update_status("Ready.")
            print("[DEBUG] Fields cleared.")
        except Exception as e:
            print(f"[ERROR] Error during clear fields: {e}")
            self._update_status("Error clearing fields.")

    def _display_favorites(self):
        print("[DEBUG] Displaying favorites...")
        try:
            for widget in self.favorites_scrollable_frame.winfo_children():
                widget.destroy()
            if self.favorites:
                print(f"[DEBUG] Found {len(self.favorites)} favorites to display.")
                valid_favorites = [str(fav) for fav in self.favorites if fav is not None]
                for i, fav_text in enumerate(reversed(valid_favorites)):
                    self._add_favorite_widget(self.favorites_scrollable_frame, fav_text)
            else:
                print("[DEBUG] No favorites found to display.")
                no_favs_label = ctk.CTkLabel(self.favorites_scrollable_frame, text="No favorites saved yet.")
                no_favs_label.pack(pady=10)
            print("[DEBUG] Finished displaying favorites.")
        except Exception as e:
            print(f"[ERROR] Failed to display favorites: {e}")
            self._update_status("Error displaying favorites.")


# --- Run the Application ---
if __name__ == "__main__":
    print("[DEBUG] Starting application setup...")
    try:
        if not os.path.exists(TEMPLATES_FILE):
             print(f"'{TEMPLATES_FILE}' not found. Creating default file with comprehensive templates...")
             with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
                 json.dump(DEFAULT_TEMPLATES, f, indent=2, ensure_ascii=False)
             print(f"Default '{TEMPLATES_FILE}' created successfully with multiple example templates.")

        if not os.path.exists(FAVORITES_FILE):
            print(f"'{FAVORITES_FILE}' not found. Creating empty file...")
            with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print(f"Empty '{FAVORITES_FILE}' created successfully.")
    except IOError as e:
         print(f"[FATAL ERROR] Could not create necessary data files ({TEMPLATES_FILE} or {FAVORITES_FILE}): {e}")
         messagebox.showerror("Startup Error", f"Could not create necessary data files:\n{e}\nApplication may not work correctly.")

    print("[DEBUG] Creating App instance...")
    app = None
    try:
        app = IdeaGeneratorApp()
        print("[DEBUG] Starting main loop...")
        app.mainloop()
    except Exception as e:
         print(f"[FATAL ERROR] An error occurred during app execution: {e}")
         import traceback
         traceback.print_exc()
         try:
             root_err = tkinter.Tk()
             root_err.withdraw()
             messagebox.showerror("Application Error", f"A fatal error occurred:\n{e}\nSee console for detailed traceback.")
             root_err.destroy()
         except Exception as me:
             print(f"[ERROR] Could not show final error messagebox: {me}")
    finally:
        print("[DEBUG] Application finished or crashed.")