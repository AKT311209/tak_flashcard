# Application Flows & Logic

## 1. Application Startup Flow

```
┌─────────────────┐
│  Start App      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Check Database         │
│  (≥1000 words?)         │
└────────┬────────────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
  YES         NO
    │          │
    │          ▼
    │    ┌─────────────────────┐
    │    │  Import vocab_      │
    │    │  source.csv         │
    │    └─────────┬───────────┘
    │              │
    │              ▼
    │    ┌─────────────────────┐
    │    │  Show Progress      │
    │    │  Bar                │
    │    └─────────┬───────────┘
    │              │
    │         ┌────┴────┐
    │         │Success? │
    │         └────┬────┘
    │              │
    │         ┌────┴────┐
    │         │         │
    │         ▼         ▼
    │        YES       NO
    │         │         │
    │         │         ▼
    │         │   ┌──────────────┐
    │         │   │ Show Error & │
    │         │   │ Exit         │
    │         │   └──────────────┘
    │         │
    └─────────┘
         │
         ▼
┌─────────────────┐
│  Home Screen    │
└─────────────────┘
```

---

## 2. Home Screen Flow

```
┌──────────────────────────┐
│      Home Screen         │
│                          │
│  ┌─────────────────┐    │
│  │  [Flashcard]    │────┼─────▶ Flashcard Configuration
│  └─────────────────┘    │
│                          │
│  ┌─────────────────┐    │
│  │ [Dictionary]    │────┼─────▶ Dictionary View
│  └─────────────────┘    │
│                          │
│  ┌─────────────────┐    │
│  │    [Guide]      │────┼─────▶ Guide View
│  └─────────────────┘    │
│                          │
│  ┌─────────────────┐    │
│  │  [Settings]     │────┼─────▶ Settings View
│  └─────────────────┘    │
│                          │
│  ┌─────────────────┐    │
│  │    [Exit]       │────┼─────▶ Exit Application
│  └─────────────────┘    │
└──────────────────────────┘
```

---

## 3. Flashcard Settings Flow

```
┌──────────────────────────────────────┐
│   Flashcard Settings                 │
│                                      │
│  Select Mode:                        │
│  ◉ Endless  ○ Speed  ○ Testing      │
│                                      │
│  Select Direction:                   │
│  ◉ Eng→Vn  ○ Vn→Eng  ○ Mixed       │
│                                      │
│  Select Difficulty:                  │
│  1 ─────●─────────── 5              │
│  (Easy)          (Hard)              │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ Mode-Specific Options          │ │
│  │                                │ │
│  │ [Testing Mode]                 │ │
│  │ • Question Count: [___]        │ │
│  │                                │ │
│  │ [Speed Mode]                   │ │
│  │ • Time Limit (sec): [___]      │ │
│  │ • Show Answer: [✓]             │ │
│  │   - Penalty: ▼ Time Deduction  │ │
│  │                                │ │
│  │ [Endless Mode]                 │ │
│  │ • Show Answer: [✓]             │ │
│  │   - Penalty: ▼ Score Deduction │ │
│  └────────────────────────────────┘ │
│                                      │
│  [START SESSION]  [Back]             │
└──────────────────────────────────────┘
           │
           ▼
    Flashcard Session View
```

---

## 4. Flashcard Session Flow

### 4.1 General Flow (All Modes)

