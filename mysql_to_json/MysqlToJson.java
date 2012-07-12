import java.sql.PreparedStatement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

import java.io.BufferedReader; 
import java.io.IOException; 
import java.io.InputStreamReader; 
import java.util.ArrayList; 
import java.util.LinkedList;
import java.lang.Integer;

public class FillRelations{


	private Connection con = null;
	private PreparedStatement pst = null;
	private ResultSet rs = null;
	private String url = "jdbc:mysql://localhost:3306/CREAKB";
	
	public static final String jsonFormat = "{\\\"subject_x\\\":\\\"999\\\",\\\"subject_y\\\":\\\"999\\\",\\\"subject_z\\\":\\\"999\\\",\\\"subject_val\\\":\\\"999\\\",\\\"object1_x\\\":\\\"999\\\",\\\"object1_y\\\":\\\"999\\\",\\\"object1_z\\\":\\\"999\\\",\\\"object1_val\\\":\\\"999\\\",\\\"type\\\":\\\"SD2\\\",\\\"direction\\\":\\\"1\\\",\\\"subject_name\\\":\\\"xxxsubject_namexxx\\\",\\\"subject_name_alias\\\":\\\"xxxsubject_namexxx\\\",\\\"object1_name\\\":\\\"xxxobject1_namexxx\\\",\\\"object1_name_alias\\\":\\\"xxxobject1_namexxx\\\",\\\"verb\\\":\\\"xxxverbxxx\\\"}";
	
	
	public FillRelations(String user, String password){
		try{
			con = DriverManager.getConnection(url, user, password);
		}catch(SQLException ex){
			Logger lgr = Logger.getLogger(FillRelations.class.getName());
			lgr.log(Level.SEVERE, ex.getMessage(), ex);
			System.exit(1);
		}
	}
	
	
	
	public Connection getConnection(){
		return con;
	}
	
	public void closeConnection(){
		try {
                
        	if (con != null) 
            	con.close();
            if (rs != null)
            	rs.close();
            if (pst != null)
            	pst.close();

        } catch (SQLException ex) {
        	Logger lgr = Logger.getLogger(FillRelations.class.getName());
        	lgr.log(Level.WARNING, ex.getMessage(), ex);
        }
		
	}
	
	// if sentencePhraseID corresponds to a root node, the whole sentence will be returned
	public String getPhrase(String sentencePhraseID){
		// implement me!
		return " ";
	}
	
	// if -9999 returned, theres an error with rs
	public int getNumEntries(String tableName){
		int numEntries = -9999;
		try{
			pst = con.prepareStatement("SELECT COUNT(*) FROM " + tableName);
			rs = pst.executeQuery();
		    if (rs.next()) // COUNT(*) query should only return 1 row of result
		        numEntries = Integer.parseInt(rs.getString(1));
        }catch(SQLException ex){
        	Logger lgr = Logger.getLogger(FillRelations.class.getName());
        	lgr.log(Level.WARNING, ex.getMessage(), ex);
        }
        return numEntries;
	}
	
	public static void main(String args[]){
		
		if(args.length < 2){
			System.out.println("ERROR: USAGE =");
			System.out.println("$ java -cp .:mysql-connector-java-5.1.20-bin.jar FillRelations _user_ _password_");
			return;
		}
		
		FillRelations fillRelations1 = new FillRelations(args[0],args[1]);
		PreparedStatement pst = null;
		ResultSet rs = null;
		
		try {
			int numBooks = fillRelations1.getNumEntries("book_tbl");  // get number of books in the database
	
			System.out.println("numBooks = " + numBooks); // debugging
	
            // for every book	
            for(int bookNum = 1; bookNum < numBooks + 1; bookNum++){
            
            	// get number of chapters in the book
            	int numChapters = fillRelations1.getNumEntries("chapter_tbl");
            	
            	System.out.println("numChapters = " + numChapters); // debugging
            
            	// for every chapter in the book
            	for(int chapterNum = 1; chapterNum < numChapters + 1 ; chapterNum++){
            	
            		// debugging
            		pst = fillRelations1.getConnection().prepareStatement("SELECT count(*) FROM sentence_tbl WHERE chapter_id = " + chapterNum);
            		rs = pst.executeQuery();
            		if(rs.next()){
            			System.out.println("in chapter " + chapterNum + " numSentences is " + rs.getString(1));
            		}
            		
            		// query for all the sentences in the chapter and process them
            		pst = fillRelations1.getConnection().prepareStatement("SELECT sentence_id FROM sentence_tbl WHERE chapter_id = " + chapterNum);
            		rs = pst.executeQuery();
            		while(rs.next()){
            			String sentenceID = rs.getString(1);
            			fillRelations1.fillNounTbl(sentenceID);
            			fillRelations1.fillVerbTbl(sentenceID);
            			fillRelations1.fillCondTbl(sentenceID);
            		
            		}
            	
            	}
            
            	pst.close();
            	rs.close();
            
            }
              
            
            
            











        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(FillRelations.class.getName());
            lgr.log(Level.SEVERE, ex.getMessage(), ex);

        } finally {
           fillRelations1.closeConnection();
        }
		
	}
}
