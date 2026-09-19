"""
FinSight AI - Multi-Asset Quantitative Intelligence Backtesting Platform
Main Application Entry Point

This module orchestrates:
- Data pipeline & ingestion
- Strategy backtesting engine
- Portfolio optimization
- Risk analysis & reporting
- REST API & WebSocket connections
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
from functools import wraps

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# ============================================================================
# LOCAL MODULE IMPORTS (Update paths based on your project structure)
# ============================================================================
try:
    from src.data_pipeline import DataPipeline
    from src.backtesting_engine import BacktestingEngine
    from src.portfolio_optimizer import PortfolioOptimizer
    from src.risk_analyzer import RiskAnalyzer
    from src.technical_indicators import TechnicalIndicators
    from src.ml_models import MLPredictor
    from src.database import DatabaseManager
    from src.config import Config
    from src.logger_config import setup_logging
    from src.utils import validate_input, handle_errors
except ImportError as e:
    print(f"Warning: Module import error - {e}. Running in limited mode.")

# ============================================================================
# INITIALIZATION
# ============================================================================
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)
setup_logging()

# Flask app initialization
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# WebSocket support
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ============================================================================
# GLOBAL INSTANCES
# ============================================================================
config = Config()
data_pipeline = None
backtest_engine = None
portfolio_optimizer = None
risk_analyzer = None
db_manager = None
technical_indicators = None
ml_predictor = None

# Active sessions tracking
active_backtests = {}
active_optimizations = {}


# ============================================================================
# INITIALIZATION FUNCTION
# ============================================================================
def initialize_app():
    """Initialize all application modules"""
    global data_pipeline, backtest_engine, portfolio_optimizer, risk_analyzer
    global db_manager, technical_indicators, ml_predictor
    
    try:
        logger.info("Initializing FinSight AI application...")
        
        db_manager = DatabaseManager(config.DATABASE_URL)
        data_pipeline = DataPipeline(config, db_manager)
        backtest_engine = BacktestingEngine(config)
        portfolio_optimizer = PortfolioOptimizer()
        risk_analyzer = RiskAnalyzer()
        technical_indicators = TechnicalIndicators()
        ml_predictor = MLPredictor(config)
        
        logger.info("✓ All modules initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        return False


# ============================================================================
# DECORATORS
# ============================================================================
def require_auth(f):
    """Authentication decorator for API endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_auth_token(token):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


def validate_auth_token(token):
    """Validate JWT token"""
    try:
        # Implement your token validation logic
        return True
    except:
        return False


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def safe_execute(func, *args, **kwargs):
    """Safely execute functions with error handling"""
    try:
        return {'status': 'success', 'data': func(*args, **kwargs)}
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {e}")
        return {'status': 'error', 'message': str(e)}


