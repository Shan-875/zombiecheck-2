def get_idle_threshold(self):
        """Get AGGRESSIVE idle threshold"""
        base_thresholds = {
            'low': 60,      # Reduced from 300
            'medium': 45,   # Reduced from 180
            'high': 30,     # Reduced from 120
            'extreme': 15   # New extreme mode
        }
        
        threshold = base_thresholds.get(self.settings['sensitivity'], 30)
        
        if self.settings['gaming_mode']:
            threshold *= 1.5  # Reduced multiplier from 2
            
        if self.settings['adaptive_threshold']:
            # Less forgiving adjustment
            threshold = threshold * (1 + self.tolerance_level / 400.0)  # Reduced impact
            
        return threshold
        
    def show_warning(self, reasons):
        """Show visual warning before challenge - SHORTER DURATION"""
        if not self.settings['visual_warnings']:
            return
            
        try:
            warning_window = tk.Toplevel(self.root)
            warning_window.title("⚠️ Warning")
            warning_window.geometry("400x200")
            warning_window.configure(bg="#fd7e14")
            warning_window.attributes('-topmost', True)
            
            # Center the window
            warning_window.geometry("+{}+{}".format(
                self.root.winfo_rootx() + 50,
                self.root.winfo_rooty() + 50
            ))
            
            tk.Label(
                warning_window,
                text="⚠️ Zombie Activity Detected!",
                font=("Segoe UI", 16, "bold"),
                fg="white",
                bg="#fd7e14"
            ).pack(pady=20)
            
            tk.Label(
                warning_window,
                text="FOCUS NOW OR FACE CHALLENGE!",
                font=("Segoe UI", 12, "bold"),
                fg="white",
                bg="#fd7e14"
            ).pack()
            
            reason_text = "Patterns: " + ", ".join(reasons[:2])
            tk.Label(
                warning_window,
                text=reason_text,
                font=("Segoe UI", 10),
                fg="white",
                bg="#fd7e14",
                wraplength=350
            ).pack(pady=10)
            
            # Auto-close after 2 seconds (reduced from 3)
            warning_window.after(2000, warning_window.destroy)
        except Exception as e:
            print(f"Error showing warning: {e}")
        
    def trigger_intelligent_challenge(self, reasons, zombie_score):
        """Trigger challenge with proper state management"""
        try:
            # Prevent multiple challenges
            if self.challenge_in_progress or self.is_in_grace_period():
                return
                
            # Set challenge state
            self.challenge_in_progress = True
            
            self.zombie_incidents += 1
            self.stats['total_interventions'] += 1
            self.stats['today_interventions'] += 1
            self.warning_given = False
            
            # Play alert
            self.start_continuous_beep()
                
            # Determine challenge difficulty
            code_length = self.calculate_challenge_difficulty(zombie_score)
            challenge_code = self.generate_challenge_code(code_length)
            
            reason_text = "Detected: " + ", ".join(reasons[:3])
            self.show_challenge_window(challenge_code, reason_text, zombie_score)
        except Exception as e:
            print(f"Error in trigger_intelligent_challenge: {e}")
            self.challenge_in_progress = False
        
    def _beep_loop(self):
        """Loop to generate continuous beeps"""
        while not self.stop_beeping_event.is_set():
            try:
                if platform.system() == "Windows":
                    winsound.Beep(1000, 400)  # Higher pitch, shorter beep
                else:
                    print('\a', end='', flush=True)
            except Exception as e:
                print(f"Could not play sound: {e}")
            time.sleep(0.8)  # Faster beeping

    def start_continuous_beep(self):
        """Start the continuous beeping sound in a separate thread"""
        if self.beeping_thread and self.beeping_thread.is_alive():
            return

        self.stop_beeping_event = threading.Event()
        self.beeping_thread = threading.Thread(target=self._beep_loop, daemon=True)
        self.beeping_thread.start()

    def stop_continuous_beep(self):
        """Stop the continuous beeping sound"""
        if self.stop_beeping_event:
            self.stop_beeping_event.set()
        if self.beeping_thread:
            self.beeping_thread.join(timeout=1)
        self.beeping_thread = None
        self.stop_beeping_event = None
            
    def calculate_challenge_difficulty(self, zombie_score):
        """Calculate challenge difficulty - HARDER"""
        base_length = 7  # Increased from 6
        
        if zombie_score > 80:
            base_length += 4  # Increased
        elif zombie_score > 60:
            base_length += 3
        elif zombie_score > 40:
            base_length += 2
            
        if self.zombie_incidents > 2:
            base_length += min(self.zombie_incidents - 1, 5)  # Harsher escalation
            
        if self.settings['nightmare_mode']:
            base_length += 4  # Increased from 3
            
        if self.stats['current_streak'] > 10:  # Higher threshold for reduction
            base_length = max(5, base_length - 1)
            
        return min(base_length, 20)  # Can go up to 20 characters
        
    def generate_challenge_code(self, length):
        """Generate challenge code"""
        if self.settings['nightmare_mode']:
            # Even more confusing characters
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()[]{}|\\/<>?'
        else:
            # Removed similar looking characters for clarity
            chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
            
        return ''.join(random.choices(chars, k=length))
        
    def show_challenge_window(self, code, reason, zombie_score):
        """FIXED: Enhanced challenge window with better input handling"""
        try:
            # Create challenge window
            self.challenge_window = tk.Toplevel(self.root)
            self.challenge_window.title("🚨 ZOMBIE DETECTED!")
            self.challenge_window.geometry("600x450")
            self.challenge_window.configure(bg="#da3633")
            self.challenge_window.attributes('-topmost', True)
            self.challenge_window.grab_set()
            
            # Prevent closing
            self.challenge_window.protocol("WM_DELETE_WINDOW", lambda: None)
            
            # Center window on screen
            self.challenge_window.update_idletasks()
            screen_width = self.challenge_window.winfo_screenwidth()
            screen_height = self.challenge_window.winfo_screenheight()
            x = (screen_width - 600) // 2
            y = (screen_height - 450) // 2
            self.challenge_window.geometry(f"600x450+{x}+{y}")
            
            # Force focus
            self.challenge_window.lift()
            self.challenge_window.focus_force()
            
            self.challenge_start_time = time.time()
            
            # Header with animation effect
            header_frame = tk.Frame(self.challenge_window, bg="#da3633")
            header_frame.pack(fill="x", pady=20)
            
            header_label = tk.Label(
                header_frame,
                text="🧟‍♂️ ZOMBIE MODE DETECTED! 🚨",
                font=("Segoe UI", 22, "bold"),
                fg="white",
                bg="#da3633"
            )
            header_label.pack()
            
            severity_text = self.get_severity_text(zombie_score)
            tk.Label(
                header_frame,
                text=f"Severity: {severity_text}",
                font=("Segoe UI", 14, "bold"),
                fg="#ffeb3b",
                bg="#da3633"
            ).pack(pady=(5, 0))
            
            # Reason
            tk.Label(
                self.challenge_window,
                text=reason,
                font=("Segoe UI", 11),
                fg="white",
                bg="#da3633",
                wraplength=550
            ).pack(pady=10)
            
            # Code display with better visibility
            code_frame = tk.Frame(self.challenge_window, bg="#000000", relief="raised", bd=4)
            code_frame.pack(pady=20, padx=40)
            
            tk.Label(
                code_frame,
                text="TYPE THIS CODE TO PROVE YOU'RE AWAKE:",
                font=("Segoe UI", 12, "bold"),
                bg="#000000",
                fg="#FFFFFF"
            ).pack(pady=(15, 5))
            
            # Display code with spacing for better readability
            spaced_code = ' '.join(code[i:i+4] for i in range(0, len(code), 4))
            code_label = tk.Label(
                code_frame,
                text=spaced_code,
                font=("Courier New", 32, "bold"),  # Better font for code
                fg="#00FF00",
                bg="#000000"
            )
            code_label.pack(pady=15, padx=20)
            
            # Input section with better focus handling
            input_frame = tk.Frame(self.challenge_window, bg="#da3633")
            input_frame.pack(pady=15)
            
            tk.Label(
                input_frame,
                text="Your response (no spaces needed):",
                font=("Segoe UI", 12, "bold"),
                fg="white",
                bg="#da3633"
            ).pack()
            
            # Entry with better configuration
            entry_var = tk.StringVar()
            self.challenge_entry = tk.Entry(
                input_frame,
                textvariable=entry_var,
                font=("Courier New", 18, "bold"),
                width=max(len(code) + 4, 15),
                justify="center",
                relief="solid",
                bd=3,
                bg="white",
                fg="black",
                insertbackground="black",
                selectbackground="#4CAF50",
                selectforeground="white"
            )
            self.challenge_entry.pack(pady=10)
            
            # Real-time feedback label
            self.feedback_label = tk.Label(
                input_frame,
                text="",
                font=("Segoe UI", 11, "bold"),
                fg="#ffeb3b",
                bg="#da3633"
            )
            self.feedback_label.pack(pady=(5, 0))
            
            # Bind events for better interaction
            def on_key_release(event):
                """Update feedback as user types"""
                entered = self.challenge_entry.get().strip()
                if not entered:
                    self.feedback_label.config(text="", fg="#ffeb3b")
                    return
                    
                # Remove spaces from entered text for comparison
                entered_clean = entered.replace(" ", "").upper()
                code_clean = code.upper()
                
                # Calculate matching characters
                correct_chars = 0
                for i in range(min(len(entered_clean), len(code_clean))):
                    if entered_clean[i] == code_clean[i]:
                        correct_chars += 1
                    else:
                        break
                
                # Update feedback
                if len(entered_clean) >= len(code_clean):
                    if entered_clean == code_clean:
                        self.feedback_label.config(
                            text="✅ CORRECT! Press Enter or click Submit", 
                            fg="#4CAF50"
                        )
                    else:
                        self.feedback_label.config(
                            text=f"❌ Incorrect - {correct_chars}/{len(code_clean)} characters match", 
                            fg="#FF5252"
                        )
                else:
                    self.feedback_label.config(
                        text=f"Progress: {correct_chars}/{len(code_clean)} correct | {len(code_clean) - len(entered_clean)} more to go",
                        fg="#FFC107"
                    )
            
            def on_enter_key(event):
                """Handle Enter key press"""
                self.check_challenge_answer(code)
                return "break"
            
            # Bind events
            self.challenge_entry.bind('<KeyRelease>', on_key_release)
            self.challenge_entry.bind('<Return>', on_enter_key)
            
            # Buttons
            button_frame = tk.Frame(self.challenge_window, bg="#da3633")
            button_frame.pack(pady=15)
            
            submit_btn = tk.Button(
                button_frame,
                text="SUBMIT",
                font=("Segoe UI", 14, "bold"),
                bg="#238636",
                fg="white",
                command=lambda: self.check_challenge_answer(code),
                width=12,
                height=1,
                relief="raised",
                bd=2,
                cursor="hand2",
                activebackground="#2EA043",
                activeforeground="white"
            )
            submit_btn.pack(side="left", padx=(0, 10))
            
            feedback_btn = tk.Button(
                button_frame,
                text="FALSE ALARM",
                font=("Segoe UI", 11),
                bg="#fd7e14",
                fg="white",
                command=self.report_false_positive,
                width=12,
                height=1,
                relief="raised",
                bd=2,
                cursor="hand2",
                activebackground="#FE8500",
                activeforeground="white"
            )
            feedback_btn.pack(side="left")
            
            # Timer with aggressive countdown
            timer_duration = 35  # Fixed 35 seconds instead of dynamic timing
            self.timer_label = tk.Label(
                self.challenge_window,
                text=f"Time remaining: {timer_duration}s",
                font=("Segoe UI", 12, "bold"),
                fg="white",
                bg="#da3633"
            )
            self.timer_label.pack(pady=(10, 0))
            
            # Force focus to entry after a short delay
            self.challenge_window.after(100, lambda: self.challenge_entry.focus_force())
            self.challenge_window.after(200, lambda: self.challenge_entry.selection_range(0, tk.END))
            
            # Start timer
            self.start_challenge_timer(timer_duration)
            
        except Exception as e:
            print(f"Error showing challenge window: {e}")
            self.challenge_in_progress = False
        
    def get_severity_text(self, zombie_score):
        """Get severity description"""
        if zombie_score >= 80:
            return "🔥 CRITICAL - WAKE UP!"
        elif zombie_score >= 60:
            return "⚠️ HIGH - FOCUS NOW!"
        elif zombie_score >= 40:
            return "⚡ MEDIUM - PAY ATTENTION!"
        else:
            return "💤 LOW - STAY ALERT!"
            
    def start_challenge_timer(self, seconds):
        """Challenge timer with color changes"""
        try:
            if seconds > 0 and self.challenge_window and self.challenge_window.winfo_exists():
                # Color based on time remaining
                if seconds <= 5:
                    color = "#FF1744"
                    # Flash the window for last 5 seconds
                    if seconds % 2 == 0:
                        self.challenge_window.configure(bg="#FF1744")
                    else:
                        self.challenge_window.configure(bg="#da3633")
                elif seconds <= 10:
                    color = "#FFA726"
                else:
                    color = "white"
                    
                self.timer_label.config(text=f"Time remaining: {seconds}s", fg=color)
                self.challenge_window.after(1000, lambda: self.start_challenge_timer(seconds - 1))
            elif self.challenge_window and self.challenge_window.winfo_exists():
                self.escalate_challenge()
        except Exception as e:
            print(f"Error in challenge timer: {e}")
            
    def check_challenge_answer(self, correct_code):
        """Check challenge answer with better validation"""
        try:
            if not hasattr(self, 'challenge_entry') or not self.challenge_entry.winfo_exists():
                return
                
            # Clean up entered code (remove spaces, convert to upper)
            entered_code = self.challenge_entry.get().replace(" ", "").strip().upper()
            correct_code_clean = correct_code.upper()
            response_time = time.time() - self.challenge_start_time if self.challenge_start_time else 0
            
            if entered_code == correct_code_clean:
                self.challenge_success(response_time)
            else:
                self.challenge_failure()
        except Exception as e:
            print(f"Error checking challenge answer: {e}")
            
    def challenge_success(self, response_time):
        """Handle successful challenge with grace period"""
        try:
            print("Challenge completed successfully!")
            
            # Update stats
            self.stats['current_streak'] += 1
            self.stats['successful_detections'] += 1
            if self.stats['current_streak'] > self.stats['longest_streak']:
                self.stats['longest_streak'] = self.stats['current_streak']
                
            # Update response time
            if self.stats['avg_response_time'] == 0:
                self.stats['avg_response_time'] = response_time
            else:
                self.stats['avg_response_time'] = (self.stats['avg_response_time'] + response_time) / 2
                
            # Restore MINIMAL tolerance
            self.tolerance_level = min(self.max_tolerance, self.tolerance_level + 10)  # Reduced from 20
            
            # Stop beeping
            self.stop_continuous_beep()
            
            # Reset challenge state and start grace period
            self.challenge_in_progress = False
            self.start_grace_period()
            
            # Close challenge window
            if self.challenge_window and self.challenge_window.winfo_exists():
                self.challenge_window.destroy()
                self.challenge_window = None
            
            # Success message
            success_msg = f"✅ Consciousness Verified!\n\n"
            success_msg += f"Response time: {response_time:.1f}s\n"
            success_msg += f"Current streak: {self.stats['current_streak']}\n"
            success_msg += f"Tolerance restored: +10 points\n"
            success_msg += f"Grace period: {self.settings['grace_period']} seconds"
            
            if response_time < 5:
                success_msg += "\n🚀 Lightning fast response!"
            elif response_time < 10:
                success_msg += "\n👍 Good response time!"
            else:
                success_msg += "\n⚠️ Try to respond faster next time!"
                
            messagebox.showinfo("Challenge Complete!", success_msg)
                
            # Reset activity tracking
            self.reset_activity_tracking()
            self.update_stats_display()
            self.save_stats()
        except Exception as e:
            print(f"Error in challenge success: {e}")
            self.challenge_in_progress = False
        
    def challenge_failure(self):
        """Handle challenge failure - HARSHER PENALTIES"""
        try:
            self.stats['current_streak'] = 0
            self.tolerance_level = max(0, self.tolerance_level - 20)  # Increased penalty
            
            if hasattr(self, 'challenge_entry') and self.challenge_entry.winfo_exists():
                # Flash the entry red
                original_bg = self.challenge_entry.cget('bg')
                self.challenge_entry.config(bg="#FF5252")
                self.challenge_window.after(200, lambda: self.challenge_entry.config(bg="white") if self.challenge_entry.winfo_exists() else None)
                self.challenge_window.after(400, lambda: self.challenge_entry.config(bg="#FF5252") if self.challenge_entry.winfo_exists() else None)
                self.challenge_window.after(600, lambda: self.challenge_entry.config(bg="white") if self.challenge_entry.winfo_exists() else None)
                
                messagebox.showwarning(
                    "❌ INCORRECT!", 
                    "Wrong code! FOCUS and try again.\n\n" +
                    "Tolerance decreased by 20 points!\n" +
                    "The challenge will get HARDER if you fail again!"
                )
                
                self.challenge_entry.delete(0, tk.END)
                self.challenge_entry.focus_force()
        except Exception as e:
            print(f"Error in challenge failure: {e}")
        
    def report_false_positive(self):
        """Handle false positive with adjusted settings"""
        try:
            print("False positive reported")
            
            self.stats['false_positives'] += 1
            self.tolerance_level = min(self.max_tolerance, self.tolerance_level + 15)  # Reduced from 30
            
            # Stop beeping
            self.stop_continuous_beep()
            
            # Adjust adaptive threshold
            if self.settings['adaptive_threshold']:
                self.settings['tolerance_decay'] = max(0.5, self.settings['tolerance_decay'] - 0.2)
            
            # Reset challenge state and start grace period
            self.challenge_in_progress = False
            self.start_grace_period()
            
            # Close challenge window
            if self.challenge_window and self.challenge_window.winfo_exists():
                self.challenge_window.destroy()
                self.challenge_window = None
                
            messagebox.showinfo(
                "Feedback Received", 
                "Thank you for the feedback!\n\n" +
                "• Tolerance increased by 15 points\n" +
                "• Sensitivity slightly adjusted\n" +
                "• Grace period activated\n\n" +
                "Note: The system remains aggressive to keep you focused!"
            )
                
            self.reset_activity_tracking()
            self.update_stats_display()
        except Exception as e:
            print(f"Error reporting false positive: {e}")
            self.challenge_in_progress = False
        
    def escalate_challenge(self):
        """Handle challenge timeout - SEVERE ESCALATION"""
        try:
            if not self.challenge_window or not self.challenge_window.winfo_exists():
                return
            
            self.challenge_window.destroy()
            self.challenge_window = None
            
            # Reset state first
            self.challenge_in_progress = False
                
            messagebox.showwarning(
                "⏰ TIME EXPIRED!", 
                "Challenge timeout! You were TOO SLOW!\n\n" +
                "Generating MUCH HARDER challenge...\n" +
                "💀 Next challenge will be EXTREME!"
            )
            
            self.zombie_incidents += 2  # Double penalty
            escalated_length = min(20, 10 + self.zombie_incidents)  # Much harder
            escalated_code = self.generate_challenge_code(escalated_length)
            
            # Small delay before showing new challenge
            self.root.after(500, lambda: self.show_challenge_window(
                escalated_code, 
                "ESCALATED: Maximum difficulty due to timeout!", 
                100
            ))
        except Exception as e:
            print(f"Error escalating challenge: {e}")
            self.challenge_in_progress = False
        
    def reset_activity_tracking(self):
        """Reset activity tracking"""
        self.last_activity = time.time()
        self.mouse_movements.clear()
        self.key_presses.clear()
        self.click_patterns.clear()
        self.scroll_patterns.clear()
        self.activity_buffer.clear()
        self.repetitive_actions = 0
        self.zombie_incidents = max(0, self.zombie_incidents - 1)
        self.zombie_onset_time = None
        
    def toggle_monitoring(self):
        """Toggle monitoring"""
        if self.is_active:
            self.stop_monitoring()
        else:
            self.start_monitoring()
            
    def start_monitoring(self):
        """Start monitoring"""
        self.is_active = True
        self.status_label.config(text="🟢 ACTIVE - AGGRESSIVE MODE", fg="#4caf50")
        self.toggle_btn.config(text="STOP MONITORING", bg="#da3633")
        
        self.reset_activity_tracking()
        self.tolerance_level = 30  # Start with low tolerance
        self.challenge_in_progress = False
        self.grace_period_end = 0
        
        messagebox.showinfo(
            "⚡ AGGRESSIVE Monitoring Started", 
            "🤖 ZombieCheck AGGRESSIVE MODE activated!\n\n" +
            "⚠️ WARNING: This mode is VERY strict!\n" +
            "• Idle detection: 15-60 seconds\n" +
            "• Low tolerance for distractions\n" +
            "• Faster challenge triggers\n" +
            "• Minimal grace periods\n\n" +
            "Stay focused or face the consequences!"
        )
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_active = False
        self.status_label.config(text="🔴 INACTIVE", fg="#da3633")
        self.toggle_btn.config(text="START MONITORING", bg="#238636")
        
        self.stop_continuous_beep()
        self.challenge_in_progress = False
        
        session_summary = f"📊 Session Summary:\n\n"
        session_summary += f"Total Interventions: {self.stats['today_interventions']}\n"
        session_summary += f"Successful responses: {self.stats['successful_detections']}\n"
        session_summary += f"False positives: {self.stats['false_positives']}\n"
        session_summary += f"Final tolerance: {self.tolerance_level:.0f}/100\n\n"
        
        if self.stats['today_interventions'] > 10:
            session_summary += "😴 You had trouble staying focused today!"
        elif self.stats['today_interventions'] > 5:
            session_summary += "😐 Room for improvement in focus!"
        else:
            session_summary += "😊 Good focus session!"
        
        messagebox.showinfo("Monitoring Stopped", session_summary)
        
    def trigger_test_challenge(self):
        """Trigger test challenge"""
        messagebox.showinfo(
            "🧪 Test Challenge", 
            "Testing AGGRESSIVE challenge system!\n\n" +
            "This will demonstrate:\n" +
            "• Continuous beeping alert\n" +
            "• Code entry challenge\n" +
            "• Real-time feedback\n" +
            "• Timer countdown\n\n" +
            "Get ready to TYPE FAST!"
        )
        
        test_code = self.generate_challenge_code(8)
        self.show_challenge_window(test_code, "TEST: Aggressive difficulty demonstration", 70)
        
    def update_tolerance_bar(self):
        """Update tolerance bar"""
        try:
            if not hasattr(self, 'tolerance_canvas') or not self.tolerance_canvas.winfo_exists():
                return
                
            self.tolerance_canvas.delete("all")
            canvas_width = self.tolerance_canvas.winfo_width()
            if canvas_width <= 1:
                canvas_width = 300
                
            self.tolerance_canvas.create_rectangle(0, 0, canvas_width, 10, fill="#21262d", outline="")
            
            bar_width = (self.tolerance_level / self.max_tolerance) * canvas_width
            
            # More aggressive color coding
            if self.tolerance_level > 60:
                color = "#4caf50"
            elif self.tolerance_level > 25:
                color = "#ff9800"
            else:
                color = "#da3633"
                
            if bar_width > 0:
                self.tolerance_canvas.create_rectangle(0, 0, bar_width, 10, fill=color, outline="")
                
            # Show grace period or tolerance
            if self.is_in_grace_period():
                remaining = int(self.grace_period_end - time.time())
                text = f"Grace: {remaining}s"
                color = "#4caf50"
            else:
                text = f"{self.tolerance_level:.0f}/100"
                if self.tolerance_level < 20:
                    text += " ⚠️"
                color = "white"
                
            self.tolerance_canvas.create_text(
                canvas_width//2, 5, 
                text=text, 
                fill=color, 
                font=("Segoe UI", 8, "bold")
            )
        except Exception as e:
            print(f"Error updating tolerance bar: {e}")
        
        if self.is_active:
            self.root.after(250, self.update_tolerance_bar)  # Update 4x per second
    
    def update_stats_display(self):
        """Update stats display"""
        try:
            if hasattr(self, 'perf_text') and self.perf_text.winfo_exists():
                self.perf_text.config(state="normal")
                self.perf_text.delete(1.0, tk.END)
                
                productivity_score = max(0, 100 - (self.stats['today_interventions'] * 8) + (self.stats['current_streak'] * 3))
                
                perf_stats = f"""
📈 Productivity Score: {productivity_score:.0f}/100
🎯 Interventions Today: {self.stats['today_interventions']}
✅ Successful Responses: {self.stats['successful_detections']}
❌ False Positives: {self.stats['false_positives']}
🛡️ Tolerance Saves: {self.stats['tolerance_saves']}
⚡ Current Streak: {self.stats['current_streak']}
                """
                
                self.perf_text.insert(1.0, perf_stats.strip())
                self.perf_text.config(state="disabled")
                
            if hasattr(self, 'stats_text') and self.stats_text.winfo_exists():
                self.stats_text.config(state="normal")
                self.stats_text.delete(1.0, tk.END)
                
                accuracy = 0
                if self.stats['total_interventions'] > 0:
                    accuracy = (self.stats['successful_detections'] / max(1, self.stats['total_interventions'])) * 100
                    
                grace_status = "Active" if self.is_in_grace_period() else "Inactive"
                grace_remaining = max(0, int(self.grace_period_end - time.time())) if self.is_in_grace_period() else 0
                    
                all_stats = f"""
🏆 LIFETIME STATISTICS

Total Interventions: {self.stats['total_interventions']}
Successful Detections: {self.stats['successful_detections']}
Detection Accuracy: {accuracy:.1f}%
False Positive Rate: {self.stats['false_positives']}/{self.stats['total_interventions']}

🔥 STREAKS & RECORDS
Longest Streak: {self.stats['longest_streak']}
Current Streak: {self.stats['current_streak']}
Average Response Time: {self.stats['avg_response_time']:.1f}s

🛡️ TOLERANCE SYSTEM
Tolerance Saves: {self.stats['tolerance_saves']}
Current Tolerance: {self.tolerance_level:.0f}/100
Grace Period: {grace_status} ({grace_remaining}s remaining)
Decay Rate: {self.settings['tolerance_decay']:.1f}/sec

⚙️ SYSTEM STATUS
Monitoring: {"🟢 Active" if self.is_active else "🔴 Inactive"}
Challenge in Progress: {"🟡 Yes" if self.challenge_in_progress else "🟢 No"}
Sensitivity: {self.settings['sensitivity'].upper()}
Gaming Mode: {"✅ Enabled" if self.settings['gaming_mode'] else "❌ Disabled"}
Nightmare Mode: {"✅ Enabled" if self.settings['nightmare_mode'] else "❌ Disabled"}
Adaptive Learning: {"✅ Enabled" if self.settings['adaptive_threshold'] else "❌ Disabled"}
                """
                
                self.stats_text.insert(1.0, all_stats.strip())
                self.stats_text.config(state="disabled")
        except Exception as e:
            print(f"Error updating stats display: {e}")
            
    # Settings update methods
    def update_sensitivity(self, event=None):
        self.settings['sensitivity'] = self.sensitivity_var.get()
        self.save_stats()
        
    def update_nightmare_mode(self):
        self.settings['nightmare_mode'] = self.nightmare_var.get()
        self.save_stats()
        
    def update_gaming_mode(self):
        self.settings['gaming_mode'] = self.gaming_var.get()
        self.save_stats()
        
    def update_adaptive_mode(self):
        self.settings['adaptive_threshold'] = self.adaptive_var.get()
        self.save_stats()
        
    def update_visual_setting(self):
        self.settings['visual_warnings'] = self.visual_var.get()
        self.save_stats()
        
    def update_grace_period(self):
        """Update grace period setting"""
        try:
            self.settings['grace_period'] = int(self.grace_var.get())
            self.save_stats()
        except ValueError:
            self.settings['grace_period'] = 30  # Default
        
    def load_stats(self):
        """Load stats from file"""
        try:
            if os.path.exists('zombie_stats.json'):
                with open('zombie_stats.json', 'r') as f:
                    data = json.load(f)
                    self.stats.update(data.get('stats', {}))
                    # Don't override aggressive defaults with saved settings
                    saved_settings = data.get('settings', {})
                    # Only load certain settings
                    if 'nightmare_mode' in saved_settings:
                        self.settings['nightmare_mode'] = saved_settings['nightmare_mode']
                    if 'gaming_mode' in saved_settings:
                        self.settings['gaming_mode'] = saved_settings['gaming_mode']
                    if 'visual_warnings' in saved_settings:
                        self.settings['visual_warnings'] = saved_settings['visual_warnings']
                    # Keep aggressive defaults for other settings
                    self.tolerance_level = min(30, data.get('tolerance_level', 30))
        except Exception as e:
            print(f"Error loading stats: {e}")
            
    def save_stats(self):
        """Save stats to file"""
        try:
            data = {
                'stats': self.stats,
                'settings': self.settings,
                'tolerance_level': self.tolerance_level,
                'last_updated': datetime.now().isoformat(),
                'version': '2.2-aggressive'
            }
            with open('zombie_stats.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")
            
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        welcome_msg = """🎉 Welcome to ZombieCheck v2.2 - AGGRESSIVE MODE!

⚡ AGGRESSIVE FEATURES:
• ⏱️ 15-60 second idle detection (super fast!)
• 🎯 Hair-trigger pattern detection
• 📉 Low starting tolerance (30/100)
• ⚠️ Faster tolerance decay (3x speed)
• 🔊 Continuous beeping alerts
• 📝 Harder challenges with strict timing
• 🚀 Minimal grace periods (30 sec default)

🔥 ENHANCED CAPTCHA SYSTEM:
• Better code visibility with spacing
• Real-time typing feedback
• Character-by-character validation
• Clearer fonts (Courier New)
• Instant response on correct entry
• Support for typing with/without spaces

⚠️ WARNING: This version is VERY aggressive!
It will interrupt you frequently to ensure maximum focus.

💡 TIP: Adjust sensitivity in settings if it's too strict!"""

        messagebox.showinfo("Welcome to ZombieCheck AGGRESSIVE v2.2", welcome_msg)
        
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing"""
        if self.is_active:
            self.stop_monitoring()
        self.save_stats()
        self.stop_continuous_beep()
        self.root.destroy()

if __name__ == "__main__":
    try:
        app = ZombieCheck()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        input("Press Enter to exit...")import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import string
import json
import os
import winsound  # For Windows beep sounds
import platform
from datetime import datetime, timedelta
import sys
from collections import deque
import math

class ZombieCheck:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ZombieCheck - Anti-Mindless-Browsing App 🧟‍♂️")
        self.root.geometry("500x700")
        self.root.configure(bg="#0d1117")
        
        # Enhanced app state
        self.is_active = False
        self.monitoring_thread = None
        self.challenge_window = None
        self.last_activity = time.time()
        self.activity_buffer = deque(maxlen=100)
        self.zombie_incidents = 0
        self.challenge_start_time = None
        self.zombie_onset_time = None
        self.stop_beeping_event = None
        self.beeping_thread = None
        self.challenge_in_progress = False
        self.grace_period_end = 0
        
        # Enhanced activity tracking
        self.mouse_movements = deque(maxlen=50)
        self.key_presses = deque(maxlen=50)
        self.click_patterns = deque(maxlen=30)
        self.scroll_patterns = deque(maxlen=30)
        self.window_switches = 0
        self.last_mouse_pos = (0, 0)
        self.repetitive_actions = 0
        
        # Tolerance system - REDUCED FOR FASTER DETECTION
        self.tolerance_level = 30  # Reduced from 50
        self.max_tolerance = 100
        self.warning_given = False
        
        # Settings with MORE AGGRESSIVE OPTIONS
        self.settings = {
            'sensitivity': 'medium',
            'tolerance_decay': 0.8,  # Reduced from 1.5 for slower decay
            'nightmare_mode': False,
            'gaming_mode': False,
            'visual_warnings': True,
            'adaptive_threshold': True,
            'grace_period': 30
        }
        
        # Enhanced stats
        self.stats = {
            'total_interventions': 0,
            'today_interventions': 0,
            'longest_streak': 0,
            'current_streak': 0,
            'avg_response_time': 0,
            'false_positives': 0,
            'successful_detections': 0,
            'tolerance_saves': 0,
            'daily_productivity_score': 100
        }
        
        self.load_stats()
        self.create_enhanced_interface()
        self.setup_global_activity_tracking()
        
    def create_enhanced_interface(self):
        """Create the enhanced UI with modern design"""
        # Custom colors
        bg_primary = "#0d1117"
        bg_secondary = "#161b22"
        bg_tertiary = "#21262d"
        accent_green = "#238636"
        accent_red = "#da3633"
        accent_orange = "#fd7e14"
        text_primary = "#f0f6fc"
        text_secondary = "#8b949e"
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=bg_primary)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title section with improved styling
        title_frame = tk.Frame(main_container, bg=bg_primary)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="🧟‍♂️ ZombieCheck", 
            font=("Segoe UI", 28, "bold"),
            fg=accent_green,
            bg=bg_primary
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Aggressive Anti-Mindless-Browsing Protection",
            font=("Segoe UI", 11),
            fg=text_secondary,
            bg=bg_primary
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Status section with enhanced visual feedback
        status_frame = tk.Frame(main_container, bg=bg_secondary, relief="solid", bd=1)
        status_frame.pack(fill="x", pady=(0, 20))
        
        status_inner = tk.Frame(status_frame, bg=bg_secondary)
        status_inner.pack(fill="x", padx=20, pady=15)
        
        self.status_label = tk.Label(
            status_inner,
            text="🔴 INACTIVE",
            font=("Segoe UI", 16, "bold"),
            fg=accent_red,
            bg=bg_secondary
        )
        self.status_label.pack()
        
        # Tolerance bar
        tolerance_frame = tk.Frame(status_inner, bg=bg_secondary)
        tolerance_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(
            tolerance_frame,
            text="Tolerance Level:",
            font=("Segoe UI", 10),
            fg=text_secondary,
            bg=bg_secondary
        ).pack(anchor="w")
        
        self.tolerance_canvas = tk.Canvas(tolerance_frame, height=10, bg=bg_tertiary, highlightthickness=0)
        self.tolerance_canvas.pack(fill="x", pady=(5, 0))
        
        # Control section
        control_frame = tk.Frame(main_container, bg=bg_primary)
        control_frame.pack(fill="x", pady=(0, 20))
        
        button_frame = tk.Frame(control_frame, bg=bg_primary)
        button_frame.pack()
        
        self.toggle_btn = tk.Button(
            button_frame,
            text="START MONITORING",
            font=("Segoe UI", 12, "bold"),
            bg=accent_green,
            fg="white",
            command=self.toggle_monitoring,
            width=18,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        self.toggle_btn.pack(side="left", padx=(0, 10))
        
        test_btn = tk.Button(
            button_frame,
            text="Test Challenge",
            font=("Segoe UI", 10),
            bg=accent_orange,
            fg="white",
            command=self.trigger_test_challenge,
            width=15,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        test_btn.pack(side="left")
        
        # Notebook for organized sections
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill="both", expand=True)
        
        # Stats tab
        stats_frame = tk.Frame(notebook, bg=bg_secondary)
        notebook.add(stats_frame, text="📊 Statistics")
        
        self.create_stats_section(stats_frame, bg_secondary, text_primary, text_secondary)
        
        # Settings tab
        settings_frame = tk.Frame(notebook, bg=bg_secondary)
        notebook.add(settings_frame, text="⚙️ Settings")
        
        self.create_settings_section(settings_frame, bg_secondary, text_primary, text_secondary, accent_green)
        
        # Detection Info tab
        info_frame = tk.Frame(notebook, bg=bg_secondary)
        notebook.add(info_frame, text="🔍 Detection Info")
        
        self.create_detection_info_section(info_frame, bg_secondary, text_primary, text_secondary)
        
        self.update_tolerance_bar()
        self.update_stats_display()
        
    def create_stats_section(self, parent, bg_color, text_primary, text_secondary):
        """Create enhanced stats section"""
        stats_container = tk.Frame(parent, bg=bg_color)
        stats_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Today's performance
        perf_frame = tk.LabelFrame(
            stats_container, 
            text="Today's Performance", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        perf_frame.pack(fill="x", pady=(0, 15))
        
        self.perf_text = tk.Text(
            perf_frame,
            height=6,
            font=("Consolas", 10),
            bg="#0d1117",
            fg="#58a6ff",
            insertbackground="#58a6ff",
            selectbackground="#264f78",
            relief="flat",
            padx=10,
            pady=10
        )
        self.perf_text.pack(fill="x", padx=10, pady=10)
        
        # All-time stats
        alltime_frame = tk.LabelFrame(
            stats_container, 
            text="All-Time Statistics", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        alltime_frame.pack(fill="both", expand=True)
        
        self.stats_text = tk.Text(
            alltime_frame,
            font=("Consolas", 10),
            bg="#0d1117",
            fg="#58a6ff",
            insertbackground="#58a6ff",
            selectbackground="#264f78",
            relief="flat",
            padx=10,
            pady=10
        )
        self.stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_settings_section(self, parent, bg_color, text_primary, text_secondary, accent_color):
        """Create enhanced settings section"""
        settings_container = tk.Frame(parent, bg=bg_color)
        settings_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Detection Settings
        detection_frame = tk.LabelFrame(
            settings_container, 
            text="Detection Settings", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        detection_frame.pack(fill="x", pady=(0, 15))
        
        # Sensitivity
        sens_frame = tk.Frame(detection_frame, bg=bg_color)
        sens_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(sens_frame, text="Sensitivity Level:", bg=bg_color, fg=text_primary, font=("Segoe UI", 10)).pack(anchor="w")
        
        self.sensitivity_var = tk.StringVar(value=self.settings['sensitivity'])
        sens_menu = ttk.Combobox(
            sens_frame, 
            textvariable=self.sensitivity_var,
            values=['low', 'medium', 'high', 'extreme'],
            state="readonly",
            width=15
        )
        sens_menu.pack(anchor="w", pady=(5, 0))
        sens_menu.bind('<<ComboboxSelected>>', self.update_sensitivity)
        
        # Grace Period Setting
        grace_frame = tk.Frame(detection_frame, bg=bg_color)
        grace_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(grace_frame, text="Grace Period (seconds after challenge):", bg=bg_color, fg=text_primary, font=("Segoe UI", 10)).pack(anchor="w")
        
        self.grace_var = tk.StringVar(value=str(self.settings['grace_period']))
        grace_spinbox = tk.Spinbox(
            grace_frame,
            from_=10,
            to=120,
            increment=10,
            textvariable=self.grace_var,
            width=10,
            command=self.update_grace_period
        )
        grace_spinbox.pack(anchor="w", pady=(5, 0))
        
        # Checkboxes with better styling
        checkbox_frame = tk.Frame(detection_frame, bg=bg_color)
        checkbox_frame.pack(fill="x", padx=10, pady=10)
        
        self.adaptive_var = tk.BooleanVar(value=self.settings['adaptive_threshold'])
        adaptive_cb = tk.Checkbutton(
            checkbox_frame,
            text="Adaptive Learning (Learns your patterns)",
            variable=self.adaptive_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_adaptive_mode
        )
        adaptive_cb.pack(anchor="w", pady=2)
        
        self.nightmare_var = tk.BooleanVar(value=self.settings['nightmare_mode'])
        nightmare_cb = tk.Checkbutton(
            checkbox_frame,
            text="Nightmare Mode (Extra challenging codes)",
            variable=self.nightmare_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_nightmare_mode
        )
        nightmare_cb.pack(anchor="w", pady=2)
        
        self.gaming_var = tk.BooleanVar(value=self.settings['gaming_mode'])
        gaming_cb = tk.Checkbutton(
            checkbox_frame,
            text="Gaming Mode (Reduced interruptions)",
            variable=self.gaming_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_gaming_mode
        )
        gaming_cb.pack(anchor="w", pady=2)
        
        # Alerts (Visual only)
        av_frame = tk.LabelFrame(
            settings_container, 
            text="Alerts", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        av_frame.pack(fill="x", pady=(0, 15))
        
        av_checkbox_frame = tk.Frame(av_frame, bg=bg_color)
        av_checkbox_frame.pack(fill="x", padx=10, pady=10)
        
        self.visual_var = tk.BooleanVar(value=self.settings['visual_warnings'])
        visual_cb = tk.Checkbutton(
            av_checkbox_frame,
            text="Visual Warnings (Warning before challenge)",
            variable=self.visual_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_visual_setting
        )
        visual_cb.pack(anchor="w", pady=2)
        
    def create_detection_info_section(self, parent, bg_color, text_primary, text_secondary):
        """Create section explaining how zombie detection works"""
        info_container = tk.Frame(parent, bg=bg_color)
        info_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a frame for text and scrollbar
        text_frame = tk.Frame(info_container, bg=bg_color)
        text_frame.pack(fill="both", expand=True)
        
        # Scrollable text widget
        info_text = tk.Text(
            text_frame,
            font=("Segoe UI", 10),
            bg="#0d1117",
            fg=text_primary,
            insertbackground=text_primary,
            selectbackground="#264f78",
            relief="flat",
            padx=15,
            pady=15,
            wrap="word"
        )
        info_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=info_text.yview)
        scrollbar.pack(side="right", fill="y")
        info_text.configure(yscrollcommand=scrollbar.set)
        
        detection_info = """🔍 AGGRESSIVE ZOMBIE DETECTION (v2.2)

⚡ REDUCED TOLERANCE TIMINGS:

📊 ACTIVITY PATTERNS MONITORED:
• Mouse Movement: Detects aimless movements in 10 seconds
• Clicking Behavior: Rapid clicking triggers in 5 seconds
• Keyboard Activity: No typing for 20 seconds = warning
• Scroll Patterns: Mindless scrolling detected in 8 seconds
• Idle Detection: Triggers after just 30 seconds of inactivity

🧠 AGGRESSIVE TOLERANCE SYSTEM:
• Starting Level: 30/100 (reduced from 50)
• Decay Rate: 1.5 points/second (3x faster)
• Recovery: Slower tolerance gain
• Saves: Less forgiving of zombie behavior

⚡ QUICK DETECTION TRIGGERS:

1. IDLE DETECTION (MUCH FASTER):
   • Low Sensitivity: 60 seconds
   • Medium Sensitivity: 45 seconds  
   • High Sensitivity: 30 seconds
   • Extreme Sensitivity: 15 seconds (NEW!)
   • Gaming Mode: Only 2x threshold (reduced buffer)

2. MINDLESS BEHAVIOR (HAIR-TRIGGER):
   • Repetitive Actions: >5 times = instant trigger
   • Aimless Movement: Detected in 5 seconds
   • Rapid Switching: 3 switches = alert
   • Scroll Zombie: 3 seconds of scrolling
   • Click Spam: 5 rapid clicks = challenge

3. PATTERN ANALYSIS:
   • Smaller Activity Buffer (last 50 events)
   • Aggressive Trend Analysis
   • Minimal False Positive Prevention
   • Quick Learning Mode

🎯 SENSITIVITY LEVELS:

• LOW: 60 second idle threshold
• MEDIUM: 45 second idle threshold
• HIGH: 30 second idle threshold (DEFAULT)
• EXTREME: 15 second idle threshold (NEW!)

🔊 ALERT SYSTEM:
• Visual Warning: 5-second warning (reduced)
• Continuous Beeping Until Challenge Solved
• Modal Challenge Window (cannot be ignored)
• Harder Escalation for Failures

🛡️ REDUCED GRACE PERIOD:
• Default: 30 seconds (reduced from 60)
• Minimum: 10 seconds
• Maximum: 120 seconds
• Quick re-activation after grace

📈 FEEDBACK SYSTEM:
• Faster Response Required
• Lower Tolerance for Errors
• Aggressive Pattern Learning
• Minimal Forgiveness

⚠️ WARNING: This version is much more aggressive and will interrupt you frequently to ensure you stay focused!"""

        info_text.insert("1.0", detection_info)
        info_text.config(state="disabled")
        
    def setup_global_activity_tracking(self):
        """Setup global activity tracking"""
        self.root.bind('<Motion>', self.on_mouse_move)
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<Button-1>', self.on_click)
        self.root.bind('<Button-3>', self.on_click)
        self.root.bind('<MouseWheel>', self.on_scroll)
        self.root.focus_set()
        
        # Start periodic activity analysis
        self.analyze_activity_patterns()
        
    def on_mouse_move(self, event):
        """Track mouse movement patterns"""
        current_time = time.time()
        current_pos = (event.x_root, event.y_root)
        
        # Calculate movement distance
        if self.last_mouse_pos:
            distance = math.sqrt(
                (current_pos[0] - self.last_mouse_pos[0])**2 + 
                (current_pos[1] - self.last_mouse_pos[1])**2
            )
        else:
            distance = 0
            
        self.mouse_movements.append({
            'time': current_time,
            'pos': current_pos,
            'distance': distance
        })
        
        self.last_mouse_pos = current_pos
        self.record_activity('mouse_move', current_time)
        
    def on_key_press(self, event):
        """Track keyboard activity with improved detection"""
        current_time = time.time()
        
        # Don't record key events if challenge window is active
        if not hasattr(self, 'challenge_window') or not self.challenge_window.winfo_exists():
            self.key_presses.append({
                'time': current_time,
                'key': event.keysym
            })
            self.record_activity('key_press', current_time)
        
    def on_click(self, event):
        """Track click patterns"""
        current_time = time.time()
        self.click_patterns.append({
            'time': current_time,
            'button': event.num,
            'pos': (event.x_root, event.y_root)
        })
        self.record_activity('click', current_time)
        
    def on_scroll(self, event):
        """Track scroll patterns"""
        current_time = time.time()
        self.scroll_patterns.append({
            'time': current_time,
            'delta': event.delta
        })
        self.record_activity('scroll', current_time)
        
    def record_activity(self, activity_type, timestamp):
        """Record activity in the activity buffer"""
        self.last_activity = timestamp
        self.activity_buffer.append({
            'type': activity_type,
            'time': timestamp
        })
        
        # REDUCED tolerance gain for good activity
        if activity_type == 'key_press':
            self.tolerance_level = min(self.max_tolerance, self.tolerance_level + 0.2)  # Reduced from 0.5
        
    def is_in_grace_period(self):
        """Check if we're still in grace period after a challenge"""
        return time.time() < self.grace_period_end
    
    def start_grace_period(self):
        """Start grace period after successful challenge"""
        self.grace_period_end = time.time() + self.settings['grace_period']
        print(f"Grace period started for {self.settings['grace_period']} seconds")
        
    def analyze_activity_patterns(self):
        """AGGRESSIVE activity pattern analysis"""
        try:
            if not self.is_active:
                self.root.after(500, self.analyze_activity_patterns)  # Faster checking
                return
                
            # Skip analysis if challenge is in progress or in grace period
            if self.challenge_in_progress or self.is_in_grace_period():
                self.root.after(500, self.analyze_activity_patterns)
                return
                
            current_time = time.time()
            
            # Check idle time - MUCH MORE AGGRESSIVE
            idle_time = current_time - self.last_activity
            
            # Get threshold based on sensitivity
            idle_threshold = self.get_idle_threshold()
            
            # Immediate alarm for idle threshold
            if idle_time >= idle_threshold:
                self.trigger_intelligent_challenge(
                    [f"No activity for {int(idle_time)} seconds!"], 
                    100  # Maximum zombie score
                )
                self.root.after(500, self.analyze_activity_patterns)
                return
            
            # Check for various zombie patterns - MORE AGGRESSIVE
            zombie_score = 0
            reasons = []
            
            # 1. Check for repetitive actions - LOWER THRESHOLD
            repetitive_score = self.check_repetitive_actions()
            if repetitive_score > 0.5:  # Reduced from 0.7
                zombie_score += 40
                reasons.append("Repetitive actions detected")
                
            # 2. Check for aimless movement - LOWER THRESHOLD
            aimless_score = self.check_aimless_movement()
            if aimless_score > 0.4:  # Reduced from 0.6
                zombie_score += 35
                reasons.append("Aimless mouse movement")
                
            # 3. Check for rapid switching - LOWER THRESHOLD
            switch_score = self.check_rapid_switching()
            if switch_score > 0.5:  # Reduced from 0.8
                zombie_score += 40
                reasons.append("Rapid clicking/switching")
                
            # 4. Check for scroll zombie behavior - LOWER THRESHOLD
            scroll_score = self.check_scroll_zombie()
            if scroll_score > 0.4:  # Reduced from 0.7
                zombie_score += 35
                reasons.append("Mindless scrolling")
                
            # 5. Add score for any idle time over 10 seconds
            if idle_time > 10:
                zombie_score += min(50, idle_time * 2)
                if idle_time > 20:
                    reasons.append(f"Idle for {idle_time:.0f} seconds")
            
            # Track sustained mindless behavior - REDUCED TIME
            if zombie_score > 40:  # Reduced from 50
                if self.zombie_onset_time is None:
                    self.zombie_onset_time = current_time
                elif current_time - self.zombie_onset_time >= 15:  # Reduced from 60 seconds
                    self.trigger_intelligent_challenge(
                        reasons or ["Sustained mindless behavior"], 
                        max(zombie_score, 80)
                    )
                    self.zombie_onset_time = None
                    self.root.after(500, self.analyze_activity_patterns)
                    return
            else:
                self.zombie_onset_time = None
                    
            # Apply tolerance system - MORE AGGRESSIVE
            if zombie_score > 35:  # Reduced from 50
                if self.tolerance_level > 20:  # Reduced from 30
                    # Use tolerance but deplete it faster
                    self.tolerance_level -= zombie_score * 0.8  # Increased from 0.5
                    self.stats['tolerance_saves'] += 1
                    if self.settings['visual_warnings'] and not self.warning_given:
                        self.show_warning(reasons)
                        self.warning_given = True
                else:
                    # Trigger challenge
                    self.trigger_intelligent_challenge(reasons, zombie_score)
                    
            # FASTER tolerance decay over time
            self.tolerance_level = max(0, self.tolerance_level - self.settings['tolerance_decay'])
            self.update_tolerance_bar()
        except Exception as e:
            print(f"Error in analyze_activity_patterns: {e}")
            
        # Schedule next analysis - FASTER
        self.root.after(500, self.analyze_activity_patterns)  # Check every 0.5 seconds
        
    def check_repetitive_actions(self):
        """Check for repetitive actions - MORE SENSITIVE"""
        if len(self.activity_buffer) < 5:  # Reduced from 10
            return 0
            
        recent_activities = list(self.activity_buffer)[-10:]
        activity_types = [a['type'] for a in recent_activities]
        
        # Count consecutive same activities
        max_consecutive = 0
        current_consecutive = 1
        
        for i in range(1, len(activity_types)):
            if activity_types[i] == activity_types[i-1]:
                current_consecutive += 1
            else:
                max_consecutive = max(max_consecutive, current_consecutive)
                current_consecutive = 1
                
        return min(1.0, max_consecutive / 5.0)  # Reduced from 15.0
        
    def check_aimless_movement(self):
        """Check for aimless mouse movement - MORE SENSITIVE"""
        if len(self.mouse_movements) < 5:  # Reduced from 10
            return 0
            
        recent_moves = list(self.mouse_movements)[-10:]
        total_distance = sum(move['distance'] for move in recent_moves)
        time_span = recent_moves[-1]['time'] - recent_moves[0]['time'] if len(recent_moves) > 1 else 1
        
        if time_span < 0.5:  # Reduced from 1
            return 0
            
        # High movement with low keyboard activity suggests aimless browsing
        recent_keys = [a for a in self.activity_buffer if a['type'] == 'key_press' and a['time'] > recent_moves[0]['time']]
        
        movement_rate = total_distance / max(time_span, 0.1)
        key_rate = len(recent_keys) / max(time_span, 0.1)
        
        if movement_rate > 50 and key_rate < 1:  # More sensitive thresholds
            return min(1.0, movement_rate / 200.0)  # Reduced from 500.0
            
        return 0
        
    def check_rapid_switching(self):
        """Check for rapid clicking/switching - MORE SENSITIVE"""
        if len(self.click_patterns) < 3:  # Reduced from 5
            return 0
            
        recent_clicks = list(self.click_patterns)[-5:]  # Reduced from -10
        if len(recent_clicks) < 3:
            return 0
            
        time_span = recent_clicks[-1]['time'] - recent_clicks[0]['time'] if len(recent_clicks) > 1 else 1
        click_rate = len(recent_clicks) / max(time_span, 0.1)
        
        return min(1.0, max(0, (click_rate - 1) / 2.0))  # More sensitive
        
    def check_scroll_zombie(self):
        """Check for mindless scrolling - MORE SENSITIVE"""
        if len(self.scroll_patterns) < 3:  # Reduced from 5
            return 0
            
        recent_scrolls = list(self.scroll_patterns)[-8:]  # Reduced from -15
        if len(recent_scrolls) < 3:
            return 0
            
        time_span = recent_scrolls[-1]['time'] - recent_scrolls[0]['time'] if len(recent_scrolls) > 1 else 1
        scroll_rate = len(recent_scrolls) / max(time_span, 0.1)
        
        # Check for continuous scrolling without pauses
        gaps = []
        for i in range(1, len(recent_scrolls)):
            gaps.append(recent_scrolls[i]['time'] - recent_scrolls[i-1]['time'])
            
        avg_gap = sum(gaps) / len(gaps) if gaps else 1
        
        if scroll_rate > 1 and avg_gap < 1:  # More sensitive
            return min(1.0, scroll_rate / 3.0)  # Reduced from 5.0
            
        return 0
        
    def get_idle_threshold(self):
        """Get AGGRESSIVE idle threshold"""
        base_thresholds = {
            'low': 60,      # Reduced from 300
            'medium': 45,   # Reduced from 180
            'high': 30,     # Reduced from 120
            'extreme': 15   # New extreme mode