```
┌─────────────────────┐
│  Initialize Session │
│  • Load words       │
│  • Start timer (if  │
│    Speed mode)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Select Next Card   │◀──────────┐
│  Based on:          │           │
│  • Difficulty       │           │
│  • Direction        │           │
│  • Randomization    │           │
└──────────┬──────────┘           │
           │                      │
           ▼                      │
┌─────────────────────┐           │
│  Display Question   │           │
│  • Show word        │           │
│  • Increment        │           │
│    display_count    │           │
└──────────┬──────────┘           │
           │                      │
           ▼                      │
┌─────────────────────┐           │
│  User Input         │           │
│  • Type answer OR   │           │
│  • Select choice    │           │
│  • Show Answer (opt)├────┐      │
└──────────┬──────────┘    │      │
           │               │      │
           ▼               ▼      │
┌─────────────────┐ ┌──────────────┐
│  Submit Answer  │ │ Show Answer  │
└────────┬────────┘ │ Apply Penalty│
         │          └──────┬───────┘
         ▼                 │
┌─────────────────────┐    │
│  Validate Answer    │    │
│  • Compare input    │    │
│  • Update stats     │    │
└────────┬────────────┘    │
         │                 │
    ┌────┴─────┐           │
    │ Correct? │           │
    └────┬─────┘           │
         │                 │
    ┌────┴────┐            │
    │         │            │
    ▼         ▼            │
  YES        NO            │
    │         │            │
    ▼         ▼            │
┌────────┐ ┌────────┐     │
│ +Score │ │ -Score │     │
│+Correct│ │        │     │
└───┬────┘ └───┬────┘     │
    │          │          │
    └────┬─────┘          │
         │                │
         ▼                │
┌─────────────────────┐   │
│  Show Result        │   │
│  • Correct answer   │   │
│  • Current score    │   │
└──────────┬──────────┘   │
           │              │
           ▼              │
┌─────────────────────┐   │
│  Check End          │   │
│  Condition          │   │
└──────────┬──────────┘   │
           │              │
      ┌────┴────┐         │
      │  End?   │         │
      └────┬────┘         │
           │              │
      ┌────┴────┐         │
      │         │         │
      ▼         ▼         │
     YES       NO         │
      │         │         │
      │         └─────────┘
      │
      ▼
┌─────────────┐
│  Show Final │
│  Results    │
└─────────────┘
```

### 4.2 End Conditions by Mode

| Mode | End Condition |
|------|---------------|
| **Endless** | User clicks "Exit" or "Back" |
| **Speed** | Timer reaches 0 OR User exits |
| **Testing** | All questions answered OR User exits |

---

## 5. Flashcard Mode Specifics

### 5.1 Endless Mode Logic

```python
# Pseudo-code
while True:
    card = select_card_weighted(difficulty_setting, direction)
    show_question(card)
    
    if user_clicks_show_answer:
        apply_penalty(penalty_type)  # e.g., -10 points, -1 HP
        show_answer(card)
    
    answer = get_user_input()
    is_correct = validate_answer(answer, card)
    
    if is_correct:
        score += base_points
        card.correct_count += 1
    
    card.display_count += 1
    save_to_db(card)
    
    show_result(is_correct, card.answer)
    
    if user_clicks_exit:
        break
```

### 5.2 Speed Mode Logic

```python
# Pseudo-code
timer = TimeLimit  # e.g., 300 seconds
score = 0

while timer > 0:
    card = select_card_weighted(difficulty_setting, direction)
    show_question(card)
    
    start_time = current_time()
    
    if user_clicks_show_answer:
        apply_time_penalty()  # e.g., -10 seconds
        show_answer(card)
    
    answer = get_user_input()
    response_time = current_time() - start_time
    
    is_correct = validate_answer(answer, card)
    
    if is_correct:
        score += base_points + time_bonus(response_time)
        card.correct_count += 1
    else:
        score -= penalty_points
    
    card.display_count += 1
    save_to_db(card)
    
    show_result(is_correct, card.answer, score)
    
    timer -= response_time
    
    if user_clicks_exit:
        break

show_final_results(score, cards_answered)
```

### 5.3 Testing Mode Logic

```python
# Pseudo-code
total_questions = QuestionCount  # e.g., 20
current_question = 0
score = 0
results = []

cards = select_cards_weighted(total_questions, difficulty_setting, direction)

for card in cards:
    current_question += 1
    show_question(card, f"{current_question}/{total_questions}")
    
    answer = get_user_input()  # No Show Answer option
    is_correct = validate_answer(answer, card)
    
    if is_correct:
        score += base_points
        card.correct_count += 1
    
    card.display_count += 1
    save_to_db(card)
    
    results.append({
        'card': card,
        'user_answer': answer,
        'is_correct': is_correct
    })

show_final_results(score, results)
```

---

## 6. Direction Logic

### 6.1 Eng→Vn
- **Question:** Display English word
- **Expected Answer:** Vietnamese translation
- **Example:** "hello" → User types "xin chào"

### 6.2 Vn→Eng
- **Question:** Display Vietnamese word
- **Expected Answer:** English word
- **Example:** "xin chào" → User types "hello"

### 6.3 Mixed (Random)
- **Question:** Randomly choose Eng→Vn OR Vn→Eng
- **Implementation:**
  ```python
  if random.choice([True, False]):
      direction = "Eng→Vn"
  else:
      direction = "Vn→Eng"
  ```

