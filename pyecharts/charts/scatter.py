#!/usr/bin/env python
#coding=utf-8

try:
    from PIL import Image
except ImportError:
    import Image

from pyecharts.base import Base
from pyecharts.option import get_all_options

class Scatter(Base):
    """
    <<< Scatter chart >>>
    The scatter chart in rectangular coordinate could be used to present the relation between x and y.
    If data have multiple dimensions, the values of the other dimensions can be visualized through symbol with
    various sizes and colors, which becomes a bubble chart. These can be done by using with visualMap component.
    """
    def __init__(self, title="", subtitle="", **kwargs):
        super(Scatter, self).__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, x_value, y_value,
              symbol_size=10,
              **kwargs):
        """

        :param name:
            Series name used for displaying in tooltip and filtering with legend,
            or updaing data and configuration with setOption.
        :param x_axis:
            data of xAxis
        :param y_axis:
            data of yAxis
        :param symbol_size:
            symbol size
        :param kwargs:
        """
        if isinstance(x_value, list) and isinstance(y_value, list):
            assert len(x_value) == len(y_value)
            kwargs.update(type="scatter")
            chart = get_all_options(**kwargs)
            xaxis, yaxis = chart['xy_axis']
            self._option.update(xAxis=xaxis, yAxis=yaxis)
            self._option.get('legend')[0].get('data').append(name)
            self._option.get('series').append({
                "type": "scatter",
                "name": name,
                "symbol": chart['symbol'],
                "symbolSize": symbol_size,
                "data": [list(z) for z in zip(x_value, y_value)],
                "label": chart['label'],
                "indexflag": self._option.get('_index_flag')
            })
            self._legend_visualmap_colorlst(**kwargs)
        else:
            raise TypeError("x_axis and y_axis must be list")

    def draw(self, path, color=None):
        """ Converts the pixels on the image to an array

        :param path:
            path of Image that want to draw
        :param color:
            select a color to exclude, (225, 225, 225) means Keep only white pixel information.
        :return:
        """
        color = color or (255, 255, 255)
        im = Image.open(path)
        width, height = im.size
        imarray = im.load()
        # flip vertical Images
        for x in range(width):
            for y in range(height):
                if y < int(height / 2):
                    imarray[x, y], imarray[x, height-y-1] = imarray[x, height-y-1], imarray[x, y]
        # [:3] is r,g,b
        result = [(x, y) for x in range(width) for y in range(height) if imarray[x, y][:3] != color]
        return self.cast(result)
