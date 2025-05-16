from IPython.display import display, clear_output
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import ast #convert a string that looks like a list or dict into an actual Python object. ast stands for Abstract Syntax Tree.

#load dataset
titles_df = pd.read_csv('/Users/viviancenguyen/Python Project/Updated_netflix_movie_by_mood/titles.csv')
print(titles_df.head())

titles_df['genres'] = titles_df['genres'].apply(ast.literal_eval)

#mapping genres to mood
genres_to_moods = {
    "comedy": "happy",
    "romance": "romantic",
    "drama": "sad",
    "thriller": "thrilling",
    "action": "exciting",
    "horror": "scary",
    "biography": "inspirational",
    "documentary": "inspirational",
    "animation": "happy",
    "fantasy": "exciting",
    "crime": "thrilling",
    "war": "sad",
    "adventure": "exciting"
}

#function to get genres by mood
def get_moods(genres):
    moods = {genres_to_moods[g.lower()] for g in genres if g.lower() in genres_to_moods}
    return list(moods) if moods else ['other']     
titles_df['moods'] = titles_df['genres'].apply(get_moods)

#recommendation function
def get_movies_by_mood_with_rating(mood, top=15):
    filtered = titles_df[titles_df['moods'].apply(lambda mood_list: mood in mood_list) & 
                         (titles_df['release_year'] >= 2008)]
    filtered = filtered[filtered['imdb_score'] >= 7.0]
    filtered = filtered.sort_values(by='imdb_score', ascending=False).reset_index(drop=True)
    return filtered[['title', 'genres', 'release_year', 'imdb_score', 'tmdb_score']].head(top)

#GUI setup
root = tk.Tk()
root.title('🎬 Movie Recommender')
root.geometry("750x680")
root.configure(bg="red")

#add logo 
logo_path = "/Users/viviancenguyen/Python Project/Updated_netflix_movie_by_mood/Netflix.png"
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((120, 75))
logo_photo = ImageTk.PhotoImage(logo_image)
#create a frame to hold logo
top_frame = tk.Frame(root, bg='red')
top_frame.pack(pady=15, anchor = "n") # Top-left corner is Northwest
# Logo on the left
logo_label = tk.Label(top_frame, image=logo_photo, bg="black")
logo_label.image = logo_photo  # Prevent garbage collection
logo_label.pack(side="left",pady=15)


#create mood dropdown
mood_var = tk.StringVar()
mood_options = sorted(set(m.capitalize() for m_list in titles_df['moods'] for m in m_list if m != 'other'))
mood_dropdown = ttk.Combobox(root, textvariable=mood_var, values=mood_options, state="readonly")
mood_dropdown.set("Select a mood")
mood_dropdown.pack(pady=15, anchor ='n')

# Output box
output_box = tk.Text(root, height=20, width=80, fg="black")
output_box.pack(pady=15)
output_box.tag_configure('title', font=("Arial", 13, "bold")) #tag_configure is used for only 1 tag at a time
output_box.tag_configure('genres', font=("Arial", 13))
output_box.tag_configure('release_year', font=("Arial", 13))
output_box.tag_configure('imdb_score', font=("Arial", 13, "italic"))

# Recommend Button
def on_button_click():
    output_box.delete("1.0", tk.END)
    selected_mood = mood_var.get()
    if not selected_mood or selected_mood == "Select a mood":
        output_box.insert(tk.END, "⚠️ Please select a mood from the dropdown.\n")
    else:
        results = get_movies_by_mood_with_rating(selected_mood.lower())
        if results.empty:
            output_box.insert(tk.END, "No high-rated movies found for this mood.\n")
        else:
            for _, row in results.iterrows():
                output_box.insert(
                    tk.END, f"{row['title']} ({row['release_year']}) - TMDB Score: {row['tmdb_score']}\n"
                )

recommend_button = tk.Button(
    root, 
    text="Recommend Movies", 
    command=on_button_click, 
    bg="black",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5)
recommend_button.pack(pady=15)

# Run the App
root.mainloop()