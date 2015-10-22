<?php
        $status = 200; // set all blocked request to status 200
        http_response_code($status);
        $user_agent = $_SERVER['HTTP_USER_AGENT'];
        $method = $_SERVER['REQUEST_METHOD'];
        $uri = $_SERVER['REQUEST_URI'];
        $triggered_ip = $_SERVER['REMOTE_ADDR'];
        $post_data = array($_POST);
        $trigger_data = array(
                'trigger_ip' => $triggered_ip,
                'user-agent' => $user_agent,
                'method' => $method,
                'uri' => $uri,
                'post_data' => $post_data,
        );
?>
