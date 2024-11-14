import os, re
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox


### --- Underlying Functions --- ###

def is_float(num):
    return '.' in str(num)

def sort_files(listbox):
    files = list(listbox.get(0, tk.END))
    
    # Custom sort key to handle both numeric and alphabetic sorting
    def custom_sort_key(file_name):
        match = re.match(r"(\d+)", file_name)
        if match:
            return (0, int(match.group(1)))  # Numeric part
        else:
            return (1, file_name.lower())  # Alphabetic part
    
    files.sort(key=custom_sort_key)
    listbox.delete(0, tk.END)
    for file in files:
        listbox.insert(tk.END, file)

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)
        update_file_lists()

def update_file_lists():
    directory = directory_entry.get()
    if os.path.isdir(directory):
        files = [item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))]
        file_listbox.delete(0, tk.END)
        for file in files:
            file_listbox.insert(tk.END, file)
        update_selected_files()

def update_selected_files():
    selected_files = filtered_listbox.get(0, tk.END)
    filtered_listbox.delete(0, tk.END)
    for file in selected_files:
        filtered_listbox.insert(tk.END, file)


### --- Main Feature Functions --- ###

def add_numeric_pattern(directory, files, start_num, step, position):
    current_num = start_num
    for file_name in files:
        name, ext = os.path.splitext(file_name)
        
        # Check if both start_num and step are integers
        if not is_float(start_num) and not is_float(step):
            formatted_num = f"{int(current_num)}"  # Format as integer
        else:
            formatted_num = f"{current_num:.1f}"  # Format as float with one decimal place
        
        if position == 0:
            new_file_name = f"{formatted_num}. " + file_name
        elif position == 21:
            new_file_name = name + f" {formatted_num}" + ext
        else:
            new_file_name = name[:position] + f"{formatted_num}" + name[position:] + ext
        
        os.rename(os.path.join(directory, file_name), os.path.join(directory, new_file_name))
        current_num += step

def add_characters(text, directory, files, position):
    for file_name in files:
        name, ext = os.path.splitext(file_name)
        if position == 0:
            new_file_name = text + file_name
        elif position == 21:
            new_file_name = name + text + ext
        else:
            pos = position - 1
            new_file_name = name[:pos] + text + name[pos:] + ext
        os.rename(os.path.join(directory, file_name), os.path.join(directory, new_file_name))

def remove_chars(num_characters, directory, files, position):
    for file_name in files:
        name, ext = os.path.splitext(file_name)
        if position == 0:
            new_file_name = file_name[num_characters:]
        elif position == 21:
            new_file_name = name[:-num_characters] + ext
        else:
            pos = position - 1
            new_file_name = name[:pos] + name[pos + num_characters:] + ext
        os.rename(os.path.join(directory, file_name), os.path.join(directory, new_file_name))

### --- List Box Features --- ###

def add_file():
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file and selected_file not in filtered_listbox.get(0, tk.END):
        filtered_listbox.insert(tk.END, selected_file)

def remove_file():
    selected_file_index = filtered_listbox.curselection()
    if selected_file_index:
        filtered_listbox.delete(selected_file_index)

def add_all_files():
    files = file_listbox.get(0, tk.END)
    for file in files:
        if file not in filtered_listbox.get(0, tk.END):
            filtered_listbox.insert(tk.END, file)

def remove_all_files():
    filtered_listbox.delete(0, tk.END)

def move_up():
    selected_file_index = filtered_listbox.curselection()
    if selected_file_index:
        index = selected_file_index[0]
        if index > 0:
            file = filtered_listbox.get(index)
            filtered_listbox.delete(index)
            filtered_listbox.insert(index - 1, file)
            filtered_listbox.select_set(index - 1)

def move_down():
    selected_file_index = filtered_listbox.curselection()
    if selected_file_index:
        index = selected_file_index[0]
        if index < filtered_listbox.size() - 1:
            file = filtered_listbox.get(index)
            filtered_listbox.delete(index)
            filtered_listbox.insert(index + 1, file)
            filtered_listbox.select_set(index + 1)


### --- Execution Process --- ###

def execute_function():
    directory = directory_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory")
        return

    files = filtered_listbox.get(0, tk.END)
    if not files:
        messagebox.showerror("Error", "No files selected")
        return

    function = function_var.get()
    position = location_scale.get()
    
    if function == "Add Numeric Pattern":
        try:
            if is_float(start_num_entry.get()) or is_float(step_entry.get()):
                start_num = float(start_num_entry.get())
                step = float(step_entry.get())
            else:
                start_num = int(start_num_entry.get())
                step = int(step_entry.get())
            add_numeric_pattern(directory, files, start_num, step, position)
        except ValueError:
            messagebox.showerror("Error", "Starting Number and Step must be numeric values")
    elif function == "Add Characters":
        text = string_entry.get()
        add_characters(text, directory, files, position)
    elif function == "Remove Characters":
        num_characters = num_chars_scale.get()
        remove_chars(num_characters, directory, files, position)

    update_file_lists()
    remove_all_files()
    messagebox.showinfo("Success", "Operation completed")


