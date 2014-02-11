from matplotlib.offsetbox import AnchoredOffsetbox


class AnchoredScaleBar(AnchoredOffsetbox):
    def __init__(self, transform, sizex=0, sizey=0, labelx=None, labely=None,
                 loc=7, pad=0.1, borderpad=0.1, sep=2, prop=None, **kwargs):
        """
        Modified, draw a horizontal and/or vertical  bar with the size in data coordinate
        of the give axes. A label will be drawn underneath (center-aligned).
 
        - transform : the coordinate frame (typically axes.transData)
        - sizex,sizey : width of x,y bar, in data units. 0 to omit
        - labelx,labely : labels for x,y bars; None to omit
        - loc : position in containing axes
        - pad, borderpad : padding, in fraction of the legend font size (or prop)
        - sep : separation between labels and bars in points.
        - **kwargs : additional arguments passed to base class constructor
        """
        from matplotlib.lines import Line2D
        from matplotlib.pyplot import arrow
        from matplotlib.text import Text
        from matplotlib.offsetbox import AuxTransformBox
        bars = AuxTransformBox(transform)
        inv = transform.inverted()
        pixelxy = inv.transform((1, 1)) - inv.transform((0, 0))

        if sizex:
            barx = Line2D([sizex, 0], [0, 0], transform=transform, color='k')
            bars.add_artist(barx)            

        if sizey:
            bary = Line2D([0, 0], [0, sizey], transform=transform, color='k')
            bars.add_artist(bary)             
 
        if sizex and labelx:
            textx = Text(text=labelx, x=sizex/2.0, y=-5*pixelxy[1], ha="center", va="top")
            bars.add_artist(textx)
            
        if sizey and labely:
            texty = Text(text=labely, rotation='vertical', y=sizey/2.0, x=-2*pixelxy[0], va="center", ha="right")
            bars.add_artist(texty)
            
        AnchoredOffsetbox.__init__(self, loc=7, pad=pad, borderpad=borderpad,
                                       child=bars, prop=prop, frameon=False, **kwargs)

def add_scalebar(ax, matchx=True, matchy=True, hidex=True, hidey=True, **kwargs):
    """ Add scalebars to axes

    Adds a set of scale bars to *ax*, matching the size to the ticks of the 
    plot and optionally hiding the x and y axes
 
    - ax : the axis to attach ticks to
    - matchx,matchy : if True, set size of scale bars to spacing between ticks
                    if False, size should be set using sizex and sizey params
    - hidex,hidey : if True, hide x-axis and y-axis of parent
    - **kwargs : additional arguments passed to AnchoredScaleBars
 
    Returns created scalebar object
    """
    def f(axis):
        l = axis.get_majorticklocs()
        return len(l)>1 and (l[1] - l[0])
    
    if matchx:
        kwargs['sizex'] = f(ax.xaxis)
        kwargs['labelx'] = str(kwargs['sizex'])
    if matchy:
        kwargs['sizey'] = f(ax.yaxis)
        kwargs['labely'] = str(kwargs['sizey'])
        
    sb = AnchoredScaleBar(ax.transData, **kwargs)
    ax.add_artist(sb)
 
    return sb