---

## 7. Difficulty System

### 7.1 Word Difficulty Calculation

Each word has an individual difficulty score calculated as:

$$
difficulty = 1 - \frac{correct\_count}{display\_count + \epsilon}
$$

Where $\epsilon$ (epsilon) is a small value (e.g., 0.001) to avoid division by zero.

**Interpretation:**
- difficulty = 0: Always answered correctly (easiest)
- difficulty = 1: Never answered correctly (hardest)
- difficulty = 0.5: 50% accuracy

### 7.2 Difficulty Setting (User Selection: 1-5)

The user selects a difficulty level from 1 to 5, which controls the **proportion** of high-difficulty words:

| Setting | Behavior | Word Selection Bias |
|---------|----------|---------------------|
| 1 | Easiest | Heavily favor low-difficulty words |
| 2 | Easy | Slightly favor low-difficulty words |
| 3 | Balanced | Equal probability across all difficulties |
| 4 | Hard | Slightly favor high-difficulty words |
| 5 | Hardest | Heavily favor high-difficulty words |

### 7.3 Selection Probability (Weighted Random)

Instead of filtering words, we use **weighted random selection**:

```python
def calculate_selection_weight(word_difficulty, user_setting):
    """
    word_difficulty: 0-1 (word's calculated difficulty)
    user_setting: 1-5 (user's chosen difficulty level)
    """
    # Convert user_setting (1-5) to bias factor (-2 to +2)
    bias = (user_setting - 3)  # -2, -1, 0, 1, 2
    
    if bias < 0:  # Setting 1-2: Favor easy words
        # Lower word difficulty → higher weight
        weight = (1 - word_difficulty) ** abs(bias)
    elif bias > 0:  # Setting 4-5: Favor hard words
        # Higher word difficulty → higher weight
        weight = word_difficulty ** bias
    else:  # Setting 3: Balanced
        weight = 1.0  # All words equally likely
    
    return weight

# Example usage
words = get_all_words()
weights = [calculate_selection_weight(w.difficulty, user_setting) 
           for w in words]
selected_word = random.choices(words, weights=weights)[0]
```

**Examples:**
- User setting = 1, word difficulty = 0.1 (easy word) → High selection probability
- User setting = 1, word difficulty = 0.9 (hard word) → Low selection probability
- User setting = 5, word difficulty = 0.9 (hard word) → High selection probability
- User setting = 5, word difficulty = 0.1 (easy word) → Low selection probability
- User setting = 3 → All words have equal probability

### 7.4 Dynamic Updates

```python
# After each answer
word.display_count += 1
if is_correct:
    word.correct_count += 1

word.difficulty = 1 - (word.correct_count / (word.display_count + 0.001))
save_to_db(word)
```

---

## 8. Scoring System

### 8.1 Base Points

| Action | Points |
|--------|--------|
| Correct answer | +10 |
| Wrong answer | 0 or -5 (configurable) |
| Show Answer (Endless) | -10 penalty |
| Show Answer (Speed) | -10 seconds penalty |

### 8.2 Speed Mode Bonuses

```python
time_bonus = max(0, 10 - response_time)  # Faster response = more points
final_score = base_points + time_bonus
```

### 8.3 Testing Mode Score

```python
total_score = correct_count * base_points
percentage = (correct_count / total_questions) * 100
```

---

## 9. Penalty System

### 9.1 Penalty Types

| Penalty Type | Effect | Applicable Modes |
|--------------|--------|------------------|
| Score Deduction | -10 points per Show Answer | Endless, Speed |
| Time Deduction | -10 seconds per Show Answer | Speed |
| HP Limit | Max 3 Show Answer uses | Endless, Speed |

### 9.2 Implementation

```python
if penalty_type == "score":
    score -= 10
elif penalty_type == "time":
    remaining_time -= 10
elif penalty_type == "hp":
    show_answer_count += 1
    if show_answer_count >= 3:
        disable_show_answer_button()
```

---

## 10. Settings Flow

