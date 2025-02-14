# Dice Game with Tkinter

This is a simple game for Mac based on original Kingdom Come Deliverance mini-game in taverns.

## Game Rules

The valid scoring combinations in this game are:

1. **Single 1**: 100 points  
2. **Single 5**: 50 points  
3. **Triple 1s (1+1+1)**: 1 point  
4. **Triple 2s (2+2+2)**: 200 points  
5. **Triple 3s (3+3+3)**: 300 points  
6. **Triple 4s (4+4+4)**: 400 points  
7. **Triple 5s (5+5+5)**: 500 points  
8. **Triple 6s (6+6+6)**: 600 points  
9. **Sequence 1+2+3+4+5**: 500 points  
10. **Sequence 2+3+4+5+6**: 750 points  
11. **Sequence 1+2+3+4+5+6**: 1500 points  

### How to Play

- **Roll the Dice:** Click the **"Roll!"** button to roll all active dice.
- **Select Dice:** Use the checkboxes below each die to select those that form valid scoring combinations.
- **Hold and Continue:** After selecting scoring dice, click **"Hold and continue"** to lock in your score and re-roll the remaining dice.
- **Save and Pass:** If you want to end your turn, click **"Save and pass"** to add your turn's points to your overall score.
- **Busted Roll:** If no valid scoring combination is rolled (a "bust"), you'll see a message (e.g., `"Kurwa!"`) and your turn will automatically reset after a short delay.
- **Clear Overall Score:** Use the **"Clear Overall Score"** button to reset your overall score if desired.

## Requirements

- Python 3.x  
- Tkinter (usually included with Python but I had to install it separately)

## Installation and Running

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/dice-game.git
