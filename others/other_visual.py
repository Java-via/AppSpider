# _*_ coding: utf-8 _*_

"""
other_visual.py by xianhu
"""

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def simple_plot():
    """
    simple plot
    """
    x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    y_cos, y_sin = np.cos(x), np.sin(x)

    plt.figure(figsize=(8, 6), dpi=80)
    plt.title("plot title")
    plt.grid(True)

    plt.xlabel("x label")
    plt.xlim(-4.0, 4.0)
    plt.xticks(np.linspace(-4, 4, 9, endpoint=True))

    plt.ylabel("y label")
    plt.ylim(-1.0, 1.0)
    plt.yticks(np.linspace(-1, 1, 9, endpoint=True))

    plt.plot(x, y_cos, "b--", linewidth=2.0, label="cos")
    plt.plot(x, y_sin, "g-", linewidth=2.0, label="sin")

    # loc in [upper, lower, left, right, center]
    plt.legend(loc="upper left", shadow=True)

    plt.show()
    return
# simple_plot()


def simple_advanced_plot():
    """
    simple advanced plot
    """
    x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    y_cos, y_sin = np.cos(x), np.sin(x)

    plt.figure(figsize=(8, 6), dpi=80)
    plt.title("plot title")
    plt.grid(True)

    ax_1 = plt.subplot(111)
    ax_1.plot(x, y_cos, color="blue", linewidth=2.0, linestyle="--", label="cos in left")
    ax_1.legend(loc="upper left", shadow=True)
    ax_1.set_ylabel("y lable for cos in left")
    ax_1.set_ylim(-1.0, 1.0)
    ax_1.set_yticks(np.linspace(-1, 1, 9, endpoint=True))

    ax_2 = ax_1.twinx()
    ax_2.plot(x, y_sin, color="green", linewidth=2.0, linestyle="-", label="sin in right")
    ax_2.legend(loc="upper right", shadow=True)
    ax_2.set_ylabel("y lable for sin in right")
    ax_2.set_ylim(-2.0, 2.0)
    ax_2.set_yticks(np.linspace(-2, 2, 9, endpoint=True))

    ax_2.set_xlabel("x label")
    ax_2.set_xlim(-4.0, 4.0)
    ax_2.set_xticks(np.linspace(-4, 4, 9, endpoint=True))

    plt.show()
    return
# simple_advanced_plot()


def subplot_plot():
    """
    subplot plot
    """
    style_list = ["g+-", "r*-", "b.-", "yo-"]
    for num in range(4):
        x = np.linspace(0.0, 2+num, num=10*(num+1))
        y = np.sin((5-num) * np.pi * x)

        plt.subplot(2, 2, num+1)
        plt.plot(x, y, style_list[num])

    plt.grid(True)
    plt.show()
    return
# subplot_plot()


def bar_plot():
    """
    bar plot
    """
    means_men = (20, 35, 30, 35, 27)
    means_women = (25, 32, 34, 20, 25)

    index = np.arange(len(means_men))
    bar_width = 0.35

    plt.bar(index, means_men, width=bar_width, alpha=0.4, color="b", label="Men")
    plt.bar(index+bar_width, means_women, width=bar_width, alpha=0.4, color="r", label="Women")
    plt.legend(loc="upper right", shadow=True)

    for x, y in zip(index, means_men):
        plt.text(x+(bar_width/2), y+0.3, "%d" % y, ha="center", va="bottom")
    for x, y in zip(index, means_women):
        plt.text(x+bar_width+(bar_width/2), y+0.3, "%d" % y, ha="center", va="bottom")

    plt.ylim(0, 45)
    plt.xlabel("Group")
    plt.ylabel("Scores")
    plt.xticks(index+bar_width, ("A组", "B组", "C组", "D组", "E组"))

    plt.show()
    return
# bar_plot()


def barh_plot():
    """
    barh plot
    """
    means_men = (20, 35, 30, 35, 27)
    means_women = (25, 32, 34, 20, 25)

    index = np.arange(len(means_men))
    bar_height = 0.35

    plt.barh(index, means_men, height=bar_height, alpha=0.4, color="b", label="Men")
    plt.barh(index+bar_height, means_women, height=bar_height, alpha=0.4, color="r", label="Women")
    plt.legend(loc="upper right", shadow=True)

    for x, y in zip(index, means_men):
        plt.text(y+0.3, x+(bar_height/2), "%d" % y, ha="left", va="center")
    for x, y in zip(index, means_women):
        plt.text(y+0.3, x+bar_height+(bar_height/2), "%d" % y, ha="left", va="center")

    plt.xlim(0, 45)
    plt.xlabel("Scores")
    plt.ylabel("Group")
    plt.yticks(index+bar_height, ("A组", "B组", "C组", "D组", "E组"))

    plt.show()
    return
# barh_plot()


