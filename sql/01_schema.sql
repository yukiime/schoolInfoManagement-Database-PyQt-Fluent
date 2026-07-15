-- =====================================================================
-- 学生信息管理系统 数据库结构
--
-- 说明：原始数据库已丢失，本文件根据代码中的 SQL 语句反向推导而来，
-- 字段顺序依据代码中 SELECT * 的展示列名确定；
-- 两个存储过程的实现为按调用方式重建的版本，与原实现可能略有出入。
-- =====================================================================

-- 确保客户端连接按 utf8mb4 解析本文件中的中文标识符
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS school_info_db DEFAULT CHARACTER SET utf8mb4;
USE school_info_db;

-- ---------------------------------------------------------------------
-- 专业表
-- ---------------------------------------------------------------------
CREATE TABLE sms_major (
    Mno   VARCHAR(20)  NOT NULL COMMENT '专业编号',
    Mname VARCHAR(50)  NOT NULL COMMENT '专业名称',
    PRIMARY KEY (Mno)
);

-- ---------------------------------------------------------------------
-- 班级表
-- ---------------------------------------------------------------------
CREATE TABLE sms_class (
    Cno   VARCHAR(20)  NOT NULL COMMENT '班级编号',
    Mno   VARCHAR(20)  NOT NULL COMMENT '所属专业编号',
    Cname VARCHAR(50)  NOT NULL COMMENT '班级名称',
    PRIMARY KEY (Cno),
    FOREIGN KEY (Mno) REFERENCES sms_major (Mno)
);

-- ---------------------------------------------------------------------
-- 学生表（学号为 12 位数字）
-- ---------------------------------------------------------------------
CREATE TABLE sms_students (
    Sno      CHAR(12)      NOT NULL COMMENT '学号',
    Cno      VARCHAR(20)   NOT NULL COMMENT '所属班级编号',
    Sname    VARCHAR(50)   NOT NULL COMMENT '姓名',
    Ssex     CHAR(2)       NOT NULL COMMENT '性别：男/女',
    Sage     INT           NOT NULL COMMENT '年龄',
    Sarea    VARCHAR(50)   NOT NULL COMMENT '生源地',
    Scredits DECIMAL(5,1)  NOT NULL DEFAULT 0 COMMENT '已修学分',
    PRIMARY KEY (Sno),
    FOREIGN KEY (Cno) REFERENCES sms_class (Cno)
);

-- ---------------------------------------------------------------------
-- 教师表（教师编号为 8 位数字）
-- ---------------------------------------------------------------------
CREATE TABLE sms_teacher (
    Tno        CHAR(8)     NOT NULL COMMENT '教师编号',
    Tname      VARCHAR(50) NOT NULL COMMENT '教师姓名',
    TphoneCode VARCHAR(20) COMMENT '联系电话',
    PRIMARY KEY (Tno)
);

-- ---------------------------------------------------------------------
-- 课程表
-- ---------------------------------------------------------------------
CREATE TABLE sms_lesson (
    Lno       VARCHAR(20)  NOT NULL COMMENT '课程编号',
    Lname     VARCHAR(50)  NOT NULL COMMENT '课程名',
    Lhours    INT          NOT NULL COMMENT '学时',
    Lcredits  DECIMAL(4,1) NOT NULL COMMENT '学分',
    Lsemester VARCHAR(30)  NOT NULL COMMENT '上课学期，如 "2021学年第一学期"',
    Lexam     VARCHAR(10)  NOT NULL COMMENT '考核方式：考试/考查',
    PRIMARY KEY (Lno)
);

-- ---------------------------------------------------------------------
-- 排课表（班级-课程-教师 关联）
-- ---------------------------------------------------------------------
CREATE TABLE sms_schedule (
    Cno VARCHAR(20) NOT NULL COMMENT '班级编号',
    Lno VARCHAR(20) NOT NULL COMMENT '课程编号',
    Tno CHAR(8)     NOT NULL COMMENT '授课教师编号',
    PRIMARY KEY (Cno, Lno),
    FOREIGN KEY (Cno) REFERENCES sms_class (Cno),
    FOREIGN KEY (Lno) REFERENCES sms_lesson (Lno),
    FOREIGN KEY (Tno) REFERENCES sms_teacher (Tno)
);

-- ---------------------------------------------------------------------
-- 成绩表
-- ---------------------------------------------------------------------
-- 列顺序须与代码中 `INSERT INTO sms_grades VALUES(Lno, Sno, grade)` 一致
CREATE TABLE sms_grades (
    Lno   VARCHAR(20)  NOT NULL COMMENT '课程编号',
    Sno   CHAR(12)     NOT NULL COMMENT '学号',
    grade DECIMAL(5,1) NOT NULL COMMENT '成绩',
    PRIMARY KEY (Sno, Lno),
    FOREIGN KEY (Sno) REFERENCES sms_students (Sno),
    FOREIGN KEY (Lno) REFERENCES sms_lesson (Lno)
);

