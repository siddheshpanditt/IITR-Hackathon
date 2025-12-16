from flask_socketio import emit
from datetime import datetime

def add_real_time_log(socketio, metrics_data, message, level='info'):
    """Add real-time log entry"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'message': message
    }
    metrics_data['real_time_logs'].append(log_entry)
    metrics_data['real_time_logs'] = metrics_data['real_time_logs'][-100:]  # Keep last 100
    
    # Emit to connected clients
    socketio.emit('new_log', log_entry)

def calculate_health_score(metrics_data):
    """Calculate overall deployment health score"""
    score = 100
    
    # Deduct points for issues
    if metrics_data['status'] == 'Offline':
        score -= 50
    if metrics_data['cpu_usage'] > 80:
        score -= 10
    if metrics_data['memory_usage'] > 85:
        score -= 15
    if metrics_data['disk_usage'] > 90:
        score -= 20
    if metrics_data['latency'] > 2000:
        score -= 10
    
    return max(0, score)

def setup_websocket_handlers(socketio, metrics_data):
    """Setup WebSocket event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        metrics_data['active_users'] += 1
        emit('connected', {'message': 'Connected to real-time monitoring'})
        add_real_time_log(socketio, metrics_data, f"New user connected - Active users: {metrics_data['active_users']}", 'info')

    @socketio.on('disconnect')
    def handle_disconnect():
        metrics_data['active_users'] = max(0, metrics_data['active_users'] - 1)
        add_real_time_log(socketio, metrics_data, f"User disconnected - Active users: {metrics_data['active_users']}", 'info')

    @socketio.on('request_status')
    def handle_status_request():
        emit('status_update', {
            'status': metrics_data['status'],
            'health_score': metrics_data['deployment_health_score'],
            'active_users': metrics_data['active_users'],
            'timestamp': datetime.now().isoformat()
        })