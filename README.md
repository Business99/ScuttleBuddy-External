# Scuttle Buddy (v12.17)
### External Scripting Platform for League of Legends
#### Please note this project is still in the early stages. Anything and everything is subject to change.

# Discord
### Coming soon

# Installation Instructions

### From Source:
1. Clone or Fork the ScuttleBuddy-External repository
2. Download the latest release `.zip` of the PyMeow library located [here](https://github.com/qb-0/PyMeow).
3. Extract the contents of the `.zip` file into the ScuttleBuddy-External project folder
4. Open your terminal and run `pip install .` to install PyMeow
5. In the same terminal run `pip install -r requirements.txt` to install the needed dependencies

### Precompiled:
1. *In Progress...*

# LeagueReader
### `./resources/LeagueReader.py`
### This reader class is the root of all game data, and is refreshed every tick.

* *pm* `Pymem`
  * Pymem Object used for accessing memory.
* *mem* `PyMeow`
  * Pymeow Object used for accessing memory and drawing on screen.
* *overlay* `dict`
  * The overlay window object that displays on top of the League Client.
* *viewProjMatrix* `list`
  * The calculations necessary to convert a 3D game space into a 2D plane.
* *localPlayer* `PlayerEntity`
  * A fully populated **PlayerEntity** object in reference to the local player running the platform.
* *teamPlayers* `list[PlayerEntity]`
  * A list of **PlayerEntity** objects that are on the localPlayer's team.
* *enemyPlayers* `list[PlayerEntity]`
  * A list of **PlayerEntity** objects that are on the enemy team.

# PlayerEntity
### `./models/PlayerEntity.py`
### This is the entity object for storing a single player's data.

* *championName* `str`
* *teamId* `int`
* *level* `int`
* *isVisible* `bool`
* *health* `float`
* *maxHealth* `float`
* *mana* `float`
* *maxMana* `float`
* *magicResist* `float`
* *armor* `float`
* *ap* `float`
* *ad* `float`
* *magicPenFlat* `float`
* *magicPenPercent* `float`
* *armorPenPercent* `float`
* *gamePos* `dict`
* *screenPos* `dict`
* *spells* `list[Spell]`

# Spell
### `./models/Spell.py`
### This is the object for each spell a champion can cast.

* *name* `str`
* *readyAt* `float`
* *level* `int`
* *isReady* `bool` **Not Implemented
* *readyIn* `float`
* *isSummoner* `bool`
