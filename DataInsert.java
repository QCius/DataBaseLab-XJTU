import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class DataInsert {
    static final String JDBC_DRIVER = "org.postgresql.Driver";
    static final String DB_URL = "jdbc:postgresql://1.92.85.164:26000/MYDB?ApplicationName=app1&useUnicode=true&characterEncoding=utf8";
    static final String USER = "manager";
    static final String PASS = "Aa123456";

    public static void main(String[] args) {
        Connection conn = null;

        try {
            Class.forName(JDBC_DRIVER);
            System.out.println("Connecting to database...");
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            System.out.println("Connected successfully");

            insertStudents(conn, "C:/Users/Jiefucious/Desktop/Student1.csv");
            insertCourses(conn, "C:/Users/Jiefucious/Desktop/c034.csv");

            DeleteRunnable randomDelete = new DeleteRunnable(conn);
            Thread thread_delete = new Thread(randomDelete);
            thread_delete.start();

            insertSC(conn, "C:/Users/Jiefucious/Desktop/sc.csv");

        } catch (SQLException se) {
            se.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (conn != null)
                    conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        System.out.println("Goodbye!");
    }

    public static void insertStudents(Connection conn, String filePath) {
        //System.out.println("t0");
        String sql = "INSERT INTO \"My_mode\".\"s034\" (S#, SNAME, SEX, BDATE, HEIGHT, DORM) VALUES (?, ?, ?, ?, ?, ?)";
        int i = 0;
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(new FileInputStream(filePath), StandardCharsets.UTF_8));
                PreparedStatement pstmt = conn.prepareStatement(sql)) {
            String line;
            while ((line = br.readLine()) != null) {
                i++;
                if (i == 1)
                    continue;
                //System.out.println(line);
                String[] values = line.split(",");
                
                pstmt.setString(1, values[0]);
                pstmt.setString(2, values[1]);
                pstmt.setString(3, values[2]);
                pstmt.setDate(4, java.sql.Date.valueOf(values[3]));
                pstmt.setFloat(5, Float.parseFloat(values[4]));
                pstmt.setString(6, values[5]);
                pstmt.executeUpdate();
                System.out.println("s suc" + i);
            }

            System.out.println("Students data inserted successfully.");
        } catch (IOException | SQLException e) {
            e.printStackTrace();
        }
    }

    public static void insertCourses(Connection conn, String filePath) {
        //System.out.println("t1");
        String sql = "INSERT INTO \"My_mode\".\"c034\" (C#, CNAME, PERIOD, CREDIT, TEACHER) VALUES (?, ?, ?, ?, ?)";
        int i = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(filePath));
                PreparedStatement pstmt = conn.prepareStatement(sql)) {
            String line;
            while ((line = br.readLine()) != null) {
                i++;
                if (i == 1)
                    continue;
                //System.out.println(line);
                String[] values = line.split(",");
                
                pstmt.setString(1, values[0]);
                pstmt.setString(2, values[1]);
                //System.out.println(values[2]);
                pstmt.setInt(3, Integer.parseInt(values[2]));
                pstmt.setFloat(4, Float.parseFloat(values[3]));
                if (values.length >= 5)
                    pstmt.setString(5, values[4]);
                else
                    pstmt.setString(5, "NULL");
                pstmt.executeUpdate();
                System.out.println("c suc:" + i);
            }

            System.out.println("Courses data inserted successfully.");
        } catch (IOException | SQLException e) {
            e.printStackTrace();
        }
    }

    public static void insertSC(Connection conn, String filePath) {
        //System.out.println("t2");
        String sql = "INSERT INTO \"My_mode\".\"sc034\" (S#, C#, GRADE) VALUES (?, ?, ?)";
        int i = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(filePath));
            PreparedStatement pstmt = conn.prepareStatement(sql)) {
            String line;
            while ((line = br.readLine()) != null) {
                i++;
                if (i == 1)
                    continue;
                //System.out.println(line);
                String[] values = line.split(",");
                pstmt.setString(1, values[0]);
                pstmt.setString(2, values[1]);
                pstmt.setFloat(3, Float.parseFloat(values[2]));
                pstmt.executeUpdate();
                System.out.println("sc suc" + i);
            }

            System.out.println("SC data inserted successfully.");
        } catch (IOException | SQLException e) {
            e.printStackTrace();
        }
    }

}

class DeleteRunnable implements Runnable {
    private Connection conn;

    public DeleteRunnable(Connection conn) {
        this.conn = conn;
    }

    @Override
    public void run() {
        System.out.println("t3");
        int deleted_num = 0;
        while (deleted_num < 200){ 
            String deleteSql = "DELETE FROM \"My_mode\".\"sc034\" WHERE S# IN (SELECT S# FROM \"My_mode\".\"sc034\" WHERE GRADE < 60 ORDER BY RANDOM() LIMIT 5) AND C# IN (SELECT C# FROM \"My_mode\".\"sc034\"WHERE GRADE < 60 ORDER BY RANDOM() LIMIT 5)";
            try (PreparedStatement pstmt = conn.prepareStatement(deleteSql)) {
                int rowsAffected = pstmt.executeUpdate();
                deleted_num += rowsAffected;
            } catch (SQLException e) {
                e.printStackTrace();
            }
            System.out.println(deleted_num + " SC records with GRADE < 60 deleted successfully.");
            try{
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}