def bar_advanced_plot():
    """
    bar advanced plot
    """
    means_men = np.array((20, 35, 30, 35, 27, 25, 32, 34, 20, 25))
    means_women = np.array((25, 32, 34, 20, 25, 20, 35, 30, 35, 27))

    index = np.arange(len(means_men))
    bar_width = 0.8

    plt.bar(index, means_men, width=bar_width, alpha=0.4, color="b", label="Men")
    plt.bar(index, -means_women, width=bar_width, alpha=0.4, color="r", label="Women")

    plt.plot(index+(bar_width/2), means_men, marker="o", linestyle="-", color="r", label="Men line")
    plt.plot(index+(bar_width/2), -means_women, marker=".", linestyle="--", color="b", label="Womem line")

    for x, y in zip(index, means_men):
        plt.text(x+(bar_width/2), y+1, "%d" % y, ha="center", va="bottom")
    for x, y in zip(index, means_women):
        plt.text(x+(bar_width/2), -y-1, "%d" % y, ha="center", va="top")

    plt.ylim(-45, 80)
    plt.legend(loc="upper left", shadow=True)

    plt.show()
    return
# bar_advanced_plot()


def table_plot():
    """
    table plot, bottom=bottom
    """
    data = np.array([
        [1, 4, 2, 5, 2],
        [2, 1, 1, 3, 6],
        [5, 3, 6, 4, 1]
    ])
    index = np.arange(len(data[0]))
    color_index = ["r", "g", "b"]

    bottom = np.array([0, 0, 0, 0, 0])
    for i in range(len(data)):
        plt.bar(index+0.25, data[i], width=0.5, color=color_index[i], bottom=bottom, alpha=0.7, label="label %d" % i)
        bottom += data[i]
    plt.legend(loc="upper left", shadow=True)

    plt.show()
    return
# table_plot()


def histograms_plot():
    """
    histograms plot
    """
    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)
    num_bins = 50

    n, bins, patches = plt.hist(x, bins=num_bins, normed=1, color="green", alpha=0.6, label="hist")

    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, "r--", label="line")
    plt.legend(loc="upper left", shadow=True)

    plt.show()
    return
# histograms_plot()


def pie_plot():
    """
    pie plot
    """
    sizes = [15, 30, 45, 10]
    explode = [0, 0.05, 0, 0]
    labels = ["Frogs", "Hogs", "Dogs", "Logs"]
    colors = ["yellowgreen", "gold", "lightskyblue", "lightcoral"]

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=90)
    plt.axis("equal")

    plt.show()
    return
# pie_plot()


def scatter_plot():
    """
    scatter plot
    """
    point_count = 1000
    x_index = np.random.random(point_count)
    y_index = np.random.random(point_count)
    color_list = np.random.random(point_count)
    scale_list = np.random.random(point_count) * 100

    plt.scatter(x_index, y_index, s=scale_list, c=color_list, marker="o")

    plt.show()
    return
# scatter_plot()


def fill_plot():
    """
    fill plot
    """
    x = np.linspace(-2*np.pi, 2*np.pi, 1000, endpoint=True)
    y = np.sin(x)

    plt.plot(x, y, color="blue", alpha=1.00)

    # plt.fill_between(x, y1, y2, where=None, *kwargs)
    plt.fill_between(x, 0, y, y > 0, color="blue", alpha=.25)
    plt.fill_between(x, 0, y, y < 0, color="red", alpha=.25)

    plt.show()
    return
# fill_plot()


def radar_plot():
    """
    radar plot
    """
    labels = np.array(["A", "B", "C", "D", "E", "F"])
    data = np.array([38, 43, 90, 67, 89, 73])
    theta = np.linspace(0, 2*np.pi, len(data), endpoint=False)

    data = np.concatenate((data, [data[0]]))
    theta = np.concatenate((theta, [theta[0]]))

    plt.subplot(111, polar=True)
    plt.thetagrids(theta*(180/np.pi), labels=labels)
    plt.rgrids(np.arange(20, 101, 20), labels=["20", "40", "60", "80"], angle=0)
    plt.ylim(0, 100)

    plt.plot(theta, data, "bo-", linewidth=2)
    plt.fill(theta, data, color="red", alpha=0.25)

    plt.show()
    return
# radar_plot()


def three_dimension_scatter():
    """
    3d scatter plot
    """
    number = 1000
    x = np.random.random(number)
    y = np.random.random(number)
    z = np.random.random(number)
    color = np.random.random(number)
    scale = np.random.random(number) * 100

    fig = plt.figure()
    # ax = fig.gca(projection="3d")
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, s=scale, c=color, marker=".")

    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_zlabel("Z Label")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)

    plt.show()
    return
# three_dimension_scatter()


def three_dimension_line():
    """
    3d line plot
    """
    number = 1000
    x = np.linspace(0, 1, number)
    y = np.linspace(0, 1, number)
    z = np.sin(x * 2 * np.pi) / (y + 0.1)

    fig = plt.figure()
    ax = fig.gca(projection="3d")
    # ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, z, color="red", linestyle="-")

    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_zlabel("Z Label")

    plt.show()
    return
# three_dimension_line()


def three_dimension_bar():
    """
    3d bar plot
    """
    xpos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ypos = [2, 3, 4, 5, 1, 6, 2, 1, 7, 2]
    zpos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    dx = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    dy = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    dz = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    fig = plt.figure()
    ax = fig.gca(projection="3d")
    # ax = fig.add_subplot(111, projection="3d")
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, alpha=0.5)

    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_zlabel("Z Label")

    plt.show()
    return
# three_dimension_bar()
