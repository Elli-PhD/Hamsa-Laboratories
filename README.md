# Hamsa-Laboratories
Python code created by the founder of Hamsa Laboratories in EVE Online.

My current big coding project which I just started involves trying to reverse engineer the Python code that runs EVE Online (a game which I have been playing for over a decade) for the purposes of:

 1. Scrubbing manufacturing blueprint data and galaxy-wide market data to calculate daily profit margins for manufactured items in the game based off of raw material input.

 2. Identifying where ship orientation vector calculations are implemented for the purpose of modifying them to more accurately represent zero-gravity physics, all while preserving the preexisting overall game framework.  (In essence, for a ship to orbit a small object in a small circle, its acceleration vector (i.e., the direction the ship is pointing) needs to point towards their target at an angle relative to the ship's current velocity (i.e., the direction the ship is moving in space).)

 3. Looking into where vectors relative to orbital bodies are calculated, as they can be used to calculate a net gravitational acceleration vector, which could contribute to a ship-drift effect near large celestial bodies (moons, planets, stations, etc.) which would impact ship orientation vectors, for the purpose of more accurately representing zero-gravity physics (as with #2).  This will also add new and interesting challenges for players engaging in combat near celestial objects.

 4. Some other ideas (not fully flushed out):
  a. Removing the velocity cap and letting ships accelerate indefinitely and adding in a mass-energy conversion term (i.e., E=mc^2 with modified c).
  b. Removing the velocity need for warping.  Presumably warp speed functions by manipulating spacetime around the ship as opposed to simply increasing the momentum of the ship (recall E=mc^2 and one cannot accelerate themselves past the speed of light).  In addition, add a mechanic where the ship's current momentum is transferred to their new location after exiting warp; i.e., a player can be travelling forward at velocity v, warp backwards, and when they leave warp, their velocity will be what it was before initiating warp.
  c. Deceleration would visually rotate one's ship 180 degrees and accelerate.
  d. Celestial orbital mechanics - have planets, moons, stations, etc. warp around their respective center of mass.  A full rotation of a planet could last a period of hours to months.
  e. Calculating warp trajectories around planets instead of through them.  Can give players different options, which will add another layer to PVP mechanics.

(Pardon the quite new and quite empty github; most of my coding has been for work and thus proprietary)

**Hey CCP, if you're out there, we should chat. ;-)**
