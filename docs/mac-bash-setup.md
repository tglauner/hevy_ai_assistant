# macOS Development Environment Setup (Bash + Visual Studio Code)

The guide below walks through preparing a macOS laptop for development when you expect spotty Wi‑Fi (e.g., at an airport). It assumes **Bash** as your shell and **Visual Studio Code** as your editor. Follow the steps in order so you are ready to work offline.

## 1) Prep macOS
1. Update macOS: **Apple Menu → System Settings → General → Software Update**.
2. Open Terminal (Spotlight: `⌘ + Space`, type "Terminal") and confirm your shell is Bash with `echo $SHELL` (should be `/bin/bash`).

## 2) Install Xcode Command Line Tools (CLT)
Xcode CLT provides Git, compilers, and build utilities.
```bash
xcode-select --install
```
Accept the prompt and wait for the install to finish. Verify with:
```bash
xcode-select -p
```
You should see a path like `/Library/Developer/CommandLineTools`.

## 3) Install Homebrew (package manager)
1. Install:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Add Homebrew to Bash (append to `~/.bash_profile`):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.bash_profile
source ~/.bash_profile
```
3. Confirm Homebrew works:
```bash
brew doctor
brew update
```

## 4) Core CLI tools
Install frequently used tools so you do not need to fetch them later:
```bash
brew install git gh wget curl htop tree fzf ripgrep fd jq gnupg tmux direnv
```
Add fzf keybindings and direnv hook for Bash:
```bash
$(brew --prefix)/opt/fzf/install --key-bindings --completion
[[ -x "$(command -v direnv)" ]] && echo 'eval "$(direnv hook bash)"' >> ~/.bash_profile
source ~/.bash_profile
```

## 5) Git configuration
Set your identity and defaults:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
```
Generate an SSH key for GitHub:
```bash
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub
```
Add the printed key to GitHub (GitHub → Settings → SSH and GPG keys → **New SSH key**).

## 6) Python toolchain (pyenv + pipx)
1. Install pyenv and dependencies:
```bash
brew install pyenv openssl readline sqlite3 xz zlib
```
2. Add pyenv to Bash:
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```
3. Install and select a Python version (example: 3.11):
```bash
pyenv install 3.11.9
pyenv global 3.11.9
```
4. Install pipx for isolated CLI tools:
```bash
brew install pipx
pipx ensurepath
source ~/.bash_profile
```
5. Useful Python CLIs to preload:
```bash
pipx install pipenv
pipx install poetry
pipx install black
pipx install ruff
pipx install pre-commit
```

## 7) Node.js toolchain (fnm + npm/yarn)
1. Install fast Node manager (fnm):
```bash
brew install fnm
```
2. Add fnm to Bash:
```bash
echo 'eval "$(fnm env --use-on-cd)"' >> ~/.bash_profile
source ~/.bash_profile
```
3. Install Node LTS and verify:
```bash
fnm install --lts
fnm default lts-latest
node -v
npm -v
```
4. Optional package managers:
```bash
npm install -g yarn pnpm
```

## 8) Docker (containers)
1. Download **Docker Desktop for Mac** (Apple/Intel as appropriate) from docker.com and install.
2. Launch Docker Desktop once to complete setup.
3. Test:
```bash
docker run hello-world
```

## 9) Databases and services (optional)
Install only what you need before you travel:
```bash
brew install postgresql@15 redis mysql
brew services start postgresql@15
brew services start redis
```

## 10) Visual Studio Code setup
1. Download **Visual Studio Code** from https://code.visualstudio.com/ and drag it to **Applications**.
2. Install the `code` shell command: VS Code → Command Palette → **Shell Command: Install 'code' command in PATH**.
3. Recommended extensions to install while online:
   - Python, Pylance
   - ESLint, Prettier, TypeScript/JavaScript
   - GitLens, GitHub Pull Requests and Issues
   - Docker, YAML, Markdown All in One
4. Enable Settings Sync if you use it, so extensions and settings are ready offline.

## 11) Cache dependencies for offline work
Run these in your projects to cache packages before heading to the airport:
- Python: `pip download -r requirements.txt`
- Node: `npm install` or `yarn install`
- Docker: `docker pull <image>` for images you will need
- Homebrew: `brew fetch <formula>` for large packages if you anticipate reinstalling

## 12) Verification checklist
Run quick checks to confirm everything is wired up:
```bash
git --version
gcc --version
python --version
pip --version
pipx --version
black --version
ruff --version
node -v
npm -v
yarn -v
pnpm -v
docker info  # if Docker installed
```

## 13) Airport/offline tips
- Keep a local Markdown notes file with frequent commands.
- Use `man <tool>` and `pydoc <module>` for offline docs.
- Work in feature branches and push when you have a stable connection.
- Consider a mobile hotspot for brief syncs if permitted.

Following this checklist before you leave ensures you can code comfortably in Bash with Visual Studio Code—even with unreliable airport Wi‑Fi.
