<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1, h2 {
            text-align: center;
        }
        .user-info {
            margin-top: 30px;
        }
        .user-info p {
            margin: 5px 0;
        }
        .logout-btn {
            text-align: center;
            margin-top: 20px;
        }
        .logout-btn input {
            padding: 10px 20px;
            background-color: #ff6347;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .logout-btn input:hover {
            background-color: #cc4c38;
        }
        .userlist-btn {
            text-align: center;
            margin-top: 20px;
        }
        .userlist-btn input:hover {
            background-color: #45a049;
        }
        .userlist-btn input {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Dashboard</h1>
        <div class="user-info">
            <p><strong>Username:</strong> {{ username }}</p>
            <p><strong>Email:</strong> {{ email }}</p>
        </div>
        <div class="logout-btn">
            <form action="/logout" method="post" class="logout-btn">
                <input type="submit" value="Logout">
            </form>
        </div>
    </div>
    <div class="container">
        <form action="/dashboard/{{ username }}?List=True" method="post" class="userlist-btn">
            % if ListContent:
                <table>
                    % for inner_list in ListContent:
                        <tr>
                            % for col in inner_list:
                                <td>{{ col }}</td>
                            % end
                        </tr>
                    % end
                </table>
            % end
            <input type="submit" value="Get List">
        </form>
    <div>
</body>
</html>

