import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import matplotlib.image as mpimg
import bqplot
from matplotlib.colors import LinearSegmentedColormap
from numba import njit, prange

def representation_complexe():
    real = widgets.BoundedFloatText(value = 1, min = -2.0, max = 2.0, step = 0.1, disabled = True)
    imag = widgets.BoundedFloatText(value = 1, min = -2.0, max = 2.0, step = 0.1, disabled = True)
    sc_x = bqplot.LinearScale(min = -2, max = 2)
    sc_y = bqplot.LinearScale(min = -2, max = 2)
    ax_x = bqplot.Axis(scale=sc_x, offset=dict(value=0.5), grid_lines='none')
    ax_y = bqplot.Axis(scale=sc_y, orientation='vertical', offset=dict(value=0.5), grid_lines='none')
    z_point = bqplot.Scatter(x=[real.value], y=[imag.value], scales={'x': sc_x, 'y': sc_y}, colors=['green'], enable_move=True)
    z_point.update_on_move = True
    fig = bqplot.Figure(marks=[z_point], axes=[ax_x, ax_y], min_aspect_ratio=1, max_aspect_ratio=1)
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
    z_point = bqplot.Scatter(x=[z0.real], y=[z0.imag], scales={'x': sc_x, 'y': sc_y}, colors=['green'], enable_move=True, default_size=200)
    z_point.update_on_move = True
    z_label = bqplot.Label(x=[z0.real+.05], y=[z0.imag+.05], scales={'x': sc_x, 'y': sc_y}, colors=['green'], text=['z0'],  default_size=26, font_weight='bolder')

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

    fig = bqplot.Figure(marks=[scatt, lin, circle, z_point, z_label], axes=[ax_x, ax_y],  min_aspect_ratio=1, max_aspect_ratio=1)
    # fig = bqplot.Figure(marks=[scatt, lin, z_point, z_label], axes=[ax_x, ax_y],
    #              min_aspect_ratio=1, max_aspect_ratio=1)
    fig.layout.height = '800px'
    return fig



def plot_orbit(x0 = 0.5, y0 = 0.5, a = 0, b = 0):

    z0 = x0 + 1j*y0
    c  =  a + 1j*b

    sc_x = bqplot.LinearScale(min=-1.2, max=1.2)
    sc_y = bqplot.LinearScale(min=-1.2, max=1.2)

    c_point = bqplot.Scatter(x=[c.real], y=[c.imag], scales={'x': sc_x, 'y': sc_y}, colors=['red'], enable_move=True, default_size=200)
    c_point.update_on_move = True

    z_point = bqplot.Scatter(x=[z0.real], y=[z0.imag], scales={'x': sc_x, 'y': sc_y}, colors=['green'], enable_move=True, default_size=200)
    z_point.update_on_move = True

    c_label = bqplot.Label(x=[c.real+.05], y=[c.imag+.05], scales={'x': sc_x, 'y': sc_y}, colors=['red'], text=['c'], default_size=26, font_weight='bolder')

    z_label = bqplot.Label(x=[z0.real+.05], y=[z0.imag+.05], scales={'x': sc_x, 'y': sc_y}, colors=['green'], text=['z0'], default_size=26, font_weight='bolder')

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

    fig = bqplot.Figure(marks=[scatt, lin, circle, c_point, z_point, c_label, z_label], axes=[ax_x, ax_y], min_aspect_ratio=1, max_aspect_ratio=1)
    fig.layout.height = '800px'
    return fig