### --- App Interface --- ####

app = tk.Tk()
app.title("Bulk File Renamer")

xpadding = 3
ypadding = 3

# Directory selection
tk.Label(app, text="Directory:").grid(row=0, column=0, padx=xpadding, pady=ypadding, sticky='e')
directory_entry = tk.Entry(app, width=50)
directory_entry.grid(row=0, column=1, padx=xpadding, pady=ypadding)
tk.Button(app, text="Browse", command=select_directory).grid(row=0, column=2, padx=xpadding, pady=ypadding)

# Function selection
tk.Label(app, text="Function:").grid(row=1, column=0, padx=xpadding, pady=ypadding, sticky='e')
function_var = tk.StringVar(value="Add Numeric Pattern")
function_menu = tk.OptionMenu(app, function_var, "Add Numeric Pattern", "Add Characters", "Remove Characters")
function_menu.grid(row=1, column=1, padx=xpadding, pady=ypadding)

# Starting character
tk.Label(app, text="Starting Character:").grid(row=2, column=0, padx=xpadding, pady=ypadding, sticky='e')
location_scale = tk.Scale(app, from_=0, to_=21, orient=tk.HORIZONTAL, length=300)
location_scale.grid(row=2, column=1, padx=xpadding, pady=ypadding)
tk.Label(app, text="0 = Beginning\n21 = End").grid(row=2, column=2, padx=xpadding, pady=ypadding, sticky='w')

# Add Numeric Pattern
tk.Label(app, text="Add Numeric Pattern \nStarting Number:").grid(row=3, column=0, padx=xpadding, pady=ypadding, sticky='e')
start_num_entry = tk.Entry(app, width=50)
start_num_entry.grid(row=3, column=1, padx=xpadding, pady=ypadding)

tk.Label(app, text="Add Numeric Pattern \nStep:").grid(row=4, column=0, padx=xpadding, pady=ypadding, sticky='e')
step_entry = tk.Entry(app, width=50)
step_entry.grid(row=4, column=1, padx=xpadding, pady=ypadding)

# Add Characters
tk.Label(app, text="Add Characters \nCharacters to Add:").grid(row=5, column=0, padx=xpadding, pady=ypadding, sticky='e')
string_entry = tk.Entry(app, width=50)
string_entry.grid(row=5, column=1, padx=xpadding, pady=ypadding)

# Remove Characters
tk.Label(app, text="Remove Characters \nNumber of Characters to Remove:").grid(row=6, column=0, padx=xpadding, pady=ypadding, sticky='e')
num_chars_scale = tk.Scale(app, from_=0, to_=10, orient=tk.HORIZONTAL, length=300)
num_chars_scale.grid(row=6, column=1, padx=xpadding, pady=ypadding)

# Execute button
tk.Button(app, text="Execute", command=execute_function).grid(row=7, column=0, columnspan=2, padx=xpadding, pady=ypadding)

# File listboxes and buttons
tk.Label(app, text="Files in Directory").grid(row=0, column=3, padx=xpadding, pady=ypadding)
file_listbox = Listbox(app, width=50, height=20)
file_listbox.grid(row=1, column=3, rowspan=6, padx=xpadding, pady=ypadding)

tk.Button(app, text="Sort", command=lambda: sort_files(file_listbox)).grid(row=0, column=3, padx=xpadding, pady=ypadding, sticky='e')

tk.Label(app, text="Selected Files").grid(row=0, column=5, padx=xpadding, pady=ypadding)
filtered_listbox = Listbox(app, width=50, height=20)
filtered_listbox.grid(row=1, column=5, rowspan=6, padx=xpadding, pady=ypadding)

tk.Button(app, text="Sort", command=lambda: sort_files(filtered_listbox)).grid(row=0, column=5, padx=xpadding, pady=ypadding, sticky='e')

# File manipulation buttons
tk.Button(app, text="Add >>", command=add_file).grid(row=2, column=4, padx=xpadding, pady=ypadding)
tk.Button(app, text="<< Remove", command=remove_file).grid(row=3, column=4, padx=xpadding, pady=ypadding)
tk.Button(app, text="Add All >>", command=add_all_files).grid(row=4, column=4, padx=xpadding, pady=ypadding)
tk.Button(app, text="<< Remove All", command=remove_all_files).grid(row=5, column=4, padx=xpadding, pady=ypadding)
tk.Button(app, text="Move Up", command=move_up).grid(row=1, column=6, padx=xpadding, pady=ypadding)
tk.Button(app, text="Move Down", command=move_down).grid(row=2, column=6, padx=xpadding, pady=ypadding)

app.mainloop()
