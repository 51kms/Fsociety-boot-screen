# FSociety Boot Screen

A stylish terminal simulator inspired by the FSociety hacker collective from the TV show "Mr. Robot". This Python script creates an immersive fullscreen boot sequence with realistic kernel messages, a flickering effect, and an interactive password prompt.

## Features

✨ **Realistic boot messages** - Simulates a Linux/Windows kernel startup sequence  
🎭 **FSociety ASCII logo** - Centered display of the iconic logo  
⚡ **Smooth animations** - Messages stream in sequentially  
🔴 **Flickering effect** - Rapid white/red flicker effect on loaded messages  
🔐 **Interactive prompt** - Enter a password/key for access control  
💻 **Full terminal support** - Works on Linux, macOS, and other Unix-like systems  

## Requirements

- Python 3.6+
- Unix-like terminal (Linux, macOS, BSD, etc.)
- Terminal with ANSI color support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/51kms/Fsociety-boot-screen.git
cd Fsociety-boot-screen
```

2. Make the script executable:
```bash
chmod +x Fsec.py
```

## Usage

Run the script:
```bash
python3 Fsec.py
```

Or:
```bash
./Fsec.py
```

### What to expect:

1. **Fullscreen display** - The terminal will clear and display the FSociety logo in the center
2. **Boot sequence** - Realistic kernel messages will stream in from the left side
3. **"WRONG KEY" message** - Displayed in red after loading completes
4. **Flickering effect** - Messages flicker rapidly in white and red
5. **Password prompt** - Enter a key/password at the prompt
6. **Result** - You'll see either "ACCESS GRANTED" (try: `correct`) or "ACCESS DENIED"

## Customization

You can customize the script by editing `Fsec.py`:

- **Boot messages**: Edit the `LOADING_MESSAGES` list
- **Logo**: Modify the `FSOCIETY_LOGO` string
- **Colors**: Change ANSI color codes (e.g., `\033[91m` for red)
- **Timing**: Adjust `duration` parameters in function calls
- **Password**: Change the validation string in the `if user_input.lower() == "correct":` line

## Keyboard Controls

- `Ctrl+C` - Exit the program at any time
- `Enter` - Submit your key/password

## License

MIT License - See LICENSE file for details

## Disclaimer

This is a fan project inspired by the TV show "Mr. Robot". It's for entertainment and educational purposes only. FSociety is a fictional organization.

## Author

Created by [@51kms](https://github.com/51kms)
