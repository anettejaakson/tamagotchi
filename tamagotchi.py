from tkinter import *
import datetime

traits = [
    {'text': 'Sööda', 'color': '#00ff44', 'percent': 100, 'decay': 3, "path": "soob.gif"},
    {'text': 'Pese', 'color': '#007fff', 'percent': 100, 'decay': 1, "path": "peseb.gif"},
    {'text': 'Mängi', 'color': '#ff2200', 'percent': 100, 'decay': 2, "path": "mangib.gif"},
    {'text': 'WC', 'color': '#ffff00', 'percent': 100, 'decay': 2.5, "path": "wc.gif"}
]

config = {}
config['window_width'] = 400
config['window_height'] = 400
config['window_background'] = '#222222'
config['button_width'] = config['window_width'] / len(traits)
config['button_height'] = 50
config['button_background'] = '#333333'
config['button_foreground'] = '#ffffff'
config['button_hover_background'] = '#555555'
config['progressbar_height'] = 5
config['progressbar_background'] = '#555555'
config['general_progressbar_height'] = 10
config['general_progressbar_widht'] = config['window_width']
config['general_progressbar_y'] = 0
config['update_rate'] = 10


def redraw():
    for i, trait in enumerate(traits):
        progressbar_canvas.coords(
            trait['progressbar'],
            config['button_width'] * i,
            0,
            config['button_width'] * (i + traits[i]['percent'] / 100),
            config['progressbar_height']

        )


def update():
    if info['dead']:
        root.after(1000 // config['update_rate'], update)
        return

    sum = 0

    for trait in traits:
        trait['percent'] -= trait['decay'] / config['update_rate']

        if trait['percent'] < 0:
            trait['percent'] = 0

        sum += trait['percent']

        if not info["exceeded"]:
            vahe = (datetime.datetime.now() - info["time"]).total_seconds()

            if vahe > 2:
                change_picture("wombat.gif")
                info["exceeded"] = True

    sum = (sum - (4 * 25)) / 75 * 0.25

    if sum <= 0:
        change_picture("dead.gif")
        info['dead'] = True
        

    redraw()
    general_progressbar_canvas.coords(gpr, 0, 0, sum * config['general_progressbar_widht'],
                                      config['general_progressbar_height'])
    general_progressbar_canvas.itemconfig(gpr, fill=percentage_to_color(sum))

    root.after(1000 // config['update_rate'], update)


def on_click(trait):
    trait['percent'] += 25

    if trait['percent'] > 100:
        trait['percent'] = 100

    info["time"] = datetime.datetime.now()
    info["exceeded"] = False

    change_picture(trait["path"])

    redraw()


def percentage_to_color(protsent):
    if protsent < 0:
        return '#%02x%02x00' % (255, 0)
    elif protsent < 0.5:
        return '#%02x%02x00' % (255, round(255 * protsent / 0.5))
    else:
        return '#%02x%02x00' % (255 - round(255 * (protsent - 0.5) / 0.5), 255)


def change_picture(failname):
    img = PhotoImage(file=failname)
    picture.configure(image=img)
    picture.image = img


root = Tk()
root.configure(background=config['window_background'])
root.resizable(width=False, height=False)
root.geometry(f'{config["window_width"]}x{config["window_height"]}')
root.wm_title('Vombatlase tamagotchi')

progressbar_canvas = Canvas(
    root,
    bd=0,
    highlightthickness=0,
    relief='ridge',
    background=config['progressbar_background']
)

progressbar_canvas.place(
    x=0,
    y=config['window_height'] - config['button_height'] - config['progressbar_height'],
    width=config['window_width'],
    height=config['progressbar_height']
)

for i, trait in enumerate(traits):
    button = Button(
        root,
        text=trait['text'],
        foreground=config['button_foreground'],
        background=config['button_background'],
        activebackground=trait['color'],
        borderwidth=0,
        relief=SUNKEN,
        command=lambda trait=trait: on_click(trait)
    )

    button.bind('<Enter>', lambda _, element=button: element.configure(background=config['button_hover_background']))
    button.bind('<Leave>', lambda _, element=button: element.configure(background=config['button_background']))

    button.place(
        x=i * config['button_width'],
        y=config['window_width'] - config['button_height'],
        width=config['button_width'],
        height=config['button_height']
    )

    trait['progressbar'] = progressbar_canvas.create_rectangle(
        (0, 0, 0, 0),
        fill=trait['color'],
        width=0
    )

info = {
    "time": datetime.datetime.now(),
    "exceeded": True,
    "dead": False
}

p_picture = PhotoImage(file="wombat.gif")
picture = Label(root, image=p_picture)
picture.place(x=0, y=-20, width=config["window_width"], height=config["window_height"] - 35)

general_progressbar_canvas = Canvas(
    root,
    bd=0,
    highlightthickness=0,
    relief='ridge',
    background=config['progressbar_background']
)

general_progressbar_canvas.place(
    x=(config['window_width'] - config['general_progressbar_widht']) / 2,
    y=config['general_progressbar_y'],
    width=config['general_progressbar_widht'],
    height=config['general_progressbar_height']
)

gpr = general_progressbar_canvas.create_rectangle(
    (0, 0, config['general_progressbar_widht'], config['general_progressbar_height']),
    fill='#00ff44',
    width=0
)

update()

root.mainloop()
