#include "include/problem.hpp"
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <nlohmann/json.hpp>
using json = nlohmann::json;

static std::string readFileToString(const std::string& path) {
    std::ifstream in(path);
    if (!in.is_open()) return std::string();
    std::ostringstream ss;
    ss << in.rdbuf();
    return ss.str();
}

static std::string get_string_or(const json& j, const std::string& key, const std::string& def="") {
    if (j.contains(key) && !j.at(key).is_null()) return j.at(key).get<std::string>();
    return def;
}

static int get_int_or(const json& j, const std::string& key, int def=0) {
    if (j.contains(key) && !j.at(key).is_null()) {
        if (j.at(key).is_number_integer()) return j.at(key).get<int>();
        if (j.at(key).is_string()) {
            try { return std::stoi(j.at(key).get<std::string>());
            } catch(...) { return def; }
        }
    }
    return def;
}

static bool get_bool_or(const json& j, const std::string& key, bool def=false) {
    if (j.contains(key) && !j.at(key).is_null()) {
        if (j.at(key).is_boolean()) return j.at(key).get<bool>();
        if (j.at(key).is_string()) {
            std::string v = j.at(key).get<std::string>();
            std::transform(v.begin(), v.end(), v.begin(), ::tolower);
            return v == "true" || v == "1";
        }
        if (j.at(key).is_number_integer()) return j.at(key).get<int>() != 0;
    }
    return def;
}

static std::vector<std::string> get_vector_of_strings(const json& j, const std::string& key) {
    std::vector<std::string> out;
    if (!j.contains(key) || j.at(key).is_null()) return out;
    const json& arr = j.at(key);
    if (!arr.is_array()) return out;
    for (const auto& el : arr) {
        if (el.is_string()) out.push_back(el.get<std::string>());
        else if (el.is_number_integer()) out.push_back(std::to_string(el.get<int>()));
        else if (el.is_object() && el.contains("id")) out.push_back(el.at("id").get<std::string>());
    }
    return out;
}

static std::vector<int> get_vector_of_ints(const json& j, const std::string& key) {
    std::vector<int> out;
    if (!j.contains(key) || j.at(key).is_null()) return out;
    const json& arr = j.at(key);
    if (!arr.is_array()) return out;
    for (const auto& el : arr) {
        if (el.is_number_integer()) out.push_back(el.get<int>());
        else if (el.is_string()) {
            try { out.push_back(std::stoi(el.get<std::string>())); } catch(...) {}
        }
    }
    return out;
}

