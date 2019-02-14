package info2.bigdata.mongodb;

import com.csvreader.CsvReader;
import com.mongodb.client.MongoCollection;

import java.io.IOException;
import java.nio.charset.Charset;

import org.bson.Document; 


public class DataReader {

		private String filePath; 
		private CsvReader r;
		
		public DataReader(String path) throws IOException {
			this.filePath=path;
			char decollator =',';
	        String encode = "GBK";	
			this.r = new CsvReader(filePath,decollator,Charset.forName(encode));			
		}
		
		public void insertToMongo(int row) throws IOException {
			
			r.readHeaders();
			String[] head = r.getHeaders(); //get heads
			System.out.println(head.length);

	        MongoDB mongo=new MongoDB("dataset");// database name : dataset
	        MongoCollection<Document> data = mongo.mongoDatabase.getCollection("predict");// collection name : data
	       
	        int j=0;
	        while (r.readRecord() && j<row) // for every line of data
	        {
	        	Document document=new Document();// create a document for a line in dataset
	            for (int i = 0; i < head.length; i++)
	            {
	            	if(r.get(head[i])!="") {// if the  column is now for this line, we don't record it
	            	
						document.append(head[i], r.get(head[i]));// add the information of this line in the document
		               // System.out.println(head[i] + ":" + r.get(head[i]));
	            	}
	            }
            j++;
            data.insertOne(document);// insert this document into the collection "predict"
            System.out.println(document);           
	        }    
	        r.close();    
	        //mongo.clear();
		}

}
	
	
	

	 



