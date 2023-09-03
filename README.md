# gravity
The idea here is to see the formation of a solar system if we're honest the math here is only
vaguely related to the real world as are the starting conditions.

The simulation works by populating "space" with chunks of matter (called rocks in the code) with the same mass, but 
random positions and velocities. Next newton's law of gravitation is applied in discrete ticks. As the matter moves
if any two rocks should collide they merge this continues forever.

At the moment computing the state of every rock happens in O(n!) time (very very slow) I have an idea to speed the
process up by only splitting "space" up in to sectors and only computing each rock against other rocks in its
sector and immediate neighboring sectors, and then against the center of mass for farther away sectors. Not at
all sure that I'll ever get around to implementing that
