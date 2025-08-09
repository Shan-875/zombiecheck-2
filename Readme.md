# ZombieCheck - The Anti-Mindless-Browsing App 🧟‍♂️⚡

## Basic Details
### Team Name: null pointers
### Team Members
- Team Lead: Shan V Varghese - College of Engineering Munnar
- Member 2: Jagannath P S - College of Engineering Munnar

### Project Description
ZombieCheck is a Python-based desktop application that detects when you're mindlessly browsing or being unproductive and forces you to prove consciousness by typing random codes to continue.

### The Problem (that doesn't exist)
People are turning into digital zombies! They mindlessly scroll through social media, stare blankly at screens, and lose hours without realizing it. The modern epidemic of unconscious browsing is creating a generation of productivity zombies who need intervention to regain awareness.

### The Solution (that nobody asked for)
A vigilant desktop guardian that monitors your behavior patterns and interrupts zombie-like activities with mandatory consciousness verification challenges. It's like having a strict teacher who randomly asks "Are you paying attention?" but for your entire digital life!

## Technical Details

### Technologies/Components Used
For Software:
- **Language:** Python 3.7+
- **GUI Framework:** Tkinter (built-in)
- **Threading:** For background monitoring
- **JSON:** For data persistence
- **Libraries:**
  - `threading` - Background monitoring
  - `time` - Activity tracking
  - `random` - Code generation
  - `string` - Character sets
  - `json` - Stats storage
  - `os` - File operations
  - `datetime` - Time tracking
  - `tkinter` - GUI components

### Implementation

#### Installation
```bash
# Clone the repository
git clone https://https://github.com/Shan-875/zombiecheck-2
cd zombiecheck-2

# No additional dependencies needed - uses built-in Python libraries!
# Just ensure you have Python 3.7+ installed
python --version


```

#### Run
```bash
pip install -r requirment.txt
# Run the application
python app.py

# Or on some systems
python3 app.py
```

### Project Documentation

#### Architecture Overview
```
ZombieCheck Application Structure:

┌─────────────────────────────────────┐
│           Main GUI Thread           │
│  ┌─────────────────────────────────┐ │
│  │     Main Interface              │ │
│  │  - Control Panel                │ │
│  │  - Stats Display                │ │
│  │  - Settings Panel               │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│       Background Monitor Thread     │
│  ┌─────────────────────────────────┐ │
│  │   Activity Detection System     │ │
│  │  - Mouse Movement Tracking      │ │
│  │  - Keyboard Activity Monitor    │ │
│  │  - Idle Time Calculator         │ │
│  │  - Behavior Pattern Analysis    │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                    │
                    ▼ (When zombie detected)
┌─────────────────────────────────────┐
│        Challenge Window             │
│  ┌─────────────────────────────────┐ │
│  │     Code Challenge System       │ │
│  │  - Random Code Generator        │ │
│  │  - Input Validation             │ │
│  │  - Timer Countdown              │ │
│  │  - Escalation Logic             │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│         Stats & Persistence         │
│  ┌─────────────────────────────────┐ │
│  │      Data Management            │ │
│  │  - JSON File Storage            │ │
│  │  - Statistics Tracking          │ │
│  │  - Settings Persistence         │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### Key Features Breakdown:

**🔍 Detection System:**
- Monitors mouse movements and keyboard activity
- Tracks idle time with customizable thresholds
- Detects mindless behavior patterns (lots of mouse movement, few key presses)
- Adjustable sensitivity levels (Low: 5min, Medium: 3min, High: 2min)

**⚡ Challenge System:**
- Generates random 8-character codes (A-Z, 0-9, excluding confusing characters)
- Modal popup that can't be closed without correct code
- 30-second timer with escalation on timeout
- Nightmare mode increases code length with each incident

**📊 Statistics Tracking:**
- Daily and total intervention counts
- Focus streak tracking (longest and current)
- Average response time measurement
- Persistent storage in JSON format

**⚙️ Smart Features:**
- Gaming mode (doubles thresholds during intensive tasks)
- Sensitivity adjustment (high/medium/low)
- Nightmare mode (progressively harder challenges)
- Background monitoring with minimal resource usage

#### Screenshots

![Main Interface](screenshots/main_interface.png)
*Main ZombieCheck interface showing monitoring status, stats, and settings*

![Challenge Popup](screenshots/challenge_popup.png)
*Zombie detection challenge window with random code verification*

![Settings Panel](screenshots/settings_panel.png)
*Customizable settings for sensitivity, gaming mode, and nightmare mode*

#### Core Algorithm Flow:
```python
def monitor_behavior():
    while monitoring_active:
        check_idle_time()
        analyze_activity_patterns()
        
        if zombie_behavior_detected():
            trigger_challenge()
            wait_for_response()
            
            if correct_response():
                update_positive_stats()
                reset_monitoring()
            else:
                escalate_difficulty()
                retry_challenge()
```

#### File Structure:
```
zombiecheck/
├── zombie_check.py          # Main application file
├── zombie_stats.json        # Persistent stats storage (auto-generated)
├── README.md               # This file
├── screenshots/            # Application screenshots
│   ├── main_interface.png
│   ├── challenge_popup.png
│   └── settings_panel.png
└── requirements.txt        # Empty (uses built-in libraries only)
```

### Project Demo

#### Video Demo
[Demo Video Link](https://drive.google.com/file/d/1uyFdBC0fiOJHuXDZLzKU717I10dEae75/view?usp=drivesdk)
*Video demonstrates zombie detection triggers, challenge popups, successful code entry, and stats tracking*

#### Live Demo Scenarios:

**Scenario 1: Idle Detection**
```
User starts monitoring → Leaves computer idle for 3+ minutes → 
Challenge popup appears → User types "K7M9Q3X1" → 
Success message → Stats updated
```

**Scenario 2: Mindless Scrolling**
```
User scrolls repeatedly without typing → Detection algorithm triggers →
Warning popup with code "R5N8K2M7" → User enters wrong code →
Escalation with longer code → Correct entry → Awareness achieved
```

**Scenario 3: Nightmare Mode**
```
User enables nightmare mode → Gets caught multiple times →
Code length increases: 8 chars → 10 chars → 12 chars →
Progressively harder challenges until behavior improves
```

#### Additional Features:
- **Persistence**: All stats and settings saved automatically
- **Test Mode**: Manual challenge trigger for demonstration
- **Modal Design**: Challenge can't be dismissed without correct code
- **Visual Feedback**: Color-coded status indicators and clear messaging
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Team Contributions
- **Shan V Varghese**: Lead developer, core monitoring algorithm, GUI design, challenge system implementation, documentation
- **Jagannath P S**: Statistics tracking system, settings persistence, testing framework, user experience optimization

## Future Enhancements
- Browser integration for web-based zombie detection
- Machine learning for personalized zombie pattern recognition
- Mobile companion app
- Team challenges and leaderboards
- Integration with productivity tools (Pomodoro timers, task managers)
- Voice challenges for accessibility
- Customizable zombie detection rules

## Installation Requirements
- Python 3.7 or higher
- No additional packages required (uses only built-in libraries)
- 50MB free disk space
- Works on Windows, macOS, and Linux

## Usage Tips
1. **Start with medium sensitivity** to avoid over-interruption
2. **Enable gaming mode** when doing intensive work
3. **Use nightmare mode** only if you need extreme intervention
4. **Check stats regularly** to track improvement
5. **Test the challenge** first to understand the system

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--25-25?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)
