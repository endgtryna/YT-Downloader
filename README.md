# YT Downloader

YouTube video downloader with easy-to-use CLI interface.

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/endgtryna/YT-Downloader.git
cd YT-Downloader
```

### 2. Setup & Install

#### Windows:
```bash
python setup.py
```

#### Linux/Mac:
```bash
./setup.sh
```

Or use Python setup (works on all platforms):
```bash
python3 setup.py
```

The setup script will:
- Create virtual environment
- Install dependencies
- Setup Node.js environment
- Create launcher

### 3. Post-Installation

**Linux/Mac:** Reload terminal
```bash
source ~/.bashrc  # or ~/.zshrc
```

**Windows:** Restart terminal to use `yt-downloader` command

## Usage

### Running the Program

```bash
yt-downloader
```

### Download Modes

The program supports two modes:

#### Single Mode
Download one video by entering the URL directly.

#### Bulk Mode
Download multiple videos using a txt file containing a list of URLs.

**File format for bulk download:**
```
https://youtube.com/watch?v=video1
https://youtube.com/watch?v=video2
https://youtube.com/watch?v=video3
```

**Important notes for bulk mode:**
- Create a `.txt` file with YouTube URL list
- Each URL separated by enter (one URL per line)
- No spaces or additional characters
- Make sure all URLs are valid

**Example `playlist.txt` file:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=oHg5SJYRHA0
https://www.youtube.com/watch?v=iik25wqIuFo
```

### Output Formats

- Video: MP4
- Audio: MP3

## Dependencies

- `yt-dlp`: Core YouTube downloader
- `imageio-ffmpeg`: Video processing
- `rich`: CLI interface styling
- `nodeenv`: Node.js environment

## Troubleshooting

### Python not found
```bash
sudo apt update
sudo apt install python3 python3-venv
```

### Permission denied
```bash
chmod +x yt-downloader
chmod +x setup.sh
```

### PATH not updated
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Development

### Manual Setup (for development)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 yt-downloader
```
