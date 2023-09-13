from flask import Flask, request, jsonify
from Connect4 import Solver

app = Flask(__name__);

@app.route('/get_ai_move', methods=['POST'])
def get_ai_move():
  data = request.get_json();

  required_payload = [
     'board',
     'maxPlayer',
     'minPlayer',
     'maxDepth',
     'currentColumns',
     'winConditions'
  ]

  for payload in required_payload:
     if payload not in data:
      return jsonify({ 'error' : 'Missing required payloads' }), 400
  
  connect4 = Solver(data['board'], data['maxPlayer'], data['minPlayer'], data['maxDepth'], data['currentColumns'], data['winConditions'])

  print('Solving position with max depth of ' + str(data['maxDepth']))
  
  try:
    ai_move = connect4.solve()
  except:
    return jsonify({ 'error', 'Something went wrong with the solver'}), 400
  
  print('Done solving\n')

  return jsonify({ 'move': ai_move }), 200
  
@app.route('/wake', methods=['GET'])
def wake():
  print('Waking up')
  return jsonify({ 'message' : 'Hello, I am awake now' }), 200

if __name__ == '__main__':
   app.run()