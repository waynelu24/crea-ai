import java.util.LinkedList;
import java.awt.Point;


public class CoordinateCounter{

	private LinkedList<String> sentencePhraseIDs;
	private LinkedList<Point> coords;
	private int nthChild; 

	public CoordinateCounter(){
		sentencePhraseIDs = new LinkedList<String>();
		coords = new LinkedList<Point>();
		nthChild = 0;
	}
	
	public void addUnique(String id, int xCoord, int yCoord){
		if(!sentencePhraseIDs.contains(id)){
			sentencePhraseIDs.add(id);
			coords.add(new Point(xCoord, yCoord));
		}
	}
	
	public int getXCoord(String id){
		int index = sentencePhraseIDs.indexOf(id);
		return (int) coords.get(index).getX();
	}
	
	public int getYCoord(String id){
		int index = sentencePhraseIDs.indexOf(id);
		return (int) coords.get(index).getY();
	}
	
	public String toString(){
		int length = sentencePhraseIDs.size();
		String s = "{";
		for(int i = 0 ; i < length; i++){
			String id = sentencePhraseIDs.get(i);
			int x = (int) coords.get(i).getX();
			int y = (int) coords.get(i).getY();
			
			s += "[" + id + ": " + x + "," + y + "] ";
		}
		
		return s;
	}

}
