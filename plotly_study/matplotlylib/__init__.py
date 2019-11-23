"""
matplotlylib
============

This module converts matplotlib figure objects into JSON structures which can
be understood and visualized by plotly_study.

Most of the functionality should be accessed through the parent directory's
'tools' module or 'plotly' package.

"""
from __future__ import absolute_import

from plotly_study.matplotlylib.renderer import PlotlyRenderer
from plotly_study.matplotlylib.mplexporter import Exporter
