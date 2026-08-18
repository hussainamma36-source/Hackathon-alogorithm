import os
import shutil

base_dir = r"c:\Users\hussa\Hackathon  alogorithm"

# Move api to backend
backend_dir = os.path.join(base_dir, "backend")
api_dir = os.path.join(base_dir, "api")
if os.path.exists(api_dir):
    os.rename(api_dir, backend_dir)

# Rename backend/index.py back to main.py
index_py = os.path.join(backend_dir, "index.py")
main_py = os.path.join(backend_dir, "main.py")
if os.path.exists(index_py):
    os.rename(index_py, main_py)

# Create frontend directory
frontend_dir = os.path.join(base_dir, "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)

# Frontend files to move back
frontend_files = [
    "package.json", "package-lock.json", "vite.config.ts", 
    "tsconfig.json", "tsconfig.node.json", "tsconfig.app.json", 
    "index.html", "src", "public", ".oxlintrc.json", ".env.example", "README.md"
]

for item in frontend_files:
    src = os.path.join(base_dir, item)
    dst = os.path.join(frontend_dir, item)
    if os.path.exists(src):
        shutil.move(src, dst)

print("Restoration complete!")
