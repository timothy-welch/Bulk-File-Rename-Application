# File Renaming Application

This is a basic application written in Python using `tkinter` to solve a very common but tedious work problem - renaming files.

## Core Functions

This app has three core functions:
1. **Adding a custom numbering pattern to file names**:
   - Examples:
     - `1. `, `2. `, `3. `, ...
     - `1.1. `, `1.2. `, `1.3. `, ...
     - `2010`, `2013`, `2015`, ...
2. **Adding characters** (e.g., `hka_`)
3. **Removing characters**

These functions can be performed either on specific characters via a "Starting Character" widget or as Prefix/Suffix (by selecting 0 or 21 respectively).

## Features

- **Dual Windows for Ease of Use**:
  - The first window displays all filenames within the selected directory.
  - The second window shows the selected files to be modified via a selected action.
- **File Transfer Buttons**:
  - Easily transfer files between windows using the "Add"/"Remove" and "Add All"/"Remove All" buttons.
- **Sorting and Ordering**:
  - Sort files numerically/alphabetically using the "Sort" button.
  - Sort files individually using the "Move Up"/"Move Down" buttons.

I hope you find this helpful!
