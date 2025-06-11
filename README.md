# ACSK2025 PI Game – Group 8

This repository contains the final project for the 2025 Annual PI Game

## Structure

```
📦acsk2025-pigame-group8
 ┣ 📂code/                ← Python scripts for data analysis and simulation
 ┣ 📂report/              ← LaTeX source files for the final write-up
 ┣ 📜README.md            ← This file
 ┗ 📜.gitignore           ← Commonly ignored files (builds, logs, etc.)
```

## How to use the repository

1. Navigate to the `code` directory.
2. Install dependencies from `requirements.txt` (if available).
3. Run the analysis using your preferred Python environment.

---

## Git Setup for Team Members (Windows/macOS)

### ONE-TIME SETUP

1. **Install Git**
   - [Windows](https://git-scm.com/download/win)
   - [macOS](https://git-scm.com/download/mac)

2. **Configure Git**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

3. **Clone the Repository**
   ```bash
   cd ~/Documents  # or wherever you want the folder
   git clone https://github.com/michaaaaaal/acsk2025-pigame-group8.git
   cd acsk2025-pigame-group8
   ```

### DAILY WORKFLOW

| Task                        | Command                             |
|-----------------------------|--------------------------------------|
| Get latest version          | `git pull origin main`               |
| Stage your changes          | `git add .`                          |
| Commit with a message       | `git commit -m "Update section 2.1"` |
| Push changes to GitHub      | `git push origin main`               |

### Best Practices

- Always `git pull` before editing anything.
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
