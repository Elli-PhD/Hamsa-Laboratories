# Hamsa-Laboratories
Python code created by the founder of Hamsa Laboratories in EVE Online.

My current big coding project which I just started involves trying to reverse engineer the Python code that runs EVE Online (a game which I have been playing for over a decade) for the purposes of:

 1. Scrubbing manufacturing blueprint data and galaxy-wide market data to calculate daily profit margins for manufactured items in the game based off of raw material input.

 2. Identifying where ship orientation vector calculations are implemented for the purpose of modifying them to more accurately represent zero-gravity physics all while preserving the preexisting overall game framework.  (In essence, for a ship to orbit a small object in a small circle, its acceleration vector (i.e., the direction the ship is pointing) needs to point towards their target at an angle relative to the ship's current velocity (i.e., the direction the ship is moving in space).)

 3. Looking into where vectors relative to orbital bodies are calculated, as they could be used to calculate a net gravitational acceleration vector, which could contribute to a ship-drift effect near large celestial bodies (moons, planets, stations, etc.) which would impact ship orientation vectors, for the purpose of more accurately representing zero-gravity physics, as with #2.

(Pardon the quite new and quite empty github; most of my coding has been for work and thus proprietary)

**Hey CCP, if you're out there, we should chat. ;-)**