```
┌──────────────────────────────────────┐
│        Settings View                 │
│                                      │
│  ╔══════════════════════════════╗   │
│  ║  APPEARANCE                  ║   │
│  ╚══════════════════════════════╝   │
│                                      │
│  Theme:        [Light ▼]             │
│                                      │
│  Font Size:    [Medium ▼]            │
│                                      │
│  Window Size:  Width [800] Height [600]│
│                                      │
│  ╔══════════════════════════════╗   │
│  ║  DEFAULT SETTINGS            ║   │
│  ╚══════════════════════════════╝   │
│                                      │
│  Default Mode:       [Endless ▼]     │
│                                      │
│  Default Difficulty: 1 ───●──── 5    │
│                                      │
│  Question Count:     [20]            │
│                                      │
│  Time Limit (sec):   [300]           │
│                                      │
│  ╔══════════════════════════════╗   │
│  ║  PREFERENCES                 ║   │
│  ╚══════════════════════════════╝   │
│                                      │
│  Sound Effects:    [✓]               │
│                                      │
│  Animation Speed:  [Normal ▼]        │
│                                      │
│  ─────────────────────────────────   │
│                                      │
│  [Save & Apply]  [Reset to Default]  │
│                                      │
│  [Back to Home]                      │
└──────────────────────────────────────┘
```

### Settings Categories

#### 1. Appearance Settings
- **Theme**: Light / Dark / Custom
  - Changes color scheme across all views
  - Custom allows manual color selection
- **Font Size**: Small / Medium / Large
  - Affects all text elements in the app
- **Window Size**: Width and Height in pixels
  - Default: 800x600
  - Min: 640x480, Max: 1920x1080

#### 2. Default Settings
- **Default Mode**: Endless / Speed / Testing
  - Pre-selects mode in Flashcard configuration
- **Default Difficulty**: 1-5 slider
  - Pre-sets difficulty level
- **Question Count**: Number (10-100)
  - Default for Testing mode
- **Time Limit**: Seconds (60-600)
  - Default for Speed mode

#### 3. Preferences
- **Sound Effects**: Enable/Disable
  - Plays sounds on correct/wrong answers
  - Plays timer alarm
- **Animation Speed**: Fast / Normal / Slow / Off
  - Controls transition animations between views
  - Card flip animations

### Settings Persistence

```python
# core/settings.py
import json
import os
from pathlib import Path

SETTINGS_PATH = Path("data/user_settings.json")

DEFAULT_SETTINGS = {
    "appearance": {
        "theme": "light",
        "font_size": "medium",
        "window_width": 800,
        "window_height": 600
    },
    "defaults": {
        "flashcard_mode": "endless",
        "difficulty_level": 3,
        "question_count": 20,
        "time_limit": 300
    },
    "preferences": {
        "sound_enabled": False,
        "animation_speed": "normal"
    }
}

def load_settings():
    """Load user settings from JSON file"""
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_settings(settings):
    """Save user settings to JSON file"""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

def reset_settings():
    """Reset to default settings"""
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS
```

### Settings Application Flow

```
┌─────────────────┐
│  App Startup    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load Settings   │
│ from JSON       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Apply Settings  │
│ • Set theme     │
│ • Set font size │
│ • Set window    │
│   dimensions    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Home Screen     │
└─────────────────┘

    User clicks [Settings]
         │
         ▼
┌─────────────────────┐
│  Settings View      │
│  • Show current     │
│    values           │
│  • Allow edits      │
└────────┬────────────┘
         │
    User clicks [Save & Apply]
         │
         ▼
┌─────────────────────┐
│ Validate Settings   │
│ • Check ranges      │
│ • Check types       │
└────────┬────────────┘
         │
    ┌────┴────┐
    │ Valid?  │
    └────┬────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
   YES       NO
    │         │
    │         ▼
    │    ┌─────────────┐
    │    │ Show Error  │
    │    │ Message     │
    │    └──────┬──────┘
    │           │
    │           └───────┐
    │                   │
    ▼                   ▼
┌────────────────┐  (Stay in
│ Save to JSON   │   Settings)
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Apply Settings │
│ Immediately    │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Show Success   │
│ Message        │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Back to Home   │
└────────────────┘
```

### Settings Validation

