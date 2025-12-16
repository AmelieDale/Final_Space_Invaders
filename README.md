# Final_Space_Invaders

A Space Invaders–style arcade game developed in Python as part of the COM4023 CW1 assignment, featuring multiple difficulty levels.


<p align="center">
  <img src="https://github.com/user-attachments/assets/880937b0-7358-4328-9d20-01efdebb58ca" alt="title screen">
</p>



---
## Documentation

For detailed information about the development of *Final Space Invaders*, please visit the project **Wiki**:

- **[Home](https://github.com/AmelieDale/Final_Space_Invaders/wiki)**  
  An overview of the game, its purpose, requirment ownership, and core features.

- **[Planning & Preparation](https://github.com/AmelieDale/Final_Space_Invaders/wiki/Development-Log#planning--preparation)**  
  Details on the initial planning process, design decisions, and preparation before coding began.

- **[Amelie’s Development Log](https://github.com/AmelieDale/Final_Space_Invaders/wiki/Development-Log#amelie-dale)**  
  A breakdown of how Amelie developed her requirements, including additional features and improvements beyond the assignment brief.

- **[Holly’s Development Log](https://github.com/AmelieDale/Final_Space_Invaders/wiki/Development-Log#holly-dickinson)**  
  An explanation of how Holly implemented her requirements and extended the project with extra functionality and refinements.

- **[Integration & Collaboration](https://github.com/AmelieDale/Final_Space_Invaders/wiki/Development-Log#integration--collaboration-summary)**  
  A summary of how both codebases were combined, challenges faced during integration, and how collaboration was managed.

- **[Conclusion & Self-Evaluation](https://github.com/AmelieDale/Final_Space_Invaders/wiki/Development-Log#conclusion)**  
  A reflective evaluation of the project, discussing what went well, lessons learned, and areas for future improvement.

 - **[Issues](https://github.com/AmelieDale/Final_Space_Invaders/issues)**  
  A record of the issues encountered during development and how they were resolved. Issues have been left active to demonstrate the problem-solving process and development workflow.


---

## Project Structure

```text
Final_Space_Invaders/
│
├── MAIN_GAME.py            # Main entry point for the game
├── README.md               # Project documentation
│
├── Spaceship.py            # Player spaceship logic
├── alien.py                # Alien enemy behaviour
├── laser.py                # Laser and shooting mechanics
├── obstacle.py             # Obstacles and collision handling
├── play.py                 # Player controls and movement
├── mysteryship.py          # Mystery ship behaviour and logic
│
├── main-amelie.py          # Amelie's development version
├── main-holly.py           # Holly's development version
│
├── Fonts/                  # Font assets used in the game
│   ├── Invaders-6RY1.ttf   # Retro-style game font
│   ├── RETROTECH.ttf       # Alternative retro font
│   ├── info.txt            # Font information / licensing
│   └── misc/
│       └── invaders.txt    # Additional font-related data
│
├── Graphics/               # Game graphics and audio assets
│   ├── player.png          # Player sprite
│   ├── spaceship.png       # Spaceship sprite
│   ├── green.png           # Enemy sprite (green)
│   ├── red.png             # Enemy sprite (red)
│   ├── yellow.png          # Enemy sprite (yellow)
│   ├── mystery.png         # Mystery ship sprite
│   ├── laser.ogg           # Laser sound effect
│   ├── explosion.ogg       # Explosion sound effect
│   ├── music.ogg           # Background music
│   └── monogram.ttf        # Font used for UI elements
│
└── __pycache__/             # Cached Python files (auto-generated)
