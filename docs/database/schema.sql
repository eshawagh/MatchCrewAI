-- MatchCrewAI Database Schema
-- Phase 2: Core tables for student profiles and skills

CREATE DATABASE IF NOT EXISTS matchcrewai;
USE matchcrewai;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    class_division VARCHAR(10),
    branch VARCHAR(100),
    preferred_domains VARCHAR(255),
    preferred_role VARCHAR(100),
    working_preference VARCHAR(255),
    availability VARCHAR(50),
    experience_level VARCHAR(20),
    prior_team_experience VARCHAR(5),
    leadership INT,
    communication INT,
    independence INT,
    creativity INT
);

CREATE TABLE skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE student_skills (
    student_id INT,
    skill_id INT,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
);