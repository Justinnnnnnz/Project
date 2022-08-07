package com.example.students_management.dao;

import com.example.students_management.model.Student;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface StudentDao extends CrudRepository<Student, Long>{

    List<Student> findByName (String name);

}