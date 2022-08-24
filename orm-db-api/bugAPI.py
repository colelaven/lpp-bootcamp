from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from bugService import BugNotFoundError, BugService

from models import Bug

app = Flask(__name__)
CORS(app)

bugService = BugService('bugs.db')

@app.route('/')
def home():
    return render_template('../index.html')


@app.route('/bugs')
def get_bugs():
    return jsonify(bugService.bugs)


@app.route('/bugs', methods=['POST'])
def save_new_bug():
    newBug = bugService.addBug(request.get_json()['name'])
    return jsonify(newBug), 201


@app.route('/bugs/<int:id>')
def view_bug(id):
    try:
        targetBug = bugService.getBug(id)
    except BugNotFoundError:
        return jsonify({ 'message' : 'bug not found'}), 404
    return jsonify(targetBug)


@app.route('/bugs/<int:id>', methods=['PUT'])
def update_bug(id):
    try:
        targetBug = bugService.updateBug(id, request.get_json())
    except BugNotFoundError:
        return jsonify({ 'message' : 'bug not found'}), 404
    return jsonify(targetBug)


@app.route('/bugs/<int:id>', methods=['DELETE'])
def delete_bug(id):
    try:
        bugService.deleteBug(id)
    except BugNotFoundError:
        return jsonify({ 'message' : 'bug not found'}), 404
    return jsonify({})


app.run(port=8080, debug=True)