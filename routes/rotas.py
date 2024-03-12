from flask import Blueprint, request, jsonify
from dao import dao
import json

bp = Blueprint('rotas', __name__)

