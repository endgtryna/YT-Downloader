#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd: str, quiet: bool = False) -> bool:
    try:
        if quiet:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main() -> None:
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    
    print("Installing YT-Downloader...")
    
    if sys.version_info < (3, 7):
        print("Error: Python 3.7+ required")
        sys.exit(1)
    
    venv_dir = script_dir / ".venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv .venv"):
            print("Error: Failed to create virtual environment")
            sys.exit(1)
    
    is_windows = platform.system() == "Windows"
    venv_python = venv_dir / ("Scripts" if is_windows else "bin") / ("python.exe" if is_windows else "python")
    venv_pip = venv_dir / ("Scripts" if is_windows else "bin") / ("pip.exe" if is_windows else "pip")
    
    print("Upgrading pip...")
    run_command(f'"{venv_python}" -m pip install --upgrade pip', quiet=True)
    
    print("Installing dependencies...")
    run_command(f'"{venv_pip}" install -r requirements.txt', quiet=True)
    
    print("Setting up Node.js environment...")
    venv_nodeenv = venv_dir / ("Scripts" if is_windows else "bin") / ("nodeenv.exe" if is_windows else "nodeenv")
    run_command(f'"{venv_nodeenv}" -p --node=lts', quiet=True)
    
    if is_windows:
        install_dir = Path.home() / "AppData" / "Local" / "Programs" / "yt-downloader"
        install_dir.mkdir(parents=True, exist_ok=True)
        
        launcher = install_dir / "yt-downloader.bat"
        launcher.write_text(f'@echo off\n"{venv_python}" "{script_dir / "yt-downloader"}" %*\n', encoding='utf-8')
        
        try:
            import winreg  # type: ignore
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)  # type: ignore
            current_path, _ = winreg.QueryValueEx(key, "Path")  # type: ignore
            
            if isinstance(current_path, str) and str(install_dir) not in current_path:
                new_path = f"{current_path};{install_dir}"
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)  # type: ignore
                print(f"Added to PATH: {install_dir}")
                print("Restart terminal to use: yt-downloader")
            else:
                print("Already in PATH")
            
            winreg.CloseKey(key)  # type: ignore
        except Exception as e:
            print(f"Could not add to PATH automatically: {e}")
            print(f"Add manually: {install_dir}")
        
        print("\nYT-Downloader installed successfully!")
        print("Run with: yt-downloader")
    else:
        install_dir = Path.home() / ".local" / "bin"
        install_dir.mkdir(parents=True, exist_ok=True)
        
        launcher = install_dir / "yt-downloader"
        launcher.write_text(f'#!/usr/bin/bash\nsource "{venv_dir / "bin" / "activate"}"\nexec python3 "{script_dir / "yt-downloader"}" "$@"\n', encoding='utf-8')
        launcher.chmod(0o755)
        
        # Detect shell config
        shell_configs = []
        zshrc = Path.home() / ".zshrc"
        bashrc = Path.home() / ".bashrc"
        
        if zshrc.exists():
            shell_configs.append(zshrc)
        if bashrc.exists():
            shell_configs.append(bashrc)
        
        path_export = 'export PATH="$HOME/.local/bin:$PATH"'
        
        for shell_config in shell_configs:
            content = shell_config.read_text(encoding='utf-8')
            if ".local/bin" not in content:
                with shell_config.open("a", encoding='utf-8') as f:
                    f.write(f"\n{path_export}\n")
                print(f"Added to PATH in {shell_config}")
        
        if shell_configs:
            print(f"Run: source {shell_configs[0]}")
        
        print("\nYT-Downloader installed successfully!")
        print("Run with: yt-downloader")

if __name__ == "__main__":
    main()
