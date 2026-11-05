<?php
// "Let us know you're coming" form: emails the crew a runner's plan.
// Posted from findcam.meshtc.com and camerondeanbalser.com/run.
$allowed = ['https://findcam.meshtc.com', 'https://camerondeanbalser.com', 'https://www.camerondeanbalser.com'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $allowed, true)) { header('Access-Control-Allow-Origin: ' . $origin); header('Vary: Origin'); }
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { header('Access-Control-Allow-Methods: POST'); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo '{"ok":false}'; exit; }

function field($k, $max) { $v = trim((string)($_POST[$k] ?? '')); $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v); return mb_substr($v, 0, $max); }
if (field('website', 200) !== '') { echo '{"ok":true}'; exit; } // honeypot: bots fill it, people don't see it

$name = str_replace(["\r", "\n"], ' ', field('name', 80));
$runners = (int) field('runners', 3);
$plan = field('plan', 1500);
$test = field('test', 1) === '1';
if ($name === '' || $runners < 1 || $runners > 50 || $plan === '') { http_response_code(400); echo '{"ok":false,"error":"Please add your name and how many runners."}'; exit; }

// Simple limit: 5 submissions per hour from one address.
$ip = $_SERVER['HTTP_X_SUCURI_CLIENTIP'] ?? $_SERVER['REMOTE_ADDR'] ?? 'x';
$dir = sys_get_temp_dir() . '/runwithcam'; @mkdir($dir, 0700);
$f = $dir . '/' . md5($ip); $now = time();
$hits = array_filter(array_map('intval', @file($f) ?: []), fn($t) => $t > $now - 3600);
if (count($hits) >= 5) { http_response_code(429); echo '{"ok":false,"error":"Too many in a short time. Please try again later."}'; exit; }
$hits[] = $now; @file_put_contents($f, implode("\n", $hits));

$to = 'tj@meshtc.com'; // add more addresses here, comma separated
$subject = ($test ? '[Test] ' : '') . "Runner coming: $name ($runners)";
$body = "$name is planning to run with Cam" . ($runners > 1 ? " with $runners runners in total" : '') . ".\n\n"
      . "Their plan:\n$plan\n\nRunners: $runners\n\nSent from the Run With Cam page.\n";
$headers = "From: Run With Cam <no-reply@camerondeanbalser.com>\r\nContent-Type: text/plain; charset=UTF-8\r\n";
$ok = mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-fno-reply@camerondeanbalser.com');
echo json_encode(['ok' => (bool)$ok]);
