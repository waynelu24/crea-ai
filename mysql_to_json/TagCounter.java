import java.util.LinkedList;

public class TagCounter{
		
		//private String tag = null;
		//private int counter = 0;
		private LinkedList<String> tags;
		private LinkedList<Integer> counters;
		
		public TagCounter(){
			tags = new LinkedList<String>();
			counters = new LinkedList<Integer>();
		}
		
		public String advanceCounter(String tag){
			int index = tags.indexOf(tag);
			if(index == -1){
				tags.add(tag);
				counters.add(0);
				
				return tag + "0";
			}else{
				int numOccurance = counters.get(index);
				numOccurance++;
				counters.set(index, numOccurance);
				return tag + numOccurance;
				
			}
		}
		
		public String currentCounter(String tag){
			int index = tags.indexOf(tag);
			int numOccurance = counters.get(index);
			return tag + numOccurance;
		}
		
		public boolean contains(String tag){
			return tags.contains(tag);
		}
		
		public String toString(){
			int length = tags.size();
			String tag;
			int count;
			String toPrint = "[";
			
			for(int i = 0 ; i < length; i++){
				tag = tags.get(i);
				count = counters.get(i);
				toPrint += "(" + tag + " " + count + ") ";
			}

			toPrint += "]";
			return toPrint;
		}
	}
