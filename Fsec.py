#!/usr/bin/env python3
import pygame
import sys
import time
import math
from enum import Enum

class State(Enum):
    LOADING = 1
    FLICKERING = 2
    INPUT = 3
    RESULT = 4

FSOCIETY_TEXT = "FSEC"

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

class BootScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("FSociety Boot")
        self.width, self.height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.small_font = pygame.font.Font(None, 14)
        self.logo_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        
        # State
        self.state = State.LOADING
        self.messages = []
        self.start_time = time.time()
        self.loading_duration = 8
        self.flickering_duration = 5
        self.flicker_start = None
        self.user_input = ""
        self.result_message = ""
        self.result_start = None
        
    def render_logo(self):
        """Render the FSociety logo in the center"""
        logo_x = self.width // 2 - 80
        logo_y = self.height // 2 - 100
        
        # Draw white border around logo
        border_rect = pygame.Rect(logo_x - 20, logo_y - 20, 200, 240)
        pygame.draw.rect(self.screen, self.WHITE, border_rect, 3)
        
        # Simple face representation (smile/V logo)
        face_center_x = logo_x + 80
        face_center_y = logo_y + 80
        
        # Eyes
        pygame.draw.circle(self.screen, self.WHITE, (face_center_x - 25, face_center_y - 20), 8)
        pygame.draw.circle(self.screen, self.WHITE, (face_center_x + 25, face_center_y - 20), 8)
        
        # Smile/mouth
        pygame.draw.arc(self.screen, self.WHITE, (face_center_x - 40, face_center_y, 80, 50), 0, 3.14, 4)
        
        # Render text below logo
        text = self.logo_font.render(FSOCIETY_TEXT, True, self.WHITE)
        text_rect = text.get_rect(center=(self.width // 2, logo_y + 200))
        self.screen.blit(text, text_rect)
        
    def render_messages(self, alpha=255):
        """Render the loading messages on the left side"""
        x = 20
        y = 30
        
        for msg in self.messages:
            if msg == "":
                y += 15
            else:
                # Alternate between red and white for error/warning messages
                if "[ERROR]" in msg or "[WARN]" in msg or "KERNEL" in msg or "STOP CODE" in msg:
                    color = self.RED
                else:
                    color = self.WHITE
                
                text_surface = self.small_font.render(msg, True, color)
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, (x, y))
                y += 18
    
    def update_loading(self):
        """Update loading state"""
        elapsed = time.time() - self.start_time
        
        # Add messages based on elapsed time
        message_count = int((elapsed / self.loading_duration) * len(LOADING_MESSAGES))
        message_count = min(message_count, len(LOADING_MESSAGES))
        
        self.messages = LOADING_MESSAGES[:message_count]
        
        if elapsed >= self.loading_duration:
            self.state = State.FLICKERING
            self.flicker_start = time.time()
            self.messages = LOADING_MESSAGES.copy()
    
    def update_flickering(self):
        """Update flickering state with continuous smooth flickering"""
        elapsed = time.time() - self.flicker_start
        
        if elapsed >= self.flickering_duration:
            self.state = State.INPUT
    
    def get_flicker_alpha(self):
        """Get alpha value for smooth flickering"""
        # Continuous smooth flickering using sine wave
        time_val = time.time() * 4  # Control speed
        alpha = int(128 + 127 * abs(math.sin(time_val)))
        return alpha
    
    def render_input(self):
        """Render input prompt"""
        prompt_y = self.height - 100
        
        prompt_text = self.small_font.render("Enter key: ", True, self.WHITE)
        self.screen.blit(prompt_text, (20, prompt_y))
        
        # Render input box
        input_box = pygame.Rect(20, prompt_y + 25, 300, 25)
        pygame.draw.rect(self.screen, self.WHITE, input_box, 2)
        
        # Render input text
        if self.user_input:
            input_display = self.small_font.render(self.user_input, True, self.WHITE)
            self.screen.blit(input_display, (25, prompt_y + 28))
        
        # Render cursor
        cursor_x = 25 + self.small_font.size(self.user_input)[0]
        pygame.draw.line(self.screen, self.WHITE, (cursor_x, prompt_y + 28), (cursor_x, prompt_y + 40), 2)
    
    def render_result(self):
        """Render result message"""
        if self.user_input.lower() == "correct":
            color = self.GREEN
            text = "ACCESS GRANTED"
        else:
            color = self.RED
            text = "ACCESS DENIED"
        
        result_surface = self.text_font.render(text, True, color)
        result_rect = result_surface.get_rect(center=(self.width // 2, self.height - 80))
        self.screen.blit(result_surface, result_rect)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == State.INPUT:
                    if event.key == pygame.K_RETURN:
                        self.state = State.RESULT
                        self.result_start = time.time()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return False
                    else:
                        # Add printable characters
                        if event.unicode.isprintable():
                            self.user_input += event.unicode
        
        return True
    
    def update(self):
        """Update game state"""
        if self.state == State.LOADING:
            self.update_loading()
        elif self.state == State.FLICKERING:
            self.update_flickering()
        elif self.state == State.RESULT:
            # Stay on result for 3 seconds
            if time.time() - self.result_start >= 3:
                return False
        
        return True
    
    def render(self):
        """Render everything"""
        self.screen.fill(self.BLACK)
        
        self.render_logo()
        
        if self.state == State.LOADING:
            self.render_messages()
        elif self.state == State.FLICKERING:
            alpha = self.get_flicker_alpha()
            self.render_messages(alpha)
        elif self.state == State.INPUT:
            alpha = self.get_flicker_alpha()
            self.render_messages(alpha)
            self.render_input()
        elif self.state == State.RESULT:
            alpha = self.get_flicker_alpha()
            self.render_messages(alpha)
            self.render_result()
        
        pygame.display.flip()
    
    def run(self):
        """Main loop"""
        running = True
        
        while running:
            running = self.handle_events()
            running = self.update() and running
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    boot_screen = BootScreen()
    boot_screen.run()
