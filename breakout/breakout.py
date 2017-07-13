"""Primary module for Breakout application

This module contains the main controller class for the Breakout application.
There is no
need for any any need for additional classes in this module.  If you need more
classes, 
99% of the time they belong in either the play module or the models module."""
from constants import *
from game2d import *
from play import *
import colormodel


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/
#setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for
    processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED,
        STATE_ACTIVE]:
                the current state of the game represented a value from
                constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle,
                ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or
        STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for
    the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to
    store
    any text messages you display on the screen). If you add new attributes,
    they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    ADDITIONAL ATTRIBUTE:
        lastclick   [GPoint, None if no click occurred in the last frame]:
                    last position clicked
        time        [int >=0]:
                    time of the countdown to the beginning of the game
        _scoremssg  [GLabel, or None if there is no message to display]
                    the currently active message
    """
    
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which
        you 
        should not override or change). This method is called once the game is
        running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the
        given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a
        message 
        (in attribute _mssg) saying that the user should press to play a
        game."""
        
        self._state=STATE_INACTIVE
        self._game=None
        self._scoremssg=None
        self._mssg=GLabel(text='Press any key to play')
        self._mssg.font_size=20
        self._mssg.x=GAME_WIDTH/2
        self._mssg.y=GAME_HEIGHT/2
        self.time=0
    
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of
        playing the
