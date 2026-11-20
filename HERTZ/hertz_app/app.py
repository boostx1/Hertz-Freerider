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
<title>Hertz Freerider Route Planner</title>
<h1>Find a route</h1>
<form method="post">
  Start: <input name="start" required><br>
  Destination: <input name="end" required><br>
  <button type="submit">Search</button>
</form>
{% if routes %}
  <h2>Available routes</h2>
  <ul>
  {% for route in routes %}
    <li>{{ route | join(" → ") }}</li>
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
