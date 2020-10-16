from flask import Flask
from genetic_algorithm import execute_steady_state

app = Flask(__name__)

@app.route('/')
def generate_data():
    result = execute_steady_state()
    return {
        "message": "individu terbaik",
        "x1":  result[0]["individual_data"]['binary']['x1'],
        "x2": result[0]["individual_data"]['binary']['x2'],
        "nilai_fitness":  str(result[0]["fitness_value"])
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
