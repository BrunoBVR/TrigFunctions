import streamlit as st
import numpy as np
import pandas as pd

## Title
st.title("Exploring Trigonometric Functions")


def sec(x, a=1, b=1, c=0):

    return a * np.reciprocal(np.cos(b * x + c))


def cos(x, a=1, b=1, c=0):

    return a * np.cos(b * x + c)


with st.sidebar:
    ## Slider for function constants

    st.latex(r"a \cdot [\cos,\sec](b \cdot \theta + c)")
    s_a = st.slider("a:", -5.0, 5.0, 1.0, 0.5, key="t_a")
    s_b = st.slider("b:", -5.0, 5.0, 1.0, 0.5, key="t_b")
    s_c = st.slider("c:", -5.0, 5.0, 0.0, 0.5, key="t_c")

## Create dataframe with x, sin and cos

## Get x axis values
x = np.linspace(-np.pi, 2 * np.pi, 101)

trig_dict = {
    "x": x,
    "sec": sec(x, a=s_a, b=s_b, c=s_c),
    "cos": cos(x, a=s_a, b=s_b, c=s_c),
}

trig_df = pd.DataFrame(data=trig_dict)

# st.line_chart(trig_df, x="x")

## Using seaborn
import matplotlib.pyplot as plt
import seaborn as sns

fig = plt.figure(figsize=(12, 6))

## To get multiple of pi on x ticks
def multiple_formatter(denominator=2, number=np.pi, latex="\pi"):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def _multiple_formatter(x, pos):
        den = denominator
        num = np.int32(np.rint(den * x / number))
        com = gcd(num, den)
        (num, den) = (int(num / com), int(den / com))
        if den == 1:
            if num == 0:
                return r"$0$"
            if num == 1:
                return r"$%s$" % latex
            elif num == -1:
                return r"$-%s$" % latex
            else:
                return r"$%s%s$" % (num, latex)
        else:
            if num == 1:
                return r"$\frac{%s}{%s}$" % (latex, den)
            elif num == -1:
                return r"$\frac{-%s}{%s}$" % (latex, den)
            else:
                return r"$\frac{%s%s}{%s}$" % (num, latex, den)

    return _multiple_formatter


class Multiple:
    def __init__(self, denominator=2, number=np.pi, latex="\pi"):
        self.denominator = denominator
        self.number = number
        self.latex = latex

    def locator(self):
        return plt.MultipleLocator(self.number / self.denominator)

    def formatter(self):
        return plt.FuncFormatter(
            multiple_formatter(self.denominator, self.number, self.latex)
        )


## Plotting functions
sns.lineplot(data=trig_df, x="x", y="sec", label="a . sec(b. x + c)")
sns.lineplot(data=trig_df, x="x", y="cos", label="a . cos(b. x + c)")
plt.xlabel("x", fontsize=18)
plt.ylabel("Function Value", fontsize=18)

## Fix legend location
plt.legend(loc="upper right")

## Fix y range
plt.ylim(-4, 4)

## For the label
ax = plt.gca()
ax.grid(True)
ax.set_aspect(1.0)
ax.axhline(0, color="black", lw=2)
ax.axvline(0, color="black", lw=2)
ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.xaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter()))

# plt.grid()
st.pyplot(fig)