game.  That is the purpose of the class Play.  The primary purpose of
        this
        game is to determine the current state, and -- if the game is active --
        pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.
        However, at
        a minimum you must support the following states: STATE_INACTIVE,
        STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does
        its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It
        is a 
        paused state, waiting for the player to start the game.  It displays a
        simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the
        screen.  
        This state only lasts one animation frame before switching to
        STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball
        is 
        served.  The player can move the paddle during the countdown, but there
        is no
        ball on the screen.  Paddle movement is handled by the Play object.
        Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move
        the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).
        Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the
        game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so
        long
        as the player never presses a key.  In addition, the application
        switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent
        3 seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are
        still some tries remaining.
        
        STATE_COMPLETE: The application switches to this state if the state was
        STATE_PAUSED in the previous frame, there are no more bricks remaining,
        or there are no more tries remaining
        
        You are allowed to add more states if you wish. Should you do so, you
        should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        
        assert isinstance(dt,int) or isinstance(dt,float)
        assert dt>0
        self._determineState()
        if self._state==STATE_INACTIVE:
            self.start()
        if self._state==STATE_NEWGAME:
            self._animateNewGame()
        if self._state==STATE_COUNTDOWN:
            if self.time==0:
                self._mssg=GLabel(text='3')
                self._mssg.x=GAME_WIDTH/2
                self._mssg.y=GAME_HEIGHT/2
                self._mssg.font_size=30
            elif self.time==60:
                self._mssg=GLabel(text='2')
                self._mssg.x=GAME_WIDTH/2
                self._mssg.y=GAME_HEIGHT/2
                self._mssg.font_size=30
            elif self.time==120:
                self._mssg=GLabel(text='1')
                self._mssg.x=GAME_WIDTH/2
                self._mssg.y=GAME_HEIGHT/2
                self._mssg.font_size=30
            elif self.time==180:
                self._game.serveBall()
                self._mssg=None
                self._state=STATE_ACTIVE
            if self.time<180:
                self.time=self.time+1
            self._animateCountdown()
        if self._state==STATE_ACTIVE:
            self._animateActive()
        if self._state==STATE_PAUSED:
            self._animatePause()
        if self._state==STATE_COMPLETE and self._game!=None:
            self._animateComplete()
            self._scoremssg=GLabel(text='Score: '+str(self._game.getScore()))
            self._scoremssg.x=GAME_WIDTH/2
            self._scoremssg.y=GAME_HEIGHT/2+50
            self._scoremssg.font_size=25
            self._game=None
            
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.
        To draw a GObject g, simply use the method g.draw(self.view).
        It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Play. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to class
        Play.  We suggest the latter.  See the example subcontroller.py
        from class."""
        
        if self._mssg!=None:
            self._mssg.draw(self.view)
        if self._scoremssg!=None:
            self._scoremssg.draw(self.view)
        if self._game!=None:
            self._game.draw(self.view)
    
    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """Determines the current state of the game and assigns
        it to self._state."""
        curr_keys=self.input.key_count
        change=curr_keys>0 and self.lastclick==0
        if change and self._state==STATE_INACTIVE:
            self._state=STATE_NEWGAME
            self._mssg=None
        elif self._game!=None and self._game._ball==None:
            self._state=STATE_COUNTDOWN
        elif self._state==STATE_ACTIVE and self._game._ball.top<=0:
            if self._game._tries!=0:
                self._game._tries=self._game._tries-1
                if self._game._tries!=0:
                    self._state=STATE_PAUSED
                else:
                    self._state=STATE_COMPLETE
            if self._game._tries==0:
                self._state=STATE_COMPLETE
        elif self._state==STATE_ACTIVE:
            if self._game._tries==0 or len(self._game.getBricks())==0:
                self._state=STATE_COMPLETE
        elif (self._state==STATE_ACTIVE and self._game._tries!=0 and
                           len(self._game.getBricks())==0):
            self._state=STATE_COMPLETE    
        elif change and self._state==STATE_PAUSED and self._game._tries>0:
            self._state=STATE_COUNTDOWN
        if self._state==STATE_ACTIVE and self.input.is_key_down('1'):   
            self._state=STATE_INACTIVE
        
        self.lastclick=curr_keys
    
    def _animateNewGame(self):
        """Creates a game in the form of
        a Play object: a paddle and a full set
        of bricks. This method also allows for the
        player to move the paddle. But there is no
        ball in play yet."""
        self._game=Play(tries=NUMBER_TURNS)
        self._game.updatePaddle(self.input)
        
    def _animateCountdown(self):
        """The three-second timer is initialized
        in the above method update(dt), so this method
        simply allows for the user to move the paddle
        in STATE_COUNTDOWN."""
        self._game.updatePaddle(self.input)
    
    def _animateActive(self):
        """This method is called right when the ball is
        served, meaning right when the state is STATE_ACTIVE,
        and it allows for the ball to move on its own. It also
        allows for the ball to, if any color disappears, change
        to a different color."""
        self._mssg=GLabel(text='Press 1 to restart game')
        self._mssg.x=GAME_WIDTH/7
        self._mssg.y=GAME_HEIGHT-12
        self._mssg.font_size=11.5
        self._scoremssg=GLabel(text='Score: '+str(self._game.getScore()))
        self._scoremssg.x=GAME_WIDTH-30
        self._scoremssg.y=GAME_HEIGHT-12
        self._scoremssg.font_size=11.5
            
        self._game.updatePaddle(self.input)
        self._game.updateBall()
        self._game.change_color()
        
    def _animatePause(self):
        """Presents a message in the middle of the window
        when the player loses a ball but still has tries
        remaining. The next time the player presses a key,
        the state returns to STATE_ACTIVE."""
        self._mssg=(GLabel(text=str(self._game._tries)+' tries left! Press any '
                           +'key to get a new ball'))
        self._mssg.x=GAME_WIDTH/2
        self._mssg.y=GAME_HEIGHT/2
        self._mssg.font_size=20
        
    
    def _animateComplete(self):
        """Presents a message in the middle of the window
        either when the player or loses or when the player wins.
        The player loses when there are no more tries left, but
        there are still bricks left. The player wins when there
        is at least one try left but no more bricks left."""
        self._score=BRICKS_IN_ROW*BRICK_ROWS
        if self._game._tries==0 and len(self._game.getBricks())>0:
            self._mssg=GLabel(text='You lost!')
            self._mssg.x=GAME_WIDTH/2
            self._mssg.y=GAME_HEIGHT/2
            self._mssg.font_size=50
        elif self._game._tries!=0 and len(self._game.getBricks())==0:
            self._state=STATE_COMPLETE
            self._mssg=GLabel(text='You won!')
            self._mssg.x=GAME_WIDTH/2
            self._mssg.y=GAME_HEIGHT/2
            self._mssg.font_size=80
    
    
        

        
    
            
        

