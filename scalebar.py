from matplotlib.offsetbox import AnchoredOffsetbox


class AnchoredScaleBar(AnchoredOffsetbox):
    def __init__(self, transform, sizex=0, sizey=0, labelx=None, labely=None,
                 loc=4, pad=0.1, borderpad=0.1, sep=2, prop=None, fontsize='medium', **kwargs):
        """
        Modified, draws a horizontal and/or vertical bar with the size in data coordinate
        of the give axes. A label will be drawn underneath (center-aligned).

        Parameters
        ----------
        transform : the coordinate frame (typically axes.transData)
        sizex, sizey : width of x,y bar, in data units. 0 to omit
        labelx, labely : labels for x,y bars; None to omit
        loc : position in containing axes
        pad, borderpad : padding, in fraction of the legend font size (or prop)
        sep : separation between labels and bars in points.
        **kwargs : additional arguments passed to base class constructor

        Notes
        -----
        Adapted from mpl_toolkits.axes_grid2

        """
        from matplotlib.lines import Line2D
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
            textx = Text(text=labelx, x=sizex/2.0, y=-5*pixelxy[1], ha='center', va='top', size=fontsize)
            bars.add_artist(textx)

        if sizey and labely:
            texty = Text(text=labely, rotation='vertical', y=sizey/2.0, x=-2*pixelxy[0],
                         va='center', ha='right', size=fontsize)
            bars.add_artist(texty)

        AnchoredOffsetbox.__init__(self, loc=loc, pad=pad, borderpad=borderpad,
                                       child=bars, prop=prop, frameon=False, **kwargs)


def add_scalebar(ax, matchx=True, matchy=True, hidex=True, hidey=True, fontsize='medium', units='ms', **kwargs):
    """Add scalebars to axes
    Adds a set of scale bars to *ax*, matching the size to the ticks of the
    plot and optionally hiding the x and y axes

    Parameters
    ----------
    ax :
        The axis to attach ticks to
    matchx, matchy : boolean
        If True (default), set size of scale bars to spacing between ticks
        If False, size should be set using sizex and sizey params
    hidex, hidey : boolean
        If True, hide x-axis and y-axis of parent
    **kwargs : additional arguments passed to AnchoredScaleBars

    Returns created scalebar object
    """
    from matplotlib.ticker import AutoLocator
    locator = AutoLocator()

    def find_loc(vmin, vmax):
        loc = locator.tick_values(vmin, vmax)
        return len(loc)>1 and (loc[1] - loc[0])

    if matchx:
        kwargs['sizex'] = find_loc(*ax.get_xlim())
#         kwargs['labelx'] = str(kwargs['sizex'])
        if units == 'ms':
            kwargs['labelx'] = str(int(round(kwargs['sizex']*1000, 2))) + ' ms'
        elif units == 's':
            kwargs['labelx'] = str(int(round(kwargs['sizex'], 2))) + ' s'

    if matchy:
        kwargs['sizey'] = find_loc(*ax.get_ylim())
        kwargs['labely'] = str(kwargs['sizey'])

    scalebar = AnchoredScaleBar(ax.transData, fontsize=fontsize, **kwargs)
    ax.add_artist(scalebar)

    return scalebar
