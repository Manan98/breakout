"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout
App. 
Instances of Play represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model
objects.  
Their classes are defined in models.py."""
from constants import *
from game2d import *
from models import *
import colormodel


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent.)


class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops
    animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make
    a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT
    ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any
    attribute that 
    you need to access in Breakout.  Only add the getters and setters that you
    need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    may want
    to add new objects on the screen (e.g power-ups).  If you make changes,
    please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        _score [int >= 0]: player's score
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBricks(self):
        """Returns: list of bricks"""
        return self._bricks
    
    def getScore(self):
        """Returns: player's score"""
        return self._score
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self,tries):
        """Initializes the paddle and full set of bricks.
        The default brick pattern is ten rows of ten bricks.
        Every two rows is a different color, summing to a total
        of five colors: red (top), orange, yellow, green, and
        cyan (bottom)."""
        assert isinstance(tries,int) and tries>=0
        self._brickno = BRICKS_IN_ROW*BRICK_ROWS
        self._score=0
        self._ball=None
        self._tries=tries
        self._paddle=Paddle(GAME_WIDTH/2,PADDLE_OFFSET+PADDLE_HEIGHT/2,
                            PADDLE_WIDTH,PADDLE_HEIGHT,colormodel.BLACK)
        self._bricks=[]
        row_no=1     # row number (starting from top row)
        brick_no=1   # brick number in each row (from left to right)
        left=BRICK_SEP_H/2
        y=GAME_HEIGHT-BRICK_Y_OFFSET-(BRICK_HEIGHT/2)
        while row_no<=BRICK_ROWS:
            if row_no%10<=2 and row_no%10>0:
                fillcolor=colormodel.RED
            elif row_no%10>=3 and row_no%10<=4:
                fillcolor=colormodel.ORANGE
            elif row_no%10>=5 and row_no%10<=6:
                fillcolor=colormodel.YELLOW
            elif row_no%10>=7 and row_no%10<=8:
                fillcolor=colormodel.GREEN
            elif row_no%10>=9 or row_no%10==0:
                fillcolor=colormodel.CYAN
            while brick_no<=BRICKS_IN_ROW:
                self._bricks.append(Brick(left,y,BRICK_WIDTH,
                                          BRICK_HEIGHT,fillcolor))
                left=left+BRICK_WIDTH+BRICK_SEP_H
                brick_no=brick_no+1
            left=BRICK_SEP_H/2
            brick_no=1
            y=y-BRICK_HEIGHT-BRICK_SEP_V
            row_no=row_no+1

    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def serveBall(self):
        """Sets the ball in motion at random horizontal and
        vertical velocities right when the countdown ends (meaning
        right when the state switches to STATE_ACTIVE). Because
        the velocity components are random, the ball moves in a
        different direction each time a new one is served."""
        self._ball=Ball(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=BALL_DIAMETER/2,
                        height=BALL_DIAMETER/2,fillcolor=colormodel.CYAN)
    
    def updatePaddle(self,input):
        """Called in Breakout whenever the state
        of the game is STATE_NEWGAME, STATE_COUNTDOWN,
        or STATE_ACTIVE. This method allows for the
        player to move the paddle left or right by pressing
        the left and right arrows, respectively. No matter
        how long the player holds down one of the two keys,
        the paddle will not move past the left and right edges
        of the window.
        
        Parameter input: user input
        Precondition: input is a GInput object"""
        assert isinstance(input,GInput)
        dx=0
        colors=[colormodel.RED,colormodel.ORANGE,
                colormodel.YELLOW,colormodel.GREEN,colormodel.CYAN]
        if input.is_key_down('left'):
            dx-=10
        if input.is_key_down('right'):
            dx+=10
        if self._paddle.x+dx+PADDLE_WIDTH/2>=GAME_WIDTH:
            self._paddle.right=min(self._paddle.right,GAME_WIDTH)
        elif self._paddle.x+dx-PADDLE_WIDTH/2<=0:
            self._paddle.left=max(self._paddle.left,0)
        else:
            self._paddle.x=self._paddle.x+dx            
        
    def updateBall(self):
        """Called in Breakout whenever the state of
        the game is STATE_ACTIVE. This method simply
        moves the ball by adding the ball's velocity
        components to its coordinates in the window.
        It also causes the ball to bounce upon interaction
        with the paddle and the bricks, and each bounce
        upon a brick causes the brick to disappear."""
        saucer1=Sound('saucer1.wav')
        cup1=Sound('cup1.wav')
        self._ball.x=self._ball.x+self._ball._vx
        self._ball.y=self._ball.y+self._ball._vy
        if self._paddle.collides(self._ball):
            cup1.play()
            self._ball._vy=(-self._ball._vy)
        for x in self._bricks:
            if x.collides(self._ball):
                self._ball.incspeed()
                self._score=self._score+10
                saucer1.play()
                self._bricks.remove(x)
                self._ball._vy=(-self._ball._vy)
        self.bounceEdge()
        
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    
    def draw(self,view):
        """Draws the paddle, the ball, and the bricks,
        regardless of how many bricks there are remaining.
        
        Parameter view: game window
        Precondition: view is a GView object"""
        assert isinstance(view,GView)
        for x in self._bricks:
            x.draw(view)
        self._paddle.draw(view)
        if self._ball!=None:
            self._ball.draw(view)
      
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    
    def bounceEdge(self):
        """Adjusts the ball's horizontal and vertical velocities
        so that the ball bounces when it reaches each edge of
        the window"""
        if self._ball._vy>0:
            if self._ball.y>=GAME_HEIGHT:
                self._ball._vy=(-self._ball._vy)
        if self._ball._vx>0:
            if self._ball.right>=GAME_WIDTH:
                self._ball._vx=(-self._ball._vx)
        if self._ball._vx<0:
            if self._ball.left<=0:
                self._ball._vx=(-self._ball._vx)
                
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HER
    
    def change_color(self):
        """For each color, if all bricks of that color
        are gone, then the ball's color changes to the color
        of the adjacent row.
        
        For example, once the last cyan brick disappears, the
        ball turns green. Once the last green brick disappears,
        the ball turns yellow. And once the last yellow brick disappears,
        the ball turns red."""
        colors=[colormodel.RED,colormodel.ORANGE,colormodel.YELLOW,
                colormodel.GREEN,colormodel.CYAN]
        for x in self._bricks:
            if x.fillcolor not in colors:
                self._ball.fillcolor=x.fillcolor

