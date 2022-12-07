import matplotlib.pyplot as plt
class GUI:
    def __init__(self, xlabel, ylabel, title) -> None:
        self.data = [0]
        self.x = [0]
        self.x_label = xlabel
        self.y_label = ylabel
        self.title = title
        self.fig = plt.gcf()

    def update_data(self, inp):
        self.data.append(self.data[-1] + inp)
        if len(self.data) != 1:
            self.x.append(len(self.data)-1)

    def draw(self):
        plt.plot(self.x, self.data)
        plt.title(self.title)
        plt.ylabel(self.y_label)
        plt.xlabel(self.x_label)
        plt.show(block=False)
        plt.show()


def draw(plots):
    for i, p in enumerate(plots):
        plt.subplot(2, 1, i+1)
        plt.plot(p.x, p.data)
        plt.title(p.title)
        plt.ylabel(p.y_label)
        plt.xlabel(p.x_label)
        plt.show(block=False)
    plt.show()