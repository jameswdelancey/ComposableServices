from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template_string, send_file

app = Flask(__name__)

# HTML template that will display the image
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Matplotlib Chart</title>
</head>
<body>
  <h1>Example Chart from Pandas DataFrame</h1>
  <img src="{{ url_for('plot_png') }}" alt="Chart from Matplotlib">
</body>
</html>
"""


@app.route("/")
def home():
    # Render the HTML template with the chart
    return render_template_string(HTML_TEMPLATE)


@app.route("/plot.png")
def plot_png():
    # Create a Pandas DataFrame with example data
    df = pd.DataFrame({"x": range(1, 11), "y": [2, 1, 4, 3, 2, 5, 4, 6, 5, 7]})

    # Create a plot using Matplotlib
    fig, ax = plt.subplots()
    df.plot(x="x", y="y", ax=ax)
    ax.set_title("Example Chart")

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Send the buffer as a response
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
