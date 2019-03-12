import json
import webbrowser
import scheduler

from flask import Flask, request, render_template
from subprocess import check_output, Popen, PIPE
from time import sleep


app = Flask(__name__)


@app.route("/", methods=['GET'])
def _form():
    return render_template("submit.html")


@app.route("/", methods=['POST'])
def _scheduled():
    num_hours = float(request.form["quantity"])
    print("NUM_HOURS: ", num_hours)
    return "Your meeting is scheduled for: " + str(scheduler.schedule_event(num_hours))


def _port_number():
    return 5000
    # return "http://127.0.0.1:5000/ "


def _launch_ngrok():
    ngrok_command = "ngrok http " + str(_port_number())
    Popen(ngrok_command) #, shell=True)


def _get_ngrok_url():
    # get info from ngrok via command line process
    command = "curl http://127.0.0.1:4040/api/tunnels"
    process = Popen(command, shell=True, stdout=PIPE)
    sleep(0.4)
    process.wait()

    # get returned info
    values = process.communicate()[0]
    values = values.decode("utf-8")
    d = json.loads(values)

    return d['tunnels'][0]['public_url']


if __name__ == "__main__":
    _launch_ngrok()
    webbrowser.open(_get_ngrok_url())
    app.run()