-- ---------------------------------------------------------------------
-- 账户表（学生/教师首次登录时以 账号=密码=编号 自动创建，之后可修改密码）
-- 管理员账户需要手动插入一条记录，见文件末尾
-- ---------------------------------------------------------------------
CREATE TABLE sms_suser (
    Saccount  CHAR(12)    NOT NULL COMMENT '学生账号（学号）',
    Spassword VARCHAR(50) NOT NULL COMMENT '密码',
    PRIMARY KEY (Saccount)
);

CREATE TABLE sms_tuser (
    Taccount  CHAR(8)     NOT NULL COMMENT '教师账号（教师编号）',
    Tpassword VARCHAR(50) NOT NULL COMMENT '密码',
    PRIMARY KEY (Taccount)
);

CREATE TABLE sms_admin (
    Aaccount  VARCHAR(20) NOT NULL COMMENT '管理员账号',
    Apassword VARCHAR(50) NOT NULL COMMENT '密码',
    PRIMARY KEY (Aaccount)
);

-- ---------------------------------------------------------------------
-- 存储过程（按代码调用方式重建）
-- ---------------------------------------------------------------------
DELIMITER //

-- 查询某学生所有已有成绩的课程及成绩
-- 调用方式: CALL get_courses_and_grades_by_student('学号')
-- 返回列顺序与界面过滤逻辑对应：第 4 列为学分、第 6 列为考核方式
CREATE PROCEDURE get_courses_and_grades_by_student(IN in_sno CHAR(12))
BEGIN
    SELECT g.Sno    AS 学号,
           l.Lno    AS 课程编号,
           l.Lname  AS 课程名,
           l.Lhours AS 学时,
           l.Lcredits  AS 学分,
           l.Lsemester AS 上课学期,
           l.Lexam  AS `考试/考查`,
           g.grade  AS 成绩
    FROM sms_grades g
    JOIN sms_lesson l ON g.Lno = l.Lno
    WHERE g.Sno = in_sno;
END //

-- 按学年统计某学生的成绩
-- 调用方式: CALL YearlyGradeStatistics('学号', '2021学年')
CREATE PROCEDURE YearlyGradeStatistics(IN in_sno CHAR(12), IN in_year VARCHAR(30))
BEGIN
    SELECT g.Sno    AS 学号,
           l.Lno    AS 课程编号,
           l.Lname  AS 课程名,
           l.Lhours AS 学时,
           l.Lcredits  AS 学分,
           l.Lsemester AS 上课学期,
           l.Lexam  AS `考试/考查`,
           g.grade  AS 成绩
    FROM sms_grades g
    JOIN sms_lesson l ON g.Lno = l.Lno
    WHERE g.Sno = in_sno
      AND l.Lsemester LIKE CONCAT(in_year, '%');
END //

DELIMITER ;

-- ---------------------------------------------------------------------
-- 已修学分自动结转（原数据库丢失、代码只读取 Scredits 不更新，故在此重建）
--
-- 规则：学生已修学分 = 其成绩及格(>=60)课程的学分之和。
-- 成绩表任何增/改/删都会自动重算对应学生的 Scredits，
-- 使界面上「录入成绩后学分自动变化」的设计得以生效。
-- ---------------------------------------------------------------------
DELIMITER //

-- 重算单个学生的已修学分
CREATE PROCEDURE recalc_student_credits(IN p_sno CHAR(12))
BEGIN
    UPDATE sms_students s
    SET s.Scredits = (
        SELECT COALESCE(SUM(l.Lcredits), 0)
        FROM sms_grades g
        JOIN sms_lesson l ON g.Lno = l.Lno
        WHERE g.Sno = p_sno AND g.grade >= 60
    )
    WHERE s.Sno = p_sno;
END //

CREATE TRIGGER trg_grades_after_insert
AFTER INSERT ON sms_grades
FOR EACH ROW
    CALL recalc_student_credits(NEW.Sno); //

CREATE TRIGGER trg_grades_after_update
AFTER UPDATE ON sms_grades
FOR EACH ROW
BEGIN
    CALL recalc_student_credits(NEW.Sno);
    IF OLD.Sno <> NEW.Sno THEN
        CALL recalc_student_credits(OLD.Sno);
    END IF;
END //

CREATE TRIGGER trg_grades_after_delete
AFTER DELETE ON sms_grades
FOR EACH ROW
    CALL recalc_student_credits(OLD.Sno); //

DELIMITER ;

-- ---------------------------------------------------------------------
-- 初始化管理员账户（请自行修改账号和密码后执行）
-- ---------------------------------------------------------------------
-- INSERT INTO sms_admin (Aaccount, Apassword) VALUES ('admin', 'change_me');