void Problem::loadInstance(const std::string& filename) {
    const std::string path = "data/generated_instances/" + filename;
    std::string content = readFileToString(path);
    if (content.empty()) {
        std::cerr << "Erro ao abrir ou ler o arquivo: " << path << std::endl;
        return;
    }

    json j;
    try {
        j = json::parse(content);
    } catch (const std::exception& e) {
        std::cerr << "Erro ao parsear JSON: " << e.what() << std::endl;
        return;
    }

    schedules.clear();
    buildings.clear();
    classrooms.clear();
    professors.clear();
    subjects.clear();
    meetings.clear();
    preferences.clear();
    restrictions.clear();
    reservations.clear();

    if (j.contains("schedules") && j.at("schedules").is_array()) {
        int idx = 0;
        for (const auto& item : j.at("schedules")) {
            Schedule s;
            s.id = get_int_or(item, "ID", get_int_or(item, "id", ++idx));
            if (item.contains("startTime")) s.startTime = get_string_or(item, "startTime");
            if (item.contains("endTime")) s.endTime = get_string_or(item, "endTime");
            schedules.push_back(std::move(s));
        }
    }

    if (j.contains("buildings") && j.at("buildings").is_array()) {
        int idx = 0;
        for (const auto& item : j.at("buildings")) {
            Building b;
            b.id = get_int_or(item, "ID", get_int_or(item, "id", ++idx));
            b.name = get_string_or(item, "name");
            buildings.push_back(std::move(b));
        }
    }

    // Classrooms
    if (j.contains("classrooms") && j.at("classrooms").is_array()) {
        int idx = 0;
        for (const auto& item : j.at("classrooms")) {
            Classroom c;
            c.id = get_int_or(item, "ID", get_int_or(item, "id", ++idx));
            c.isLab = get_bool_or(item, "isLab", get_bool_or(item, "isLaboratory", false));
            c.capacity = get_int_or(item, "capacity", get_int_or(item, "vacancies", 0));
            c.buildingId = get_int_or(item, "buildingID", get_int_or(item, "buildingId", get_int_or(item, "building", 0)));
            c.description = get_string_or(item, "description");
            c.floor = get_int_or(item, "floor", 0);
            c.board = get_string_or(item, "board");
            c.projector = get_bool_or(item, "projector", false);
            classrooms.push_back(std::move(c));
        }
    }

    // Professors
    if (j.contains("professors") && j.at("professors").is_array()) {
        for (const auto& item : j.at("professors")) {
            Professor p;
            if (item.contains("code")) p.code = get_string_or(item, "code");
            else if (item.contains("id")) p.code = get_string_or(item, "id");
            p.name = get_string_or(item, "name");
            professors.push_back(std::move(p));
        }
    }

    // Subjects
    if (j.contains("subjects") && j.at("subjects").is_array()) {
        for (const auto& item : j.at("subjects")) {
            Subject s;
            if (item.contains("code")) s.code = get_string_or(item, "code");
            else if (item.contains("id")) s.code = get_string_or(item, "id");
            s.name = get_string_or(item, "name");
            subjects.push_back(std::move(s));
        }
    }

    // Meetings
    if (j.contains("meetings") && j.at("meetings").is_array()) {
        for (const auto& item : j.at("meetings")) {
            Meeting m;
            m.id = get_string_or(item, "id");
            m.isPractical = get_bool_or(item, "isPractical", get_bool_or(item, "practical", false));
            m.professorCodes = get_vector_of_strings(item, "professorCodes");
            if (m.professorCodes.empty()) m.professorCodes = get_vector_of_strings(item, "professors");
            m.subjectCode = get_string_or(item, "subjectCode");
            if (m.subjectCode.empty()) m.subjectCode = get_string_or(item, "subject");
            m.classIds = get_vector_of_strings(item, "classIds");
            m.scheduleIds = get_vector_of_ints(item, "scheduleIds");
            if (m.scheduleIds.empty()) m.scheduleIds = get_vector_of_ints(item, "schedules");
            m.demand = get_int_or(item, "demand", 0);
            m.vacancies = get_int_or(item, "vacancies", 0);
            m.dayOfWeek = get_int_or(item, "dayOfWeek", get_int_or(item, "day", 0));
            meetings.push_back(std::move(m));
        }
    }

    // Preferences
    if (j.contains("preferences") && j.at("preferences").is_array()) {
        for (const auto& item : j.at("preferences")) {
            Preference p;
            p.id = get_string_or(item, "id");
            p.category = get_string_or(item, "category");
            p.categoryCode = get_string_or(item, "categoryCode");
            p.buildingId = get_string_or(item, "buildingId");
            p.floor = get_int_or(item, "floor", -1);
            p.board = get_string_or(item, "board");
            p.projector = get_bool_or(item, "projector", false);
            preferences.push_back(std::move(p));
        }
    }

    // Restrictions
    if (j.contains("restrictions") && j.at("restrictions").is_array()) {
        for (const auto& item : j.at("restrictions")) {
            Restriction r;
            r.id = get_string_or(item, "id");
            r.category = get_string_or(item, "category");
            r.categoryCode = get_string_or(item, "categoryCode");
            r.buildingId = get_string_or(item, "buildingId");
            r.floor = get_int_or(item, "floor", -1);
            r.board = get_string_or(item, "board");
            r.projector = get_bool_or(item, "projector", false);
            restrictions.push_back(std::move(r));
        }
    }

    // Reservations
    if (j.contains("reservations") && j.at("reservations").is_array()) {
        for (const auto& item : j.at("reservations")) {
            Reservation r;
            r.id = get_string_or(item, "id");
            r.classroomId = get_int_or(item, "classroomID", get_int_or(item, "classroomId", get_int_or(item, "classroom", 0)));
            r.dayOfWeek = get_int_or(item, "dayOfWeek", get_int_or(item, "day", 0));
            r.scheduleId = get_int_or(item, "scheduleID", get_int_or(item, "scheduleId", get_int_or(item, "schedule", 0)));
            reservations.push_back(std::move(r));
        }
    }
}