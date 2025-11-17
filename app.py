# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
import nmap

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "labex"

# Initialize Nmap PortScanner
nm = nmap.PortScanner()


# Define Flask-WTF form for scanning inputs
class ScanForm(FlaskForm):
    host = StringField("Host", validators=[DataRequired()])
    ports = StringField(
        "Port Range",
        validators=[
            DataRequired(),
            Regexp(r"^\d+-\d+$", message="Format must be start-end"),
        ],
    )
    submit = SubmitField("Scan")


# Define route for the index page
@app.route("/", methods=["GET", "POST"])
def index():
    form = ScanForm()  # Instantiate the form
    if form.validate_on_submit():
        # Get data from the form
        host = form.host.data
        ports = form.ports.data  # Format: "start-end"
        # Redirect to the scan route with form data
        return redirect(url_for("scan", host=host, ports=ports))
    # Render the index page template with the form
    return render_template("index.html", form=form)


# Define route for the scan results
@app.route("/scan")
def scan():
    # Retrieve host and ports from the query string
    host = request.args.get("host")
    ports = request.args.get("ports")
    # Perform the scan using Nmap
    # -sV for service/version detection
    nm.scan(hosts=host, ports=ports, arguments="-sV")
    scan_results = []

    # Process scan results and store them in a list
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                service = nm[host][proto][port]
                scan_results.append(
                    {
                        "port": port,
                        "state": service["state"],
                        "name": service.get("name", "Unknown"),
                        "product": service.get("product", ""),
                        "version": service.get("version", ""),
                        "extra": service.get("extrainfo", ""),
                    }
                )

    # Render the results page template with the scan results
    return render_template("results.html", scan_results=scan_results, host=host)


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
