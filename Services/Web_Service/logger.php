<?php
// Enhanced JSON Logger for PRSociety - Fixed Distributed Attack Detection
header('Content-Type: application/json');

// Get real client IP (handles proxies and load balancers)
function getRealIP() {
    if (!empty($_SERVER['HTTP_CF_CONNECTING_IP'])) {
        return $_SERVER['HTTP_CF_CONNECTING_IP'];
    }
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        return trim($ips[0]);
    }
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        return $_SERVER['HTTP_CLIENT_IP'];
    }
    if (!empty($_SERVER['HTTP_X_REAL_IP'])) {
        return $_SERVER['HTTP_X_REAL_IP'];
    }
    return $_SERVER['REMOTE_ADDR'] ?? 'unknown';
}

// Get parameters
$user = isset($_GET['user']) ? $_GET['user'] : 'unknown';
if (isset($_GET['auth-status'])) {
    $status = $_GET['auth-status'];
} elseif (isset($_GET['status'])) {
    $status = $_GET['status'];
} else {
    $status = 'UNKNOWN';
}

$ip = getRealIP();
$agent = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
$timestamp = date('Y-m-d H:i:s');
$current_time = time();

// Handle password
$password = isset($_GET['pwd']) ? $_GET['pwd'] : '';
$password_length = strlen($password);

// Single log file
$log_file = '/var/log/prsociety-auth.json';

// Load all data from the log file for distributed detection
$all_logs = [];
if (file_exists($log_file)) {
    $content = file_get_contents($log_file);
    if ($content !== false) {
        $lines = explode("\n", trim($content));
        foreach ($lines as $line) {
            if (!empty($line)) {
                $log = json_decode($line, true);
                if ($log && isset($log['timestamp'])) {
                    $all_logs[] = $log;
                }
            }
        }
    }
}

// Calculate distributed attack stats from last 30 seconds
$distributed_window = 30;
$distributed_cutoff = $current_time - $distributed_window;
$unique_ips = [];
$total_attempts = 0;

foreach ($all_logs as $log) {
    $log_time = strtotime($log['timestamp']);
    if ($log_time > $distributed_cutoff) {
        if ($log['auth-status'] == 'WRONG_PASSWORD' || $log['auth-status'] == 'USER_NOT_FOUND') {
            $unique_ips[$log['src_ip']] = true;
            $total_attempts++;
        }
    }
}

// Add current attempt
if ($status == 'WRONG_PASSWORD' || $status == 'USER_NOT_FOUND') {
    $unique_ips[$ip] = true;
    $total_attempts++;
}
$unique_ip_count = count($unique_ips);

// DISTRIBUTED ATTACK detection - 30+ attempts OR 10+ unique IPs in last 30 seconds
$distributed_attack_detected = false;
if (($total_attempts >= 30 || $unique_ip_count >= 10) && ($status == 'WRONG_PASSWORD' || $status == 'USER_NOT_FOUND')) {
    $distributed_attack_detected = true;
   
    // Log DISTRIBUTED_ATTACK immediately
    $log_entry = json_encode([
        'timestamp' => $timestamp,
        'event_type' => 'authentication',
        'app_service' => 'prsociety',
        'auth-status' => 'DISTRIBUTED_ATTACK',
        'username' => $user,
        'password_length' => $password_length,
        'attempted_password' => '[DDOS DETECTED]',
        'src_ip' => $ip,
        'user_agent' => $agent,
        'distributed_total_attempts' => $total_attempts,
        'distributed_unique_ips' => $unique_ip_count,
        'time_window_seconds' => $distributed_window,
        'message' => "DISTRIBUTED_ATTACK - {$total_attempts} attempts from {$unique_ip_count} unique IPs in last {$distributed_window} seconds!"
    ], JSON_UNESCAPED_SLASHES) . "\n";
   
    file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);
   
    echo json_encode([
        'success' => false,
        'status' => 'DISTRIBUTED_ATTACK',
        'total_attempts' => $total_attempts,
        'unique_ips' => $unique_ip_count,
        'message' => "DISTRIBUTED_ATTACK detected!"
    ]);
    exit;
}

