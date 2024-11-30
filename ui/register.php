<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Register</h1>
    <form action="register.php" method="POST">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" required><br><br>

        <label for="password">Password:</label>
        <input type="password" name="password" id="password" required><br><br>

        <label for="role">Role:</label>
    <select name="role" id="role" required>
        <option value="officer">Officer</option>
        <option value="analyst">Analyst</option>
        <option value="manager">Manager</option>
    </select><br><br>
        
        <button type="submit" name="register">Register</button>
    </form>

    <?php
    // Include the database connection
    include '../db_connection.php';

    if (isset($_POST['register'])) {
        // Get user input
        $username = $_POST['username'];
        $password = $_POST['password'];

        // Hash the password
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);

        // Insert the user into the database
        $sql = "INSERT INTO users (username, password) VALUES (?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ss", $username, $hashed_password);

        if ($stmt->execute()) {
            echo "<p>Registration successful! You can now <a href='login.php'>log in</a>.</p>";
        } else {
            echo "<p>Error: Could not register user. Please try again.</p>";
        }

        $stmt->close();
    }

    $conn->close();
    ?>
</body>
</html>
