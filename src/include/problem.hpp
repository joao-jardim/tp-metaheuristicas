#ifndef PROBLEM_HPP
#define PROBLEM_HPP

#include <string>
#include <vector>

// ============= STRUCTS =============

struct Schedule {
    int id = 0;
    std::string startTime = "";
    std::string endTime = "";
};

struct Building {
    int id = 0;
    std::string name = "";
};

struct Classroom {
    int id = 0;
    bool isLab = false;
    int capacity = 0;
    int buildingId = 0;
    std::string description = "";
    int floor = 0;
    std::string board = "";
    bool projector = false;
};

struct Professor {
    std::string code = "";
    std::string name = "";
};

struct Subject {
    std::string code = "";
    std::string name = "";
};

struct Meeting { 
    std::string id = "";
    bool isPractical = false;
    std::vector<std::string> professorCodes;  // IDs dos professores
    std::string subjectCode = "";             // ID do assunto
    std::vector<std::string> classIds;        // IDs das turmas (se existir)
    std::vector<int> scheduleIds;             // IDs dos horários
    int demand = 0;
    int vacancies = 0;
    int dayOfWeek = 0;
};

struct Preference {
    std::string id = "";
    std::string category = "";
    std::string categoryCode = "";
    std::string buildingId = "";  // ID ou vazio se null
    int floor = -1;               // -1 significa não especificado
    std::string board = "";
    bool projector = false;
};

struct Restriction {
    std::string id = "";
    std::string category = "";
    std::string categoryCode = "";
    std::string buildingId = "";
    int floor = -1;               // -1 significa não especificado
    std::string board = "";
    bool projector = false;
};

struct Reservation {
    std::string id = "";
    int classroomId = 0;
    int dayOfWeek = 0;
    int scheduleId = 0;
};

class Problem {
public:
    std::vector<Schedule> schedules;
    std::vector<Building> buildings;
    std::vector<Classroom> classrooms;
    std::vector<Professor> professors;
    std::vector<Subject> subjects;
    std::vector<Meeting> meetings;
    std::vector<Preference> preferences;
    std::vector<Restriction> restrictions;
    std::vector<Reservation> reservations;

    // Métodos
    void loadInstance(const std::string& filename);
};

#endif // PROBLEM_HPP
