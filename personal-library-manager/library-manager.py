import streamlit as st
import json
import os

st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f3e8ff;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #6a5acd;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 16px;
    }
    .stButton>button:hover {
        background-color: #7b68ee;
    }
    </style>
""", unsafe_allow_html=True)

data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=2)

def add_book_ui(library):
    st.subheader("➕ Add a New Book")
    with st.form("add_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Publication Year")
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        submit = st.form_submit_button("Add Book")
        if submit:
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            library.append(new_book)
            save_library(library)
            st.success(f'Book "{title}" added successfully! ✅')

def remove_book_ui(library):
    st.subheader("🗑️ Remove a Book")
    titles = [book['title'] for book in library]
    title = st.selectbox("Select the book to remove", titles)
    if st.button("Remove Book"):
        library[:] = [book for book in library if book['title'] != title]
        save_library(library)
        st.success(f'Book "{title}" removed successfully! ❌')

def search_books_ui(library):
    st.subheader("🔍 Search Books")
    search_by = st.radio("Search by", ["title", "author"])
    search_term = st.text_input(f"Enter {search_by}")
    if search_term:
        results = [book for book in library if search_term.lower() in book[search_by].lower()]
        if results:
            for book in results:
                status = "Read" if book['read'] else "Unread"
                st.markdown(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - **{status}**")
        else:
            st.warning("No matching books found.")

def display_all_books_ui(library):
    st.subheader("📚 All Books in Library")
    if library:
        for book in library:
            status = "Read" if book['read'] else "Unread"
            st.markdown(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - **{status}**")
    else:
        st.info("No books in the library.")

def display_statistics_ui(library):
    st.subheader("📈 Statistics")
    total_books = len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"**Total Books:** {total_books}")
    st.write(f"**Books Read:** {read_books}")
    st.write(f"**Percentage Read:** {percentage_read:.2f}%")

def main():
    st.title("📖 Personal Library Manager")
    library = load_library()

    menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "All Books", "Statistics"])

    if menu == "Add Book":
        add_book_ui(library)
    elif menu == "Remove Book":
        remove_book_ui(library)
    elif menu == "Search Book":
        search_books_ui(library)
    elif menu == "All Books":
        display_all_books_ui(library)
    elif menu == "Statistics":
        display_statistics_ui(library)

if __name__ == "__main__":
    main()
