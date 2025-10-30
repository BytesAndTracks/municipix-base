import os
from git import Repo

LOCAL_PATH = "./acbr_clone"
REPO_URL = "https://github.com/frones/ACBr.git"

def clone_or_update_repo():
    if not os.path.exists(LOCAL_PATH):
        print("📥 Clonando repositório base (ACBr)...")
        Repo.clone_from(REPO_URL, LOCAL_PATH)
    else:
        print("🔄 Atualizando repositório base...")
        repo = Repo(LOCAL_PATH)
        repo.remotes.origin.pull()
    print("✅ Sincronização concluída!")

if __name__ == "__main__":
    clone_or_update_repo()
