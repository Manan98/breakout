# colormodel.py
# Walker M. White (wmw2)
# September 2, 2012
"""Classes for three different color models.

The classes are RGB, CMYK, HSV.  The constants in this module are all
defined in the RGB color space."""
import colorsys

# To handle round off error
_epsilon = 1e-13

class RGB(object):    
    """An instance is a RGB color value."""
    
    @property
    def red(self):
        """The red channel.
        
        **Invariant**: Value must be an int between 0 and 255, inclusive."""
        return self._red
       
    @red.setter
    def red(self, value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 and value <= 255), "value %s is outside of range [0,255]" % `value`
        self._red = value
       
    @red.deleter
    def red(self):
        del self._red 
    
    @property
    def green(self):
        """The green channel.
        
        **Invariant**: Value must be an int between 0 and 255, inclusive."""
        return self._green
    
    @green.setter
    def green(self, value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 and value <= 255), "value %s is outside of range [0,255]" % `value`
        self._green = value
        
    @green.deleter
    def green(self):
        del self._green     
    
    @property
    def blue(self):
        """The blue channel.
        
        **Invariant**: Value must be an int between 0 and 255, inclusive."""
        return self._blue
    
    @blue.setter
    def blue(self, value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 and value <= 255), "value %s is outside of range [0,255]" % `value`
        self._blue = value
        
    @blue.deleter
    def blue(self):
        del self._blue     
 
    @property
    def alpha(self):
        """The alpha channel.
        
        Used for transparency effects (but not in this course).
        
        **Invariant**: Value must be an int between 0 and 255, inclusive."""
        return self._alpha
        
    @alpha.setter
    def alpha(self, value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 and value <= 255), "value %s is outside of range [0,255]" % `value`
        self._alpha = value
            
    @alpha.deleter
    def alpha(self):
        del self._alpha     

    # METHODS
    
    def __init__(self, r, g, b, a=255):
        """**Constructor**: creates a new RGB value (r,g,b,a).
        
            :param r: initial red value
            :param g: initial green value
            :param b: initial blue value
            :param a: initial alpha value (default 255)

        The alpha channel is 255 by default, unless otherwise specified.
        
        **Precondition**: r, g, b, a must all be ints between 0 and 255, inclusive
        """
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
            
    def __eq__(self, other):
        """Returns: True if self and other are equivalent RGB colors. """
        return (type(other) == RGB and self.red == other.red and 
                self.green == other.green and self.blue == other.blue and
                self.alpha == other.alpha)

    def __ne__(self, other):
        """Returns: True if self and other are not equivalent RGB colors. """
        return (type(other) != RGB or self.red != other.red or 
                self.green != other.green or self.blue != other.blue or
                self.alpha != other.alpha)

    def __str__(self):
        """Returns: Readable string representation of this color. """
        from a3 import rgb_to_string # local to prevent circular import
        return rgb_to_string(self)

    def __repr__(self):
        """Returns: Unambiguous String representation of this color. """
        # return "(red="+str(self.red)+",green="+str(self.green)+",blue="+str(self.blue)+",alpha="+str(self.alpha)+")"
        return "(red="+str(self.red)+",green="+str(self.green)+",blue="+str(self.blue)+")"

    def glColor(self):
        """**Returns**: 4 element list of the attributes in the range 0 to 1
        
        This is a conversion of this object into a format that can be used in
        openGL graphics"""
        return [self.red/255.0, self.green/255.0, self.blue/255.0, self.alpha/255.0]

    def turtleColor(self):
        """**Returns**: 3 element tuple of the attributes in the range 0 to 1
        
        This is a conversion of this object into a format that can be used in
        openGL graphics"""
        return (self.red/255.0, self.green/255.0, self.blue/255.0)