```python
def validate_settings(settings):
    """Validate settings before saving"""
    errors = []
    
    # Appearance validation
    if settings['appearance']['theme'] not in ['light', 'dark', 'custom']:
        errors.append("Invalid theme selection")
    
    if settings['appearance']['font_size'] not in ['small', 'medium', 'large']:
        errors.append("Invalid font size")
    
    width = settings['appearance']['window_width']
    height = settings['appearance']['window_height']
    if not (640 <= width <= 1920 and 480 <= height <= 1080):
        errors.append("Window size out of valid range")
    
    # Defaults validation
    if settings['defaults']['flashcard_mode'] not in ['endless', 'speed', 'testing']:
        errors.append("Invalid flashcard mode")
    
    if not (1 <= settings['defaults']['difficulty_level'] <= 5):
        errors.append("Difficulty must be between 1 and 5")
    
    if not (10 <= settings['defaults']['question_count'] <= 100):
        errors.append("Question count must be between 10 and 100")
    
    if not (60 <= settings['defaults']['time_limit'] <= 600):
        errors.append("Time limit must be between 60 and 600 seconds")
    
    # Preferences validation
    if settings['preferences']['animation_speed'] not in ['fast', 'normal', 'slow', 'off']:
        errors.append("Invalid animation speed")
    
    return len(errors) == 0, errors
```

---

## 11. Dictionary Flow

```
┌──────────────────────────┐
│    Dictionary View       │
│                          │
│  Search: [_______] 🔍    │
│                          │
│  Filter:                 │
│  [All POS ▼] [Sort by ▼] │
│                          │
│  ┌────────────────────┐  │
│  │ Word List (Table)  │  │
│  │                    │  │
│  │ Eng | IPA | Vn | POS│ │
│  │ ──────────────────── │ │
│  │ hello│/həˈloʊ/│xin…│  │
│  │ world│/wɜrld/│thế…│   │
│  │ ...               │  │
│  └────────────────────┘  │
│                          │
│  [Back to Home]          │
└──────────────────────────┘
```

### Dictionary Features
- Display all vocabulary words
- Search by English or Vietnamese
- Filter by Part of Speech (noun, verb, adj, etc.)
- Sort by: Alphabetical, Difficulty (easy→hard or hard→easy), Display Count
- Show word statistics (difficulty score, display/correct counts)

---

## 12. Guide Flow

```
┌──────────────────────────┐
│      Guide View          │
│                          │
│  ┌────────────────────┐  │
│  │ Table of Contents  │  │
│  │ • Introduction     │  │
│  │ • Flashcard Modes  │  │
│  │ • Directions       │  │
│  │ • Difficulty       │  │
│  │ • Scoring          │  │
│  │ • Penalties        │  │
│  │ • Tips             │  │
│  └────────────────────┘  │
│                          │
│  [Scrollable Content]    │
│                          │
│  [Back to Home]          │
└──────────────────────────┘
```

### Guide Content Structure
1. **Introduction**
   - App purpose
   - Overview of features
2. **Flashcard Modes**
   - Endless: No time limit, practice mode
   - Speed: Timed challenges
   - Testing: Exam simulation with scoring
3. **Directions**
   - Eng→Vn: English to Vietnamese
   - Vn→Eng: Vietnamese to English
   - Mixed: Random combination
4. **Difficulty System**
   - How individual word difficulty is calculated
   - How difficulty setting (1-5) affects word selection probabilities
   - Setting 1 shows easier words more often
   - Setting 5 shows harder words more often
5. **Scoring Rules**
   - Point system
   - Bonuses and penalties
6. **Tips for Learning**
   - Best practices
   - Study recommendations

---

## 13. Navigation Map

```
                    ┌──────────────┐
                    │  Home Screen │
                    └───────┬──────┘
                            │
            ┌───────────────┼───────────────┬───────────────┐
            │               │               │               │
            ▼               ▼               ▼               ▼
    ┌───────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Flashcard │   │Dictionary│   │  Guide   │   │ Settings │
        │ Settings  │   │   View   │   │   View   │   │   View   │
    └─────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
          │              │              │              │
          ▼              │              │              │
    ┌───────────┐        │              │              │
    │ Flashcard │        │              │              │
    │  Session  │        │              │              │
    └─────┬─────┘        │              │              │
          │              │              │              │
          ▼              │              │              │
    ┌───────────┐        │              │              │
    │  Results  │        │              │              │
    │   View    │        │              │              │
    └─────┬─────┘        │              │              │
          │              │              │              │
          └──────────────┴──────────────┴──────────────┘
                         │
                         ▼
                   ┌──────────┐
                   │   Home   │
                   └──────────┘
```

---

