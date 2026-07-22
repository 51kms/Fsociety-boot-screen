#!/usr/bin/env python3
import os
import sys
import time
import random
from threading import Thread

# FSociety Logo
FSOCIETY_LOGO = """
    ╔═══════════════╗
    ║               ║
    ║  ╭─────────╮  ║
    ║  │ ◀ ◗ ◀    │  ║
    ║  │          │  ║
    ║  │  ▬▬▬─▬▬  │  ║
    ║  │          │  ║
    ║  ╰─────────╯  ║
    ║               ║
    ╚═══════════════╝
    
      fsociety
"""

# Loading messages
LOADING_MESSAGES = [
    "[OK] Loading FSEC...",
    "[OK] Loading system files...",
    "[OK] Initializing HAL.dll",
    "[OK] Checking memory...",
    "[OK] CPU: Intel Core Processor detected",
    "[OK] RAM: 16384 MB memory available",
    "[OK] Initializing ACPI subsystem",
    "[OK] PCI: Using configuration type 1",
    "[OK] Detecting storage devices...",
    "[OK] HDD: Primary disk detected",
    "[OK] Initializing device drivers...",
    "[OK] Loading NFS module...",
    "[OK] Loading network stack...",
    "[OK] Initializing TCP/IP services",
    "[OK] Loading device driver...",
    "[OK] Starting security subsystem",
    "[OK] Starting audio subsystem",
    "[OK] Loading registry hive SOFTWARE",
    "[OK] Loading user profiles...",
    "[OK] Starting graphics subsystem",
    "[OK] Initializing display driver...",
    "[OK] Checking system integrity...",
    "[OK] Verifying system files...",
    "",
    "[WARN] Unknown hardware signature detected",
    "[WARN] Driver response timeout",
    "[WARN] Failed to load optional module",
    "",
    "DEBUG: Kernel memory map:",
    "0xD0100000 - 0xD0FFFFFF Reserved",
    "0xDFF00000 - 0xDFFFFFFF Available RAM",
    "0xD8000000 - 0xDFFFFFFF Kernel space",
    "",
    "Loading kernel modules:",
    "[OK] msoknl.exe",
    "[OK] HAL.dll",
    "[OK] ntoskrnl.exe",
    "[OK] network.sys",
    "[FAIL] storage_controller.sys",
    "",
    "[ERROR] Driver initialization failed",
    "[ERROR] Kernel module corrupted",
    "[ERROR] System file missing",
    "",
    "KERNEL ERROR",
    "STOP CODE: 0x0000007B",
    "INACCESSIBLE_BOOT_DEVICE",
    "",
    "Collecting crash information...",
    "Dump location: C:\\windows\\minidump",
    "Analyzing system failure...",
    "",
    "Attempting automatic repair...",
    "Loading recovery environment...",
    "Scanning disk for errors...",
    "Checking filesystem metadata...",
    "Repairing system files...",
    "",
    "Recovery progress: 25%",
    "Recovery progress: 50%",
    "Recovery progress: 75%",
    "Recovery progress: 100%",
    "",
    "FATAL ERROR",
    "System recovery failed.",
    "The system encountered an unrecoverable problem.",
    "Please restart your computer.",
]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_centered(text, screen_width, screen_height, y_offset):
    """Print text centered horizontally"""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        x = (screen_width - len(line)) // 2
        sys.stdout.write(f'\033[{y_offset + i};{x}H{line}')
        sys.stdout.flush()

def loading_animation(duration=8):
    """Show loading messages with animation"""
    start_time = time.time()
    message_index = 0
    
    while time.time() - start_time < duration:
        if message_index < len(LOADING_MESSAGES):
            msg = LOADING_MESSAGES[message_index]
            sys.stdout.write(f'\033[{5 + message_index};5H{msg}\033[K')
            sys.stdout.flush()
            message_index += 1
            time.sleep(0.08)
        else:
            time.sleep(0.1)
    
    return message_index

def flicker_effect(lines_to_flicker, duration=3):
    """Create flickering effect on specific lines"""
    start_time = time.time()
    flicker_colors = ['\033[91m', '\033[97m']  # Red and White
    reset_color = '\033[0m'
    
    while time.time() - start_time < duration:
        color = random.choice(flicker_colors)
        for idx, line in enumerate(lines_to_flicker):
            if random.random() > 0.5:
                y = 5 + idx
                sys.stdout.write(f'\033[{y};5H{color}{line}{reset_color}\033[K')
                sys.stdout.flush()
        time.sleep(0.1)
    
    # Reset to normal after flickering
    for idx, line in enumerate(lines_to_flicker):
        y = 5 + idx
        sys.stdout.write(f'\033[{y};5H\033[91m{line}\033[0m\033[K')
        sys.stdout.flush()

def main():
    try:
        # Hide cursor
        os.system('echo -ne "\\033[?25l"')
        
        # Clear and setup
        clear_screen()
        
        # Get terminal size
        rows, cols = os.popen('stty size', 'r').read().split()
        screen_height = int(rows)
        screen_width = int(cols)
        
        # Enter fullscreen mode
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
        
        # Print logo centered
        logo_start_y = (screen_height // 2) - 6
        print_centered(FSOCIETY_LOGO, screen_width, screen_height, logo_start_y)
        
        # Start loading messages
        sys.stdout.write('\033[5;5H')
        sys.stdout.flush()
        
        # Simulate loading
        loaded_count = loading_animation(duration=8)
        
        # Get the messages that were displayed
        messages_displayed = LOADING_MESSAGES[:loaded_count]
        
        # Add "WRONG KEY" message
        sys.stdout.write(f'\033[{5 + loaded_count + 2};5H\033[91mWRONG KEY\033[0m')
        sys.stdout.flush()
        
        time.sleep(1)
        
        # Start flickering effect on the loaded messages
        flicker_thread = Thread(target=flicker_effect, args=(messages_displayed, 3))
        flicker_thread.start()
        flicker_thread.join()
        
        # Show password prompt
        prompt_y = 5 + loaded_count + 4
        sys.stdout.write(f'\033[{prompt_y};5H')
        sys.stdout.write('\033[97m')  # White text
        sys.stdout.flush()
        
        # Show cursor for input
        os.system('echo -ne "\\033[?25h"')
        
        sys.stdout.write('Enter key: ')
        sys.stdout.flush()
        user_input = input()
        
        # Hide cursor again
        os.system('echo -ne "\\033[?25l"')
        
        if user_input.lower() == "correct":
            sys.stdout.write(f'\033[{prompt_y + 2};5H\033[92mACCESS GRANTED\033[0m')
        else:
            sys.stdout.write(f'\033[{prompt_y + 2};5H\033[91mACCESS DENIED\033[0m')
        
        sys.stdout.flush()
        time.sleep(2)
        
        # Cleanup
        clear_screen()
        os.system('echo -ne "\\033[?25h"')
        
    except KeyboardInterrupt:
        os.system('echo -ne "\\033[?25h"')
        clear_screen()
        sys.exit(0)
    except Exception as e:
        os.system('echo -ne "\\033[?25h"')
        clear_screen()
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
