# 112 TP PlantsVsZombies
 Plants Vs Zombies!
 A strategy-based game where players defend their house from waves of zombies using a variety of plants. The game features different three difficulty levels: easy, medium, and hard. The easy level will be the easiest level, followed by the medium level, and the hard level. The game dynamically generates resources, such as sunlight, which is needed to plant new defenses. Sunflowers generate sunlight, while plants can only be placed if enough sunlight is available. 

 For each level, there will be two waves, the first wave and final wave. During the final wave, zombies spawn faster than the first wave.

 For the easy level, zombies are spawned randomly. For the medium and hard levels, zombies are spawned based on the plants attacking power per row; the zombies will have 90% chance spawning at row(s) that have the least plants attacking power. The hard level will have more zombies and a higher spawning rate as compared to the medium level. 

 Players must strategically place plants in the grid to defend their house. Plants only shoot when there are zombies in their lane, and there will be a variation of plants that can reduce the speed of zombies, hit multiple zombies at once (the plants shot reflect off zombie to other zombies and damages the zombies), and launch projectiles in a parabolic motion. 
 To help players strategize, the game will include an autoplay feature where the game plays for the user. The zombie becomes smarter at higher levels, with zombies able to move between rows to avoid heavily defended areas. 

 How to Run the Project
 1. Run main.py to start the game
 2. Dependencies:
    - CMU Graphics
    - PIL: install using pip install pillow
 3. Playing the game
    - When the game begins, users can select the target icon and drag it to anywhere in the grid where projectiles within the radius will change its direction and move towards the mouse. This is useful for attacking a certain location with high density of zombies.
    - There is also a play/pause button which the users can click to enable an autoplay feature!

 
