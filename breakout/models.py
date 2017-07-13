"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything
that you
interact with on the screen is model: the paddle, the ball, and any of the
bricks.

Technically, just because something is a model does not mean there has to be a
special 
class for it.  Unless you need something special, both paddle and individual
bricks could
just be instances of GRectangle.  However, we do need something special:
collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you
add
new features to your game."""

import random # To randomly generate the ball velocity
from constants import *
from game2d import *
import math


# PRIMARY RULE: Models are not allowed to access anything except the module
#constants.py.
# If you need extra information from Play, then it should be a parameter in your
#method, and Play should pass it as a argument when it calls the method.

class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as
    move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    
    def __init__(self,x,y,width,height,fillcolor):
        GRectangle.__init__(self,x=x,y=y,width=width,height=height,
                            fillcolor=fillcolor)
        GRectangle(x=x,y=y,width=width,height=height,
                   fillcolor=fillcolor).linecolor=fillcolor
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collides(self,ball):
        """Returns: True if the ball collides with this paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        if ball._vy<0:
            a=self.contains(ball.x-BALL_DIAMETER/2,ball.y+BALL_DIAMETER/2)
            b=self.contains(ball.x-BALL_DIAMETER/2,ball.y-BALL_DIAMETER/2)
            c=self.contains(ball.x+BALL_DIAMETER/2,ball.y+BALL_DIAMETER/2)
            d=self.contains(ball.x+BALL_DIAMETER/2,ball.y-BALL_DIAMETER/2)
            if a or b or c or d:
                return True
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Brick(GRectangle):
    """An instance is a game brick.
    
    This class contains a method to detect collision with the ball.  You may
    wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,left,y,width,height,fillcolor):
        """Initializes a brick. The brick has the same attributes
        as the GRectangle class. The only adjustment in this case
        is that the linecolor of the brick is set equal to the fillcolor."""
        GRectangle.__init__(self,left=left,y=y,width=width,
                            height=height,fillcolor=fillcolor)
        GRectangle(left=left,y=y,width=width,height=height,
                   fillcolor=fillcolor).linecolor=fillcolor
    
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        a=self.contains(ball.x-BALL_DIAMETER/2,ball.y+BALL_DIAMETER/2)
        b=self.contains(ball.x-BALL_DIAMETER/2,ball.y-BALL_DIAMETER/2)
        c=self.contains(ball.x+BALL_DIAMETER/2,ball.y+BALL_DIAMETER/2)
        d=self.contains(ball.x+BALL_DIAMETER/2,ball.y-BALL_DIAMETER/2)
        if a or b or c or d:
            return True
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional
    attributes for velocity. This class adds this attributes
    and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for
    these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self,x,y,width,height,fillcolor):
        """Initializes a ball. The ball has the same attributes as
        the GEllipse class. In this case, however, the linecolor of
        the ball is set equal to the fillcolor. And there are two new
        attributes that GEllipse doesn't have: _vx and _vy, the horizontal
        and vertical velocities of the ball, respectively. When initialized,
        the vertical velocity is set to a constant value, but the horizontal
        velocity is different every time a new ball is constructed."""
        GEllipse.__init__(self,x=x,y=y,width=width,height=height,
                          fillcolor=fillcolor)
        GEllipse(x=x,y=y,width=width,height=height,
                 fillcolor=fillcolor).linecolor=fillcolor
        self._vx=random.uniform(1.0,5.0) 
        self._vx=self._vx*random.choice([-1,1])
        self._vy=(-5.0)
        
    
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def incspeed(self):
        self._vx = self._vx * 1.05
        self._vy = self._vy * 1.05

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
    
