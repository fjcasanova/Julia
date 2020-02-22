import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import matplotlib.image as mpimg
import bqplot

def representation_complexe():
    real = widgets.BoundedFloatText(
        value=1,
        min=-2.0,
        max=2.0,
        step=0.1,
        disabled=True
    )

    imag = widgets.BoundedFloatText(
        value=1,
        min=-2.0,
        max=2.0,
        step=0.1,
        disabled=True
    )

    sc_x = bqplot.LinearScale(min=-2, max=2)
    sc_y = bqplot.LinearScale(min=-2, max=2)
    ax_x = bqplot.Axis(scale=sc_x, offset=dict(value=0.5), grid_lines='none')
    ax_y = bqplot.Axis(scale=sc_y, orientation='vertical', offset=dict(value=0.5), grid_lines='none')

    z_point = bqplot.Scatter(x=[real.value], y=[imag.value], scales={'x': sc_x, 'y': sc_y}, colors=['green'],
                   enable_move=True)
    z_point.update_on_move = True

    fig = bqplot.Figure(marks=[z_point], axes=[ax_x, ax_y],
             min_aspect_ratio=1, max_aspect_ratio=1)

    complex_z = widgets.HBox([widgets.Label('$z = $'), real, widgets.Label('$ + $'), imag, widgets.Label('$i$')])

    def update_z(change=None):
        real.value = z_point.x[0]
        imag.value = z_point.y[0]

    z_point.observe(update_z, names=['x', 'y'])

    #def update_point(change=None):
    #    z_point.x = [real.value]
    #    z_point.y = [imag.value]

    #real.observe(update_point, names='value')
    #imag.observe(update_point, names='value')

    return widgets.VBox([fig, complex_z], layout=widgets.Layout(align_items="center"))

def orbit(z, c =0, eps=1e-6, lim=1e5):
    out = [z]
    ite = 0
    while eps < np.abs(out[-1]) < lim and ite < 30:
        out.append(out[-1]**2+c)
        ite += 1
    return np.asarray(out)

def square_orbit(x0, y0):
    sc_x = bqplot.LinearScale(min=-1.2, max=1.2)
    sc_y = bqplot.LinearScale(min=-1.2, max=1.2)

    z0 = x0 + y0*1j

    z_point = bqplot.Scatter(x=[z0.real], y=[z0.imag], scales={'x': sc_x, 'y': sc_y}, colors=['green'],
                   enable_move=True, default_size=200)
    z_point.update_on_move = True


    z_label = bqplot.Label(x=[z0.real+.05], y=[z0.imag+.05], scales={'x': sc_x, 'y': sc_y}, colors=['green'],
                           text=['z0'],
                           default_size=26, font_weight='bolder')

    scatt = bqplot.Scatter(x=[], y=[], scales={'x': sc_x, 'y': sc_y}, colors=['black'], default_size=20)

    theta = np.linspace(0, 2.*np.pi, 1000)
    x = np.cos(theta)
    y = np.sin(theta)
    circle = bqplot.Lines(x=x, y=y, scales={'x': sc_x, 'y': sc_y}, colors=['black'])
    lin = bqplot.Lines(x=[], y=[], scales={'x': sc_x, 'y': sc_y}, colors=['black'], stroke_width=1)

    def update_line(change=None):
        out = orbit(z_point.x + 1j*z_point.y)
        z_label.x = z_point.x + 0.05
        z_label.y = z_point.y + 0.05
        lin.x = out.real
        lin.y = out.imag
        scatt.x = out.real.flatten()
        scatt.y = out.imag.flatten()

    update_line()
    # update line on change of x or y of scatter
    z_point.observe(update_line, names=['x'])
    z_point.observe(update_line, names=['y'])
    ax_x = bqplot.Axis(scale=sc_x, offset=dict(value=0.5), grid_lines='none')
    ax_y = bqplot.Axis(scale=sc_y, orientation='vertical', offset=dict(value=0.5), grid_lines='none')

    fig = bqplot.Figure(marks=[scatt, lin, circle, z_point, z_label], axes=[ax_x, ax_y],
                 min_aspect_ratio=1, max_aspect_ratio=1)
    fig.layout.height = '800px'
    return fig



def plot_orbit(x0 = 0.5, y0 = 0.5, a = 0, b = 0):

    z0 = x0 + 1j*y0
    c  =  a + 1j*b

    sc_x = bqplot.LinearScale(min=-1.2, max=1.2)
    sc_y = bqplot.LinearScale(min=-1.2, max=1.2)

    c_point = bqplot.Scatter(x=[c.real], y=[c.imag], scales={'x': sc_x, 'y': sc_y}, colors=['red'],
                   enable_move=True, default_size=200)
    c_point.update_on_move = True

    z_point = bqplot.Scatter(x=[z0.real], y=[z0.imag], scales={'x': sc_x, 'y': sc_y}, colors=['green'],
                   enable_move=True, default_size=200)
    z_point.update_on_move = True

    c_label = bqplot.Label(x=[c.real+.05], y=[c.imag+.05], scales={'x': sc_x, 'y': sc_y}, colors=['red'],
                           text=['c'],
                           default_size=26, font_weight='bolder')

    z_label = bqplot.Label(x=[z0.real+.05], y=[z0.imag+.05], scales={'x': sc_x, 'y': sc_y}, colors=['green'],
                           text=['z0'],
                           default_size=26, font_weight='bolder')

    scatt = bqplot.Scatter(x=[], y=[], scales={'x': sc_x, 'y': sc_y}, colors=['black'], default_size=20)

    theta = np.linspace(0, 2.*np.pi, 1000)
    x = np.cos(theta)
    y = np.sin(theta)
    circle = bqplot.Lines(x=x, y=y, scales={'x': sc_x, 'y': sc_y}, colors=['black'])
    lin = bqplot.Lines(x=[], y=[], scales={'x': sc_x, 'y': sc_y}, colors=['black'], stroke_width=1)

    def update_line1(change=None):
        out = orbit(z_point.x + 1j*z_point.y, c_point.x + 1j*c_point.y)
        c_label.x = c_point.x + 0.05
        c_label.y = c_point.y + 0.05
        z_label.x = z_point.x + 0.05
        z_label.y = z_point.y + 0.05
        lin.x = out.real
        lin.y = out.imag
        scatt.x = out.real.flatten()
        scatt.y = out.imag.flatten()

    update_line1()
    # update line on change of x or y of scatter
    c_point.observe(update_line1, names=['x'])
    c_point.observe(update_line1, names=['y'])
    z_point.observe(update_line1, names=['x'])
    z_point.observe(update_line1, names=['y'])
    ax_x = bqplot.Axis(scale=sc_x, offset=dict(value=0.5), grid_lines='none')
    ax_y = bqplot.Axis(scale=sc_y, orientation='vertical', offset=dict(value=0.5), grid_lines='none')

    fig = bqplot.Figure(marks=[scatt, lin, circle, c_point, z_point, c_label, z_label], axes=[ax_x, ax_y],
                 min_aspect_ratio=1, max_aspect_ratio=1)
    fig.layout.height = '800px'
    return fig