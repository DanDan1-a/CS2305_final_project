# **CS2305 Final Project Proposal**
## Title: Tank Battalion on Python
### Description
A remake of the classic 80s arcade game Tank Batallion that will be created on Python. This is a 2D top-view game where players control a tank in a maze. 
The main objective is to defeat as many enemies as possible before losing the game.

### Features
A top-view 2D game that will include:
- Enemies that roam around the level and attack player on sight
- Destructable level
- High Score capabilities

### Challenges
In my opinion the biggest challenge would be to understand the behavior of enemies in the original game and replicate it on Python.
Furthermore, destructable block will be also quite difficult to implement considering that they have dynamic size that can be changed from any direction.
- The ability of enemies to track the dynamic change of the map to create new routes
- The ability to dynamically change the map

### Outcomes
a. Ideal Outcome: Full recreation of the original game with extra levels to choose from
b. Minimal Viable Outcome: A recreation of the original game with working enemies but one level with non-destructable elements

### Milestones:
Week 1:
- Create the base game loop
- Create a player-controlled tank
- Add the ability to shoot projectiles

Week 2:
- Create blocks that would be used to build levels
- Add the ability to destroy them using projectiles
- Create a map for the main level

Week 3:
- Create enemies and add the ability to destroy them with projectiles
- Give them the ability to move and traverse the map
- Give them the ability to shoot at player

Week 4:
- Debug
- Add dynamic path creation to let enemies move from point A to point B while keeping track of all obstacles
- Add the high score system
