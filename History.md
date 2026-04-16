# History

My first encounter with Conway’s Game of Life was almost two decades ago at an IT convention.  
The challenge was to present a project on a chosen subject; I chose the game **Snake**, but someone presented the Game of Life.  
Upon learning about it, I immediately got to work and made my own implementation in **Turbo Pascal** (the only language I knew at the time).

I recall my initial approach was to set up a matrix with a pattern, then walk each cell and apply the rules.  
The resulting behaviour was nonsensical, as I had already suspected.  
Changing a cell affects its unprocessed neighbours, so it became clear I needed a second matrix to mutate and then swap it to become the current state before rendering.  
Once I did that, it felt like a portal to a new world had opened right in front of me, and I spent hours and hours late into the night coming up with different patterns to experiment with.
This was partly due to the fascination of exploring this new found world, but also the limited intractability. I was working in Turbo Pascal in console mode, inputting the starting pattern via code and hitting run – not very efficient.

Fast‑forward to today: I’m embarking on a new chapter and have recently picked up Python via boot.dev.  
After the Python section there was a “Personal Project 1” section, and I wanted to revisit that inspiration with modern tools.  
The current version adds real‑time mouse drawing, zoom & pan, speed controls, and other QoL improvements.  
I want this to remain a playground for anyone who feels the same fascination I felt back then.