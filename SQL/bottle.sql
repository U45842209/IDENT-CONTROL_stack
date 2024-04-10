-- Création de la base de données
CREATE DATABASE IF NOT EXISTS user_auth;

-- Table pour les utilisateurs enregistrés
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);