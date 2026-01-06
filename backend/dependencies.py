import sys
import os

# Add ml_engine to path to ensure imports work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_engine'))

from ml_engine.predictor import MLPredictor
from ml_engine.graph_logic import KnowledgeEngine

# Initialize ML components (singleton pattern)
predictor = None
knowledge_engine = None

def get_predictor():
    global predictor
    if predictor is None:
        predictor = MLPredictor()
    return predictor

def get_knowledge_engine():
    global knowledge_engine
    if knowledge_engine is None:
        knowledge_engine = KnowledgeEngine()
    return knowledge_engine
