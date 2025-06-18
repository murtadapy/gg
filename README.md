# GG (Go to GIT)

**GG** is a minimal lightweight Git-inspired version control system built from scratch in Python. It supports core Git functionalities like committing, branching, merging, switching, and configuration.

![icon](https://github.com/user-attachments/assets/50c1db19-a466-4c2e-a42c-ddf28a954a6e)

## ⚠️ Disclaimer

> This project is **not intended for production use**.

`gg` was built for fun and educational experiment to better understand how version control systems work under the hood. It may have **bugs**, missing features, or design limitations. This repository is **not actively maintained**, and there are **no plans for continued development**.

You're welcome to explore the code, fork it, or use it as inspiration.

## 🚀 Features

- `gg init` — Initialize a new gg repository
- `gg status` — Show changes compared to last commit
- `gg commit` — Save a snapshot of current project state
- `gg sprint` — Create a new sprint (branch)
- `gg switch` — Switch between sprints
- `gg merge` — Merge current sprint to its parent sprint
- `gg config` — Set local user configurations

## 🗂 Project Structure

```text
gg/
├── base/               # Shared command base classes
│   └── command.py
├── commands/           # CLI command implementations
│   ├── commit.py
│   ├── config.py
│   ├── initiate.py
│   ├── merge.py
│   ├── sprint.py
│   ├── status.py
│   └── switch.py
├── core/               # Internal core logic
│   ├── blob_manager.py
│   ├── database.py
│   ├── file_manager.py
│   ├── logger.py
│   ├── models.py
│   └── path.py
├── database.sql        # SQLite schema file
├── gg.py               # CLI dispatcher
└── __main__.py         # Python module entry point
```
🧱 4 Directories, 25 Files, 1000+ lines of Python Code

## 📦 Installation (Dev Mode)

```
git clone https://github.com/murtadapy/gg.git
cd gg
pip install .
```

## 📸 Demo
```bash
$ gg init
Initialized empty gg repository in .gg/

$ gg status
On sprint main
No changes have been made

$ touch main.py

$ gg status
On sprint main
    Created: main.py

$ gg commit
1 change has been committed successfully

$ gg sprint -n new-feature
Switched to new-feature

$ echo "#hello" > main.py

$ gg status
On sprint new-feature
    Modified: main.py

$ gg commit
1 change has been committed successfully

$ gg merge
Merged new-feature to main
```

![Peek 2025-06-16 20-20](https://github.com/user-attachments/assets/20441c9c-a697-456a-95f5-f17f7110d9c9)

