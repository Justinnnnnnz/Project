package com.example.students_management.exceptions;

public class StudentNonExistException extends RuntimeException{
    public StudentNonExistException(String message) {
        super(message);
    }

}
