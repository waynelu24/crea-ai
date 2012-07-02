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
	
	
	public FillRelations(String user, String password){
		try{
			con = DriverManager.getConnection(url, user, password);
		}catch(SQLException ex){
			Logger lgr = Logger.getLogger(FillRelations.class.getName());
			lgr.log(Level.SEVERE, ex.getMessage(), ex);
			System.exit(1);
		}
	}
	
	// process at sentence level
	public void fillNounTbl(int sentenceID){
	
	//Get the list of IDs of Noun Phrases from this sentence
	LinkedList <String>nounPhraseList = getPhraseIDWithTAG(sentenceID,"NP");
	
	String Word_POS_id = "";
	String current_NounPhraseID = "";
	String current_NounText = "";
	String current_WordPOSID = "";
	

	for (int i = 0; i < nounPhraseList.size(); i++)
	{
	 current_NounPhraseID = nounPhraseList.pop();
	 
	 //1- Insert Sentence ID
	 //From the input sentenceID
	 
	 //2- Insert Noun sequence
	 //Count++ for each sentence
	 
         //3- Insert the Noun Text
         current_NounText = getPhrase(current_NounPhraseID);
         
         //4- Insert Word_POS_id
         //Use the function getWordPOSID()
         
	}
	
	}
	

	// process at sentence level
	public void fillVerbTbl(int sentenceID){
		// implement me!
	}
	
	
	// process at sentence level
	public void fillCondTbl(int sentenceID){
		// implement me!
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
	
	//Returns the Word_POS_ID matching the inputted word
	public static String getWordPOSID(String word)
	{
	  String wordPOSID = "";
	  try {
	        //Check for the ID matching the word_name
		pst = con.prepareStatement("SELECT word_POS_id FROM word_POS_tbl WHERE word_name = " + word);
		rs = pst.executeQuery();
	        
		wordPOSID = rs.getString(1);        
	      }
	   
	   catch (SQLException ex){
		Logger lgr = Logger.getLogger(FillRelations.class.getName());
		lgr.log(Level.WARNING, ex.getMessage(), ex);
           }
           
           return wordPOSID;
	}
	
	//Retruns a linkedlist of TEXT from inputted phrases IDs in the same order
	//ex. {15, 16, 25, 29} => {"Hello", " ", "Dog", " "} where 16 and 29 are not leaf nodes
	//Probably a useless function?
	public static LinkedList<String> getTextPhraseFromID(LinkedList <String>list_IDs)
	{
	  LinkedList <String>textPhrase_list = new LinkedList<String>();
	  String current_ID = "";
	  
	  for (int i=0; i < list_IDs.size(); i++)
	  {
	    //Pop an ID from the input list
	    current_ID = list_IDs.pop();
	    //Get the text corresponding the that Phrase ID
	    pst = con.prepareStatement("SELECT sentence_phrase_text FROM sentence_phrase_tbl WHERE sentence_phrase_id = " + current_ID);
	    rs = pst.executeQuery();
	    
	    //Add it to the linked list to be returend
	    textPhrase_list.add(rs.getString(1));
	  }
	  return textPhrase_list;
	}
	
	//Returns a linkedlist of Phrase ID with the containing the specified TAG in a particular sentence
	public static LinkedList<String> getPhraseIDWithTAG(String sentenceID, String sentencePhraseTAG)
	{
	  //Create a linkedlist for nodes to be returned
	  LinkedList <String>sentencePhraseID_list = new LinkedList<String>();
	  try {
		pst = con.prepareStatement("SELECT sentence_phrase_id FROM sentence_phrase_tbl WHERE sentence_phrase_text_TAG = " + sentencePhraseTAG + " AND sentence_id = " + sentenceID);
		rs = pst.executeQuery();
	  
		while(rs.next()) //While more nodes left
		{
		  //Add it to the linkedlist
		  sentencePhraseID_list.add(rs.getString(1));               
		}
		
	  }
	   
	   catch (SQLException ex){
		Logger lgr = Logger.getLogger(FillRelations.class.getName());
		lgr.log(Level.WARNING, ex.getMessage(), ex);
           }
           
          return sentencePhraseID_list; //Return the linkedlist 
	}
        
        //Return a list of nodes which have the same parents(same level and same origin of arrows pointing to them)
	public String LinkedList<String> getCommonParentPhrases(Stirng sentencePhraseID)
	{
	 try {
	 
	 
	   //List of nodes that share the same parent as the input node
	   LinkedList <String>sentencePhraseID_list = new LinkedList<String>();
	   
	   //Get the parent node of the input node
	   pst = con.prepareStatement("SELECT object_phrase_id FROM sentence_phrase_rel_tbl WHERE target_phrase_id = " + sentencePhraseID);
	   rs = pst.executeQuery();
	   
	   String parentPhraseID = rs.getString(1);
	   
	   //Get the list of all of the children from the parent node
	   pst = con.prepareStatement("SELECT target_phrase_id FROM sentence_phrase_rel_tbl WHERE object_phrase_id = " + parentPhraseID);
	   rs = pst.executeQuery();
	   
	   //Add of the children to the linkedlist
           while(rs.next())
	   {
             sentencePhraseID_list.add(rs.getString(1));               
           }
		
		
	   }
	
         catch (SQLException ex) {
        	Logger lgr = Logger.getLogger(FillRelations.class.getName());
        	lgr.log(Level.WARNING, ex.getMessage(), ex);}
	
	   return sentencePhraseID_list; //Return the constructed list
	}
	
	// if sentencePhraseID corresponds to a root node, the whole sentence will be returned
	public String getPhrase(String sentencePhraseID)
	{
	
	//Create a linkedlist for nodes to be popped
	LinkedList <String>sentencePhraseID_list = new LinkedList<String>();
        sentencePhraseID_list.add(sentencePhraseID); //Adds the initial parent
        
        String current_sentencePhraseID = ""; //current node
        String current_word = ""; //current word from a leaf node
        String sentence = ""; //sentence to be returned
        
        try {
                
		while (sentencePhraseID_list.size() != 0) //As long as the linkedlist is not empty
		{
			//Pop the node
			current_sentencePhraseID = sentencePhraseID_list.pop();
		        
		        //Get the current node's TEXT
			pst = con.prepareStatement("SELECT sentence_phrase_text FROM sentence_phrase_tbl WHERE sentence_phrase_id = " + current_sentencePhraseID);
			rs = pst.executeQuery();
		
			//If the node is a leaf, record the text
			if (rs.next()) //If the node's text is NOT empty
			{
			  //Get the word
			  current_word = rs.getString(1);
			  //Add it to the sentence
			  sentence = sentence + " " + current_word;
			}
		
			//Get the current node's children
			pst = con.prepareStatement("SELECT target_phrase_id FROM sentence_phrase_rel_tbl WHERE object_phrase_id = " + current_sentencePhraseID);
			rs = pst.executeQuery();
		
			//Apend its children to the list.
			while(rs.next()) //If the node has children
			{
			  //Add it to the linkedlist
			  sentencePhraseID_list.add(rs.getString(1));               
			}
		}
	
	} catch (SQLException ex) {
        	Logger lgr = Logger.getLogger(FillRelations.class.getName());
        	lgr.log(Level.WARNING, ex.getMessage(), ex);
        }
        
          return sentence;//Return the reconsturcted sentence
	}
	
	
	// if -9999 returned, theres an error with rs
	public int getNumEntries(String tableName){
		int numEntries = -9999;
		
		pst = fillRelations1.getConnection().prepareStatement("SELECT COUNT(*) FROM " + tableName);
		rs = pst.executeQuery();
        if (rs.next()) // COUNT(*) query should only return 1 row of result
            numEntries = Integer.parseInt(rs.getString(1));
        
        return numEntries;
	}
	
	public static void main(String args[]){
		
		if(args.length < 2){
			System.out.println("ERROR: USAGE =");
			System.out.println("$ java -cp .:mysql-connector-java-5.1.20-bin.jar FillRelations _user_ _password_");
			return;
		}
		


		FillRelations fillRelations1 = new FillRelations(args[0],args[1]);
	
		
		
		try {
			int numBooks = fillRelations1.getNumEntries("book_tbl");  // get number of books in the database
	
            // for every book	
            for(int bookNum = 1; bookNum < numBooks + 1; bookNum++){
            	
            	// get number of chapters in the book
            	int numChapters = fillRelations1.getNumEntries("chapter_tbl");
            
            	// for every chapter in the book
            	for(int chapterNum = 1; chapterNum < numChapters + 1 ; chapterNum++){
            		
            		int numSentences = null;
            		
            		// get number of sentences in the chapter
            		pst = fillRelations1.getConnection().prepareStatment("SELECT COUNT(*) FROM sentence_tbl WHERE chapter_id = " + chapterNum);
            		rs = pst.executeQuery();
            		if(rs.next())
            			numSentences = Integer.parseInt(rs.getString(1));
            		
            		// for every sentence in the chapter
            		for(int sentenceNum = 1; sentenceNum < numSentences + 1; sentenceNum++){
            			
            			
            			
            		}
            	
            	}
            
            
            }
              
            
            
            pst.close();
            rs.close();











        } catch (SQLException ex) {
            Logger lgr = Logger.getLogger(FillRelations.class.getName());
            lgr.log(Level.SEVERE, ex.getMessage(), ex);

        } finally {
           fillRelations1.closeConnection();
        }
		
	}
}
