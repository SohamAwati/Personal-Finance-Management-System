#Student Model

from dataclasses import dataclass, asdict

@dataclass
class Student: 
    student_id : int
    name : str
    age : int
    course : str
    marks : float

    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        return cls(
            student_id = data['student_id'],
            name = data['name'],
            age = data['age'],
            course = data['course'],
            marks = data['marks']
        )
    
    def __str__(self) -> str:
        return(
            f"ID : {self.student_id} | "
            f"Name : {self.name} | "
            f"Age : {self.age} | "
            f"Course : {self.course} | "
            f"Marks : {self.marks}"
        )