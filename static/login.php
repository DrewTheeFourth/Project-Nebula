<?php
// Start session to handle user information
session_start();

// Check if the form is submitted via POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Collect and sanitize the form data
    $username = htmlspecialchars($_POST['username']);
    $password = htmlspecialchars($_POST['password']);
    
    // API Gateway endpoint
    $apiUrl = 'https://your-api-id.execute-api.your-region.amazonaws.com/authenticate'; // Replace with your API Gateway URL

    // Prepare the data to send
    $data = json_encode(['username' => $username, 'password' => $password]);

    // Initialize cURL
    $ch = curl_init($apiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    // Execute the request
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // Handle the response
    $responseData = json_decode($response, true);
    
    if ($httpCode === 200) {
        // Successful authentication
        $_SESSION['username'] = $username;
        header("Location: dashboard.php");
        exit();
    } else {
        // Handle failed authentication
        header("Location: failed.html");
        exit();
    }
}
?>