# ============================================================================
# ROUTES: DATA INGESTION & MANAGEMENT
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/data/ingest', methods=['POST'])
def ingest_data():
    """
    Ingest market data (CSV, JSON, or API)
    Expected JSON:
    {
        "source": "csv|api|json",
        "assets": ["BTC", "ETH", "SPY"],
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "interval": "1d" (1m, 5m, 15m, 1h, 1d, 1w)
    }
    """
    try:
        payload = request.get_json()
        
        # Validate input
        required_fields = ['source', 'assets']
        if not all(field in payload for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Fetch data
        result = data_pipeline.fetch_data(
            assets=payload['assets'],
            source=payload.get('source', 'api'),
            start_date=payload.get('start_date'),
            end_date=payload.get('end_date'),
            interval=payload.get('interval', '1d')
        )
        
        if result.get('status') == 'success':
            # Store in database
            db_manager.store_market_data(result['data'])
            return jsonify({
                'status': 'success',
                'message': f"Ingested data for {len(payload['assets'])} assets",
                'records': len(result['data'])
            }), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Data ingestion error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/market/<asset>', methods=['GET'])
def get_market_data(asset):
    """
    Get market data for a specific asset
    Query params: start_date, end_date, interval
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        interval = request.args.get('interval', '1d')
        
        data = data_pipeline.get_asset_data(
            asset=asset,
            start_date=start_date,
            end_date=end_date,
            interval=interval
        )
        
        if data is not None:
            return jsonify({
                'status': 'success',
                'asset': asset,
                'records': len(data),
                'data': data.to_dict('records')
            }), 200
        else:
            return jsonify({'error': 'No data found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: BACKTESTING
# ============================================================================

@app.route('/api/backtest/create', methods=['POST'])
def create_backtest():
    """
    Create and run a backtest
    Expected JSON:
    {
        "strategy_name": "strategy_name",
        "assets": ["BTC", "ETH"],
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "initial_capital": 100000,
        "strategy_params": {...}
    }
    """
    try:
        payload = request.get_json()
        
        # Validate required fields
        required = ['strategy_name', 'assets', 'start_date', 'initial_capital']
        if not all(f in payload for f in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create backtest ID
        backtest_id = f"bt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Fetch data for assets
        data = data_pipeline.fetch_data(
            assets=payload['assets'],
            start_date=payload['start_date'],
            end_date=payload.get('end_date')
        )
        
        if data.get('status') != 'success':
            return jsonify({'error': 'Failed to fetch market data'}), 400
        
        # Run backtest
        backtest_result = backtest_engine.run_backtest(
            strategy_name=payload['strategy_name'],
            data=data['data'],
            initial_capital=payload['initial_capital'],
            strategy_params=payload.get('strategy_params', {})
        )
        
        # Store backtest result
        active_backtests[backtest_id] = backtest_result
        db_manager.store_backtest_result(backtest_id, backtest_result)
        
        return jsonify({
            'status': 'success',
            'backtest_id': backtest_id,
            'results': {
                'total_return': backtest_result.get('total_return'),
                'sharpe_ratio': backtest_result.get('sharpe_ratio'),
                'max_drawdown': backtest_result.get('max_drawdown'),
                'win_rate': backtest_result.get('win_rate'),
                'trades': backtest_result.get('num_trades')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Backtest creation error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/backtest/<backtest_id>', methods=['GET'])
def get_backtest_result(backtest_id):
    """Get backtest results and analysis"""
    try:
        if backtest_id in active_backtests:
            result = active_backtests[backtest_id]
        else:
            result = db_manager.get_backtest_result(backtest_id)
        
        if result:
            return jsonify({
                'status': 'success',
                'backtest_id': backtest_id,
                'results': result
            }), 200
        else:
            return jsonify({'error': 'Backtest not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/backtest/<backtest_id>/equity-curve', methods=['GET'])
def get_equity_curve(backtest_id):
    """Get equity curve data for visualization"""
    try:
        if backtest_id in active_backtests:
            result = active_backtests[backtest_id]
        else:
            result = db_manager.get_backtest_result(backtest_id)
        
        equity_curve = result.get('equity_curve', [])
        dates = result.get('dates', [])
        
        return jsonify({
            'status': 'success',
            'data': list(zip(dates, equity_curve))
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: PORTFOLIO OPTIMIZATION
# ============================================================================

@app.route('/api/optimize/portfolio', methods=['POST'])
def optimize_portfolio():
    """
    Optimize portfolio allocation
    Expected JSON:
    {
        "assets": ["BTC", "ETH", "SPY"],
        "target_return": 0.10,
        "max_risk": 0.15,
        "constraints": {...}
    }
    """
    try:
        payload = request.get_json()
        optimize_id = f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Fetch historical data for correlation
        data = data_pipeline.fetch_data(
            assets=payload['assets'],
            interval='1d',
            periods=252  # 1 year of data
        )
        
        if data.get('status') != 'success':
            return jsonify({'error': 'Failed to fetch data'}), 400
        
        # Optimize
        result = portfolio_optimizer.optimize(
            data=data['data'],
            assets=payload['assets'],
            target_return=payload.get('target_return'),
            max_risk=payload.get('max_risk'),
            constraints=payload.get('constraints', {})
        )
        
        active_optimizations[optimize_id] = result
        
        return jsonify({
            'status': 'success',
            'optimize_id': optimize_id,
            'allocation': result.get('allocation'),
            'expected_return': result.get('expected_return'),
            'expected_risk': result.get('expected_risk'),
            'sharpe_ratio': result.get('sharpe_ratio')
        }), 200
        
    except Exception as e:
        logger.error(f"Portfolio optimization error: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: RISK ANALYSIS
# ============================================================================

@app.route('/api/risk/analyze', methods=['POST'])
def analyze_risk():
    """
    Analyze portfolio risk metrics
    Expected JSON:
    {
        "portfolio": {"BTC": 0.5, "ETH": 0.3, "SPY": 0.2},
        "confidence_level": 0.95
    }
    """
    try:
        payload = request.get_json()
        portfolio = payload.get('portfolio', {})
        confidence = payload.get('confidence_level', 0.95)
        
        # Fetch market data for assets
        assets = list(portfolio.keys())
        data = data_pipeline.fetch_data(assets=assets, periods=252)
        
        if data.get('status') != 'success':
            return jsonify({'error': 'Failed to fetch data'}), 400
        
        # Analyze risk
        risk_metrics = risk_analyzer.calculate_metrics(
            data=data['data'],
            portfolio=portfolio,
            confidence_level=confidence
        )
        
        return jsonify({
            'status': 'success',
            'metrics': {
                'var': risk_metrics.get('value_at_risk'),
                'cvar': risk_metrics.get('conditional_var'),
                'expected_shortfall': risk_metrics.get('expected_shortfall'),
                'volatility': risk_metrics.get('volatility'),
                'beta': risk_metrics.get('beta'),
                'correlation_matrix': risk_metrics.get('correlation_matrix')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Risk analysis error: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: TECHNICAL ANALYSIS
# ============================================================================

@app.route('/api/technical/<asset>', methods=['GET'])
def get_technical_indicators(asset):
    """Get technical indicators for an asset"""
    try:
        periods = request.args.get('periods', 252, type=int)
        interval = request.args.get('interval', '1d')
        
        data = data_pipeline.get_asset_data(
            asset=asset,
            interval=interval,
            periods=periods
        )
        
        if data is None:
            return jsonify({'error': 'No data found'}), 404
        
        indicators = technical_indicators.calculate_all(data)
        
        return jsonify({
            'status': 'success',
            'asset': asset,
            'indicators': indicators
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: ML PREDICTIONS
# ============================================================================

@app.route('/api/predict/<asset>', methods=['GET'])
def predict_price(asset):
    """ML-based price prediction"""
    try:
        periods = request.args.get('periods', 30, type=int)
        model_type = request.args.get('model', 'lstm')
        
        data = data_pipeline.get_asset_data(asset=asset, periods=252)
        
        if data is None:
            return jsonify({'error': 'No data found'}), 404
        
        predictions = ml_predictor.predict(
            data=data,
            asset=asset,
            periods=periods,
            model_type=model_type
        )
        
        return jsonify({
            'status': 'success',
            'asset': asset,
            'predictions': predictions.get('forecast'),
            'confidence_interval': predictions.get('confidence_interval'),
            'model_metrics': predictions.get('metrics')
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: REPORTING & EXPORT
# ============================================================================

@app.route('/api/report/<backtest_id>', methods=['GET'])
def generate_report(backtest_id):
    """Generate detailed PDF report"""
    try:
        report_format = request.args.get('format', 'pdf')
        
        if backtest_id in active_backtests:
            data = active_backtests[backtest_id]
        else:
            data = db_manager.get_backtest_result(backtest_id)
        
        if not data:
            return jsonify({'error': 'Backtest not found'}), 404
        
        # Generate report based on format
        if report_format == 'pdf':
            report_path = backtest_engine.generate_pdf_report(backtest_id, data)
        elif report_format == 'html':
            report_path = backtest_engine.generate_html_report(backtest_id, data)
        else:
            return jsonify({'error': 'Invalid format'}), 400
        
        return send_file(report_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<backtest_id>', methods=['GET'])
def export_results(backtest_id):
    """Export backtest results as CSV/JSON"""
    try:
        export_format = request.args.get('format', 'csv')
        
        if backtest_id in active_backtests:
            data = active_backtests[backtest_id]
        else:
            data = db_manager.get_backtest_result(backtest_id)
        
        if not data:
            return jsonify({'error': 'Backtest not found'}), 404
        
        export_path = backtest_engine.export_results(backtest_id, data, export_format)
        return send_file(export_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES: CONFIGURATION
# ============================================================================

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get application configuration"""
    try:
        return jsonify({
            'status': 'success',
            'config': {
                'supported_assets': config.SUPPORTED_ASSETS,
                'supported_strategies': config.SUPPORTED_STRATEGIES,
                'supported_intervals': ['1m', '5m', '15m', '1h', '1d', '1w'],
                'max_backtest_period': config.MAX_BACKTEST_PERIOD,
                'database': config.DATABASE_TYPE
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# WEBSOCKET EVENTS (Real-time updates)
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('response', {'data': 'Connected to FinSight AI'})


@socketio.on('subscribe_backtest')
def handle_subscribe_backtest(data):
    """Subscribe to backtest updates"""
    backtest_id = data.get('backtest_id')
    if backtest_id:
        join_room(backtest_id)
        emit('subscribed', {'backtest_id': backtest_id})


@socketio.on('unsubscribe_backtest')
def handle_unsubscribe_backtest(data):
    """Unsubscribe from backtest updates"""
    backtest_id = data.get('backtest_id')
    if backtest_id:
        leave_room(backtest_id)


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnect"""
    logger.info(f"Client disconnected: {request.sid}")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Initialize application
    if initialize_app():
        # Run app
        debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('HOST', '0.0.0.0')
        
        logger.info(f"Starting FinSight AI on {host}:{port}")
        socketio.run(
            app,
            host=host,
            port=port,
            debug=debug_mode,
            allow_unsafe_werkzeug=True
        )
    else:
        logger.error("Failed to initialize application")
        exit(1)