## 14. Data Flow Summary

```
┌──────────────┐
│ vocab_       │
│ source.csv   │
└──────┬───────┘
       │ Import
       ▼
┌──────────────┐
│   SQLite DB  │──────┐
│   (Words)    │      │
└──────┬───────┘      │
       │              │ Read
       │              ▼
       │      ┌──────────────┐
       │      │  Repository  │
       │      │   Layer      │
       │      └──────┬───────┘
       │             │
       │             ▼
       │      ┌──────────────┐
       │      │   Services   │
       │      │   (Business  │
       │      │    Logic)    │
       │      └──────┬───────┘
       │             │
       │             ▼
       │      ┌──────────────┐
       │      │ Controllers  │
       │      └──────┬───────┘
       │             │
       │             ▼
       │      ┌──────────────┐
       │      │  GUI Views   │
       │      │  (Tkinter)   │
       │      └──────┬───────┘
       │             │
       │             ▼
       │      ┌──────────────┐
       │      │    User      │
       │      └──────┬───────┘
       │             │ Interaction
       │             ▼
       │      (User answers, selections)
       │             │
       └─────────────┘
         Update stats
         (display_count,
          correct_count,
          difficulty)
```

---

## 15. State Machine (Flashcard Session)

```
        ┌──────────┐
        │   INIT   │
        └─────┬────┘
              │
              ▼
        ┌──────────┐
    ┌───┤ QUESTION │◀────────┐
    │   └─────┬────┘         │
    │         │              │
    │         ▼              │
    │   ┌──────────┐         │
    │   │ ANSWERING│         │
    │   └─────┬────┘         │
    │         │              │
    │    ┌────┴────┐         │
    │    │         │         │
    │    ▼         ▼         │
    │ ┌──────┐ ┌──────────┐  │
    │ │SUBMIT│ │SHOW_ANS  │  │
    │ └──┬───┘ └────┬─────┘  │
    │    │          │        │
    │    └────┬─────┘        │
    │         │              │
    │         ▼              │
    │   ┌──────────┐         │
    │   │ VALIDATE │         │
    │   └─────┬────┘         │
    │         │              │
    │         ▼              │
    │   ┌──────────┐         │
    │   │  RESULT  │         │
    │   └─────┬────┘         │
    │         │              │
    │    ┌────┴────┐         │
    │    │Continue?│         │
    │    └────┬────┘         │
    │         │              │
    │    ┌────┴────┐         │
    │    │         │         │
    │    ▼         ▼         │
    │   YES       NO         │
    │    │         │         │
    │    └─────────┘         │
    │                        │
    └────────────────────────┘
              │
              ▼
        ┌──────────┐
        │  FINISH  │
        └──────────┘
```

---

## 16. Error Handling

### 15.1 Common Errors

| Error | Cause | Handling |
|-------|-------|----------|
| Import Failed | Invalid CSV format | Show error message, allow retry |
| DB Empty | <1000 words | Force import on startup |
| Invalid Input | User types special chars | Sanitize input, show warning |
| Timer < 0 | Speed mode timeout | Auto-end session |

### 15.2 Validation Points

```python
# Before starting session
if word_count < 1000:
    show_error("Database must have ≥1000 words")
    trigger_import()

# Before creating session
if mode == "Testing" and question_count > available_words:
    show_warning("Not enough words for this difficulty")
    adjust_question_count()

# During answer validation
if user_input.strip() == "":
    show_error("Please enter an answer")
    return
```

---

## 17. 9 Study Modes Summary

| # | Mode | Direction | Description |
|---|------|-----------|-------------|
| 1 | Endless | Eng→Vn | Practice English→Vietnamese, no time limit |
| 2 | Endless | Vn→Eng | Practice Vietnamese→English, no time limit |
| 3 | Endless | Mixed | Practice both directions randomly, no time limit |
| 4 | Speed | Eng→Vn | Timed English→Vietnamese challenge |
| 5 | Speed | Vn→Eng | Timed Vietnamese→English challenge |
| 6 | Speed | Mixed | Timed mixed direction challenge |
| 7 | Testing | Eng→Vn | Exam with English→Vietnamese questions |
| 8 | Testing | Vn→Eng | Exam with Vietnamese→English questions |
| 9 | Testing | Mixed | Exam with mixed direction questions |

---

This flow document covers all major application logic and user interactions.
