from flask import Flask, request, render_template_string
from data_utils import fetch_routes, build_graph
from route_finder import bfs_find_routes

app = Flask(__name__)
graph = None

@app.before_first_request
def setup():
    global graph
    routes = fetch_routes()
    graph = build_graph(routes)

HTML_TEMPLATE = '''
<!doctype html>
<title>Hertz Freerider Ruttoptimering</title>
<h1>Sök rutt</h1>
<form method="post">
  Start: <input name="start" required><br>
  Slut: <input name="end" required><br>
  <button type="submit">Sök</button>
</form>
{% if routes %}
  <h2>Rutter hittade:</h2>
  <ul>
  {% for rutt in routes %}
    <li>{{ rutt | join(" → ") }}</li>
  {% endfor %}
  </ul>
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def index():
    routes = None
    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")
        routes = bfs_find_routes(graph, start, end)
    return render_template_string(HTML_TEMPLATE, routes=routes)

if __name__ == "__main__":
    app.run(debug=True)