// Per-IP rate limiting
$ip_data_file = '/tmp/prsociety_ip_' . md5($ip);
$ip_data = [];
if (file_exists($ip_data_file)) {
    $ip_data = json_decode(file_get_contents($ip_data_file), true) ?: [];
}
if (!isset($ip_data['attempts'])) $ip_data['attempts'] = 0;
if (!isset($ip_data['cooldown'])) $ip_data['cooldown'] = 0;
if (!isset($ip_data['wave'])) $ip_data['wave'] = 0;

// Check cooldown
if ($ip_data['cooldown'] > $current_time && ($status == 'WRONG_PASSWORD' || $status == 'USER_NOT_FOUND')) {
    $wait = $ip_data['cooldown'] - $current_time;
    echo json_encode(['success' => false, 'status' => 'RATE_LIMITED', 'wait_time' => $wait]);
    exit;
}

// Track failed attempts
$detected_status = $status;
$should_cooldown = false;

if ($status == 'WRONG_PASSWORD' || $status == 'USER_NOT_FOUND') {
    $ip_data['attempts']++;
   
    if ($ip_data['attempts'] >= 3) {
        $ip_data['wave']++;
        $ip_data['cooldown'] = $current_time + 30;
        $ip_data['attempts'] = 0;
        $should_cooldown = true;
       
        if ($ip_data['wave'] >= 2 && $ip_data['wave'] < 5) {
            $detected_status = 'BRUTE_FORCE_ATTEMPT';
        } elseif ($ip_data['wave'] >= 5) {
            $detected_status = 'CRITICAL';
        } else {
            $detected_status = 'RATE_LIMITED';
        }
    }
   
    file_put_contents($ip_data_file, json_encode($ip_data));
}

// Prepare log entry for normal attempts
$logged_password = '';
$message = '';

switch($detected_status) {
    case 'SUCCESS':
        $logged_password = '[NOT LOGGED]';
        $message = "User $user successfully logged in";
        break;
    case 'WRONG_PASSWORD':
        $logged_password = $password;
        $message = "User $user attempted with wrong password";
        break;
    case 'USER_NOT_FOUND':
        $logged_password = $password;
        $message = "Non-existent user \"$user\" attempted login";
        break;
    case 'RATE_LIMITED':
        $logged_password = '[RATE LIMITED]';
        $message = "Rate limit triggered - 3+ attempts for user $user from IP $ip (Wave {$ip_data['wave']})";
        break;
    case 'BRUTE_FORCE_ATTEMPT':
        $logged_password = '[BRUTE FORCE]';
        $message = "BRUTE_FORCE_ATTEMPT - IP $ip wave {$ip_data['wave']}";
        break;
    case 'CRITICAL':
        $logged_password = '[CRITICAL]';
        $message = "CRITICAL - IP $ip wave {$ip_data['wave']}";
        break;
    default:
        $logged_password = $password;
        $message = "User $user - $status";
}

$log_entry = json_encode([
    'timestamp' => $timestamp,
    'event_type' => 'authentication',
    'app_service' => 'prsociety',
    'auth-status' => $detected_status,
    'username' => $user,
    'password_length' => $password_length,
    'attempted_password' => $logged_password,
    'src_ip' => $ip,
    'user_agent' => $agent,
    'wave' => $ip_data['wave'],
    'distributed_total_attempts' => $total_attempts,
    'distributed_unique_ips' => $unique_ip_count,
    'message' => $message
], JSON_UNESCAPED_SLASHES) . "\n";

file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);

if ($should_cooldown) {
    echo json_encode([
        'success' => false,
        'status' => $detected_status,
        'message' => "Too many failed attempts. Please wait 30 seconds.",
        'wait_time' => 30
    ]);
} else {
    echo json_encode([
        'success' => true,
        'status' => $detected_status
    ]);
}
?>