@njit(parallel=True)
def julia_smooth(a, b, n_max, N=300, xmin= -1.5, xmax = 1.5, ymin=-1.5, ymax =  1.5):
    image = np.zeros((N, N))
    for i in prange(N//2 + 1):
        for j in range(N):
            x = xmin + (xmax - xmin) * j / (N - 1)
            y = ymin + (ymax - ymin) * i / (N - 1)
            zr = x
            zi = y
            iteration = 0
            while zr*zr + zi*zi <= 4.0 and iteration < n_max:
                temp = zr*zr - zi*zi + a
                zi = 2.0*zr*zi + b
                zr = temp
                iteration += 1
            if iteration < n_max:
                mod = np.sqrt(zr*zr + zi*zi)
                nu = iteration + 1 - np.log(np.log(mod)) / np.log(2.0)
                image[i, j] = nu
                image[N - i - 1, N - j - 1] = nu
            else:
                image[i, j] = n_max
                image[N - i - 1, N - j - 1] = n_max
    return image

def julia_interactive(couleur_1=[59,67,113], couleur_2=[243,144,79],
                      xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5):
    couleur_1, couleur_2 = np.array(couleur_1)/255, np.array(couleur_2)/255
    cmap = LinearSegmentedColormap.from_list(
        "julia_custom",[couleur_1,couleur_2],256
    )
    n_slider = widgets.IntSlider(value=100,min=10,max=200,step=10,
                                 description='n_max',continuous_update=True)
    N_slider = widgets.IntSlider(value=600,min=100,max=1000,step=50,
                                 description='N',continuous_update=True)
    save_button = widgets.Button(description="Enregistrer")

    def save_image(event=None):
        point.set_visible(False)
        label.set_visible(False)
        fig.savefig("julia.png", dpi=600, bbox_inches="tight")
        point.set_visible(True)
        label.set_visible(True)
        fig.canvas.draw_idle()
    save_button.on_click(save_image)

    a, b = 0.0, 0.0
    dragging = {"active": False}
    last_update = {"t": 0}

    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis("off")
    img = julia_smooth(a,b,n_slider.value,N_slider.value,xmin,xmax,ymin,ymax)
    im = ax.imshow(img,cmap=cmap,extent=[xmin,xmax,ymin,ymax])
    point = ax.scatter(a, b, color="red", s=60, zorder=5)
    label = ax.text(a, b, r"$c = 0.00 + 0.00i$", color='red',
                    fontsize=12, zorder=5)

    def update(N=None):
        if N is None:
            N = N_slider.value
        img = julia_smooth(a, b, n_slider.value, N, xmin, xmax, ymin, ymax)
        im.set_data(img)
        fig.canvas.draw_idle()

    def update_label():
        signe = '+' if b >= 0 else '-'
        label.set_position((a, b))
        label.set_text(rf"   $  c = {a:.2f} {signe} {abs(b):.2f}\,i$")

    def on_press(event):
        if event.inaxes != ax:
            return
        dragging["active"] = True

    def on_release(event):
        if not dragging["active"]:
            return
        dragging["active"] = False
        # recalcul haute résolution au relâchement
        update()

    def on_move(event):
        nonlocal a, b
        if not dragging["active"]:
            return
        if event.inaxes != ax:
            return
        import time
        now = time.time()
        a = event.xdata
        b = event.ydata
        point.set_offsets([[a, b]])
        update_label()
        # throttling : recalcul image max toutes les 80ms
        if now - last_update["t"] > 0.08:
            last_update["t"] = now
            update(N=150)   # basse résolution pendant le drag
        else:
            fig.canvas.draw_idle()  # redessine juste le point et le label

    fig.canvas.mpl_connect("button_press_event", on_press)
    fig.canvas.mpl_connect("button_release_event", on_release)
    fig.canvas.mpl_connect("motion_notify_event", on_move)
    n_slider.observe(lambda x: update(), "value")
    N_slider.observe(lambda x: update(), "value")
    display(widgets.VBox([n_slider, N_slider, save_button]))
@njit(parallel=True)
def mandelbrot_smooth(n_max=100, N=300, xmin= -1.5, xmax = 1.5, ymin=-1.5, ymax =  1.5):
    image = np.zeros((N, N))
    for i in prange(N//2 + 1):
        for j in range(N):
            a = xmin + (xmax - xmin) * j / (N - 1)
            b = ymin + (ymax - ymin) * i / (N - 1)
            zr = 0
            zi = 0
            iteration = 0
            while zr*zr + zi*zi <= 4.0 and iteration < n_max:
                temp = zr*zr - zi*zi + a
                zi = 2.0*zr*zi + b
                zr = temp
                iteration += 1
            if iteration < n_max:
                mod = np.sqrt(zr*zr + zi*zi)
                nu = iteration + 1 - np.log(np.log(mod)) / np.log(2.0)
                image[i, j] = nu
                image[N - i - 1, j] = nu
            else :
                image[i, j] = n_max
                image[N - i - 1, j] = n_max
    return image

def mandelbrot_interactive(xmin=-2.25, xmax=0.75, ymin=-1.5, ymax=1.5, couleur_1 = [59, 67, 113], couleur_2 = [243, 144, 79]):
    couleur_1, couleur_2 = np.array(couleur_1)/255, np.array(couleur_2)/255
    n_slider = widgets.IntSlider(value=100, min=10, max=200, step=10, description='n_max :', continuous_update=True)
    N_slider = widgets.IntSlider( value=300, min=100, max=1000, step=50, description='N :', continuous_update=True)

    cmap_custom = LinearSegmentedColormap.from_list( "julia_custom", [couleur_1, couleur_2], N=256 )

    output = widgets.Output()

    view = {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax}

    fig, ax = plt.subplots(figsize=(8,8))
    ax.axis('off')
    img_plot = None
    def draw():
        nonlocal img_plot
        img = mandelbrot_smooth(n_slider.value, N_slider.value, **view)
        ax.clear()
        ax.axis('off')
        img_plot = ax.imshow(img, cmap=cmap_custom, extent=[view['xmin'], view['xmax'], view['ymin'], view['ymax']])
        fig.canvas.draw_idle()
    def on_scroll(event):
        # Zoom factor per scroll
        zoom = 0.9 if event.step > 0 else 1.1
        x_range = view['xmax'] - view['xmin']
        y_range = view['ymax'] - view['ymin']

        # Zoom around mouse pointer
        xcenter = event.xdata if event.xdata is not None else (view['xmin'] + view['xmax']) / 2
        ycenter = event.ydata if event.ydata is not None else (view['ymin'] + view['ymax']) / 2

        view['xmin'] = xcenter - x_range * zoom / 2
        view['xmax'] = xcenter + x_range * zoom / 2
        view['ymin'] = ycenter - y_range * zoom / 2
        view['ymax'] = ycenter + y_range * zoom / 2
        draw()

    fig.canvas.mpl_connect('scroll_event', on_scroll)

    def update(change=None):
        draw()

    n_slider.observe(update, names='value')
    N_slider.observe(update, names='value')

    update()

    display(widgets.VBox([n_slider, N_slider, output]))