class CMYK(object):
    """An instance is a CMYK color value."""
    
    @property
    def cyan(self):
        """The cyan channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive."""
        return self._cyan
       
    @cyan.setter
    def cyan(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % `value`
        if (value > 100.0):
        	value = min(value,100.0) if value < 100.0+_epsilon else value
        if (value < 0.0):
        	value = max(value,0.0) if value > -_epsilon else value
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % `value`
        self._cyan = float(value)
       
    @cyan.deleter
    def cyan(self):
        del self._cyan 
    
    @property
    def magenta(self):
        """The magenta channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive."""
        return self._magenta
    
    @magenta.setter
    def magenta(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % `value`
        if (value > 100.0):
        	value = min(value,100.0) if value < 100.0+_epsilon else value
        if (value < 0.0):
        	value = max(value,0.0) if value > -_epsilon else value
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % `value`
        self._magenta = float(value)
        
    @magenta.deleter
    def magenta(self):
        del self._magenta     
    
    @property
    def yellow(self):
        """The yellow channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive."""
        return self._yellow
    
    @yellow.setter
    def yellow(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % `value`
        if (value > 100.0):
        	value = min(value,100.0) if value < 100.0+_epsilon else value
        if (value < 0.0):
        	value = max(value,0.0) if value > -_epsilon else value
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0.0,100.0]" % `value`
        self._yellow = float(value)
        
    @yellow.deleter
    def yellow(self):
        del self._yellow     
 
    @property
    def black(self):
        """The black channel.
        
        **Invariant**: Value must be a float between 0.0 and 100.0, inclusive."""
        return self._black
        
    @black.setter
    def black(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % `value`
        if (value > 100.0):
        	value = min(value,100.0) if value < 100.0+_epsilon else value
        if (value < 0.0):
        	value = max(value,0.0) if value > -_epsilon else value
        assert (value >= 0.0 and value <= 100.0), "value %s is outside of range [0,255]" % `value`
        self._black = float(value)
            
    @black.deleter
    def black(self):
        del self._black     

    def __init__(self, c, m, y, k):
        """**Constructor**: creates a new CMYK color (c,m,y,k).
        
            :param c: initial cyan value
            :param m: initial magenta value
            :param y: initial yellow value
            :param k: initial black value

        **Precondition**: The values c,m,y,k are floats between 0.0 and 100.0, inclusive."""

        self.cyan = c
        self.magenta = m
        self.yellow = y
        self.black = k
    
    def __eq__(self, other):
        """Returns: True if self and other are equivalent CMYK colors. """
        return (type(other) == CMYK and self.cyan == other.cyan and 
                self.magenta == other.magenta and self.yellow == other.yellow and
                self.black == other.black)   

    def __ne__(self, other):
        """Returns: True if self and other are not equivalent CMYK colors. """
        return (type(other) != CMYK or self.cyan != other.cyan or 
                self.magenta != other.magenta or self.yellow != other.yellow or
                self.black != other.black)

    def __str__(self):
        """Returns: Readable String representation of this color. """
        from a3 import cmyk_to_string # local to prevent circular import
        return cmyk_to_string(self)

    def __repr__(self):
        """Returns: Unambiguous String representation of this color. """
        return "(cyan="+str(self.cyan)+",magenta="+str(self.magenta)+",yellow="+str(self.yellow)+",black="+str(self.black)+")"

class HSV(object):
    """An instance is a HSV color value."""

    @property
    def hue(self):
        """The hue channel.
        
        **Invariant**: Value must be a float between 0.0 and 360.0, not including 360.0."""
        return self._hue
       
    @hue.setter
    def hue(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % `value`
        if (value < 0.0):
        	value = max(value,0.0) if value > -_epsilon else value
        assert (value >= 0.0 and value < 360.0), "value %s is outside of range [0.0,360.0)" % `value`
        self._hue = float(value)
       
    @hue.deleter
    def hue(self):
        del self._hue 
    
    @property
    def saturation(self):
        """The staturation channel.
        
        **Invariant**: Value must be a float between 0.0 and 1.0, inclusive."""
        return self._saturation
    
    @saturation.setter
    def saturation(self, value):
        assert (type(value) == int or type(value) == float), "value %s is not a number" % `value`
        if (value > 1.0):
        	value = min(value,1.0) if value < 100.0+_epsilon else value
        if (value < 0.0):
        	value = max(value,0.0) if value > -_epsilon else value
        assert (value >= 0.0 and value <= 1.0), "value %s is outside of range [0.0,1.0]" % `value`
        self._saturation = float(value)
        
    @saturation.deleter
    def saturation(self):
        del self._saturation     
    
    @property
    def value(self):
        """The value channel.
        
        **Invariant**: Value must be a float between 0.0 and 1.0, inclusive."""
        return self._value
    
    @value.setter
    def value(self, val):
        assert (type(val) == int or type(val) == float), "value %s is not a number" % `value`
        if (val > 1.0):
        	value = min(val,1.0) if val < 100.0+_epsilon else val
        if (val < 0.0):
        	value = max(val,0.0) if val > -_epsilon else val
        assert (val >= 0.0 and val <= 1.0), "value %s is outside of range [0.0,1.0]" % `val`
        self._value = float(val)
        
    @value.deleter
    def value(self):
        del self._value     
        
    def __init__(self, h, s, v):
        """**Constructor**: creates a new HSV color (h,s,v).
        
            :param h: the initial hue 
            :param h: the initial saturation
            :param h: the initial value
            
        **Precondition**: The value h is a float between 0.0 and 360.0, not
        including 360.0.  The values s and v are floats between 0.0 and 1.0, inclusive."""
        self.hue = h
        self.saturation = s
        self.value = v
    
    def __eq__(self, other):
        """Returns: True if self and other are equivalent HSV colors. """
        return (type(other) == HSV and self.hue == other.hue and 
                self.saturation == other.saturation and self.value == other.value)
    
    def __ne__(self, other):
        """Returns: True if self and other are equivalent HSV colors. """
        return (type(other) != HSV or self.hue != other.hue or 
                self.saturation != other.saturation or self.value != other.value)

    def __str__(self):
        """Returns: Readable String representation of this color. """
        from a3 import hsv_to_string # local to prevent circular import
        return hsv_to_string(self)

    def __repr__(self):
        """Returns: Unambiguous String representation of this color. """
        return "(hue="+str(self.hue)+",saturation="+str(self.saturation)+",value="+str(self.value)+")"

    def glColor(self):
        """**Returns**: 4 element list of the equivalent rgba color.
        
        This method converts this object to an RGB object and then extracts
        a 4 element list with color values between 0 and 1. This is a conversion
        of this object into a format that can be used in openGL graphics"""
        rgb = colorsys.hsv_to_rgb(self.hue/360.0,self.saturation,self.value)
        return [rgb[0], rgb[1], rgb[2], 1.0]

    def turtleColor(self):
        """**Returns**: 3 element tuple of the equivalent rgba color.
        
        This method converts this object to an RGB object and then extracts
        a 3 element tuple with color values between 0 and 1. This is a conversion
        of this object into a format that can be used in openGL graphics"""
        return colorsys.hsv_to_rgb(self.hue/360.0,self.saturation,self.value)


# Color Constants

#: The color white in the default sRGB space.
WHITE = RGB(255, 255, 255)

#: The color light gray in the default sRGB space.
LIGHT_GRAY = RGB(192, 192, 192)

#: The color gray in the default sRGB space.
GRAY = RGB(128, 128, 128)

#: The color dark gray in the default sRGB space.
DARK_GRAY = RGB(64, 64, 64)

#: The color black in the default sRGB space.
BLACK = RGB(0, 0, 0)

#: The color red, in the default sRGB space.
RED = RGB(255, 0, 0)

#: The color pink in the default sRGB space.
PINK = RGB(255, 175, 175)

#: The color orange in the default sRGB space.
ORANGE = RGB(255, 200, 0)

#: The color yellow in the default sRGB space.
YELLOW = RGB(255, 255, 0)

#: The color green in the default sRGB space.
GREEN = RGB(0, 255, 0);

#: The color magenta in the default sRGB space.
MAGENTA = RGB(255, 0, 255)

#: The color cyan in the default sRGB space.
CYAN = RGB(0, 255, 255)

#: The color blue in the default sRGB space.
BLUE = RGB(0, 0, 255)