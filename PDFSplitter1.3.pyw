# Import the modules.
import PyPDF2
import tkinter as tk
from tkinter import filedialog
import os
from PIL import ImageTk, Image
from tkinter import ttk

def split_pdf(pdf_file, start_page, pages_per_file):
  """Splits a PDF file into several different PDFs based on the number of pages per file.

  Args:
    pdf_file: The path to the PDF file to split.
    start_page: The page number to start splitting from.
    pages_per_file: The number of pages to include in each split file.

  Returns:
    A list of the paths to the split PDF files.
  """

  # Open the PDF file.
  pdf_reader = PyPDF2.PdfReader(pdf_file)

  # Get the number of pages in the PDF file.
  num_pages = len(pdf_reader.pages)

  # Create a list to store the paths to the split PDF files.
  split_files = []

  # Get the destination folder from the entry widget.
  dest_folder = dest_entry.get()

  # Check if the destination folder exists and create it if not.
  if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

  # Iterate over the pages in the PDF file.
  for i in range(start_page, num_pages, pages_per_file):
    # Create a new PDF writer.
    pdf_writer = PyPDF2.PdfWriter()

    # Add the current page to the PDF writer.
    for page_num in range(i, min(i + pages_per_file, num_pages)):
      pdf_writer.add_page(pdf_reader.pages[page_num])

    # Write the PDF writer to a new file in the destination folder.
    split_file_name = os.path.join(dest_folder, f"split-{i}.pdf")
    with open(split_file_name, "wb") as f:
      pdf_writer.write(f)

    # Add the path to the split file to the list of split files.
    split_files.append(split_file_name)

  # Return the list of split files.
  return split_files

def select_pdf():
  """Selects a PDF file using a file dialog and updates the entry widget."""

  # Get the path to the PDF file using a file dialog.
  pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

  # Update the entry widget with the path to the PDF file.
  pdf_entry.delete(0, tk.END)
  pdf_entry.insert(0, pdf_file_path)

def run_split():
  """Runs the split_pdf function and displays the output in a text widget."""

  # Get the input values from the entry widgets.
  pdf_file_path = pdf_entry.get()
  start_page = int(start_entry.get())
  pages_per_file = int(pages_entry.get())

  # Clear the text widget.
  output_text.delete(1.0, tk.END)

  # Try to run the split_pdf function and display the output in the text widget.
  try:
    split_files = split_pdf(pdf_file_path, start_page, pages_per_file)
    for split_file in split_files:
      output_text.insert(tk.END, f"{split_file}\n")
    output_text.insert(tk.END, f"Saved {len(split_files)} files in {dest_folder}\n")
  except Exception as e:
    output_text.insert(tk.END, f"Error: {e}")

def reset_app():
    """Resets the app by clearing all inputs, outputs, and variables."""
    pdf_entry.delete(0, tk.END)
    start_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)
    dest_entry.delete(0, tk.END)
    output_text.delete(1.0, tk.END)
    split_files.clear()

# Create a root window.
root = tk.Tk()
root.title("PDF Splitter")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
offset_x = int((screen_width - window_width) / 2)
offset_y = int((screen_height - window_height) / 2)
root.geometry(f"+{offset_x}+{offset_y}")

icon = ImageTk.PhotoImage(Image.open("icon.ico"))
logo = ImageTk.PhotoImage(Image.open("logo.png"))

root.iconphoto(False, icon)

# logo_label = tk.Label(root, image=logo)
# logo_label.place(x=10, y=10)

# logo_label.place(x=10, y=10, width=100, height=100)


style = ttk.Style()
style.configure("MyButton.TButton", font=("Arial", 10), foreground="black", background="white", borderwidth=2, relief=tk.RAISED)


# Create a frame for the input widgets.
input_frame = tk.LabelFrame(root, text="Input", font=("Arial", 12, "bold"), borderwidth=2, relief=tk.GROOVE)
input_frame.pack(padx=10, pady=10)

# Create a label and an entry for the PDF file path.
pdf_label = tk.Label(input_frame, text="PDF File:", font=("Arial", 10))
pdf_label.grid(row=0, column=0, sticky=tk.E)
pdf_entry = tk.Entry(input_frame)
pdf_entry.grid(row=0, column=1)

# Create a button to select a PDF file using a file dialog.
select_button = ttk.Button(input_frame, text="Select", command=select_pdf, style="MyButton.TButton")
select_button.grid(row=0, column=2)

# Create a label and an entry for the start page number.
start_label = tk.Label(input_frame, text="Start Page:", font=("Arial", 10))
start_label.grid(row=1, column=0, sticky=tk.E)
start_entry = tk.Entry(input_frame)
start_entry.grid(row=1, column=1)

# Create a label and an entry for the number of pages per file.
pages_label = tk.Label(input_frame, text="Pages per File:", font=("Arial", 10))
pages_label.grid(row=2, column=0, sticky=tk.E)
pages_entry = tk.Entry(input_frame)
pages_entry.grid(row=2, column=1)

# Create a label and an entry for the destination folder.
dest_label = tk.Label(input_frame, text="Destination Folder:", font=("Arial", 10))
dest_label.grid(row=3, column=0, sticky=tk.E)
dest_entry = tk.Entry(input_frame)
dest_entry.grid(row=3, column=1)

# Create a button to select a destination folder using a file dialog.
dest_button = ttk.Button(input_frame, text="Browse", command=lambda: dest_entry.insert(0, filedialog.askdirectory()), style="MyButton.TButton")
dest_button.grid(row=3, column=2)

# Create a button to run the split_pdf function and display the output in a text widget.
run_button = ttk.Button(input_frame, text="Run", command=run_split, style="MyButton.TButton")
run_button.grid(row=4, column=1)

# Create a frame for the output widget.
output_frame = tk.LabelFrame(root, text="Output", font=("Arial", 12, "bold"), borderwidth=2, relief=tk.GROOVE)
output_frame.pack(padx=10, pady=10)

# Create a label and a text widget for the output.
output_label = tk.Label(output_frame, text="Output:", font=("Arial", 10))
output_label.pack()
output_text = tk.Text(output_frame, width=40, height=10)
output_text.pack()

# Create a button to reset the app.
reset_button = ttk.Button(input_frame, text="Reset", command=reset_app, style="MyButton.TButton")
reset_button.grid(row=4, column=2)

# Initialize a list to store split file paths.
split_files = []

root.resizable(False, False)

# Start the main loop.
root.mainloop()