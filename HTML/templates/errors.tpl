<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        .error-container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
        }
        h1 {
            color: #ff6347;
        }
        p {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>Error {{ error_code }}</h1>
        <p>{{ error_description }}</p>
        <p>We apologize for the inconvenience. Please try again later.</p>
    </div>
</body>
</html>
