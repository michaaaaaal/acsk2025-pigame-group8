# ACSK2025 PI Game – Group 8

This repository contains the final project for the 2025 Annual PI Game

## Structure (might and probably will change later)

```
📦acsk2025-pigame-group8
 ┣ 📂assignment_files/    ← All the files we were provided via canvas
 ┣ 📂code/                ← Python scripts we work with
 ┣ 📂data/                ← BakeryData2025_Vilnius.xlsx
 ┣ 📂report/              ← LaTeX source files (we will work in overleaf and add here at the end)
 ┣ 📜README.md            ← This file
 ┗ 📜.gitignore           ← Commonly ignored files (builds, logs, etc.)
```
---
## Completion Checklist
```
• Task 1: 🟨 (half of this is the writing assignment)
• Task 2: 🟨 (report + code to be finished)
• Task 3: 🟥
• Task 4: 🟥
• Task 5: 🟩 (complete to be verified)
• Task 6: 🟨 (report to be written)
• Task 7: 🟥
• Task 8: 🟥

```
---

## Git Setup for Team Members (Windows/macOS)

### ONE-TIME SETUP

1. **Create a GitHub account**
   [Sign-up](https://github.com/signup)

2. **Install Git**
   - [Windows](https://git-scm.com/download/win)
   - [macOS](https://git-scm.com/download/mac)

3. **Configure Git**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

4. **Clone the Repository**
   ```bash
   cd ~/Documents  # or wherever you want the folder
   git clone https://github.com/michaaaaaal/acsk2025-pigame-group8.git
   cd acsk2025-pigame-group8
   ```
**Note**
   If you do not feel comfortable using the terminal, you can use [GitDesktop](https://github.com/apps/desktop)

### DAILY WORKFLOW

| Task                        | Command                              |
|-----------------------------|--------------------------------------|
| Get latest version          | `git pull origin main`               |
| Stage your changes          | `git add .`                          |
| Stage your changes to 1 file| `git add "file.name" .`              |
| Commit with a message       | `git commit -m "Update section 2.1"` |
| Push changes to GitHub      | `git push origin main`               |

### Best Practices

- Always `git pull` before you start editing anything.
- Only edit one LaTeX file at a time to avoid merge conflicts.
- Use descriptive commit messages.
- Do not commit temporary files or LaTeX build files (`.aux`, `.log`, etc.).

---

## Group Members

- Thijs van Dijkman  
- Xiaoyang Liu  
- Chinechem Okere  
- Michał Śliwiński  
- Anthony Vári

---

## Notes

- For full reproducibility, all code used for figures and computations is included.
- Final report compiled in LaTeX, adhering to course style guidelines.
- If you make any structural changes to the repository, please update the README too
