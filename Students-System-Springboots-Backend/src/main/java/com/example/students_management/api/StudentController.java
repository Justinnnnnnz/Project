package com.example.students_management.api;

import com.example.students_management.exceptions.InvalidUniversityClassException;
import com.example.students_management.exceptions.StudentEmptyNameException;
import com.example.students_management.exceptions.StudentNonExistException;
import com.example.students_management.model.Student;
import com.example.students_management.service.StudentService;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("api/student")
public class StudentController {

    private StudentService studentService;

    @Autowired
    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @GetMapping
    @RequiresPermissions("student:read")
    public List<Student> getAllStudent(){
        return studentService.getAllStudent();
    }

    @GetMapping("/name")
    // localhost:8080/api/student/name?name=Jack
    public List<Student> getStudents(@RequestParam String name){
        return studentService.getStudentByName(name);
    }

    @GetMapping("/contain_name")
    // localhost:8080/api/student/name?name=contain_name=T
    public List<Student> getStudentsContainName(@RequestParam String name){
        return studentService.getStudentsContainName(name);
    }

    @GetMapping("/class")
    // localhost:8080/api/student/class?year=2022&number=1
    public List<Student> getStudentsInClass(@RequestParam int year,@RequestParam int number){
        return studentService.getStudentsInClass(year, number);
    }

    @RequestMapping("/register")
    @PostMapping
    public ResponseEntity<String> registerStudent(@RequestBody Student student){
        try{
            Student savedStudent = studentService.addStudent(student);
            return ResponseEntity.ok("Registered Student. Name :"+ student.toString());
        }catch (StudentEmptyNameException e){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }
}

    @PostMapping(path = "assignclass/{sid}/{cid}")
    public ResponseEntity<String> assignClass(@PathVariable("sid") Long studentId,
                                              @PathVariable("cid") Long classId){
        try{
            Student updateStudent = studentService.assignClass(studentId, classId);
            return ResponseEntity.ok("Assigned class. :"+ updateStudent.toString());
        } catch(StudentNonExistException e){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }catch (InvalidUniversityClassException e){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }


}}
